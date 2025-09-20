"""
Sorting algorithm implementations with visualization support.
"""

from typing import List, Dict, Type, Optional, Union, Sequence
from ..core.base import AlgorithmVisualizer, Number
import copy

class MergeSortVisualizer(AlgorithmVisualizer):
    """Visualizer for Merge Sort algorithm."""
    
    def __init__(self, name: str = "Merge Sort", data: Optional[Sequence[Union[int, float]]] = None):
        super().__init__(name, data or [])
        self.recursion_depth = 0
        
    def sort(self) -> List[Number]:
        """Execute merge sort with step tracking."""
        import time
        
        if not self.current_data:
            return []
        
        self._start_time = time.time()
        
        self.add_step("Starting Merge Sort", self.current_data.copy(), 
                      highlighted_indices=list(range(len(self.current_data))))
        
        result = self._merge_sort_recursive(self.current_data.copy(), 0, len(self.current_data) - 1)
        
        self._end_time = time.time()
        self.metrics.execution_time = self._end_time - self._start_time
        
        self.add_step("Merge Sort Complete", result, 
                      highlighted_indices=list(range(len(result))))
        return result
    
    def _merge_sort_recursive(self, arr: List[Number], left: int, right: int) -> List[Number]:
        """Recursive merge sort implementation with visualization."""
        if left >= right:
            return [arr[left]] if left == right else []
        
        self.recursion_depth += 1
        mid = (left + right) // 2
        
        # Divide phase - show the current subarray being divided
        current_state = arr.copy()
        self.add_step(f"Dividing subarray at indices {left}-{right} (mid={mid})", 
                      current_state, highlighted_indices=[i for i in range(left, right + 1)])
        
        # Recursive calls
        left_half = self._merge_sort_recursive(arr, left, mid)
        right_half = self._merge_sort_recursive(arr, mid + 1, right)
        
        # Merge phase - show the actual merging process
        merged = self._merge_with_visualization(left_half, right_half, arr, left, mid, right)
        
        # Update the original array section with merged result
        for i, val in enumerate(merged):
            if left + i < len(arr):
                arr[left + i] = val
        
        # Show the updated state after merging
        self.add_step(f"Merged subarray [{left}-{right}]: {merged}", 
                      arr.copy(), 
                      swapped_indices=[i for i in range(left, left + len(merged))])
        
        self.recursion_depth -= 1
        return merged
    
    def _merge_with_visualization(self, left: List[Number], right: List[Number], 
                                  original_arr: List[Number], left_start: int, 
                                  mid: int, right_end: int) -> List[Number]:
        """Merge two sorted arrays with step-by-step visualization."""
        merged = []
        left_idx = right_idx = 0
        
        # Create a working array to show the merge process
        working_arr = original_arr.copy()
        merge_position = left_start
        
        self.add_step(f"Merging sorted subarrays: {left} and {right}", 
                      working_arr, 
                      highlighted_indices=[i for i in range(left_start, right_end + 1)])
        
        while left_idx < len(left) and right_idx < len(right):
            self.record_comparison(left_idx, right_idx)
            
            if left[left_idx] <= right[right_idx]:
                merged.append(left[left_idx])
                # Update working array to show current merge state
                working_arr[merge_position] = left[left_idx]
                self.add_step(f"Placing {left[left_idx]} from left subarray at position {merge_position}", 
                              working_arr.copy(),
                              comparison_indices=[left_start + left_idx, mid + 1 + right_idx],
                              swapped_indices=[merge_position])
                left_idx += 1
            else:
                merged.append(right[right_idx])
                # Update working array to show current merge state
                working_arr[merge_position] = right[right_idx]
                self.add_step(f"Placing {right[right_idx]} from right subarray at position {merge_position}", 
                              working_arr.copy(),
                              comparison_indices=[left_start + left_idx, mid + 1 + right_idx],
                              swapped_indices=[merge_position])
                right_idx += 1
            
            merge_position += 1
        
        # Add remaining elements from left subarray
        while left_idx < len(left):
            merged.append(left[left_idx])
            working_arr[merge_position] = left[left_idx]
            self.add_step(f"Adding remaining element {left[left_idx]} from left at position {merge_position}", 
                          working_arr.copy(), 
                          highlighted_indices=[merge_position])
            left_idx += 1
            merge_position += 1
        
        # Add remaining elements from right subarray
        while right_idx < len(right):
            merged.append(right[right_idx])
            working_arr[merge_position] = right[right_idx]
            self.add_step(f"Adding remaining element {right[right_idx]} from right at position {merge_position}", 
                          working_arr.copy(), 
                          highlighted_indices=[merge_position])
            right_idx += 1
            merge_position += 1
        
        return merged
    
    def get_algorithm_info(self) -> Dict[str, str]:
        """Return merge sort complexity information."""
        return {
            'time_complexity': 'O(n log n)',
            'space_complexity': 'O(n)',
            'stability': 'Stable',
            'description': 'Divide-and-conquer algorithm that recursively divides the array and merges sorted subarrays'
        }

