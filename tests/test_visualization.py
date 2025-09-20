"""
Test Suite for Algorithm Visualization Framework

Comprehensive tests for all components of the visualization framework.
Tests algorithm correctness, performance metrics, and visualization functionality.

Author: Senior Data Visualization Developer
"""

import unittest
import time
import tempfile
import os
import json
import sys
from typing import List

# Add the project root to the path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

# Import the framework
from algorithm_visualizer.core.base import AlgorithmVisualizer, AlgorithmStep, PerformanceMetrics
from algorithm_visualizer.core.comparator import AlgorithmComparator
from algorithm_visualizer.core.text_visualizer import TextVisualizer
from algorithm_visualizer.utils.data_io import export_metrics, import_metrics
from algorithm_visualizer.algorithms import (
    MergeSortVisualizer, QuickSortVisualizer, 
    SelectionSortVisualizer, PriorityQueueSortVisualizer
)

# Define available visualizers for tests
AVAILABLE_VISUALIZERS = {
    'merge_sort': MergeSortVisualizer,
    'quick_sort': QuickSortVisualizer,
    'selection_sort': SelectionSortVisualizer,
    'priority_queue_sort': PriorityQueueSortVisualizer
}

def create_visualizer(algorithm_name: str, data):
    """Create visualizer instance for testing."""
    if algorithm_name in AVAILABLE_VISUALIZERS:
        return AVAILABLE_VISUALIZERS[algorithm_name](algorithm_name, data)
    else:
        raise ValueError(f"Unknown algorithm: {algorithm_name}")

class TestAlgorithmVisualizerCore(unittest.TestCase):
    """Test the core visualization framework."""
    
    def setUp(self):
        self.sample_data = [64, 34, 25, 12, 22, 11, 90]
        self.sorted_data = [11, 12, 22, 25, 34, 64, 90]
    
    def test_algorithm_step_creation(self):
        """Test AlgorithmStep dataclass creation."""
        step = AlgorithmStep(
            step_number=1,
            description="Test step",
            array_state=[3, 1, 2],
            highlighted_indices=[0, 1],
            comparison_indices=[1, 2]
        )
        
        self.assertEqual(step.step_number, 1)
        self.assertEqual(step.description, "Test step")
        self.assertEqual(step.array_state, [3, 1, 2])
        self.assertEqual(step.highlighted_indices, [0, 1])
        self.assertEqual(step.comparison_indices, [1, 2])
        self.assertEqual(step.swapped_indices, [])
        self.assertIsNone(step.pivot_index)
    
    def test_performance_metrics(self):
        """Test PerformanceMetrics tracking."""
        metrics = PerformanceMetrics()
        
        # Initial state
        self.assertEqual(metrics.execution_time, 0.0)
        self.assertEqual(metrics.comparisons, 0)
        self.assertEqual(metrics.swaps, 0)
        
        # Update metrics
        metrics.execution_time = 1.5
        metrics.comparisons = 10
        metrics.swaps = 5
        
        self.assertEqual(metrics.execution_time, 1.5)
        self.assertEqual(metrics.comparisons, 10)
        self.assertEqual(metrics.swaps, 5)

class TestSortingAlgorithms(unittest.TestCase):
    """Test sorting algorithm implementations and correctness."""
    
    def setUp(self):
        self.test_cases = [
            [64, 34, 25, 12, 22, 11, 90],
            [5, 2, 4, 6, 1, 3],
            [1],
            [],
            [1, 1, 1, 1],
            list(range(10, 0, -1)),  # Reverse sorted
            list(range(1, 11)),      # Already sorted
        ]
    
    def test_merge_sort_correctness(self):
        """Test merge sort produces correct results."""
        for test_data in self.test_cases:
            with self.subTest(data=test_data):
                visualizer = MergeSortVisualizer(data=test_data.copy())
                result = visualizer.sort()
                expected = sorted(test_data)
                self.assertEqual(result, expected)
    
    def test_quick_sort_correctness(self):
        """Test quick sort produces correct results."""
        for test_data in self.test_cases:
            with self.subTest(data=test_data):
                visualizer = QuickSortVisualizer(data=test_data.copy())
                result = visualizer.sort()
                expected = sorted(test_data)
                self.assertEqual(result, expected)
    
    def test_selection_sort_correctness(self):
        """Test selection sort produces correct results."""
        for test_data in self.test_cases:
            with self.subTest(data=test_data):
                visualizer = SelectionSortVisualizer(data=test_data.copy())
                result = visualizer.sort()
                expected = sorted(test_data)
                self.assertEqual(result, expected)
    
    def test_priority_queue_sort_correctness(self):
        """Test priority queue sort produces correct results."""
        for test_data in self.test_cases:
            with self.subTest(data=test_data):
                visualizer = PriorityQueueSortVisualizer(data=test_data.copy())
                result = visualizer.sort()
                expected = sorted(test_data)
                self.assertEqual(result, expected)
    
    def test_algorithm_info(self):
        """Test that all algorithms provide complexity information."""
        test_data = [3, 1, 4, 1, 5]
        
        algorithms = [
            MergeSortVisualizer,
            QuickSortVisualizer,
            SelectionSortVisualizer,
            PriorityQueueSortVisualizer
        ]
        
        for alg_class in algorithms:
            with self.subTest(algorithm=alg_class.__name__):
                visualizer = alg_class(data=test_data.copy())
                info = visualizer.get_algorithm_info()
                
                # Check required keys
                required_keys = ['time_complexity', 'space_complexity', 'description']
                for key in required_keys:
                    self.assertIn(key, info)
                    self.assertIsInstance(info[key], str)
                    self.assertTrue(len(info[key]) > 0)

