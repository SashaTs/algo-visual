import sys
import os
# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from algorithm_visualizer.utils.data_io import read_numbers
from typing import List, Union
import os
import sys

Number = Union[int, float]


def main(path: str | None = None) -> None:
    """Load numbers from a file using read_numbers and print them.

    NOTE: sorting is intentionally NOT implemented here per instructions.
    """
    if path is None:
        # Prefer the largest sample if available, fall back to command-line arg or smaller files
        data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'algorithm_visualizer', 'data')
        if os.path.exists(os.path.join(data_dir, "numbers100.txt")):
            path = os.path.join(data_dir, "numbers100.txt")
        elif len(sys.argv) > 1:
            path = sys.argv[1]
        else:
            path = os.path.join(data_dir, "numbers10.txt")

    nums = read_numbers(path)
    print(f"Loaded {len(nums)} numbers from {path}:")
    print(nums)

    sorted_nums = sort_numbers(nums)
    print("Sorted numbers:")
    print(sorted_nums)

def sort_numbers(numbers: List[Number]) -> List[Number]:
    """Sort the list of numbers in ascending order."""
    if len(numbers) <= 1:
        return numbers
    pivot = numbers[0]
    left = []
    right = []
    for n in numbers[1:]:
        if n <= pivot:
            left.append(n)
        else:
            right.append(n)
    # left = [x for x in numbers[1:] if x <= pivot]
    # right = [x for x in numbers[1:] if x > pivot]

    return sort_numbers(left) + [pivot] + sort_numbers(right)

if __name__ == "__main__":
    main()
