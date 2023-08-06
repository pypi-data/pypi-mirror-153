import logging

import numpy as np
import zarr
from numpy.random import default_rng
from typing import List, Tuple
from torch.utils.data import IterableDataset


class BatchedZarrDataset(IterableDataset):
    """Torch Dataset class for loading Zarr arrays in shuffled batches.

    Loads data from a Zarr array in batches of the given size. In order to
    randomize batch content, a number of batches are loaded together . Compared to shuffling the whole array, this
    approach can reduce memory consumption drastically at the cost of reducing
    the quality of the random sampling.

    Creates an iterable which in each iteration returns a tuple containing a
    single batch of images from the given Zarr array and their corresponding
    labels.

    The position of batches, their order, and the set of batches whose contents
    are shuffled together is random.

    The Zarr array is assumed to have shape (#channels, #cells, x, y). The
    labels are assumed to be one-dimensional numpy arrays.

    In this example with four batches and n_shuffled_baches=2, batch 1 and 2 are
    randomized together, and batch 3 and 4.

    Looping over the batches the first time might put them in this order and
    position ("." corresponds to unused elements of the array that occur because
    the array size is rarely a perfect multiple of batch size):

    [(--2--)(--1--).(--4--)..(--3--)]

    Looping over the same dataset again will return them in a different order
    and position. Note that since batch 1 and 2, and 3 and 4 are shuffled
    together, the cells present in each batch is competely different each run.

    [.(--3--)(--1--)(--2--).(--4--).]

    The class is mostly a plain Python iterable so it can also be used in a
    simple loop:

    for batch in BatchedZarrDataset(...):
        # do stuff with batch cells and labels
    """

    def __init__(
        self,
        zarr: zarr.Array,
        labels: List[np.ndarray],
        batch_size: int,
        n_shuffled_batches: int,
        return_view: bool = False,
    ):
        super().__init__()
        self.zarr = zarr
        self.labels = labels
        ns_cells = [self.zarr.shape[1]] + [len(x) for x in self.labels]
        if len(set(ns_cells)) != 1:
            raise ValueError(
                f"Number of cells in all inputs must be identical, not {ns_cells}"
            )
        self.n_shuffled_batches = n_shuffled_batches
        self.return_view = return_view
        self.n_cells = zarr.shape[1]
        self.batch_size = batch_size
        self.batch_number = self.n_cells // batch_size
        if self.batch_size > self.n_cells:
            raise ValueError(
                f"Batch size can't be larger than the number of cells {self.batch_size} > {self.n_cells}"
            )

    def __iter__(self):
        return BatchedZarrDatasetIterator(
            self.zarr,
            self.labels,
            self.batch_size,
            self.n_shuffled_batches,
            self.return_view,
        )

    def __len__(self) -> int:
        return self.batch_number