class TestVisualizationTracking(unittest.TestCase):
    """Test step tracking and visualization features."""
    
    def setUp(self):
        self.test_data = [5, 2, 8, 1, 9]
    
    def test_step_recording(self):
        """Test that steps are properly recorded."""
        visualizer = MergeSortVisualizer(data=self.test_data.copy())
        result = visualizer.sort()
        
        # Should have recorded steps
        self.assertGreater(len(visualizer.steps), 0)
        
        # Check step structure
        for step in visualizer.steps:
            self.assertIsInstance(step, AlgorithmStep)
            self.assertIsInstance(step.step_number, int)
            self.assertIsInstance(step.description, str)
            self.assertIsInstance(step.array_state, list)
            self.assertGreater(step.step_number, 0)
            self.assertTrue(len(step.description) > 0)
    
    def test_metrics_tracking(self):
        """Test that performance metrics are tracked."""
        visualizer = SelectionSortVisualizer(data=self.test_data.copy())
        result = visualizer.sort()
        
        # Should have recorded comparisons (selection sort makes many)
        self.assertGreater(visualizer.metrics.comparisons, 0)
        
        # Should have recorded some operations
        self.assertGreater(len(visualizer.steps), 1)
    
    def test_performance_summary(self):
        """Test performance summary generation."""
        visualizer = QuickSortVisualizer(data=self.test_data.copy())
        result = visualizer.sort()
        
        summary = visualizer.get_performance_summary()
        
        # Check required keys
        required_keys = [
            'algorithm', 'array_size', 'execution_time', 
            'comparisons', 'swaps', 'total_steps', 'complexity_info'
        ]
        
        for key in required_keys:
            self.assertIn(key, summary)
        
        # Check types and values
        self.assertEqual(summary['algorithm'], visualizer.name)
        self.assertEqual(summary['array_size'], len(self.test_data))
        self.assertIsInstance(summary['execution_time'], float)
        self.assertIsInstance(summary['comparisons'], int)
        self.assertIsInstance(summary['swaps'], int)
        self.assertIsInstance(summary['total_steps'], int)
        self.assertIsInstance(summary['complexity_info'], dict)

class TestAlgorithmComparator(unittest.TestCase):
    """Test algorithm comparison functionality."""
    
    def setUp(self):
        self.test_data = [8, 3, 5, 4, 7, 6, 1, 2]
    
    def test_algorithm_comparison(self):
        """Test comparing multiple algorithms."""
        comparator = AlgorithmComparator(self.test_data.copy())
        
        # Add algorithms
        merge_viz = comparator.add_algorithm(MergeSortVisualizer, "Merge Sort")
        quick_viz = comparator.add_algorithm(QuickSortVisualizer, "Quick Sort")
        
        # Check results
        self.assertEqual(len(comparator.results), 2)
        self.assertIn("Merge Sort", comparator.results)
        self.assertIn("Quick Sort", comparator.results)
        
        # Both should produce correct sorted results
        for viz in comparator.results.values():
            self.assertTrue(hasattr(viz, 'metrics'))
            self.assertTrue(hasattr(viz, 'steps'))
    
    def test_comparison_report(self):
        """Test comparison report generation."""
        comparator = AlgorithmComparator(self.test_data.copy())
        
        comparator.add_algorithm(MergeSortVisualizer, "Merge Sort")
        comparator.add_algorithm(SelectionSortVisualizer, "Selection Sort")
        
        report = comparator.get_comparison_report()
        
        # Check report structure
        self.assertIn('dataset_size', report)
        self.assertIn('algorithms', report)
        self.assertIn('rankings', report)
        
        self.assertEqual(report['dataset_size'], len(self.test_data))
        self.assertEqual(len(report['algorithms']), 2)
        
        # Check rankings
        ranking_metrics = ['execution_time', 'comparisons', 'swaps', 'total_steps']
        for metric in ranking_metrics:
            self.assertIn(metric, report['rankings'])
            self.assertEqual(len(report['rankings'][metric]), 2)