class QuickSortVisualizer(AlgorithmVisualizer):
    """Visualizer for Quick Sort algorithm."""
    
    def __init__(self, name: str = "Quick Sort", data: Optional[Sequence[Union[int, float]]] = None):
        super().__init__(name, data or [])
        
    def sort(self) -> List[Number]:
        """Execute quick sort with step tracking."""
        if not self.current_data:
            return []
        
        import time
        self._start_time = time.time()
        
        self.add_step("Starting Quick Sort", self.current_data.copy(), 
                      highlighted_indices=list(range(len(self.current_data))))
        
        self._quick_sort_recursive(self.current_data, 0, len(self.current_data) - 1)
        
        self.add_step("Quick Sort Complete", self.current_data.copy(), 
                      highlighted_indices=list(range(len(self.current_data))))
        
        self._end_time = time.time()
        self.metrics.execution_time = self._end_time - self._start_time
        
        return self.current_data.copy()
    
    def _quick_sort_recursive(self, arr: List[Number], low: int, high: int):
        """Recursive quick sort implementation with visualization."""
        if low < high:
            # Partition the array
            pivot_index = self._partition_with_visualization(arr, low, high)
            
            # Recursively sort subarrays
            if pivot_index > low:
                self.add_step(f"Recursively sorting left subarray (indices {low}-{pivot_index-1})", 
                              arr, highlighted_indices=[i for i in range(low, pivot_index)])
                self._quick_sort_recursive(arr, low, pivot_index - 1)
            
            if pivot_index < high:
                self.add_step(f"Recursively sorting right subarray (indices {pivot_index+1}-{high})", 
                              arr, highlighted_indices=[i for i in range(pivot_index + 1, high + 1)])
                self._quick_sort_recursive(arr, pivot_index + 1, high)
    
    def _partition_with_visualization(self, arr: List[Number], low: int, high: int) -> int:
        """Partition array with step-by-step visualization using in-place approach."""
        pivot = arr[high]  # Choose last element as pivot for clearer visualization
        
        self.add_step(f"Choosing pivot: {pivot} at index {high}", 
                      arr.copy(), pivot_index=high, 
                      highlighted_indices=[i for i in range(low, high + 1)])
        
        # Index of smaller element (indicates right position of pivot)
        i = low - 1
        
        for j in range(low, high):
            self.record_comparison(j, high)
            self.add_step(f"Comparing arr[{j}]={arr[j]} with pivot {pivot}", 
                          arr.copy(), pivot_index=high, 
                          comparison_indices=[j, high],
                          highlighted_indices=[i+1 if i >= 0 else low])
            
            # If current element is smaller than or equal to pivot
            if arr[j] <= pivot:
                i += 1  # Increment index of smaller element
                if i != j:
                    self.record_swap(i, j)
                    arr[i], arr[j] = arr[j], arr[i]
                    self.add_step(f"Swapping arr[{i}]={arr[i]} with arr[{j}]={arr[j]} (moving smaller element left)", 
                                  arr.copy(), pivot_index=high,
                                  swapped_indices=[i, j])
                else:
                    self.add_step(f"arr[{j}]={arr[j]} <= pivot, already in correct relative position", 
                                  arr.copy(), pivot_index=high,
                                  highlighted_indices=[j])
        
        # Place pivot in correct position
        pivot_final_pos = i + 1
        if pivot_final_pos != high:
            self.record_swap(pivot_final_pos, high)
            arr[pivot_final_pos], arr[high] = arr[high], arr[pivot_final_pos]
            self.add_step(f"Placing pivot {pivot} in final position {pivot_final_pos}", 
                          arr.copy(), pivot_index=pivot_final_pos,
                          swapped_indices=[pivot_final_pos, high])
        else:
            self.add_step(f"Pivot {pivot} already in correct position {pivot_final_pos}", 
                          arr.copy(), pivot_index=pivot_final_pos)
        
        # Show final partitioned state
        self.add_step(f"Partition complete: elements ≤ {pivot} are left of index {pivot_final_pos}, elements > {pivot} are right", 
                      arr.copy(), pivot_index=pivot_final_pos,
                      highlighted_indices=[k for k in range(low, pivot_final_pos)] + 
                                         [k for k in range(pivot_final_pos + 1, high + 1)])
        
        return pivot_final_pos
    
    def get_algorithm_info(self) -> Dict[str, str]:
        """Return quick sort complexity information."""
        return {
            'time_complexity': 'O(n²) worst, O(n log n) average',
            'space_complexity': 'O(log n)',
            'stability': 'Unstable',
            'description': 'Divide-and-conquer algorithm that partitions around a pivot element'
        }

