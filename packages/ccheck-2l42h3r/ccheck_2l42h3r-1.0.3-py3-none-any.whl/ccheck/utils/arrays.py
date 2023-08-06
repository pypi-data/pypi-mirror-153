"""Functions aiding manipulating arrays"""

import itertools
from typing import List, Optional, TypeVar

T = TypeVar("T")


def intersperse(array: List[T], item: T) -> List[T]:
    """Return given array with separator (item) inserted between every item"""
    result = [item] * (len(array) * 2 - 1)
    result[0::2] = array
    return result


def check_for_ordered_subarray(array: List[T], subarray: List[T]) -> bool:
    """Return true if a subarray can be found within given array (with correct order kept)"""
    match = False

    try:
        for master_index, master_element in enumerate(array):
            if master_element == subarray[0]:
                match = True
                for sub_index, sub_element in enumerate(subarray):
                    if array[master_index + sub_index] != sub_element:
                        match = False
                if match is True:
                    return match
    except IndexError:
        return False
    return match


def filter_out_none(array: List[Optional[T]]) -> List[T]:
    """Return array with any 'None' values removes"""
    return list(filter(lambda i: i is not None, array))  # type: ignore


def flatten(arrays: List[List[T]]) -> List[T]:
    """Return flattened array from single-level nested array of arrays"""
    return list(itertools.chain.from_iterable(arrays))