class TestTextVisualization(unittest.TestCase):
    """Test text-based visualization features."""
    
    def setUp(self):
        self.text_viz = TextVisualizer()
        self.sample_step = AlgorithmStep(
            step_number=1,
            description="Test step",
            array_state=[3, 1, 4, 1, 5],
            highlighted_indices=[0, 2],
            comparison_indices=[1, 3]
        )
    
    def test_symbol_assignment(self):
        """Test that symbols are correctly assigned to array elements."""
        # Test different roles
        symbol_default = self.text_viz._get_symbol(4, self.sample_step)
        symbol_highlighted = self.text_viz._get_symbol(0, self.sample_step)
        symbol_comparison = self.text_viz._get_symbol(1, self.sample_step)
        
        self.assertEqual(symbol_default, self.text_viz.color_symbols['default'])
        self.assertEqual(symbol_highlighted, self.text_viz.color_symbols['highlighted'])
        self.assertEqual(symbol_comparison, self.text_viz.color_symbols['comparing'])
    
    def test_summary_report_generation(self):
        """Test that summary reports are generated correctly."""
        visualizer = MergeSortVisualizer(data=[3, 1, 4, 1, 5])
        result = visualizer.sort()
        
        report = self.text_viz.create_summary_report(visualizer)
        
        # Should contain key information
        self.assertIn("ALGORITHM ANALYSIS REPORT", report)
        self.assertIn("Merge Sort", report)
        self.assertIn("Time Complexity", report)
        self.assertIn("Space Complexity", report)

class TestDataExportImport(unittest.TestCase):
    """Test data export and import functionality."""
    
    def setUp(self):
        self.test_data = [6, 2, 8, 4, 1]
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        # Clean up temporary files
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_metrics_export_import(self):
        """Test exporting and importing metrics."""
        # Run algorithm
        visualizer = QuickSortVisualizer(data=self.test_data.copy())
        result = visualizer.sort()
        
        # Export metrics
        export_file = os.path.join(self.temp_dir, "test_metrics.json")
        export_metrics(visualizer, export_file)
        
        # Check file was created
        self.assertTrue(os.path.exists(export_file))
        
        # Import and verify
        imported_data = import_metrics(export_file)
        
        # Check structure
        self.assertIn('summary', imported_data)
        self.assertIn('steps', imported_data)
        
        # Check summary content
        summary = imported_data['summary']
        self.assertEqual(summary['algorithm'], visualizer.name)
        self.assertEqual(summary['array_size'], len(self.test_data))
        
        # Check steps content
        steps = imported_data['steps']
        self.assertEqual(len(steps), len(visualizer.steps))
        
        for i, step_data in enumerate(steps):
            original_step = visualizer.steps[i]
            self.assertEqual(step_data['step_number'], original_step.step_number)
            self.assertEqual(step_data['description'], original_step.description)
            self.assertEqual(step_data['array_state'], original_step.array_state)

class TestVisualizerFactory(unittest.TestCase):
    """Test visualizer factory and registry functions."""
    
    def test_available_visualizers(self):
        """Test that all expected visualizers are available."""
        expected_algorithms = [
            'merge_sort', 'quick_sort', 'selection_sort', 'priority_queue_sort'
        ]
        
        for alg_name in expected_algorithms:
            self.assertIn(alg_name, AVAILABLE_VISUALIZERS)
            self.assertTrue(callable(AVAILABLE_VISUALIZERS[alg_name]))
    
    def test_visualizer_creation(self):
        """Test creating visualizers through factory function."""
        test_data = [5, 3, 8, 1]
        
        for alg_name in AVAILABLE_VISUALIZERS.keys():
            with self.subTest(algorithm=alg_name):
                visualizer = create_visualizer(alg_name, test_data.copy())
                self.assertIsInstance(visualizer, AlgorithmVisualizer)
                
                # Should be able to sort
                result = visualizer.sort()
                self.assertEqual(result, sorted(test_data))
    
    def test_invalid_algorithm_name(self):
        """Test handling of invalid algorithm names."""
        with self.assertRaises(ValueError):
            create_visualizer("invalid_algorithm", [1, 2, 3])

