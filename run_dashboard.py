#!/usr/bin/env python3
"""
Dashboard launcher script for the Algorithm Visualization Framework.

This script provides an easy way to launch the Streamlit dashboard,
handling import issues and providing helpful error messages.
"""

import sys
import os
import subprocess

def main():
    """Launch the Streamlit dashboard."""
    
    # Add the current directory to Python path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    # Check if streamlit is installed
    try:
        import streamlit
        print(f"✅ Streamlit {streamlit.__version__} found")
    except ImportError:
        print("❌ Streamlit not found. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit"])
            print("✅ Streamlit installed successfully")
        except subprocess.CalledProcessError:
            print("❌ Failed to install Streamlit. Please install manually:")
            print("   pip install streamlit")
            return 1
    
    # Check if the dashboard file exists
    dashboard_path = os.path.join(current_dir, "algorithm_visualizer", "ui", "dashboard.py")
    if not os.path.exists(dashboard_path):
        print(f"❌ Dashboard file not found: {dashboard_path}")
        return 1
    
    print("🚀 Launching Algorithm Visualization Dashboard...")
    print(f"📁 Dashboard location: {dashboard_path}")
    print("🌐 Dashboard will open in your default web browser")
    print("⏹️  Press Ctrl+C to stop the dashboard")
    print("-" * 50)
    
    # Launch the dashboard
    try:
        cmd = [sys.executable, "-m", "streamlit", "run", dashboard_path]
        subprocess.run(cmd, cwd=current_dir)
    except KeyboardInterrupt:
        print("\n🛑 Dashboard stopped by user")
        return 0
    except Exception as e:
        print(f"❌ Error launching dashboard: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)