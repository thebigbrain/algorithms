# Python program for implementation of Selection
# Sort
import sys


def should_swap(current, new, desc: bool):
    return current < new if desc else current > new


def swap(arr, old, new):
    arr[old], arr[new] = arr[new], arr[old]


def selection_sort(arr: [], desc=False):
    _arr = arr.copy()
    _index_arr = [i for i in range(len(_arr))]

    # Traverse through all array elements
    for idx in range(len(_arr)):
        # Find the element in remaining unsorted array
        min_idx = idx
        for j in range(idx + 1, len(_arr)):
            if should_swap(_arr[min_idx], _arr[j], desc):
                min_idx = j

        # Swap the found minimum element with
        # the first element
        swap(_arr, idx, min_idx)
        swap(_index_arr, idx, min_idx)
    return _arr, _index_arr


if __name__ == "__main__":
    result = selection_sort([64, 25, 12, 22, 11], desc=True)
    print(result)
    # for i in range(len(result)):
    #     print("%d" % result[i], end=" , ")