class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions."""
    
    def test_empty_array(self):
        """Test handling of empty arrays."""
        for alg_class in [MergeSortVisualizer, QuickSortVisualizer, 
                          SelectionSortVisualizer, PriorityQueueSortVisualizer]:
            with self.subTest(algorithm=alg_class.__name__):
                visualizer = alg_class(data=[])
                result = visualizer.sort()
                self.assertEqual(result, [])
    
    def test_single_element(self):
        """Test handling of single-element arrays."""
        for alg_class in [MergeSortVisualizer, QuickSortVisualizer, 
                          SelectionSortVisualizer, PriorityQueueSortVisualizer]:
            with self.subTest(algorithm=alg_class.__name__):
                visualizer = alg_class(data=[42])
                result = visualizer.sort()
                self.assertEqual(result, [42])
    
    def test_duplicate_elements(self):
        """Test handling of arrays with duplicate elements."""
        test_data = [5, 3, 5, 1, 3, 5]
        expected = [1, 3, 3, 5, 5, 5]
        
        for alg_class in [MergeSortVisualizer, QuickSortVisualizer, 
                          SelectionSortVisualizer, PriorityQueueSortVisualizer]:
            with self.subTest(algorithm=alg_class.__name__):
                visualizer = alg_class(data=test_data.copy())
                result = visualizer.sort()
                self.assertEqual(result, expected)
    
    def test_already_sorted(self):
        """Test handling of already sorted arrays."""
        test_data = [1, 2, 3, 4, 5]
        
        for alg_class in [MergeSortVisualizer, QuickSortVisualizer, 
                          SelectionSortVisualizer, PriorityQueueSortVisualizer]:
            with self.subTest(algorithm=alg_class.__name__):
                visualizer = alg_class(data=test_data.copy())
                result = visualizer.sort()
                self.assertEqual(result, test_data)
    
    def test_reverse_sorted(self):
        """Test handling of reverse sorted arrays (worst case for some algorithms)."""
        test_data = [5, 4, 3, 2, 1]
        expected = [1, 2, 3, 4, 5]
        
        for alg_class in [MergeSortVisualizer, QuickSortVisualizer, 
                          SelectionSortVisualizer, PriorityQueueSortVisualizer]:
            with self.subTest(algorithm=alg_class.__name__):
                visualizer = alg_class(data=test_data.copy())
                result = visualizer.sort()
                self.assertEqual(result, expected)

class TestPerformanceConsistency(unittest.TestCase):
    """Test that performance measurements are consistent and reasonable."""
    
    def test_execution_time_measurement(self):
        """Test that execution time is properly measured."""
        # Large enough dataset to have measurable time
        test_data = list(range(100, 0, -1))  # Reverse sorted for worst case
        
        comparator = AlgorithmComparator(test_data)
        visualizer = comparator.add_algorithm(MergeSortVisualizer)
        
        # Should have recorded some execution time
        self.assertGreater(visualizer.metrics.execution_time, 0)
        self.assertLess(visualizer.metrics.execution_time, 10)  # Should be reasonable
    
    def test_comparison_counting(self):
        """Test that comparisons are properly counted."""
        test_data = [4, 2, 7, 1, 9, 3]
        
        # Selection sort should make many comparisons
        visualizer = SelectionSortVisualizer(data=test_data)
        result = visualizer.sort()
        
        # For selection sort, expect O(n²) comparisons
        n = len(test_data)
        expected_min_comparisons = (n - 1)  # At least n-1 comparisons
        
        self.assertGreaterEqual(visualizer.metrics.comparisons, expected_min_comparisons)
    
    def test_metric_consistency(self):
        """Test that metrics are consistent across runs."""
        test_data = [3, 1, 4, 1, 5, 9, 2, 6]
        
        # Run the same algorithm multiple times
        results = []
        for _ in range(3):
            visualizer = MergeSortVisualizer(data=test_data.copy())
            visualizer.sort()
            results.append({
                'comparisons': visualizer.metrics.comparisons,
                'swaps': visualizer.metrics.swaps,
                'steps': len(visualizer.steps)
            })
        
        # Deterministic algorithms should give consistent results
        first_result = results[0]
        for result in results[1:]:
            self.assertEqual(result['comparisons'], first_result['comparisons'])
            self.assertEqual(result['swaps'], first_result['swaps'])
            self.assertEqual(result['steps'], first_result['steps'])

if __name__ == '__main__':
    # Create test suite
    test_classes = [
        TestAlgorithmVisualizerCore,
        TestSortingAlgorithms,
        TestVisualizationTracking,
        TestAlgorithmComparator,
        TestTextVisualization,
        TestDataExportImport,
        TestVisualizerFactory,
        TestEdgeCases,
        TestPerformanceConsistency
    ]
    
    suite = unittest.TestSuite()
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\\n{'='*60}")
    print(f"TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print(f"\\nFAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print(f"\\nERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    success_rate = (result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100
    print(f"\\nSuccess Rate: {success_rate:.1f}%")
    
    if result.wasSuccessful():
        print("\\n🎉 All tests passed! The algorithm visualization framework is working correctly.")
    else:
        print("\\n❌ Some tests failed. Please review the errors above.")