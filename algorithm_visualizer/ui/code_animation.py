"""
Animated Code Block System for Algorithm Visualization

This module provides synchronized code and data visualization,
inspired by algorithm-visualizer.org's approach.
"""

import streamlit as st
import streamlit.components.v1 as components
import time
from typing import List, Dict, Any, Optional
import inspect
import re


class CodeBlockAnimator:
    """Creates animated code blocks synchronized with algorithm execution."""
    
    def __init__(self):
        self.code_style = {
            'font_family': '"Fira Code", "SF Mono", Monaco, Consolas, monospace',
            'background': '#1e1e1e',
            'text': '#d4d4d4',
            'keyword': '#569cd6',
            'string': '#ce9178',
            'comment': '#6a9955',
            'number': '#b5cea8',
            'highlight': '#ffffff1a',
            'active_line': '#f39c1240',
            'border_radius': '8px',
            'padding': '16px',
            'line_height': '1.5'
        }
    
    def get_algorithm_source_code(self, algorithm_name: str) -> List[str]:
        """Extract and format source code for the algorithm."""
        code_templates = {
            'quick_sort': [
                "def quick_sort(arr, low, high):",
                "    if low < high:",
                "        # Partition the array and get pivot index",
                "        pivot_index = partition(arr, low, high)",
                "        ",
                "        # Recursively sort elements before partition",
                "        quick_sort(arr, low, pivot_index - 1)",
                "        ",
                "        # Recursively sort elements after partition", 
                "        quick_sort(arr, pivot_index + 1, high)",
                "",
                "def partition(arr, low, high):",
                "    # Choose rightmost element as pivot",
                "    pivot = arr[high]",
                "    i = low - 1  # Index of smaller element",
                "    ",
                "    for j in range(low, high):",
                "        # If current element is smaller than or equal to pivot",
                "        if arr[j] <= pivot:",
                "            i += 1",
                "            arr[i], arr[j] = arr[j], arr[i]  # Swap",
                "    ",
                "    # Place pivot in correct position",
                "    arr[i + 1], arr[high] = arr[high], arr[i + 1]",
                "    return i + 1  # Return partition index"
            ],
            'merge_sort': [
                "def merge_sort(arr):",
                "    if len(arr) <= 1:",
                "        return arr",
                "    ",
                "    # Divide the array into two halves",
                "    mid = len(arr) // 2",
                "    left_half = arr[:mid]",
                "    right_half = arr[mid:]",
                "    ",
                "    # Recursively sort both halves",
                "    left_sorted = merge_sort(left_half)",
                "    right_sorted = merge_sort(right_half)",
                "    ",
                "    # Merge the sorted halves",
                "    return merge(left_sorted, right_sorted)",
                "",
                "def merge(left, right):",
                "    result = []",
                "    i = j = 0",
                "    ",
                "    # Compare and merge elements",
                "    while i < len(left) and j < len(right):",
                "        if left[i] <= right[j]:",
                "            result.append(left[i])",
                "            i += 1",
                "        else:",
                "            result.append(right[j])",
                "            j += 1",
                "    ",
                "    # Add remaining elements",
                "    result.extend(left[i:])",
                "    result.extend(right[j:])",
                "    return result"
            ],
            'selection_sort': [
                "def selection_sort(arr):",
                "    n = len(arr)",
                "    ",
                "    # Traverse through all array elements",
                "    for i in range(n):",
                "        # Find minimum element in remaining unsorted array",
                "        min_idx = i",
                "        ",
                "        for j in range(i + 1, n):",
                "            # Update minimum if smaller element found",
                "            if arr[j] < arr[min_idx]:",
                "                min_idx = j",
                "        ",
                "        # Swap the found minimum element with first element",
                "        arr[i], arr[min_idx] = arr[min_idx], arr[i]",
                "    ",
                "    return arr"
            ],
            'priority_queue_sort': [
                "def priority_queue_sort(arr):",
                "    import heapq",
                "    ",
                "    # Create a min-heap from the array",
                "    heap = []",
                "    ",
                "    # Add all elements to the heap",
                "    for element in arr:",
                "        heapq.heappush(heap, element)",
                "    ",
                "    # Extract elements from heap in sorted order",
                "    sorted_arr = []",
                "    while heap:",
                "        min_element = heapq.heappop(heap)",
                "        sorted_arr.append(min_element)",
                "    ",
                "    return sorted_arr"
            ],
            'binary_search': [
                "def binary_search(arr, target):",
                "    # Ensure array is sorted",
                "    arr = sorted(arr)",
                "    left, right = 0, len(arr) - 1",
                "    ",
                "    while left <= right:",
                "        mid = (left + right) // 2",
                "        ",
                "        # Check if target is found",
                "        if arr[mid] == target:",
                "            return mid",
                "        ",
                "        # Target is in left half",
                "        elif arr[mid] > target:",
                "            right = mid - 1",
                "        ",
                "        # Target is in right half",
                "        else:",
                "            left = mid + 1",
                "    ",
                "    return -1  # Target not found"
            ],
            'bubble_sort': [
                "def bubble_sort(arr):",
                "    n = len(arr)",
                "    ",
                "    # Traverse through all array elements",
                "    for i in range(n):",
                "        swapped = False",
                "        ",
                "        # Last i elements are already sorted",
                "        for j in range(0, n - i - 1):",
                "            ",
                "            # Compare adjacent elements",
                "            if arr[j] > arr[j + 1]:",
                "                # Swap if they are in wrong order",
                "                arr[j], arr[j + 1] = arr[j + 1], arr[j]",
                "                swapped = True",
                "        ",
                "        # If no swapping occurred, array is sorted",
                "        if not swapped:",
                "            break",
                "    ",
                "    return arr"
            ],
            'breadth_first_search': [
                "def breadth_first_search(graph, start, target=None):",
                "    from collections import deque",
                "    ",
                "    visited = set()",
                "    queue = deque([start])",
                "    path = []",
                "    ",
                "    while queue:",
                "        current = queue.popleft()",
                "        ",
                "        if current in visited:",
                "            continue",
                "        ",
                "        visited.add(current)",
                "        path.append(current)",
                "        ",
                "        # Check if target found",
                "        if target and current == target:",
                "            return path",
                "        ",
                "        # Add unvisited neighbors to queue",
                "        for neighbor in graph.get(current, []):",
                "            if neighbor not in visited:",
                "                queue.append(neighbor)",
                "    ",
                "    return path"
            ]
        }
        
        return code_templates.get(algorithm_name, [f"# Code for {algorithm_name} not available yet"])
    
    def map_step_to_code_line(self, step_description: str, algorithm_name: str) -> int:
        """Map algorithm step description to corresponding code line number."""
        description_lower = step_description.lower()
        
        if algorithm_name == 'quick_sort':
            # More sophisticated mapping based on actual step descriptions
            if 'starting quick sort' in description_lower:
                return 1  # def quick_sort
            elif 'choosing pivot' in description_lower:
                return 13  # pivot = arr[high]
            elif 'comparing' in description_lower and 'pivot' in description_lower:
                return 17  # for j in range
            elif 'already in correct relative position' in description_lower:
                return 18  # if arr[j] <= pivot
            elif 'placing pivot' in description_lower:
                return 23  # Place pivot in correct position
            elif 'partition complete' in description_lower:
                return 24  # return i + 1
            elif 'recursively sorting' in description_lower:
                if 'left' in description_lower or 'before' in description_lower:
                    return 6   # quick_sort(arr, low, pivot_index - 1)
                else:
                    return 9   # quick_sort(arr, pivot_index + 1, high)
            elif 'swap' in description_lower:
                return 20  # arr[i], arr[j] = arr[j], arr[i]
            else:
                return 2   # if low < high (main condition)
                
        elif algorithm_name == 'merge_sort':
            if 'dividing' in description_lower or 'divide' in description_lower:
                return 5   # mid = len(arr) // 2
            elif 'recursively sort' in description_lower:
                return 10  # left_sorted = merge_sort(left_half)
            elif 'merging' in description_lower or 'merge' in description_lower:
                return 14  # return merge(left_sorted, right_sorted)
            elif 'comparing' in description_lower:
                return 21  # if left[i] <= right[j]
            elif 'adding' in description_lower or 'append' in description_lower:
                return 22  # result.append(left[i])
            else:
                return 1   # def merge_sort
                
        elif algorithm_name == 'selection_sort':
            if 'traverse' in description_lower or 'starting' in description_lower:
                return 4   # for i in range(n)
            elif 'finding minimum' in description_lower or 'find minimum' in description_lower:
                return 6   # min_idx = i
            elif 'comparing' in description_lower or 'update minimum' in description_lower:
                return 9   # for j in range(i + 1, n)
            elif 'smaller element found' in description_lower:
                return 11  # if arr[j] < arr[min_idx]
            elif 'swap' in description_lower:
                return 14  # arr[i], arr[min_idx] = arr[min_idx], arr[i]
            else:
                return 1   # def selection_sort
                
        elif algorithm_name == 'priority_queue_sort':
            if 'create' in description_lower and 'heap' in description_lower:
                return 4   # heap = []
            elif 'add' in description_lower or 'push' in description_lower:
                return 8   # heapq.heappush(heap, element)
            elif 'extract' in description_lower or 'pop' in description_lower:
                return 13  # min_element = heapq.heappop(heap)
            else:
                return 1   # def priority_queue_sort
                
        elif algorithm_name == 'binary_search':
            if 'starting binary search' in description_lower:
                return 1   # def binary_search
            elif 'ensure' in description_lower and 'sorted' in description_lower:
                return 2   # arr = sorted(arr)
            elif 'checking middle element' in description_lower:
                return 6   # mid = (left + right) // 2
            elif 'found target' in description_lower:
                return 9   # if arr[mid] == target
            elif 'searching left' in description_lower:
                return 13  # elif arr[mid] > target
            elif 'searching right' in description_lower:
                return 17  # else left = mid + 1
            else:
                return 5   # while left <= right
                
        elif algorithm_name == 'bubble_sort':
            if 'starting bubble sort' in description_lower:
                return 1   # def bubble_sort
            elif 'pass' in description_lower and 'bubbling' in description_lower:
                return 4   # for i in range(n)
            elif 'comparing elements' in description_lower:
                return 10  # if arr[j] > arr[j + 1]
            elif 'swapped' in description_lower and 'bubble' in description_lower:
                return 12  # arr[j], arr[j + 1] = arr[j + 1], arr[j]
            elif 'no swap needed' in description_lower:
                return 8   # for j in range(0, n - i - 1)
            elif 'no swaps in pass' in description_lower:
                return 16  # if not swapped
            else:
                return 2   # n = len(arr)
                
        elif algorithm_name == 'breadth_first_search':
            if 'starting bfs' in description_lower:
                return 1   # def breadth_first_search
            elif 'initialize queue' in description_lower:
                return 5   # queue = deque([start])
            elif 'visiting node' in description_lower and 'adding to path' in description_lower:
                return 14  # path.append(current)
            elif 'target.*found' in description_lower:
                return 17  # if target and current == target
            elif 'adding neighbors' in description_lower:
                return 21  # for neighbor in graph.get(current, [])
            elif 'queue now contains' in description_lower:
                return 8   # while queue
            else:
                return 4   # visited = set()
        
        # Default fallback
        return 1
    
    def create_animated_code_visualization(self, 
                                         algorithm_name: str, 
                                         current_step: Dict[str, Any],
                                         array_data: List[int]) -> str:
        """Create synchronized code and data visualization."""
        
        code_lines = self.get_algorithm_source_code(algorithm_name)
        current_line = self.map_step_to_code_line(current_step.get('description', ''), algorithm_name)
        
        # Ensure current_line is within bounds
        current_line = max(1, min(current_line, len(code_lines)))
        
        style = self.code_style
        max_value = max(array_data) if array_data else 1
        
        # Generate syntax-highlighted code
        highlighted_code = ""
        for i, line in enumerate(code_lines, 1):
            is_active = (i == current_line)
            line_class = "active-line" if is_active else "code-line"
            
            # Simple syntax highlighting
            highlighted_line = self._apply_syntax_highlighting(line)
            
            highlighted_code += f'''
                <div class="{line_class}" data-line="{i}">
                    <span class="line-number">{i:2d}</span>
                    <span class="line-content">{highlighted_line}</span>
                </div>
            '''
        
        # Generate animated bars
        bars_html = ""
        comparison_indices = current_step.get('comparison_indices', [])
        swap_indices = current_step.get('swap_indices', [])
        highlight_indices = current_step.get('highlight_indices', [])
        
        for i, value in enumerate(array_data):
            height_percent = (value / max_value) * 100
            
            # Determine bar state
            bar_class = "bar"
            if i in comparison_indices:
                bar_class += " comparing"
            elif i in swap_indices:
                bar_class += " swapping"
            elif i in highlight_indices:
                bar_class += " highlight"
            
            bars_html += f'''
                <div class="{bar_class}" 
                     style="height: {height_percent}%;"
                     data-value="{value}"
                     data-index="{i}">
                    <span class="bar-value">{value}</span>
                </div>
            '''
        
        # Create complete HTML with CSS
        html = f'''
        <div class="code-animation-container">
            <style>
            .code-animation-container {{
                font-family: {style['font_family']};
                background: {style['background']};
                border-radius: {style['border_radius']};
                padding: {style['padding']};
                color: {style['text']};
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
                min-height: 500px;
            }}
            
            .code-section {{
                background: rgba(255, 255, 255, 0.02);
                border-radius: 6px;
                padding: 16px;
                overflow-y: auto;
                max-height: 450px;
                scroll-behavior: smooth;
                position: relative;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }}
            
            .code-section h3 {{
                margin: 0 0 12px 0;
                color: {style['keyword']};
                font-size: 16px;
                font-weight: 600;
            }}
            
            .code-line, .active-line {{
                display: flex;
                line-height: {style['line_height']};
                padding: 2px 0;
                margin: 1px 0;
                border-radius: 3px;
                transition: all 0.3s ease;
            }}
            
            .active-line {{
                background: {style['active_line']};
                animation: codeHighlight 1s ease-in-out infinite alternate;
                transform: translateX(4px);
                box-shadow: 2px 0 4px rgba(243, 156, 18, 0.3);
            }}
            
            .line-number {{
                color: #858585;
                margin-right: 12px;
                user-select: none;
                font-weight: 500;
            }}
            
            .line-content {{
                flex: 1;
            }}
            
            .keyword {{ color: {style['keyword']}; font-weight: 600; }}
            .string {{ color: {style['string']}; }}
            .comment {{ color: {style['comment']}; font-style: italic; }}
            .number {{ color: {style['number']}; }}
            
            .visualization-section {{
                display: flex;
                flex-direction: column;
                gap: 16px;
            }}
            
            .step-info {{
                background: rgba(255, 255, 255, 0.05);
                padding: 12px;
                border-radius: 6px;
                border-left: 3px solid {style['keyword']};
            }}
            
            .step-title {{
                font-size: 14px;
                font-weight: 600;
                margin-bottom: 4px;
                color: {style['keyword']};
            }}
            
            .step-description {{
                font-size: 13px;
                line-height: 1.4;
                color: {style['text']};
            }}
            
            .bars-container {{
                display: flex;
                align-items: flex-end;
                justify-content: center;
                height: 280px;
                gap: 6px;
                padding: 20px;
                background: rgba(0, 0, 0, 0.2);
                border-radius: 6px;
                position: relative;
            }}
            
            .bar {{
                background: linear-gradient(to top, #64B5F6, #42A5F5);
                border-radius: 3px 3px 0 0;
                min-width: 25px;
                position: relative;
                transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
                cursor: pointer;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            
            .bar:hover {{
                transform: translateY(-3px);
                box-shadow: 0 4px 8px rgba(100, 181, 246, 0.3);
            }}
            
            .bar.comparing {{
                background: linear-gradient(to top, #FFB74D, #FF9800);
                animation: pulse 1s ease-in-out infinite alternate;
                transform: scale(1.05);
            }}
            
            .bar.swapping {{
                background: linear-gradient(to top, #E57373, #F44336);
                animation: shake 0.5s ease-in-out;
                transform: scale(1.1);
            }}
            
            .bar.highlight {{
                background: linear-gradient(to top, #FFD54F, #FFC107);
                animation: glow 1s ease-in-out infinite alternate;
                transform: scale(1.02);
            }}
            
            .bar-value {{
                position: absolute;
                top: -25px;
                left: 50%;
                transform: translateX(-50%);
                font-size: 11px;
                font-weight: 600;
                color: {style['text']};
                opacity: 0;
                transition: opacity 0.3s ease;
            }}
            
            .bar:hover .bar-value {{
                opacity: 1;
            }}
            
            @keyframes codeHighlight {{
                0% {{ background: {style['active_line']}; }}
                100% {{ background: rgba(243, 156, 18, 0.15); }}
            }}
            
            @keyframes pulse {{
                0% {{ transform: scale(1.05); }}
                100% {{ transform: scale(1.08); }}
            }}
            
            @keyframes shake {{
                0%, 100% {{ transform: translateX(0) scale(1.1); }}
                25% {{ transform: translateX(-2px) scale(1.1); }}
                75% {{ transform: translateX(2px) scale(1.1); }}
            }}
            
            @keyframes glow {{
                0% {{ box-shadow: 0 0 5px rgba(255, 213, 79, 0.3); }}
                100% {{ box-shadow: 0 0 15px rgba(255, 213, 79, 0.6); }}
            }}
            
            /* Responsive design */
            @media (max-width: 768px) {{
                .code-animation-container {{
                    grid-template-columns: 1fr;
                    gap: 16px;
                }}
                
                .bars-container {{
                    height: 200px;
                }}
                
                .bar {{
                    min-width: 20px;
                }}
            }}
            </style>
            
            <div class="code-section">
                <h3>🖥️ Algorithm Code</h3>
                <div class="code-lines">
                    {highlighted_code}
                </div>
            </div>
            
            <div class="visualization-section">
                <div class="step-info">
                    <div class="step-title">Step {current_step.get('step_number', 1)}</div>
                    <div class="step-description">{current_step.get('description', 'Initializing algorithm...')}</div>
                </div>
                
                <div class="bars-container">
                    {bars_html}
                </div>
            </div>
        </div>
        
        <script>
        // Auto-scroll to highlighted line
        function scrollToActiveLine() {{
            const activeLine = document.querySelector('.active-line');
            const codeSection = document.querySelector('.code-section');
            
            if (activeLine && codeSection) {{
                const containerHeight = codeSection.clientHeight;
                const lineTop = activeLine.offsetTop;
                const lineHeight = activeLine.clientHeight;
                
                // Calculate scroll position to center the active line
                const scrollTop = lineTop - (containerHeight / 2) + (lineHeight / 2);
                
                codeSection.scrollTo({{
                    top: Math.max(0, scrollTop),
                    behavior: 'smooth'
                }});
            }}
        }}
        
        // Auto-scroll when page loads
        document.addEventListener('DOMContentLoaded', scrollToActiveLine);
        
        // Auto-scroll with a slight delay to ensure DOM is ready
        setTimeout(scrollToActiveLine, 100);
        </script>
        '''
        
        return html
    
    def _apply_syntax_highlighting(self, line: str) -> str:
        """Apply basic syntax highlighting to a line of code."""
        import html
        
        # Escape HTML first to prevent issues
        line = html.escape(line)
        
        # Comments (everything after #) - do this first as comments override everything else
        comment_match = re.search(r'(#.*)', line)
        if comment_match:
            comment_part = comment_match.group(1)
            before_comment = line[:comment_match.start()]
            highlighted_comment = f'<span class="comment">{comment_part}</span>'
            line = before_comment + highlighted_comment
        
        # Only process the part before the comment for other highlighting
        if comment_match:
            processable_part = line[:line.find('<span class="comment">')]
            comment_part = line[line.find('<span class="comment">'):]
        else:
            processable_part = line
            comment_part = ""
        
        # Strings
        processable_part = re.sub(r'(["\'][^"\']*["\'])', r'<span class="string">\1</span>', processable_part)
        
        # Keywords
        keywords = ['def', 'if', 'else', 'elif', 'for', 'while', 'return', 'in', 'and', 'or', 'not', 'range', 'len']
        for keyword in keywords:
            pattern = f'\\b{keyword}\\b'
            replacement = f'<span class="keyword">{keyword}</span>'
            processable_part = re.sub(pattern, replacement, processable_part)
        
        # Numbers
        processable_part = re.sub(r'\b(\d+)\b', r'<span class="number">\1</span>', processable_part)
        
        return processable_part + comment_part


