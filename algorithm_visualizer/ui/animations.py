"""
Modern Animation System for Algorithm Visualization

This module provides smooth, educational animations for sorting algorithms
using CSS animations and modern web technologies within Streamlit.
"""

import streamlit as st
import streamlit.components.v1 as components
import time
from typing import List, Dict, Any, Optional
import json

class AlgorithmAnimator:
    """Modern animation system for algorithm visualization."""
    
    def __init__(self):
        self.animation_config = {
            'duration': 0.6,  # Reduced for smoother feel
            'easing': 'cubic-bezier(0.25, 0.46, 0.45, 0.94)',  # Improved easing for smoother motion
            'transition_delay': 0.05,  # Stagger animations for better visual flow
            'colors': {
                'default': '#64B5F6',      # Light blue
                'comparing': '#FFB74D',     # Orange
                'swapping': '#E57373',      # Red
                'sorted': '#81C784',        # Green
                'pivot': '#BA68C8',         # Purple
                'highlight': '#FFD54F',     # Yellow
                'background': '#1E1E1E',    # Dark background
                'text': '#FFFFFF'           # White text
            },
            'shadows': {
                'default': '0 2px 4px rgba(0,0,0,0.1)',
                'active': '0 4px 12px rgba(100, 181, 246, 0.3)',
                'glow': '0 0 20px rgba(255, 183, 77, 0.5)'
            },
            'performance': {
                'gpu_acceleration': True,
                'will_change': 'transform, height, background-color',
                'backface_visibility': 'hidden'
            }
        }
    
    def create_animated_bars(self, data: List[int], step_info: Dict[str, Any]) -> str:
        """Create animated bar chart HTML with CSS animations."""
        max_value = max(data) if data else 1
        
        # Generate CSS for animations
        css = self._generate_animation_css()
        
        # Generate HTML for bars
        html = f"""
        <div class="algorithm-container">
            <style>{css}</style>
            <div class="bars-container">
        """
        
        for i, value in enumerate(data):
            height_percent = (value / max_value) * 100
            bar_class = self._get_bar_class(i, step_info)
            
            html += f"""
                <div class="bar {bar_class}" 
                     style="height: {height_percent}%; --value: {value}; --index: {i};"
                     data-index="{i}"
                     data-value="{value}">
                    <div class="bar-value">{value}</div>
                </div>
            """
        
        html += """
            </div>
        </div>
        """
        
        return html
    
    def _generate_animation_css(self) -> str:
        """Generate CSS for smooth animations."""
        colors = self.animation_config['colors']
        shadows = self.animation_config['shadows']
        duration = self.animation_config['duration']
        easing = self.animation_config['easing']
        
        return f"""
        .algorithm-container {{
            padding: 20px;
            background: linear-gradient(135deg, {colors['background']} 0%, #2D2D2D 100%);
            border-radius: 12px;
            box-shadow: {shadows['default']};
            font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
        }}
        
        .bars-container {{
            display: flex;
            align-items: flex-end;
            justify-content: center;
            height: 300px;
            gap: 4px;
            padding: 20px 0;
            position: relative;
        }}
        
        .bar {{
            background: linear-gradient(to top, {colors['default']}, #42A5F5);
            border-radius: 4px 4px 0 0;
            min-width: 30px;
            position: relative;
            transition: all {duration}s {easing};
            cursor: pointer;
            box-shadow: {shadows['default']};
            will-change: {self.animation_config['performance']['will_change']};
            backface-visibility: {self.animation_config['performance']['backface_visibility']};
            transform: translateZ(0); /* Force GPU acceleration */
        }}
        
        .bar:nth-child(n) {{
            animation-delay: calc(var(--index, 0) * {self.animation_config['transition_delay']}s);
        }}
        
        .bar:hover {{
            transform: translateY(-2px) translateZ(0);
            box-shadow: {shadows['active']};
            transition: all 0.2s {easing};
        }}
        
        .bar-value {{
            position: absolute;
            top: -25px;
            left: 50%;
            transform: translateX(-50%);
            color: {colors['text']};
            font-weight: 600;
            font-size: 12px;
            opacity: 0;
            transition: opacity 0.3s ease;
        }}
        
        .bar:hover .bar-value {{
            opacity: 1;
        }}
        
        /* Animation states with improved performance */
        .bar.comparing {{
            background: linear-gradient(to top, {colors['comparing']}, #FFB74D);
            animation: smoothPulse 1.2s ease-in-out infinite alternate;
            box-shadow: {shadows['glow']};
            transform: translateZ(0) scale(1.02);
        }}
        
        .bar.swapping {{
            background: linear-gradient(to top, {colors['swapping']}, #E57373);
            animation: smoothSwap 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            box-shadow: 0 0 20px rgba(229, 115, 115, 0.5);
            transform: translateZ(0);
        }}
        
        .bar.sorted {{
            background: linear-gradient(to top, {colors['sorted']}, #81C784);
            animation: sortedSuccess 1s ease-out forwards;
            transform: translateZ(0);
        }}
        
        .bar.pivot {{
            background: linear-gradient(to top, {colors['pivot']}, #BA68C8);
            animation: pivotHighlight 1s ease-in-out infinite alternate;
            box-shadow: 0 0 15px rgba(186, 104, 200, 0.4);
            transform: translateZ(0) scale(1.05);
        }}
        
        .bar.highlight {{
            background: linear-gradient(to top, {colors['highlight']}, #FFD54F);
            animation: smoothHighlight 0.8s ease-in-out infinite alternate;
            transform: translateZ(0);
        }}
        
        /* Enhanced keyframe animations for smooth motion */
        @keyframes smoothPulse {{
            0% {{ 
                transform: translateZ(0) scale(1);
                filter: brightness(1);
            }}
            100% {{ 
                transform: translateZ(0) scale(1.02);
                filter: brightness(1.1);
            }}
        }}
        
        @keyframes smoothSwap {{
            0% {{ 
                transform: translateZ(0) translateX(0) rotate(0deg);
            }}
            25% {{ 
                transform: translateZ(0) translateX(-5px) rotate(-2deg);
            }}
            50% {{ 
                transform: translateZ(0) translateX(0) rotate(0deg) scale(1.05);
            }}
            75% {{ 
                transform: translateZ(0) translateX(5px) rotate(2deg);
            }}
            100% {{ 
                transform: translateZ(0) translateX(0) rotate(0deg);
            }}
        }}
        
        @keyframes sortedSuccess {{
            0% {{ 
                transform: translateZ(0) scale(1);
                box-shadow: {shadows['default']};
            }}
            50% {{ 
                transform: translateZ(0) scale(1.08);
                box-shadow: 0 0 25px rgba(129, 199, 132, 0.8);
            }}
            100% {{ 
                transform: translateZ(0) scale(1);
                box-shadow: 0 0 15px rgba(129, 199, 132, 0.4);
            }}
        }}
        
        @keyframes pivotHighlight {{
            0% {{ 
                transform: translateZ(0) scale(1.05);
                filter: brightness(1);
            }}
            100% {{ 
                transform: translateZ(0) scale(1.08);
                filter: brightness(1.15);
            }}
        }}
        
        @keyframes smoothHighlight {{
            0% {{ 
                opacity: 0.9;
                transform: translateZ(0) scale(1);
            }}
            100% {{ 
                opacity: 1;
                transform: translateZ(0) scale(1.02);
            }}
        }}
        
        /* Height transition animations */
        @keyframes heightChange {{
            from {{ 
                height: var(--old-height, 50%);
                transform: translateZ(0) scaleY(0.95);
            }}
            to {{ 
                height: var(--new-height, 50%);
                transform: translateZ(0) scaleY(1);
            }}
        }}
        
        /* Performance optimizations */
        .bar.animating {{
            animation-fill-mode: both;
            animation-timing-function: cubic-bezier(0.25, 0.46, 0.45, 0.94);
        }}
        
        /* Modern responsive design */
        @media (max-width: 768px) {{
            .bar {{
                min-width: 20px;
            }}
            
            .bars-container {{
                height: 200px;
                gap: 2px;
            }}
        }}
        """
    
    def _get_bar_class(self, index: int, step_info: Dict[str, Any]) -> str:
        """Determine the CSS class for a bar based on step information."""
        if not step_info:
            return ""
        
        classes = []
        
        # Check if this index is involved in current operation
        if 'comparison_indices' in step_info and index in step_info['comparison_indices']:
            classes.append('comparing')
        
        if 'swap_indices' in step_info and index in step_info['swap_indices']:
            classes.append('swapping')
        
        if 'pivot_index' in step_info and index == step_info['pivot_index']:
            classes.append('pivot')
        
        if 'highlight_indices' in step_info and index in step_info['highlight_indices']:
            classes.append('highlight')
        
        if 'sorted_indices' in step_info and index in step_info['sorted_indices']:
            classes.append('sorted')
        
        return ' '.join(classes)
    
    def create_enhanced_step_controls(self, total_steps: int = 0) -> Dict[str, Any]:
        """Create enhanced interactive controls for smooth animation playback."""
        st.subheader("🎬 Enhanced Animation Controls")
        
        # Initialize animation state
        if 'animation_state' not in st.session_state:
            st.session_state.animation_state = {
                'is_playing': False,
                'current_step': 0,
                'total_steps': total_steps,
                'speed': 1.0,
                'auto_play': False,
                'smooth_transitions': True,
                'last_update_time': time.time()
            }
        
        # Update total_steps if provided
        if total_steps > 0:
            st.session_state.animation_state['total_steps'] = total_steps
        
        # Ensure current_step is within bounds
        max_step = max(0, st.session_state.animation_state.get('total_steps', 1) - 1)
        current_step = st.session_state.animation_state.get('current_step', 0)
        if current_step > max_step:
            st.session_state.animation_state['current_step'] = max_step
            current_step = max_step
        
        # Create control layout
        control_col1, control_col2, control_col3 = st.columns([2, 2, 3])
        
        # Track button clicks to prevent double updates
        button_clicked = False
        
        with control_col1:
            st.markdown("**Playback Controls**")
            col1a, col1b, col1c = st.columns(3)
            
            with col1a:
                if st.button("⏮️", key="anim_first", help="First step"):
                    st.session_state.animation_state['current_step'] = 0
                    st.session_state.animation_state['is_playing'] = False
                    button_clicked = True
            
            with col1b:
                play_icon = "⏸️" if st.session_state.animation_state['is_playing'] else "▶️"
                play_text = "Pause" if st.session_state.animation_state['is_playing'] else "Play"
                if st.button(f"{play_icon}", key="anim_play_pause", help=play_text):
                    st.session_state.animation_state['is_playing'] = not st.session_state.animation_state['is_playing']
                    st.session_state.animation_state['last_update_time'] = time.time()
                    button_clicked = True
            
            with col1c:
                if st.button("⏭️", key="anim_step", help="Next step"):
                    if current_step < total_steps - 1:
                        st.session_state.animation_state['current_step'] = current_step + 1
                    st.session_state.animation_state['is_playing'] = False
                    button_clicked = True
        
        with control_col2:
            st.markdown("**Settings**")
            
            # Speed control with better options
            speed_options = {
                "0.25x": 0.25,
                "0.5x": 0.5,
                "1x": 1.0,
                "1.5x": 1.5,
                "2x": 2.0,
                "3x": 3.0
            }
            
            selected_speed = st.selectbox(
                "Speed",
                options=list(speed_options.keys()),
                index=2,  # Default to 1x
                key="anim_speed_select"
            )
            st.session_state.animation_state['speed'] = speed_options[selected_speed]
            
            # Smooth transitions toggle
            st.session_state.animation_state['smooth_transitions'] = st.checkbox(
                "Smooth transitions", 
                value=True, 
                key="smooth_transitions"
            )
        
        with control_col3:
            st.markdown("**Progress**")
            
            # Step progress slider - only update if not button clicked
            if total_steps > 0 and not button_clicked:
                new_step = st.slider(
                    "Step",
                    min_value=0,
                    max_value=total_steps - 1,
                    value=current_step,
                    key="step_slider",
                    help="Drag to navigate to specific step"
                )
                
                # Only update if slider actually changed (not during rerun)
                if new_step != current_step:
                    st.session_state.animation_state['current_step'] = new_step
                    st.session_state.animation_state['is_playing'] = False
                
                # Progress indicator
                progress = (st.session_state.animation_state['current_step'] + 1) / total_steps
                st.progress(progress)
                st.caption(f"Step {st.session_state.animation_state['current_step'] + 1} of {total_steps}")
            else:
                st.info("No animation steps available")
                st.session_state.animation_state['current_step'] = 0
        
        return {
            'current_step': st.session_state.animation_state.get('current_step', 0),
            'is_playing': st.session_state.animation_state.get('is_playing', False),
            'speed': st.session_state.animation_state.get('speed', 1.0),
            'smooth_transitions': st.session_state.animation_state.get('smooth_transitions', True),
            'total_steps': st.session_state.animation_state.get('total_steps', 0)
        }
    
    def create_algorithm_info_panel(self, algorithm_name: str, step_info: Dict[str, Any]) -> str:
        """Create an information panel showing current algorithm step."""
        colors = self.animation_config['colors']
        
        current_step = step_info.get('step_number', 0)
        description = step_info.get('description', 'Algorithm initialization')
        
        html = f"""
        <div class="info-panel">
            <style>
            .info-panel {{
                background: linear-gradient(135deg, {colors['background']} 0%, #2D2D2D 100%);
                border-radius: 12px;
                padding: 20px;
                margin: 10px 0;
                border-left: 4px solid {colors['default']};
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }}
            
            .step-title {{
                color: {colors['default']};
                font-size: 18px;
                font-weight: 600;
                margin-bottom: 10px;
            }}
            
            .step-description {{
                color: {colors['text']};
                font-size: 14px;
                line-height: 1.5;
            }}
            
            .step-counter {{
                color: {colors['highlight']};
                font-size: 12px;
                font-weight: 500;
                text-transform: uppercase;
                letter-spacing: 1px;
            }}
            </style>
            
            <div class="step-counter">Step {current_step}</div>
            <div class="step-title">{algorithm_name}</div>
            <div class="step-description">{description}</div>
        </div>
        """
        
        return html
    
    def create_smooth_animation_container(self, data: List[int], step_info: Dict[str, Any], algorithm_name: str) -> str:
        """Create a smooth animation container that updates without page refresh."""
        max_value = max(data) if data else 1
        
        # Generate unique container ID for this animation
        container_id = f"algorithm-container-{hash(str(data))}"
        
        # Enhanced CSS for smoother animations
        css = self._generate_animation_css()
        
        # JavaScript for smooth updates without page refresh
        javascript = f"""
        <script>
        function updateBars_{container_id.replace('-', '_')}(newData, stepInfo) {{
            const container = document.getElementById('{container_id}');
            if (!container) return;
            
            const bars = container.querySelectorAll('.bar');
            const stepNumber = stepInfo.step_number || 0;
            const description = stepInfo.description || '';
            
            // Update step info
            const stepCounter = container.querySelector('.step-counter');
            const stepDesc = container.querySelector('.step-description');
            if (stepCounter) stepCounter.textContent = `Step ${{stepNumber}}`;
            if (stepDesc) stepDesc.textContent = description;
            
            // Update bars with smooth transitions
            bars.forEach((bar, index) => {{
                if (index < newData.length) {{
                    const value = newData[index];
                    const heightPercent = (value / Math.max(...newData)) * 100;
                    
                    // Remove all existing classes
                    bar.className = 'bar';
                    
                    // Add appropriate classes based on step info
                    if (stepInfo.comparison_indices && stepInfo.comparison_indices.includes(index)) {{
                        bar.classList.add('comparing');
                    }}
                    if (stepInfo.swap_indices && stepInfo.swap_indices.includes(index)) {{
                        bar.classList.add('swapping');
                    }}
                    if (stepInfo.pivot_index === index) {{
                        bar.classList.add('pivot');
                    }}
                    if (stepInfo.highlight_indices && stepInfo.highlight_indices.includes(index)) {{
                        bar.classList.add('highlight');
                    }}
                    
                    // Smooth height transition
                    bar.style.height = heightPercent + '%';
                    bar.querySelector('.bar-value').textContent = value;
                }}
            }});
        }}
        
        // Make function globally available
        window.updateBars_{container_id.replace('-', '_')} = updateBars_{container_id.replace('-', '_')};
        </script>
        """
        
        # Generate HTML with smooth transition support
        html = f"""
        <div class="algorithm-container" id="{container_id}">
            <style>{css}</style>
            {javascript}
            <div class="info-section">
                <div class="step-counter">Step {step_info.get('step_number', 1)}</div>
                <div class="step-title">{algorithm_name}</div>
                <div class="step-description">{step_info.get('description', 'Algorithm step')}</div>
            </div>
            <div class="animation-section">
                <div class="bars-container">
        """
        
        for i, value in enumerate(data):
            height_percent = (value / max_value) * 100
            bar_class = self._get_bar_class(i, step_info)
            
            html += f"""
                <div class="bar {bar_class}" 
                     style="height: {height_percent}%; --value: {value}; --index: {i};"
                     data-index="{i}"
                     data-value="{value}">
                    <div class="bar-value">{value}</div>
                </div>
            """
        
        html += """
                </div>
            </div>
        </div>
        """
        
        return html
        """Create a combined block with step info and animated bars for smoother rendering."""
        colors = self.animation_config['colors']
        shadows = self.animation_config['shadows']
        duration = self.animation_config['duration']
        easing = self.animation_config['easing']
        
        current_step = step_info.get('step_number', 0)
        description = step_info.get('description', 'Algorithm initialization')
        max_value = max(data) if data else 1
        
        html = f"""
        <div class="combined-animation-container">
            <style>
            .combined-animation-container {{
                background: linear-gradient(135deg, {colors['background']} 0%, #2D2D2D 100%);
                border-radius: 16px;
                padding: 24px;
                box-shadow: {shadows['default']};
                font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
                overflow: hidden;
                position: relative;
            }}
            
            .step-info-section {{
                margin-bottom: 20px;
                padding: 16px;
                background: rgba(255, 255, 255, 0.05);
                border-radius: 12px;
                border-left: 4px solid {colors['default']};
            }}
            
            .step-counter {{
                color: {colors['highlight']};
                font-size: 14px;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 1px;
                margin-bottom: 8px;
            }}
            
            .step-title {{
                color: {colors['default']};
                font-size: 20px;
                font-weight: 700;
                margin-bottom: 8px;
            }}
            
            .step-description {{
                color: {colors['text']};
                font-size: 16px;
                line-height: 1.5;
                opacity: 0.9;
            }}
            
            .animation-section {{
                position: relative;
                background: rgba(0, 0, 0, 0.2);
                border-radius: 12px;
                padding: 20px;
            }}
            
            .bars-container {{
                display: flex;
                align-items: flex-end;
                justify-content: center;
                height: 300px;
                gap: 4px;
                padding: 20px 0;
                position: relative;
            }}
            
            .bar {{
                background: linear-gradient(to top, {colors['default']}, #42A5F5);
                border-radius: 4px 4px 0 0;
                min-width: 30px;
                position: relative;
                transition: all {duration}s {easing};
                cursor: pointer;
                box-shadow: {shadows['default']};
                will-change: transform, background, box-shadow;
            }}
            
            .bar:hover {{
                transform: translateY(-2px);
                box-shadow: {shadows['active']};
            }}
            
            .bar-value {{
                position: absolute;
                top: -25px;
                left: 50%;
                transform: translateX(-50%);
                color: {colors['text']};
                font-weight: 600;
                font-size: 12px;
                opacity: 0;
                transition: opacity 0.3s ease;
            }}
            
            .bar:hover .bar-value {{
                opacity: 1;
            }}
            
            /* Enhanced animation states for smoothness */
            .bar.comparing {{
                background: linear-gradient(to top, {colors['comparing']}, #FFB74D);
                animation: smoothPulse 1.2s ease-in-out infinite alternate;
                box-shadow: {shadows['glow']};
                transform: scale(1.02);
            }}
            
            .bar.swapping {{
                background: linear-gradient(to top, {colors['swapping']}, #E57373);
                animation: smoothShake 0.6s ease-in-out;
                box-shadow: 0 0 20px rgba(229, 115, 115, 0.5);
            }}
            
            .bar.sorted {{
                background: linear-gradient(to top, {colors['sorted']}, #81C784);
                animation: smoothSortedGlow 2s ease-in-out;
                transform: scale(1.01);
            }}
            
            .bar.pivot {{
                background: linear-gradient(to top, {colors['pivot']}, #BA68C8);
                animation: smoothPivotGlow 1.8s ease-in-out infinite alternate;
                box-shadow: 0 0 15px rgba(186, 104, 200, 0.4);
            }}
            
            .bar.highlight {{
                background: linear-gradient(to top, {colors['highlight']}, #FFD54F);
                animation: smoothHighlightPulse 1s ease-in-out infinite alternate;
                transform: scale(1.03);
            }}
            
            /* Smoother keyframe animations */
            @keyframes smoothPulse {{
                0% {{ transform: scale(1.02); }}
                100% {{ transform: scale(1.06); }}
            }}
            
            @keyframes smoothShake {{
                0%, 100% {{ transform: translateX(0) scale(1); }}
                25% {{ transform: translateX(-2px) scale(1.02); }}
                75% {{ transform: translateX(2px) scale(1.02); }}
            }}
            
            @keyframes smoothSortedGlow {{
                0% {{ box-shadow: {shadows['default']}; transform: scale(1.01); }}
                50% {{ box-shadow: 0 0 20px rgba(129, 199, 132, 0.6); transform: scale(1.03); }}
                100% {{ box-shadow: {shadows['default']}; transform: scale(1.01); }}
            }}
            
            @keyframes smoothPivotGlow {{
                0% {{ transform: scale(1); }}
                100% {{ transform: scale(1.05); }}
            }}
            
            @keyframes smoothHighlightPulse {{
                0% {{ opacity: 0.8; transform: scale(1.03); }}
                100% {{ opacity: 1; transform: scale(1.05); }}
            }}
            
            /* Responsive design */
            @media (max-width: 768px) {{
                .bar {{
                    min-width: 20px;
                }}
                
                .bars-container {{
                    height: 200px;
                    gap: 2px;
                }}
                
                .step-info-section {{
                    padding: 12px;
                }}
            }}
            </style>
            
            <!-- Step Information Section -->
            <div class="step-info-section">
                <div class="step-counter">Step {current_step}</div>
                <div class="step-title">{algorithm_name}</div>
                <div class="step-description">{description}</div>
            </div>
            
            <!-- Animation Section -->
            <div class="animation-section">
                <div class="bars-container">
        """
        
        for i, value in enumerate(data):
            height_percent = (value / max_value) * 100
            bar_class = self._get_bar_class(i, step_info)
            
            html += f"""
                    <div class="bar {bar_class}" 
                         style="height: {height_percent}%; --value: {value};"
                         data-index="{i}">
                        <div class="bar-value">{value}</div>
                    </div>
            """
        
        html += """
                </div>
            </div>
        </div>
        """
        
        return html