class SelectionSortVisualizer(AlgorithmVisualizer):
    """Visualizer for Selection Sort algorithm."""
    
    def __init__(self, name: str = "Selection Sort", data: Optional[Sequence[Union[int, float]]] = None):
        super().__init__(name, data or [])
        
    def sort(self) -> List[Number]:
        """Execute selection sort with step tracking."""
        if not self.current_data:
            return []
        
        import time
        self._start_time = time.time()
            
        # Work with a copy of the data for in-place sorting visualization
        arr = self.current_data.copy()
        n = len(arr)
        
        self.add_step("Starting Selection Sort", arr.copy(), 
                      highlighted_indices=list(range(len(arr))))
        
        for i in range(n):
            # Find the minimum element in the remaining unsorted array
            min_idx = i
            
            self.add_step(f"Finding minimum in unsorted portion (indices {i}-{n-1})", 
                          arr.copy(), 
                          highlighted_indices=[j for j in range(i, n)],
                          pivot_index=min_idx)
            
            # Search for minimum in remaining array
            for j in range(i + 1, n):
                self.record_comparison(min_idx, j)
                self.add_step(f"Comparing arr[{j}]={arr[j]} with current minimum arr[{min_idx}]={arr[min_idx]}", 
                              arr.copy(),
                              comparison_indices=[min_idx, j],
                              highlighted_indices=[k for k in range(i, n)])
                
                if arr[j] < arr[min_idx]:
                    min_idx = j
                    self.add_step(f"New minimum found: arr[{min_idx}]={arr[min_idx]}", 
                                  arr.copy(),
                                  highlighted_indices=[min_idx])
            
            # Swap the found minimum element with the first element of unsorted part
            if min_idx != i:
                self.record_swap(i, min_idx)
                arr[i], arr[min_idx] = arr[min_idx], arr[i]
                self.add_step(f"Swapping arr[{i}]={arr[min_idx]} with arr[{min_idx}]={arr[i]}", 
                              arr.copy(),
                              swapped_indices=[i, min_idx])
            else:
                self.add_step(f"Element arr[{i}]={arr[i]} is already in correct position", 
                              arr.copy(),
                              highlighted_indices=[i])
            
            # Show the sorted portion growing
            self.add_step(f"Sorted portion now includes indices 0-{i}: {arr[:i+1]}", 
                          arr.copy(),
                          highlighted_indices=[k for k in range(i + 1)])
        
        self.add_step("Selection Sort Complete", arr.copy(), 
                      highlighted_indices=list(range(len(arr))))
        
        self._end_time = time.time()
        self.metrics.execution_time = self._end_time - self._start_time
        
        return arr
    
    def get_algorithm_info(self) -> Dict[str, str]:
        """Return selection sort complexity information."""
        return {
            'time_complexity': 'O(n²)',
            'space_complexity': 'O(1)',
            'stability': 'Unstable',
            'description': 'Repeatedly finds the minimum element and moves it to the sorted portion'
        }