class SynchronizedAnimationManager:
    """Manages synchronized code and visualization animations."""
    
    def __init__(self):
        self.code_animator = CodeBlockAnimator()
    
    def create_code_data_animation(self, visualizer, algorithm_name: str):
        """Create synchronized code and data animation."""
        steps = visualizer.get_steps()
        if not steps:
            st.warning("No steps recorded. Run the algorithm first.")
            return
        
        st.subheader("🎬 Code & Data Animation")
        
        # Enhanced controls for code animation
        controls = self._create_code_animation_controls(len(steps))
        
        # Get current step
        current_step_idx = controls['current_step']
        current_step = steps[current_step_idx] if current_step_idx < len(steps) else steps[-1]
        
        # Create step info
        step_info = {
            'step_number': current_step.step_number,
            'description': current_step.description,
            'comparison_indices': getattr(current_step, 'comparison_indices', []),
            'swap_indices': getattr(current_step, 'swapped_indices', []),
            'highlight_indices': getattr(current_step, 'highlighted_indices', []),
        }
        
        # Create synchronized visualization
        animation_html = self.code_animator.create_animated_code_visualization(
            algorithm_name, step_info, current_step.array_state
        )
        
        # Display the animation
        components.html(animation_html, height=600)
        
        # Progress indicator
        progress = min((current_step_idx + 1) / len(steps), 1.0)
        st.progress(progress, text=f"Step {current_step_idx + 1} of {len(steps)}")
        
        # Auto-advance logic
        if controls['is_playing'] and current_step_idx < len(steps) - 1:
            time.sleep(1.0 / controls['speed'])
            st.session_state.code_animation_state['current_step'] = current_step_idx + 1
            st.rerun()
        elif controls['is_playing'] and current_step_idx >= len(steps) - 1:
            st.session_state.code_animation_state['is_playing'] = False
            st.success("🎉 Animation completed!")
    
    def _create_code_animation_controls(self, total_steps: int) -> Dict[str, Any]:
        """Create controls specifically for code animation."""
        if 'code_animation_state' not in st.session_state:
            st.session_state.code_animation_state = {
                'is_playing': False,
                'current_step': 0,
                'speed': 1.0
            }
        
        # Add custom CSS for enhanced button styling
        st.markdown("""
        <style>
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 8px 16px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
            min-height: 44px;
            position: relative;
            overflow: hidden;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
            background: linear-gradient(135deg, #7c90ea 0%, #8b5ba2 100%);
        }
        
        .stButton > button:active {
            transform: translateY(0);
            box-shadow: 0 2px 4px rgba(102, 126, 234, 0.3);
        }
        
        .stButton > button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.5s;
        }
        
        .stButton > button:hover::before {
            left: 100%;
        }
        
        /* Special styling for play/pause button */
        div[data-testid="column"]:nth-child(2) .stButton > button {
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
            box-shadow: 0 2px 8px rgba(255, 107, 107, 0.3);
        }
        
        div[data-testid="column"]:nth-child(2) .stButton > button:hover {
            background: linear-gradient(135deg, #ff7979 0%, #fd7f32 100%);
            box-shadow: 0 4px 12px rgba(255, 107, 107, 0.4);
        }
        
        /* Control section styling */
        .control-section {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 20px;
            margin: 16px 0;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .control-title {
            color: #667eea;
            font-size: 16px;
            font-weight: 700;
            margin-bottom: 12px;
            text-align: center;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Create control sections with improved layout
        st.markdown('<div class="control-section">', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([2, 2, 2])
        
        with col1:
            st.markdown('<div class="control-title">🎮 Playback Controls</div>', unsafe_allow_html=True)
            play_col1, play_col2, play_col3 = st.columns(3)
            
            with play_col1:
                if st.button("⏮️ First", key="code_first", help="Go to first step"):
                    st.session_state.code_animation_state['current_step'] = 0
                    st.session_state.code_animation_state['is_playing'] = False
            
            with play_col2:
                play_icon = "⏸️ Pause" if st.session_state.code_animation_state['is_playing'] else "▶️ Play"
                if st.button(play_icon, key="code_play", help="Play/Pause animation"):
                    st.session_state.code_animation_state['is_playing'] = not st.session_state.code_animation_state['is_playing']
            
            with play_col3:
                if st.button("⏭️ Next", key="code_step", help="Next step"):
                    if st.session_state.code_animation_state['current_step'] < total_steps - 1:
                        st.session_state.code_animation_state['current_step'] += 1
                    st.session_state.code_animation_state['is_playing'] = False
        
        with col2:
            st.markdown('<div class="control-title">⚡ Speed Control</div>', unsafe_allow_html=True)
            speed = st.slider("Animation Speed", 0.1, 3.0, 1.0, 0.1, key="code_speed", 
                            help="Adjust animation speed (higher = faster)")
            st.session_state.code_animation_state['speed'] = speed
            
            # Speed indicators
            if speed <= 0.5:
                st.markdown("🐌 **Slow**", unsafe_allow_html=True)
            elif speed <= 1.5:
                st.markdown("🚶 **Normal**", unsafe_allow_html=True)
            else:
                st.markdown("🏃 **Fast**", unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="control-title">🎯 Navigation</div>', unsafe_allow_html=True)
            if total_steps > 0:
                new_step = st.slider(
                    "Jump to Step", 0, total_steps - 1, 
                    st.session_state.code_animation_state['current_step'],
                    key="code_step_slider",
                    help=f"Jump directly to any step (1-{total_steps})"
                )
                st.session_state.code_animation_state['current_step'] = new_step
                
                # Show current step info
                st.markdown(f"**Step {new_step + 1}** of **{total_steps}**", unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        return st.session_state.code_animation_state


# Public interface functions
def create_code_animation(visualizer, algorithm_name: str):
    """Create an animated code and data visualization."""
    manager = SynchronizedAnimationManager()
    manager.create_code_data_animation(visualizer, algorithm_name)