class StreamlitAnimationManager:
    """Manages animations within Streamlit interface."""
    
    def __init__(self):
        self.animator = AlgorithmAnimator()
        self._initialize_session_state()
    
    def _initialize_session_state(self):
        """Initialize session state for animation control."""
        if 'animation_state' not in st.session_state:
            st.session_state.animation_state = {
                'current_step': 0,
                'is_playing': False,
                'steps': [],
                'speed': 1.0
            }
    
    def animate_algorithm_steps(self, visualizer, algorithm_name: str):
        """Create animated visualization of algorithm steps."""
        steps = visualizer.get_steps()
        if not steps:
            st.warning("No steps recorded. Run the algorithm first.")
            return
        
        # Animation controls with total steps
        controls = self.animator.create_enhanced_step_controls(total_steps=len(steps))
        
        # Get current step
        current_step_idx = controls['current_step']
        current_step = steps[current_step_idx] if current_step_idx < len(steps) else steps[-1]
        
        # Create step info for visualization
        step_info = {
            'step_number': current_step.step_number,
            'description': current_step.description,
            'comparison_indices': getattr(current_step, 'comparison_indices', []),
            'swap_indices': getattr(current_step, 'swapped_indices', []),
            'pivot_index': getattr(current_step, 'pivot_index', None),
            'highlight_indices': getattr(current_step, 'highlighted_indices', []),
        }
        
        # Create animation container with smooth transitions
        animation_container = st.container()
        with animation_container:
            combined_html = self.animator.create_smooth_animation_container(
                current_step.array_state, 
                step_info, 
                algorithm_name
            )
            components.html(combined_html, height=520)
        
        # Step progress indicator
        progress = min((current_step_idx + 1) / len(steps), 1.0)
        st.progress(progress, text=f"Step {current_step_idx + 1} of {len(steps)}")
        
        # Handle auto-advance for playing state with better timing
        if controls['is_playing'] and current_step_idx < len(steps) - 1:
            # Use a placeholder to show countdown without blocking
            countdown_placeholder = st.empty()
            delay_seconds = 1.0 / controls['speed']
            
            # Show countdown
            for i in range(int(delay_seconds * 10), 0, -1):
                with countdown_placeholder.container():
                    st.info(f"⏩ Next step in {i/10:.1f}s (Speed: {controls['speed']}x)")
                time.sleep(0.1)
            
            countdown_placeholder.empty()
            
            # Advance to next step
            st.session_state.animation_state['current_step'] = current_step_idx + 1
            st.rerun()
            
        elif controls['is_playing'] and current_step_idx >= len(steps) - 1:
            # End of animation
            st.session_state.animation_state['is_playing'] = False
            st.success("🎉 Animation completed!")

    def _handle_auto_advance(self, current_step_idx: int, steps: List):
        """Handle auto-advance logic with smooth timing control."""
        # This method is now replaced by the logic in animate_algorithm_steps
        pass
    
    def _update_animation_state(self, controls: Dict[str, Any], steps: List):
        """Update animation state based on user controls."""
        state = st.session_state.animation_state
        
        # Update speed
        state['speed'] = controls['speed']
        
        # Handle play/pause
        if controls['play_pause']:
            state['is_playing'] = not state['is_playing']
            # Reset timer when play state changes
            if 'last_auto_advance' in st.session_state:
                del st.session_state.last_auto_advance
        
        # Handle step forward
        if controls['step_forward']:
            state['is_playing'] = False
            if state['current_step'] < len(steps) - 1:
                state['current_step'] += 1
        
        # Handle reset
        if controls['reset']:
            state['current_step'] = 0
            state['is_playing'] = False
            # Clean up any timer states
            if 'last_auto_advance' in st.session_state:
                del st.session_state.last_auto_advance
            if 'animation_timer' in st.session_state:
                del st.session_state.animation_timer
            if 'next_advance_time' in st.session_state:
                del st.session_state.next_advance_time
        
        # Store steps for reference
        state['steps'] = steps

    def create_side_by_side_animation(self, visualizers: Dict[str, Any], current_steps: Dict[str, int]):
        """Create side-by-side comparison animation for multiple algorithms."""
        st.subheader("🎭 Algorithm Comparison Animation")
        
        # Create columns for each algorithm
        cols = st.columns(len(visualizers))
        
        for i, (algorithm_name, visualizer) in enumerate(visualizers.items()):
            with cols[i]:
                st.write(f"**{algorithm_name}**")
                
                steps = visualizer.get_steps()
                if not steps:
                    st.warning(f"No steps for {algorithm_name}")
                    continue
                
                current_step_idx = current_steps.get(algorithm_name, 0)
                current_step = steps[min(current_step_idx, len(steps) - 1)]
                
                # Create step info
                step_info = {
                    'step_number': current_step.step_number,
                    'description': current_step.description[:50] + "...",  # Truncate for space
                    'comparison_indices': getattr(current_step, 'comparison_indices', []),
                    'swap_indices': getattr(current_step, 'swapped_indices', []),
                    'pivot_index': getattr(current_step, 'pivot_index', None),
                    'highlight_indices': getattr(current_step, 'highlighted_indices', []),
                }
                
                # Create compact bars for comparison
                bars_html = self._create_compact_bars(current_step.array_state, step_info, algorithm_name)
                components.html(bars_html, height=180)
                
                # Progress indicator
                progress = min(current_step_idx / len(steps), 1.0)
                st.progress(progress, text=f"{current_step_idx + 1}/{len(steps)}")
    
    def _create_compact_bars(self, data: List[int], step_info: Dict[str, Any], algorithm_name: str) -> str:
        """Create compact bar chart for side-by-side comparison."""
        max_value = max(data) if data else 1
        colors = self.animator.animation_config['colors']
        
        html = f"""
        <div class="compact-algorithm-container" data-algorithm="{algorithm_name}">
            <style>
            .compact-algorithm-container {{
                padding: 10px;
                background: linear-gradient(135deg, {colors['background']} 0%, #2D2D2D 100%);
                border-radius: 8px;
                margin: 5px 0;
                min-height: 150px;
            }}
            
            .compact-bars-container {{
                display: flex;
                align-items: flex-end;
                justify-content: center;
                height: 120px;
                gap: 2px;
                padding: 10px 0;
            }}
            
            .compact-bar {{
                background: linear-gradient(to top, {colors['default']}, #42A5F5);
                border-radius: 2px 2px 0 0;
                min-width: 8px;
                position: relative;
                transition: all 0.6s cubic-bezier(0.4, 0.0, 0.2, 1);
            }}
            
            .compact-bar.comparing {{
                background: linear-gradient(to top, {colors['comparing']}, #FFB74D);
                animation: compactPulse 0.8s ease-in-out infinite alternate;
            }}
            
            .compact-bar.swapping {{
                background: linear-gradient(to top, {colors['swapping']}, #E57373);
                animation: compactShake 0.4s ease-in-out;
            }}
            
            .compact-bar.sorted {{
                background: linear-gradient(to top, {colors['sorted']}, #81C784);
            }}
            
            .compact-bar.pivot {{
                background: linear-gradient(to top, {colors['pivot']}, #BA68C8);
                animation: compactGlow 1s ease-in-out infinite alternate;
            }}
            
            @keyframes compactPulse {{
                0% {{ transform: scale(1); }}
                100% {{ transform: scale(1.1); }}
            }}
            
            @keyframes compactShake {{
                0%, 100% {{ transform: translateX(0); }}
                25% {{ transform: translateX(-2px); }}
                75% {{ transform: translateX(2px); }}
            }}
            
            @keyframes compactGlow {{
                0% {{ transform: scale(1); }}
                100% {{ transform: scale(1.05); }}
            }}
            </style>
            
            <div class="compact-bars-container">
        """
        
        for i, value in enumerate(data):
            height_percent = (value / max_value) * 100
            bar_class = self.animator._get_bar_class(i, step_info)
            
            html += f"""
                <div class="compact-bar {bar_class}" 
                     style="height: {height_percent}%;"
                     title="{value}">
                </div>
            """
        
        html += """
            </div>
        </div>
        """
        
        return html

