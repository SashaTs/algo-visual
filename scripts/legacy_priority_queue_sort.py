from collections import deque
from queue import PriorityQueue
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
    
    q = PriorityQueue()

    for n in numbers:
        q.put(n)
    
    res = []
    while not q.empty():
        res += [q.get()]

    return list(res)
    # return sorted(numbers)

if __name__ == "__main__":
    main()
