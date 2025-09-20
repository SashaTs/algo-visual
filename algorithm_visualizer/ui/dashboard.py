"""Streamlit dashboard for algorithm visualization."""

import streamlit as st
import pandas as pd
from typing import List, Optional
import time
import sys
import os

# Add the parent directory to the path to enable absolute imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Try relative imports first (when run as module), fall back to absolute imports
try:
    from ..algorithms import create_algorithm_visualizer, get_available_algorithms, get_algorithm_info
    from ..core.comparator import AlgorithmComparator
    from ..utils.data_io import read_numbers, export_metrics, save_dataset, generate_test_data
    from ..visualizers import get_available_backends, create_visualizer, MATPLOTLIB_AVAILABLE, PLOTLY_AVAILABLE
    from ..core.base import Number
    from .animations import create_modern_visualization, StreamlitAnimationManager
    from .code_animation import create_code_animation
except ImportError:
    # Fallback to absolute imports when run directly
    from algorithm_visualizer.algorithms import create_algorithm_visualizer, get_available_algorithms, get_algorithm_info
    from algorithm_visualizer.core.comparator import AlgorithmComparator
    from algorithm_visualizer.utils.data_io import read_numbers, export_metrics, save_dataset, generate_test_data
    from algorithm_visualizer.visualizers import get_available_backends, create_visualizer, MATPLOTLIB_AVAILABLE, PLOTLY_AVAILABLE
    from algorithm_visualizer.core.base import Number
    from algorithm_visualizer.ui.animations import create_modern_visualization, StreamlitAnimationManager
    from algorithm_visualizer.ui.code_animation import create_code_animation
    from algorithm_visualizer.ui.animations import create_modern_visualization, StreamlitAnimationManager