class BatchedZarrDatasetIterator:
    def __init__(
        self,
        zarr: zarr.Array,
        labels: List[np.ndarray],
        batch_size: int,
        n_shuffled_batches: int,
        seed: int = None,
        return_view: bool = False,
    ):
        self.zarr = zarr
        self.labels = labels
        self.return_view = return_view
        ns_cells = [self.zarr.shape[1]] + [len(x) for x in self.labels]
        if len(set(ns_cells)) != 1:
            raise ValueError(
                f"Number of cells in all inputs must be identical, not {ns_cells}"
            )
        self.n_shuffled_batches = n_shuffled_batches
        self.n_cells = zarr.shape[1]
        self.batch_size = batch_size
        self.batch_number = self.n_cells // batch_size
        self.batch_remainder = self.n_cells % batch_size
        if self.batch_size > self.n_cells:
            raise ValueError(
                f"Batch size can't be larger than the number of cells {self.batch_size} > {self.n_cells}"
            )
        # Generating #batch_number randomly distributed slices along the
        # cell axis that are all #batch_size long with
        # randomly sized gaps between them
        self.rng = default_rng(seed=seed)
        rand_floats = self.rng.uniform(size=self.batch_number + 1)
        # extend the floats so the sum is approximately batch_remainder
        # (might be less because of flooring)
        rand_gaps = (self.batch_remainder * rand_floats / np.sum(rand_floats)).astype(
            int
        )
        # randomly add missing numbers
        for _ in range(self.batch_remainder - np.sum(rand_gaps)):
            rand_gaps[self.rng.integers(0, len(rand_gaps))] += 1
        batch_starts = np.cumsum(rand_gaps)[:-1] + np.cumsum(
            [0] + [self.batch_size] * (self.batch_number - 1)
        )
        self.batch_coords = np.stack(
            [batch_starts, batch_starts + self.batch_size], axis=-1
        )
        # Random order in which batches will be processed
        self.batches_remaining = self.rng.choice(
            self.batch_number, size=self.batch_number, replace=False
        )
        self.cache_shape = list(self.zarr.shape)
        self.cache_shape[1] = self.batch_size * self.n_shuffled_batches
        logging.debug(f"cache shape {self.cache_shape}")
        self.batch_cache = np.empty(self.cache_shape, dtype=self.zarr.dtype)
        self.label_cache = [
            np.empty(self.cache_shape[1], dtype=x.dtype) for x in self.labels
        ]
        # Keep track of which batch in the current cache is returned next
        self.cache_idx = 0
        self.n_cached = 0

    def __next__(self) -> Tuple[np.ndarray, ...]:
        if len(self.batches_remaining) == 0 and self.cache_idx == 0:
            raise StopIteration
        # Cache is empty / exhausted
        if self.cache_idx == 0:
            logging.debug(f"Filling cache. batches {self.batches_remaining} available")
            self.n_cached = min(len(self.batches_remaining), self.n_shuffled_batches)
            logging.debug(f"batches taken {self.n_cached}")
            for i, batch_idx in enumerate(self.batches_remaining[: self.n_cached]):
                logging.debug(f"Taking batch {batch_idx}")
                cache_start = i * self.batch_size
                cache_coords = (cache_start, cache_start + self.batch_size)
                batch_coords = self.batch_coords[batch_idx]
                logging.debug(
                    f"cache coords {cache_coords} batch coords {batch_coords}"
                )
                self.batch_cache[:, cache_coords[0] : cache_coords[1], ...] = self.zarr[
                    :, batch_coords[0] : batch_coords[1], ...
                ]
                for j, l in enumerate(self.labels):
                    self.label_cache[j][cache_coords[0] : cache_coords[1]] = l[
                        batch_coords[0] : batch_coords[1]
                    ]
            self.batches_remaining = self.batches_remaining[self.n_cached :]
            # Randomize order of cells within the loaded batches
            # try to do in-place using np.shuffle with same seed
            rand_seed = self.rng.integers(np.iinfo(np.int64).max)
            logging.debug(f"Shuffling using seed {rand_seed}")
            # Take care to only shuffle the part of the cache that is used
            batch_cache_used = self.batch_cache[
                :, : self.n_cached * self.batch_size, ...
            ]
            default_rng(seed=rand_seed).shuffle(batch_cache_used, axis=1)
            for l in self.label_cache:
                label_cache_used = l[: self.n_cached * self.batch_size]
                default_rng(seed=rand_seed).shuffle(label_cache_used)
        logging.debug(f"Returning cache entry {self.cache_idx}")
        batch_start = self.cache_idx * self.batch_size
        # Update current cache position pointer
        self.cache_idx = (self.cache_idx + 1) % self.n_cached
        output_mat = self.batch_cache[
            :, batch_start : batch_start + self.batch_size, ...
        ]
        output_labels = tuple(
            x[batch_start : batch_start + self.batch_size] for x in self.label_cache
        )
        if not self.return_view:
            # We can only return views if we know that the data
            # is going to be consumed immediately before the next
            # iteration step. Otherwise, if the data is stored somewhere,
            # for future use we need to copy the data.
            output_mat = output_mat.copy()
            output_labels = tuple(x.copy() for x in output_labels)
        output_tuple = (output_mat,) + output_labels
        return output_tuple
