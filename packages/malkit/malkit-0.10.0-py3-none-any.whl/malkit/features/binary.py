import functools
import math
from typing import Any, Iterable, Optional, Tuple, cast

import numpy as np
from numpy.typing import NDArray

from ..parallel import reduce_parallel
from ..typing import FilePath

__all__ = [
    "get_byte_hist",
    "extract_byte_hist",
    "extract_byte_hist_parallel",
    "get_byte_entropy_hist",
    "extract_byte_entropy_hist",
    "extract_byte_entropy_hist_parallel",
]


def get_byte_hist(buffer: bytes) -> NDArray:
    """Get byte histogram."""

    binary = np.frombuffer(buffer, dtype=np.uint8)
    return np.bincount(binary, minlength=256)


def extract_byte_hist(binary_file: FilePath) -> NDArray:
    """Extract byte histogram."""

    with open(binary_file, "rb") as f:
        buffer = f.read()
    return get_byte_hist(buffer)


def extract_byte_hist_parallel(
    binary_files: Iterable[FilePath], *, n_jobs: Optional[int] = None, **kwargs: Any
) -> NDArray:
    """Extract byte histogram in parallel."""

    return reduce_parallel(extract_byte_hist, binary_files, n_jobs=n_jobs, **kwargs)


def _get_entropy_and_byte_hist(window: NDArray) -> Tuple[float, NDArray]:
    byte_hist = np.bincount(window, minlength=256)
    prob = byte_hist / len(window)
    mask = prob > 0
    entropy = -np.sum(prob * np.log2(prob, where=mask))
    return float(entropy), byte_hist


def get_byte_entropy_hist(buffer: bytes, *, window_size: int = 1024, step_size: int = 256) -> NDArray:
    """Get byte entropy histogram.

    References:
        - J. Saxe and K. Berlin. 2015.
          Deep neural network based malware detection using two dimensional binary program features.
          https://doi.org/10.1109/MALWARE.2015.7413680
    """

    binary = np.frombuffer(buffer, dtype=np.uint8)
    matrix = np.zeros((16, 256), dtype=np.int64)
    # https://numpy.org/doc/stable/reference/generated/numpy.lib.stride_tricks.sliding_window_view.html
    for window in np.lib.stride_tricks.sliding_window_view(binary, window_size)[::step_size]:
        entropy, byte_hist = _get_entropy_and_byte_hist(window)
        index = min(math.floor(entropy * 2), 15)
        matrix[index] += byte_hist
    result = cast(NDArray, matrix.reshape((16, 16, 16)).sum(-1))
    return result.reshape(256)


def extract_byte_entropy_hist(binary_file: FilePath, *, window_size: int = 1024, step_size: int = 256) -> NDArray:
    """Extract byte entropy histogram."""

    with open(binary_file, "rb") as f:
        buffer = f.read()
    return get_byte_entropy_hist(buffer, window_size=window_size, step_size=step_size)


def extract_byte_entropy_hist_parallel(
    binary_files: Iterable[FilePath],
    *,
    window_size: int = 1024,
    step_size: int = 256,
    n_jobs: Optional[int] = None,
    **kwargs: Any,
) -> NDArray:
    """Extract byte entropy histogram in parallel."""

    function = functools.partial(extract_byte_entropy_hist, window_size=window_size, step_size=step_size)
    return reduce_parallel(function, binary_files, n_jobs=n_jobs, **kwargs)
