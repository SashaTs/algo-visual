"""
Specialized visualizers for algorithms that need custom visualizations.

This module provides custom visualization implementations for algorithms
that don't fit the standard array-based visualization pattern.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
import networkx as nx
from collections import deque

try:
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

from ..core.base import AlgorithmStep, Number


class BinarySearchVisualizer:
    """Specialized visualizer for Binary Search algorithm."""
    
    def __init__(self):
        self.color_scheme = {
            'target': '#e74c3c',      # Red for target
            'current': '#3498db',     # Blue for current middle
            'search_range': '#95a5a6', # Gray for search range
            'eliminated': '#ecf0f1',   # Light gray for eliminated
            'found': '#27ae60',       # Green for found
            'background': '#ffffff',   # White background
            'text': '#2c3e50'         # Dark blue for text
        }
    
    def create_matplotlib_visualization(self, steps: List[AlgorithmStep], 
                                      data: List[Number], title: str) -> plt.Figure:
        """Create matplotlib visualization for binary search."""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        fig.suptitle(title, fontsize=16, fontweight='bold')
        
        # Get target from the algorithm steps
        target = self._extract_target_from_steps(steps)
        sorted_data = sorted(data)
        
        # Upper plot: Array visualization with search range
        self._create_array_plot(ax1, sorted_data, steps, target)
        
        # Lower plot: Search progress and elimination
        self._create_progress_plot(ax2, steps, len(sorted_data))
        
        plt.tight_layout()
        return fig
    
    def create_plotly_visualization(self, steps: List[AlgorithmStep], 
                                  data: List[Number], title: str) -> go.Figure:
        """Create plotly visualization for binary search."""
        if not PLOTLY_AVAILABLE:
            raise ImportError("Plotly is required for this visualization")
        
        target = self._extract_target_from_steps(steps)
        sorted_data = sorted(data)
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Binary Search Array', 'Search Progress'),
            row_heights=[0.6, 0.4],
            vertical_spacing=0.1
        )
        
        # Add array visualization
        self._add_plotly_array_plot(fig, sorted_data, steps, target)
        
        # Add progress visualization
        self._add_plotly_progress_plot(fig, steps, len(sorted_data))
        
        fig.update_layout(
            title=title,
            height=600,
            showlegend=True
        )
        
        return fig
    
    def _extract_target_from_steps(self, steps: List[AlgorithmStep]) -> Optional[Number]:
        """Extract target value from step descriptions."""
        for step in steps:
            if 'target:' in step.description.lower():
                try:
                    # Extract number after "target:"
                    parts = step.description.lower().split('target:')
                    if len(parts) > 1:
                        target_str = parts[1].strip().split()[0]
                        return float(target_str) if '.' in target_str else int(target_str)
                except (ValueError, IndexError):
                    continue
        return None
    
    def _create_array_plot(self, ax, data: List[Number], steps: List[AlgorithmStep], target: Optional[Number]):
        """Create array visualization with search range indicators."""
        ax.clear()
        
        positions = list(range(len(data)))
        
        # Draw all elements as bars
        bars = ax.bar(positions, data, color=self.color_scheme['search_range'], 
                     alpha=0.7, edgecolor='black', linewidth=1)
        
        # Highlight based on the last step
        if steps:
            last_step = steps[-1]
            
            # Extract search range information
            left, right, mid = self._extract_search_info(last_step, len(data))
            
            # Color the search range
            if left is not None and right is not None:
                for i in range(left, right + 1):
                    if i < len(bars):
                        bars[i].set_color(self.color_scheme['search_range'])
                        bars[i].set_alpha(0.8)
            
            # Highlight middle element
            if mid is not None and mid < len(bars):
                bars[mid].set_color(self.color_scheme['current'])
                bars[mid].set_alpha(1.0)
            
            # Show eliminated regions
            if left is not None:
                for i in range(left):
                    if i < len(bars):
                        bars[i].set_color(self.color_scheme['eliminated'])
                        bars[i].set_alpha(0.3)
            
            if right is not None:
                for i in range(right + 1, len(data)):
                    if i < len(bars):
                        bars[i].set_color(self.color_scheme['eliminated'])
                        bars[i].set_alpha(0.3)
        
        # Add target line if available
        if target is not None:
            ax.axhline(y=target, color=self.color_scheme['target'], 
                      linestyle='--', linewidth=2, label=f'Target: {target}')
        
        # Customize the plot
        ax.set_xlabel('Array Index')
        ax.set_ylabel('Value')
        ax.set_title('Binary Search Array with Search Range')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # Add value labels on bars
        for i, (bar, value) in enumerate(zip(bars, data)):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                   str(value), ha='center', va='bottom', fontsize=10)
    
    def _create_progress_plot(self, ax, steps: List[AlgorithmStep], array_size: int):
        """Create search progress visualization."""
        ax.clear()
        
        step_numbers = []
        search_space_sizes = []
        
        for i, step in enumerate(steps):
            step_numbers.append(i + 1)
            left, right, _ = self._extract_search_info(step, array_size)
            
            if left is not None and right is not None:
                search_space_size = right - left + 1
            else:
                search_space_size = array_size
            
            search_space_sizes.append(search_space_size)
        
        # Plot search space reduction
        ax.plot(step_numbers, search_space_sizes, 'o-', 
               color=self.color_scheme['current'], linewidth=2, markersize=8)
        
        # Add theoretical O(log n) line for comparison
        if len(step_numbers) > 1:
            theoretical = [array_size / (2 ** (i)) for i in range(len(step_numbers))]
            ax.plot(step_numbers, theoretical, '--', 
                   color=self.color_scheme['target'], alpha=0.7, 
                   label='Theoretical O(log n)')
        
        ax.set_xlabel('Step Number')
        ax.set_ylabel('Search Space Size')
        ax.set_title('Search Space Reduction Progress')
        ax.grid(True, alpha=0.3)
        ax.legend()
        ax.set_ylim(0, array_size + 1)
    
    def _extract_search_info(self, step: AlgorithmStep, array_size: int) -> Tuple[Optional[int], Optional[int], Optional[int]]:
        """Extract left, right, and mid indices from step description."""
        desc = step.description.lower()
        left = right = mid = None
        
        # Look for range information like "range [2, 7]"
        import re
        range_match = re.search(r'range \[(\d+),\s*(\d+)\]', desc)
        if range_match:
            left = int(range_match.group(1))
            right = int(range_match.group(2))
        
        # Look for middle index like "index 4"
        mid_match = re.search(r'index (\d+)', desc)
        if mid_match:
            mid = int(mid_match.group(1))
        
        return left, right, mid
    
    def _add_plotly_array_plot(self, fig, data: List[Number], steps: List[AlgorithmStep], target: Optional[Number]):
        """Add array visualization to plotly figure."""
        positions = list(range(len(data)))
        colors = [self.color_scheme['search_range']] * len(data)
        
        # Update colors based on last step
        if steps:
            last_step = steps[-1]
            left, right, mid = self._extract_search_info(last_step, len(data))
            
            # Color eliminated regions
            if left is not None:
                for i in range(left):
                    colors[i] = self.color_scheme['eliminated']
            if right is not None:
                for i in range(right + 1, len(data)):
                    colors[i] = self.color_scheme['eliminated']
            
            # Highlight middle element
            if mid is not None and mid < len(data):
                colors[mid] = self.color_scheme['current']
        
        # Add bar chart
        fig.add_trace(
            go.Bar(x=positions, y=data, marker_color=colors,
                  text=[str(v) for v in data], textposition='outside',
                  name='Array Elements'),
            row=1, col=1
        )
        
        # Add target line if available
        if target is not None:
            fig.add_hline(y=target, line_dash="dash", line_color=self.color_scheme['target'],
                         annotation_text=f"Target: {target}", row=1, col=1)
    
    def _add_plotly_progress_plot(self, fig, steps: List[AlgorithmStep], array_size: int):
        """Add progress visualization to plotly figure."""
        step_numbers = []
        search_space_sizes = []
        
        for i, step in enumerate(steps):
            step_numbers.append(i + 1)
            left, right, _ = self._extract_search_info(step, array_size)
            
            if left is not None and right is not None:
                search_space_size = right - left + 1
            else:
                search_space_size = array_size
            
            search_space_sizes.append(search_space_size)
        
        # Add actual progress line
        fig.add_trace(
            go.Scatter(x=step_numbers, y=search_space_sizes, mode='lines+markers',
                      name='Actual Search Space', line_color=self.color_scheme['current']),
            row=2, col=1
        )
        
        # Add theoretical line
        if len(step_numbers) > 1:
            theoretical = [array_size / (2 ** i) for i in range(len(step_numbers))]
            fig.add_trace(
                go.Scatter(x=step_numbers, y=theoretical, mode='lines',
                          name='Theoretical O(log n)', line_dash='dash',
                          line_color=self.color_scheme['target']),
                row=2, col=1
            )


class BFSGraphVisualizer:
    """Specialized visualizer for Breadth-First Search algorithm."""
    
    def __init__(self):
        self.color_scheme = {
            'unvisited': '#ecf0f1',    # Light gray for unvisited
            'visiting': '#3498db',     # Blue for currently visiting
            'visited': '#27ae60',      # Green for visited
            'in_queue': '#f39c12',     # Orange for in queue
            'target': '#e74c3c',       # Red for target
            'path': '#9b59b6',         # Purple for final path
            'edge': '#95a5a6',         # Gray for edges
            'background': '#ffffff'     # White background
        }
    
    def create_matplotlib_visualization(self, steps: List[AlgorithmStep], 
                                      data: List[Number], title: str) -> plt.Figure:
        """Create matplotlib visualization for BFS."""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))
        fig.suptitle(title, fontsize=16, fontweight='bold')
        
        # Create graph from data
        graph = self._create_sample_graph(data)
        
        # Left plot: Graph visualization
        self._create_graph_plot(ax1, graph, steps)
        
        # Right plot: Queue state visualization
        self._create_queue_plot(ax2, steps)
        
        plt.tight_layout()
        return fig
    
    def create_plotly_visualization(self, steps: List[AlgorithmStep], 
                                  data: List[Number], title: str) -> go.Figure:
        """Create plotly visualization for BFS."""
        if not PLOTLY_AVAILABLE:
            raise ImportError("Plotly is required for this visualization")
        
        # Create subplots
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Graph Structure & BFS Progress', 'Queue State'),
            column_widths=[0.7, 0.3],
            horizontal_spacing=0.1,
            specs=[[{"type": "scatter"}, {"type": "bar"}]]
        )
        
        # Create graph from data
        graph = self._create_sample_graph(data)
        
        # Add graph visualization
        self._add_plotly_graph_plot(fig, graph, steps)
        
        # Add queue visualization
        self._add_plotly_queue_plot(fig, steps)
        
        fig.update_layout(
            title=title,
            height=600,
            showlegend=True
        )
        
        return fig
    
    def _create_sample_graph(self, data: List[Number]) -> Dict[int, List[int]]:
        """Create a sample graph structure for BFS demonstration."""
        # Create a graph based on the data size
        num_nodes = len(data)
        graph = {}
        
        # Create a connected graph with some interesting structure
        for i in range(num_nodes):
            graph[i] = []
        
        # Add edges to create an interesting graph structure
        if num_nodes >= 2:
            # Create a tree-like structure with some cross-connections
            for i in range(num_nodes - 1):
                graph[i].append(i + 1)
                graph[i + 1].append(i)
            
            # Add some cross-connections for more interesting BFS
            if num_nodes >= 4:
                graph[0].append(2)
                graph[2].append(0)
            if num_nodes >= 6:
                graph[1].append(4)
                graph[4].append(1)
                graph[2].append(5)
                graph[5].append(2)
        
        return graph
    
    def _create_graph_plot(self, ax, graph: Dict[int, List[int]], steps: List[AlgorithmStep]):
        """Create graph visualization with BFS progress."""
        ax.clear()
        
        # Create NetworkX graph for layout
        G = nx.Graph()
        for node, neighbors in graph.items():
            for neighbor in neighbors:
                G.add_edge(node, neighbor)
        
        # Use spring layout for nice visualization
        pos = nx.spring_layout(G, seed=42, k=2, iterations=50)
        
        # Extract BFS state from last step
        visited, queue, current = self._extract_bfs_state(steps)
        
        # Draw edges
        for node, neighbors in graph.items():
            for neighbor in neighbors:
                if node < neighbor:  # Avoid drawing edges twice
                    x_coords = [pos[node][0], pos[neighbor][0]]
                    y_coords = [pos[node][1], pos[neighbor][1]]
                    ax.plot(x_coords, y_coords, '-', color=self.color_scheme['edge'], 
                           alpha=0.6, linewidth=2, zorder=1)
        
        # Draw nodes with colors based on BFS state
        for node in G.nodes():
            color = self.color_scheme['unvisited']
            size = 300
            
            if node in visited:
                color = self.color_scheme['visited']
            elif node in queue:
                color = self.color_scheme['in_queue']
            elif node == current:
                color = self.color_scheme['visiting']
                size = 500
            
            ax.scatter(pos[node][0], pos[node][1], c=color, s=size, 
                      edgecolors='black', linewidth=2, zorder=3)
            
            # Add node labels
            ax.text(pos[node][0], pos[node][1], str(node), 
                   ha='center', va='center', fontsize=12, fontweight='bold', 
                   color='white' if color != self.color_scheme['unvisited'] else 'black',
                   zorder=4)
        
        ax.set_title('Graph Structure & BFS Progress')
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Add legend
        legend_elements = [
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=self.color_scheme['unvisited'], 
                      markersize=10, label='Unvisited'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=self.color_scheme['in_queue'], 
                      markersize=10, label='In Queue'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=self.color_scheme['visiting'], 
                      markersize=12, label='Currently Visiting'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=self.color_scheme['visited'], 
                      markersize=10, label='Visited')
        ]
        ax.legend(handles=legend_elements, loc='upper right')
    
    def _create_queue_plot(self, ax, steps: List[AlgorithmStep]):
        """Create queue state visualization."""
        ax.clear()
        
        # Extract queue state from last step
        visited, queue, current = self._extract_bfs_state(steps)
        
        if queue:
            # Create bar chart of queue contents
            positions = list(range(len(queue)))
            ax.bar(positions, [1] * len(queue), color=self.color_scheme['in_queue'], 
                  alpha=0.8, edgecolor='black', linewidth=1)
            
            # Add queue element labels
            for i, node in enumerate(queue):
                ax.text(i, 0.5, str(node), ha='center', va='center', 
                       fontsize=14, fontweight='bold', color='white')
            
            ax.set_title('Queue Contents')
            ax.set_xlabel('Queue Position')
            ax.set_ylabel('Element')
            ax.set_ylim(0, 1.2)
            ax.set_xticks(positions)
            ax.set_xticklabels([f'Pos {i}' for i in positions])
        else:
            ax.text(0.5, 0.5, 'Queue Empty', ha='center', va='center', 
                   transform=ax.transAxes, fontsize=16, fontweight='bold')
            ax.set_title('Queue Contents')
        
        ax.grid(True, alpha=0.3)
    
    def _extract_bfs_state(self, steps: List[AlgorithmStep]) -> Tuple[List[int], List[int], Optional[int]]:
        """Extract BFS state from steps."""
        visited = []
        queue = []
        current = None
        
        if not steps:
            return visited, queue, current
        
        last_step = steps[-1]
        desc = last_step.description.lower()
        
        # Extract visited nodes
        if 'path:' in desc:
            try:
                path_part = desc.split('path:')[1].strip()
                # Extract numbers from path
                import re
                numbers = re.findall(r'\d+', path_part)
                visited = [int(n) for n in numbers]
            except (IndexError, ValueError):
                pass
        
        # Extract queue contents
        if 'queue' in desc and 'contains:' in desc:
            try:
                queue_part = desc.split('contains:')[1].strip()
                import re
                numbers = re.findall(r'\d+', queue_part)
                queue = [int(n) for n in numbers]
            except (IndexError, ValueError):
                pass
        
        # Extract current node
        if 'visiting node' in desc:
            try:
                import re
                match = re.search(r'visiting node (\d+)', desc)
                if match:
                    current = int(match.group(1))
            except (ValueError, AttributeError):
                pass
        
        return visited, queue, current
    
    def _add_plotly_graph_plot(self, fig, graph: Dict[int, List[int]], steps: List[AlgorithmStep]):
        """Add graph visualization to plotly figure."""
        # Create NetworkX graph for layout
        G = nx.Graph()
        for node, neighbors in graph.items():
            for neighbor in neighbors:
                G.add_edge(node, neighbor)
        
        pos = nx.spring_layout(G, seed=42, k=2, iterations=50)
        
        # Extract BFS state
        visited, queue, current = self._extract_bfs_state(steps)
        
        # Add edges
        edge_x = []
        edge_y = []
        for node, neighbors in graph.items():
            for neighbor in neighbors:
                if node < neighbor:  # Avoid duplicates
                    edge_x.extend([pos[node][0], pos[neighbor][0], None])
                    edge_y.extend([pos[node][1], pos[neighbor][1], None])
        
        fig.add_trace(
            go.Scatter(x=edge_x, y=edge_y, mode='lines', line_color=self.color_scheme['edge'],
                      line_width=2, showlegend=False, hoverinfo='none'),
            row=1, col=1
        )
        
        # Add nodes
        node_x = []
        node_y = []
        node_colors = []
        node_text = []
        node_sizes = []
        
        for node in G.nodes():
            node_x.append(pos[node][0])
            node_y.append(pos[node][1])
            node_text.append(str(node))
            
            if node in visited:
                node_colors.append(self.color_scheme['visited'])
                node_sizes.append(20)
            elif node in queue:
                node_colors.append(self.color_scheme['in_queue'])
                node_sizes.append(20)
            elif node == current:
                node_colors.append(self.color_scheme['visiting'])
                node_sizes.append(25)
            else:
                node_colors.append(self.color_scheme['unvisited'])
                node_sizes.append(20)
        
        fig.add_trace(
            go.Scatter(x=node_x, y=node_y, mode='markers+text', text=node_text,
                      textposition="middle center", textfont_size=12,
                      marker=dict(size=node_sizes, color=node_colors, line=dict(width=2, color='black')),
                      name='Graph Nodes', showlegend=False),
            row=1, col=1
        )
    
    def _add_plotly_queue_plot(self, fig, steps: List[AlgorithmStep]):
        """Add queue visualization to plotly figure."""
        visited, queue, current = self._extract_bfs_state(steps)
        
        if queue:
            fig.add_trace(
                go.Bar(x=[f'Pos {i}' for i in range(len(queue))], 
                      y=[1] * len(queue),
                      text=[str(node) for node in queue],
                      textposition='inside',
                      marker_color=self.color_scheme['in_queue'],
                      name='Queue Contents'),
                row=1, col=2
            )
        else:
            fig.add_trace(
                go.Bar(x=['Empty'], y=[0], 
                      text=['Queue Empty'], textposition='inside',
                      marker_color=self.color_scheme['unvisited'],
                      name='Queue Contents'),
                row=1, col=2
            )