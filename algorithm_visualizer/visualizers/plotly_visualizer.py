"""Plotly-based visualization backend."""

from typing import List, Optional
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from ..core.base import AlgorithmStep, Number


class PlotlyVisualizer:
    """Plotly-based visualizer for sorting algorithms."""
    
    def __init__(self, width: int = 800, height: int = 600):
        """Initialize the plotly visualizer.
        
        Args:
            width: Figure width in pixels
            height: Figure height in pixels
        """
        self.width = width
        self.height = height
        
    def visualize_steps(self, steps: List[AlgorithmStep], data: List[Number], 
                       title: str = "Algorithm Visualization") -> None:
        """Create static visualization of algorithm steps.
        
        Args:
            steps: List of algorithm steps
            data: Original data
            title: Title for the visualization
        """
        if not steps:
            print("No steps to visualize")
            return
            
        # Select key steps to display
        num_steps = min(len(steps), 6)
        step_indices = self._select_key_steps(steps, num_steps)
        
        # Create subplots
        cols = 3
        rows = (num_steps + cols - 1) // cols
        
        fig = make_subplots(
            rows=rows, cols=cols,
            subplot_titles=[f"Step {i+1}: {steps[i].description}" 
                          for i in step_indices],
            vertical_spacing=0.1
        )
        
        for idx, step_idx in enumerate(step_indices):
            row = idx // cols + 1
            col = idx % cols + 1
            step = steps[step_idx]
            
            # Create bar chart for this step
            colors = ['red' if i in step.highlighted_indices else 'lightblue' 
                     for i in range(len(step.array_state))]
            
            fig.add_trace(
                go.Bar(
                    x=list(range(len(step.array_state))),
                    y=step.array_state,
                    marker_color=colors,
                    showlegend=False,
                    text=step.array_state,
                    textposition='outside'
                ),
                row=row, col=col
            )
        
        fig.update_layout(
            title=title,
            height=self.height,
            width=self.width,
            showlegend=False
        )
        
        fig.show()
    
    def animate_algorithm(self, steps: List[AlgorithmStep], data: List[Number],
                         title: str = "Algorithm Animation") -> None:
        """Create animated visualization of algorithm steps.
        
        Args:
            steps: List of algorithm steps
            data: Original data
            title: Title for the animation
        """
        if not steps:
            print("No steps to animate")
            return
            
        # Create frames for animation
        frames = []
        for i, step in enumerate(steps):
            colors = ['red' if j in step.highlighted_indices else 'lightblue' 
                     for j in range(len(step.array_state))]
            
            frame = go.Frame(
                data=[go.Bar(
                    x=list(range(len(step.array_state))),
                    y=step.array_state,
                    marker_color=colors,
                    text=step.array_state,
                    textposition='outside'
                )],
                name=f"Step {i+1}",
                layout=go.Layout(
                    title=f"Step {i+1}: {step.description}"
                )
            )
            frames.append(frame)
        
        # Create initial figure
        initial_step = steps[0]
        colors = ['red' if i in initial_step.highlighted_indices else 'lightblue' 
                 for i in range(len(initial_step.array_state))]
        
        fig = go.Figure(
            data=[go.Bar(
                x=list(range(len(initial_step.array_state))),
                y=initial_step.array_state,
                marker_color=colors,
                text=initial_step.array_state,
                textposition='outside'
            )],
            frames=frames
        )
        
        # Add animation controls
        fig.update_layout(
            title=title,
            width=self.width,
            height=self.height,
            updatemenus=[{
                "buttons": [
                    {
                        "args": [None, {"frame": {"duration": 1000, "redraw": True},
                                      "fromcurrent": True}],
                        "label": "Play",
                        "method": "animate"
                    },
                    {
                        "args": [[None], {"frame": {"duration": 0, "redraw": True},
                                        "mode": "immediate",
                                        "transition": {"duration": 0}}],
                        "label": "Pause",
                        "method": "animate"
                    }
                ],
                "direction": "left",
                "pad": {"r": 10, "t": 87},
                "showactive": False,
                "type": "buttons",
                "x": 0.1,
                "xanchor": "right",
                "y": 0,
                "yanchor": "top"
            }],
            sliders=[{
                "active": 0,
                "yanchor": "top",
                "xanchor": "left",
                "currentvalue": {
                    "font": {"size": 20},
                    "prefix": "Step:",
                    "visible": True,
                    "xanchor": "right"
                },
                "transition": {"duration": 300, "easing": "cubic-in-out"},
                "pad": {"b": 10, "t": 50},
                "len": 0.9,
                "x": 0.1,
                "y": 0,
                "steps": [
                    {
                        "args": [[f"Step {i+1}"],
                               {"frame": {"duration": 300, "redraw": True},
                                "mode": "immediate",
                                "transition": {"duration": 300}}],
                        "label": f"Step {i+1}",
                        "method": "animate"
                    }
                    for i in range(len(steps))
                ]
            }]
        )
        
        fig.show()
    
    def plot_performance_comparison(self, algorithms: List[str], 
                                  times: List[float], comparisons: List[int],
                                  title: str = "Performance Comparison") -> None:
        """Create performance comparison charts.
        
        Args:
            algorithms: List of algorithm names
            times: Execution times for each algorithm
            comparisons: Number of comparisons for each algorithm
            title: Title for the charts
        """
        # Create subplots
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=("Execution Time", "Number of Comparisons"),
            specs=[[{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Execution time chart
        fig.add_trace(
            go.Bar(
                x=algorithms,
                y=times,
                name="Time (s)",
                marker_color='skyblue',
                text=[f'{t:.4f}' for t in times],
                textposition='outside'
            ),
            row=1, col=1
        )
        
        # Comparisons chart
        fig.add_trace(
            go.Bar(
                x=algorithms,
                y=comparisons,
                name="Comparisons",
                marker_color='lightcoral',
                text=[str(c) for c in comparisons],
                textposition='outside'
            ),
            row=1, col=2
        )
        
        fig.update_layout(
            title=title,
            height=self.height,
            width=self.width,
            showlegend=False
        )
        
        fig.show()
    
    def _select_key_steps(self, steps: List[AlgorithmStep], num_steps: int) -> List[int]:
        """Select key steps to display from all steps.
        
        Args:
            steps: All algorithm steps
            num_steps: Number of steps to select
            
        Returns:
            List of step indices to display
        """
        if len(steps) <= num_steps:
            return list(range(len(steps)))
        
        # Always include first and last steps
        if num_steps < 2:
            return [0]
        
        indices = [0]
        
        # Select evenly spaced steps in between
        if num_steps > 2:
            step_size = (len(steps) - 2) / (num_steps - 2)
            for i in range(1, num_steps - 1):
                idx = int(1 + (i - 1) * step_size)
                indices.append(idx)
        
        # Always include the last step
        indices.append(len(steps) - 1)
        
        return indices