def create_modern_visualization(visualizer, algorithm_name: str):
    """Create a modern, animated visualization of the algorithm."""
    manager = StreamlitAnimationManager()
    manager.animate_algorithm_steps(visualizer, algorithm_name)

def create_comparison_animation(visualizers: Dict[str, Any]):
    """Create animated comparison of multiple algorithms."""
    manager = StreamlitAnimationManager()
    
    # Initialize step counters for each algorithm
    if 'comparison_steps' not in st.session_state:
        st.session_state.comparison_steps = {name: 0 for name in visualizers.keys()}
    
    # Get maximum steps from all visualizers
    max_steps = 0
    for visualizer in visualizers.values():
        steps = visualizer.get_steps() if hasattr(visualizer, 'get_steps') else []
        max_steps = max(max_steps, len(steps))
    
    # Create controls with maximum steps
    controls = manager.animator.create_enhanced_step_controls(total_steps=max_steps)
    
    # Update steps based on controls
    if controls['play_pause']:
        st.session_state.comparison_playing = not st.session_state.get('comparison_playing', False)
    
    if controls['step_forward']:
        for name in st.session_state.comparison_steps:
            steps = visualizers[name].get_steps()
            if st.session_state.comparison_steps[name] < len(steps) - 1:
                st.session_state.comparison_steps[name] += 1
    
    if controls['reset']:
        st.session_state.comparison_steps = {name: 0 for name in visualizers.keys()}
        st.session_state.comparison_playing = False
    
    # Create side-by-side animation
    manager.create_side_by_side_animation(visualizers, st.session_state.comparison_steps)
    
    # Auto-advance if playing
    if st.session_state.get('comparison_playing', False):
        time.sleep(1.0 / controls['speed'])
        any_can_advance = False
        for name in st.session_state.comparison_steps:
            steps = visualizers[name].get_steps()
            if st.session_state.comparison_steps[name] < len(steps) - 1:
                st.session_state.comparison_steps[name] += 1
                any_can_advance = True
        
        if any_can_advance:
            st.rerun()
        else:
            st.session_state.comparison_playing = False