class StreamlitDashboard:
    """Streamlit-based web dashboard for algorithm visualization."""
    
    def __init__(self):
        """Initialize the dashboard."""
        self.setup_page()
        
    def setup_page(self):
        """Set up the Streamlit page configuration."""
        st.set_page_config(
            page_title="Algorithm Visualizer",
            page_icon="📊",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Custom CSS
        st.markdown("""
        <style>
        .metric-card {
            background-color: #f0f2f6;
            border-radius: 10px;
            padding: 10px;
            margin: 5px 0;
        }
        .algorithm-header {
            background-color: #e1f5fe;
            border-radius: 5px;
            padding: 10px;
            margin: 10px 0;
        }
        </style>
        """, unsafe_allow_html=True)
    
    def run(self):
        """Run the main dashboard."""
        st.title("🔍 Algorithm Visualization Dashboard")
        st.markdown("Explore and compare sorting algorithms with interactive visualizations")
        
        # Sidebar for configuration
        self.render_sidebar()
        
        # Main content area
        tab1, tab2, tab3, tab4 = st.tabs([
            "📈 Single Algorithm", 
            "⚡ Algorithm Comparison", 
            "📊 Performance Analysis",
            "ℹ️ Algorithm Info"
        ])
        
        with tab1:
            self.render_single_algorithm_tab()
        
        with tab2:
            self.render_comparison_tab()
        
        with tab3:
            self.render_performance_tab()
        
        with tab4:
            self.render_info_tab()
    
    def render_sidebar(self):
        """Render the sidebar configuration."""
        st.sidebar.header("⚙️ Configuration")
        
        # Data input section
        st.sidebar.subheader("📋 Data Input")
        
        data_source = st.sidebar.radio(
            "Choose data source:",
            ["Manual Input", "Random Generation", "File Upload"]
        )
        
        if data_source == "Manual Input":
            data_input = st.sidebar.text_input(
                "Enter numbers (comma-separated):",
                value="64, 34, 25, 12, 22, 11, 90"
            )
            try:
                st.session_state.data = [int(x.strip()) for x in data_input.split(',')]
            except ValueError:
                st.sidebar.error("Please enter valid numbers separated by commas")
                st.session_state.data = [64, 34, 25, 12, 22, 11, 90]
        
        elif data_source == "Random Generation":
            col1, col2 = st.sidebar.columns(2)
            with col1:
                size = st.number_input("Size:", min_value=5, max_value=100, value=10)
            with col2:
                seed = st.number_input("Seed:", min_value=0, value=42)
            
            min_val = st.sidebar.slider("Min value:", 1, 50, 1)
            max_val = st.sidebar.slider("Max value:", 51, 200, 100)
            
            if st.sidebar.button("Generate New Data"):
                st.session_state.data = generate_test_data(size, min_val, max_val, 'random')
            
            if 'data' not in st.session_state:
                st.session_state.data = generate_test_data(size, min_val, max_val, 'random')
        
        elif data_source == "File Upload":
            uploaded_file = st.sidebar.file_uploader(
                "Choose a file", 
                type=['txt', 'csv']
            )
            if uploaded_file is not None:
                try:
                    content = uploaded_file.read().decode()
                    numbers = [int(x.strip()) for x in content.replace('\n', ',').split(',') if x.strip()]
                    st.session_state.data = numbers
                    st.sidebar.success(f"Loaded {len(numbers)} numbers")
                except Exception as e:
                    st.sidebar.error(f"Error loading file: {e}")
        
        # Visualization settings
        st.sidebar.subheader("🎨 Visualization")
        
        available_backends = get_available_backends()
        # Add modern animation options
        available_backends.extend(["animated", "code"])
        
        backend_options = {
            "text": "📝 Text",
            "matplotlib": "📊 Matplotlib", 
            "plotly": "📈 Plotly",
            "animated": "🎬 Modern Animated",
            "code": "💻 Code Animation"
        }
        
        # Filter to only show available options
        filtered_options = {k: v for k, v in backend_options.items() if k in available_backends}
        
        backend = st.sidebar.selectbox(
            "Visualization backend:",
            options=list(filtered_options.keys()),
            format_func=lambda x: filtered_options[x],
            index=len(filtered_options) - 1 if "animated" in filtered_options else 0
        )
        st.session_state.visualization_backend = backend
        
        # Display current data
        if 'data' in st.session_state:
            st.sidebar.subheader("📊 Current Data")
            st.sidebar.write(f"Size: {len(st.session_state.data)}")
            st.sidebar.write(f"Range: {min(st.session_state.data)} - {max(st.session_state.data)}")
            with st.sidebar.expander("View data"):
                st.write(st.session_state.data)
    
    def render_single_algorithm_tab(self):
        """Render the single algorithm tab."""
        if 'data' not in st.session_state:
            st.warning("Please configure data in the sidebar first")
            return
        
        st.header("📈 Single Algorithm Analysis")
        
        # Algorithm selection
        algorithms = get_available_algorithms()
        selected_algorithm = st.selectbox(
            "Choose an algorithm:",
            algorithms,
            key="single_algo"
        )
        
        # Configuration
        col1, col2 = st.columns(2)
        with col1:
            show_steps = st.checkbox("Show step-by-step visualization", value=True)
        with col2:
            show_metrics = st.checkbox("Show performance metrics", value=True)
        
        if st.button("🚀 Run Algorithm", key="run_single"):
            with st.spinner(f"Running {selected_algorithm}..."):
                try:
                    # Create and run visualizer
                    visualizer = create_algorithm_visualizer(selected_algorithm, st.session_state.data.copy())
                    visualizer.sort()
                    
                    # Store results in session state for animation
                    st.session_state.current_visualizer = visualizer
                    st.session_state.current_algorithm = selected_algorithm
                    st.session_state.algorithm_executed = True
                    
                    # Display results
                    st.success(f"✅ {selected_algorithm} completed successfully!")
                    
                except Exception as e:
                    st.error(f"Error running algorithm: {e}")
                    st.session_state.algorithm_executed = False
        
        # Display results if algorithm has been executed
        if st.session_state.get('algorithm_executed', False) and 'current_visualizer' in st.session_state:
            visualizer = st.session_state.current_visualizer
            selected_algorithm = st.session_state.current_algorithm
            
            # Show before/after
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Before")
                st.write(st.session_state.data)
            with col2:
                st.subheader("After")
                st.write(visualizer.get_sorted_data())
            
            # Show metrics
            if show_metrics:
                self.display_metrics(visualizer, selected_algorithm)
            
            # Show steps (only if not using animated or code visualization)
            if show_steps and st.session_state.visualization_backend not in ['animated', 'code']:
                self.display_algorithm_steps(visualizer, selected_algorithm)
            
            # Visualization
            if st.session_state.visualization_backend == 'animated':
                st.subheader("🎬 Modern Animation")
                create_modern_visualization(visualizer, selected_algorithm)
            elif st.session_state.visualization_backend == 'code':
                st.subheader("💻 Code Animation")
                create_code_animation(visualizer, selected_algorithm)
            elif st.session_state.visualization_backend != 'text':
                self.render_visualization(visualizer, selected_algorithm)
    
    def render_comparison_tab(self):
        """Render the algorithm comparison tab."""
        if 'data' not in st.session_state:
            st.warning("Please configure data in the sidebar first")
            return
        
        st.header("⚡ Algorithm Comparison")
        
        # Algorithm selection
        algorithms = get_available_algorithms()
        selected_algorithms = st.multiselect(
            "Choose algorithms to compare:",
            algorithms,
            default=algorithms[:3] if len(algorithms) >= 3 else algorithms
        )
        
        if len(selected_algorithms) < 2:
            st.warning("Please select at least 2 algorithms for comparison")
            return
        
        if st.button("🏁 Compare Algorithms", key="compare"):
            with st.spinner("Running comparison..."):
                try:
                    comparator = AlgorithmComparator(st.session_state.data)
                    results = {}
                    
                    # Progress bar
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    for i, algorithm in enumerate(selected_algorithms):
                        status_text.text(f"Running {algorithm}...")
                        
                        visualizer = create_algorithm_visualizer(algorithm, st.session_state.data.copy())
                        visualizer.sort()
                        results[algorithm] = visualizer
                        
                        progress_bar.progress((i + 1) / len(selected_algorithms))
                    
                    status_text.text("Comparison complete!")
                    st.success("✅ All algorithms completed!")
                    
                    # Display comparison table
                    self.display_comparison_results(comparator, results)
                    
                except Exception as e:
                    st.error(f"Error during comparison: {e}")
    
    def render_performance_tab(self):
        """Render the performance analysis tab."""
        st.header("📊 Performance Analysis")
        
        if 'data' not in st.session_state:
            st.warning("Please configure data in the sidebar first")
            return
        
        st.subheader("🔬 Detailed Performance Testing")
        
        # Test configuration
        col1, col2, col3 = st.columns(3)
        with col1:
            test_sizes = st.multiselect(
                "Test data sizes:",
                [10, 25, 50, 100, 200, 500],
                default=[10, 25, 50]
            )
        with col2:
            test_types = st.multiselect(
                "Data types:",
                ["Random", "Sorted", "Reverse Sorted", "Nearly Sorted"],
                default=["Random"]
            )
        with col3:
            algorithms_to_test = st.multiselect(
                "Algorithms:",
                get_available_algorithms(),
                default=get_available_algorithms()[:3]
            )
        
        if st.button("🧪 Run Performance Tests", key="perf_test"):
            if not test_sizes or not test_types or not algorithms_to_test:
                st.warning("Please select test parameters")
                return
            
            with st.spinner("Running performance tests..."):
                results_data = []
                total_tests = len(test_sizes) * len(test_types) * len(algorithms_to_test)
                progress_bar = st.progress(0)
                test_count = 0
                
                for size in test_sizes:
                    for data_type in test_types:
                        # Generate test data
                        if data_type == "Random":
                            test_data = generate_test_data(size, 1, size, 'random')
                        elif data_type == "Sorted":
                            test_data = generate_test_data(size, 1, size, 'sorted')
                        elif data_type == "Reverse Sorted":
                            test_data = generate_test_data(size, 1, size, 'reverse')
                        else:  # Nearly Sorted
                            test_data = generate_test_data(size, 1, size, 'nearly_sorted')
                            # Swap a few elements
                            for i in range(min(3, size // 10)):
                                j = (i + size // 3) % size
                                test_data[i], test_data[j] = test_data[j], test_data[i]
                        
                        for algorithm in algorithms_to_test:
                            try:
                                visualizer = create_algorithm_visualizer(algorithm, test_data.copy())
                                visualizer.sort()
                                metrics = visualizer.get_performance_metrics()
                                
                                results_data.append({
                                    'Algorithm': algorithm,
                                    'Data Size': size,
                                    'Data Type': data_type,
                                    'Execution Time': metrics.execution_time,
                                    'Comparisons': metrics.comparisons,
                                    'Swaps': metrics.swaps,
                                    'Memory Usage': metrics.memory_usage
                                })
                            except Exception as e:
                                st.warning(f"Failed {algorithm} on {data_type} size {size}: {e}")
                            
                            test_count += 1
                            progress_bar.progress(test_count / total_tests)
                
                if results_data:
                    df = pd.DataFrame(results_data)
                    self.display_performance_analysis(df)
    
    def render_info_tab(self):
        """Render the algorithm information tab."""
        st.header("ℹ️ Algorithm Information")
        
        algorithms = get_available_algorithms()
        
        for algorithm in algorithms:
            with st.expander(f"📖 {algorithm}"):
                try:
                    # Get algorithm info without creating full instance
                    info = get_algorithm_info(algorithm)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("**Time Complexity:**", info.get('time_complexity', 'N/A'))
                        st.write("**Space Complexity:**", info.get('space_complexity', 'N/A'))
                    with col2:
                        st.write("**Stable:**", info.get('stable', 'N/A'))
                        st.write("**In-place:**", info.get('in_place', 'N/A'))
                    
                    st.write("**Description:**", info.get('description', 'No description available'))
                    
                except Exception as e:
                    st.error(f"Error getting info for {algorithm}: {e}")
    
    def display_metrics(self, visualizer, algorithm_name: str):
        """Display performance metrics."""
        st.subheader(f"📊 Performance Metrics - {algorithm_name}")
        
        metrics = visualizer.get_performance_metrics()
        steps_count = len(visualizer.get_steps())
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Steps", steps_count)
        with col2:
            st.metric("Comparisons", metrics.comparisons)
        with col3:
            st.metric("Swaps", metrics.swaps)
        with col4:
            st.metric("Time (s)", f"{metrics.execution_time:.6f}")
    
    def display_algorithm_steps(self, visualizer, algorithm_name: str):
        """Display algorithm steps."""
        st.subheader(f"👣 Algorithm Steps - {algorithm_name}")
        
        steps = visualizer.get_steps()
        if not steps:
            st.info("No steps recorded")
            return
        
        # Show step count
        st.write(f"Total steps: {len(steps)}")
        
        # Option to show all steps or key steps
        show_all = st.checkbox("Show all steps (may be slow for large datasets)")
        
        if show_all:
            steps_to_show = steps
        else:
            # Show first 10 steps
            steps_to_show = steps[:10]
            if len(steps) > 10:
                st.info(f"Showing first 10 steps out of {len(steps)} total")
        
        for i, step in enumerate(steps_to_show):
            with st.expander(f"Step {i+1}: {step.description}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Array state:**", step.array_state)
                with col2:
                    if step.highlighted_indices:
                        st.write("**Highlighted indices:**", step.highlighted_indices)
    
    def display_comparison_results(self, comparator, results):
        """Display algorithm comparison results."""
        st.subheader("📋 Comparison Results")
        
        # Get comparison data
        comparison_data = []
        for algorithm_name, visualizer in results.items():
            metrics = visualizer.get_performance_metrics()
            steps_count = len(visualizer.get_steps())
            comparison_data.append({
                'Algorithm': algorithm_name,
                'Steps': steps_count,
                'Comparisons': metrics.comparisons,
                'Swaps': metrics.swaps,
                'Time (s)': f"{metrics.execution_time:.6f}",
                'Memory': metrics.memory_usage
            })
        
        df = pd.DataFrame(comparison_data)
        st.dataframe(df, width='stretch')
        
        # Best algorithm
        best = comparator.get_best_algorithm()
        if best:
            st.success(f"🏆 Best overall algorithm: **{best}**")
        
        # Visualization
        if MATPLOTLIB_AVAILABLE or PLOTLY_AVAILABLE:
            self.render_comparison_charts(results)
    
    def display_performance_analysis(self, df):
        """Display performance analysis results."""
        st.subheader("📈 Performance Analysis Results")
        
        # Show raw data
        with st.expander("📋 Raw Data"):
            st.dataframe(df)
        
        # Summary statistics
        st.subheader("📊 Summary Statistics")
        numeric_cols = ['Execution Time', 'Comparisons', 'Swaps']
        summary = df.groupby('Algorithm')[numeric_cols].agg(['mean', 'std', 'min', 'max'])
        st.dataframe(summary)
        
        # Charts
        if MATPLOTLIB_AVAILABLE or PLOTLY_AVAILABLE:
            self.render_performance_charts(df)
    
    def render_visualization(self, visualizer, algorithm_name: str):
        """Render algorithm visualization."""
        st.subheader(f"🎨 Visualization - {algorithm_name}")
        
        backend = st.session_state.get('visualization_backend', 'text')
        
        if backend == 'text':
            # Already shown in steps
            st.info("Text visualization is shown in the steps above")
        elif backend == 'animated':
            # Animated visualization is handled separately
            st.info("Animated visualization is shown above")
        elif backend == 'code':
            # Code animation is handled separately
            st.info("Code animation is shown above")
        else:
            try:
                viz = create_visualizer(backend)
                steps = visualizer.get_steps()
                data = st.session_state.data
                
                if hasattr(viz, 'visualize_steps') and callable(getattr(viz, 'visualize_steps', None)):
                    # Type narrowing: we know viz has visualize_steps method
                    fig = getattr(viz, 'visualize_steps')(steps, data, f"{algorithm_name} Visualization")
                    if fig is not None:
                        if backend == 'matplotlib':
                            st.pyplot(fig)
                        elif backend == 'plotly':
                            st.plotly_chart(fig, width='stretch')
                    else:
                        st.error(f"Failed to create {backend} visualization")
                else:
                    # Fallback for visualizers that don't support visualize_steps
                    st.text("Step-by-step visualization:")
                    for i, step in enumerate(steps[:10]):  # Show first 10 steps
                        st.text(f"Step {step.step_number}: {step.description}")
                        st.text(f"Array: {step.array_state}")
                        if i < len(steps) - 1 and i < 9:
                            st.text("---")
                
            except Exception as e:
                st.error(f"Error creating {backend} visualization: {e}")
                st.info("Falling back to text visualization")
    
    def render_comparison_charts(self, results):
        """Render comparison charts."""
        st.subheader("📊 Performance Charts")
        
        algorithms = list(results.keys())
        times = [results[alg].get_performance_metrics().execution_time for alg in algorithms]
        comparisons = [results[alg].get_performance_metrics().comparisons for alg in algorithms]
        
        backend = st.session_state.get('visualization_backend', 'text')
        
        if backend == 'text':
            # Text doesn't support performance comparison charts
            pass
        elif backend == 'animated':
            # Animated backend doesn't support performance comparison charts
            st.info("Performance comparison charts not available for animated backend")
        elif backend == 'code':
            # Code backend doesn't support performance comparison charts
            st.info("Performance comparison charts not available for code animation backend")
        else:
            try:
                viz = create_visualizer(backend)
                if hasattr(viz, 'plot_performance_comparison') and callable(getattr(viz, 'plot_performance_comparison', None)):
                    # Type narrowing: we know viz has plot_performance_comparison method
                    fig = getattr(viz, 'plot_performance_comparison')(algorithms, times, comparisons)
                    if fig is not None:
                        if backend == 'matplotlib':
                            st.pyplot(fig)
                        elif backend == 'plotly':
                            st.plotly_chart(fig, width='stretch')
                    else:
                        st.error(f"Failed to create {backend} performance charts")
                else:
                    st.info(f"Performance comparison charts not available for {backend} backend")
            except Exception as e:
                st.error(f"Error creating {backend} charts: {e}")
        
        # Fallback to streamlit charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.bar_chart(dict(zip(algorithms, times)))
            st.caption("Execution Time (seconds)")
        
        with col2:
            st.bar_chart(dict(zip(algorithms, comparisons)))
            st.caption("Number of Comparisons")
    
    def render_performance_charts(self, df):
        """Render performance analysis charts."""
        st.subheader("📈 Performance Charts")
        
        backend = st.session_state.get('visualization_backend', 'text')
        
        if backend == 'text':
            # Text backend - show data tables
            st.write("**Execution Time by Data Size**")
            pivot_time = df.pivot_table(values='Execution Time', index='Data Size', columns='Algorithm')
            st.dataframe(pivot_time)
            
            st.write("**Comparisons by Data Size**")
            pivot_comparisons = df.pivot_table(values='Comparisons', index='Data Size', columns='Algorithm')
            st.dataframe(pivot_comparisons)
            
        elif backend == 'animated':
            # Animated backend doesn't support performance analysis charts
            st.info("Performance analysis charts not available for animated backend")
            
        elif backend == 'code':
            # Code backend doesn't support performance analysis charts
            st.info("Performance analysis charts not available for code animation backend")
            
        else:
            try:
                viz = create_visualizer(backend)
                if hasattr(viz, 'plot_performance_analysis') and callable(getattr(viz, 'plot_performance_analysis', None)):
                    # Use dedicated performance analysis method if available
                    fig = getattr(viz, 'plot_performance_analysis')(df)
                    if fig is not None:
                        if backend == 'matplotlib':
                            st.pyplot(fig)
                        elif backend == 'plotly':
                            st.plotly_chart(fig, width='stretch')
                    else:
                        st.error(f"Failed to create {backend} performance analysis charts")
                else:
                    st.info(f"Performance analysis charts not available for {backend} backend")
            except Exception as e:
                st.error(f"Error creating {backend} charts: {e}")
        
        # Fallback to streamlit charts - unified view
        st.write("**Execution Time by Data Size (All Algorithms)**")
        pivot_time = df.pivot_table(values='Execution Time', index='Data Size', columns='Algorithm')
        st.line_chart(pivot_time)
        
        st.write("**Comparisons by Data Size (All Algorithms)**")
        pivot_comparisons = df.pivot_table(values='Comparisons', index='Data Size', columns='Algorithm')
        st.line_chart(pivot_comparisons)


def main():
    """Main entry point for the dashboard."""
    dashboard = StreamlitDashboard()
    dashboard.run()


if __name__ == "__main__":
    main()