class PriorityQueueSortVisualizer(AlgorithmVisualizer):
    """Visualizer for Priority Queue Sort (Heap Sort variant)."""
    
    def __init__(self, name: str = "Priority Queue Sort", data: Optional[Sequence[Union[int, float]]] = None):
        super().__init__(name, data or [])
        
    def sort(self) -> List[Number]:
        """Execute priority queue sort with step tracking."""
        if not self.current_data:
            return []
        
        import time
        import heapq
        
        self._start_time = time.time()
            
        # Work with a copy of the original data
        arr = self.current_data.copy()
        
        self.add_step("Starting Priority Queue Sort (using min-heap)", arr.copy(), 
                      highlighted_indices=list(range(len(arr))))
        
        # Build heap in-place
        self.add_step("Building min-heap from array", arr.copy())
        heapq.heapify(arr)
        self.add_step("Min-heap built", arr.copy(), 
                      highlighted_indices=list(range(len(arr))))
        
        # Extract elements from heap to build sorted array
        result = []
        heap_size = len(arr)
        
        for i in range(heap_size):
            if arr:  # Check if heap is not empty
                min_val = heapq.heappop(arr)
                result.append(min_val)
                
                self.add_step(f"Extracted minimum: {min_val} (heap size now {len(arr)})", 
                              result + arr,  # Show sorted portion + remaining heap
                              swapped_indices=[len(result) - 1],  # Highlight newly added element
                              highlighted_indices=list(range(len(result), len(result) + len(arr))))  # Highlight remaining heap
        
        self.add_step("Priority Queue Sort Complete", result, 
                      highlighted_indices=list(range(len(result))))
        
        self._end_time = time.time()
        self.metrics.execution_time = self._end_time - self._start_time
        
        return result
    
    def get_algorithm_info(self) -> Dict[str, str]:
        """Return priority queue sort complexity information."""
        return {
            'time_complexity': 'O(n log n)',
            'space_complexity': 'O(n)',
            'stability': 'Depends on implementation',
            'description': 'Uses a priority queue (heap) to extract elements in sorted order'
        }

# Registry of available algorithms
AVAILABLE_ALGORITHMS: Dict[str, Type[AlgorithmVisualizer]] = {
    'merge_sort': MergeSortVisualizer,
    'quick_sort': QuickSortVisualizer,
    'selection_sort': SelectionSortVisualizer,
    'priority_queue_sort': PriorityQueueSortVisualizer
}

def create_algorithm_visualizer(algorithm_name: str, data: Sequence[Union[int, float]]) -> AlgorithmVisualizer:
    """Factory function to create visualizers by name."""
    if algorithm_name not in AVAILABLE_ALGORITHMS:
        raise ValueError(f"Unknown algorithm: {algorithm_name}. Available: {list(AVAILABLE_ALGORITHMS.keys())}")
    
    return AVAILABLE_ALGORITHMS[algorithm_name](name=algorithm_name, data=list(data))

def get_available_algorithms() -> List[str]:
    """Get list of available algorithm names."""
    return list(AVAILABLE_ALGORITHMS.keys())

def get_algorithm_info(algorithm_name: str) -> Dict[str, str]:
    """Get algorithm information without creating an instance."""
    if algorithm_name not in AVAILABLE_ALGORITHMS:
        raise ValueError(f"Unknown algorithm: {algorithm_name}")
    
    # Create temporary instance to get info
    temp_instance = AVAILABLE_ALGORITHMS[algorithm_name](name=algorithm_name, data=[])
    return temp_instance.get_algorithm_info()