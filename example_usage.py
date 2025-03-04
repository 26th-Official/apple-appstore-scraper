#!/usr/bin/env python
"""
Example script demonstrating how to use the Apple App Store scraper with pause and resume functionality.
This script shows how to:
1. Start a new crawl
2. Pause it after a certain number of items
3. Resume it later
"""

import os
import sys
import time
import json
import subprocess
from datetime import datetime

def count_items_in_file(file_path):
    """Count the number of items in a JSON file."""
    if not os.path.exists(file_path):
        return 0
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                return 0
            
            # Handle both JSON array and JSON Lines formats
            if content.startswith('['):
                # JSON array format
                data = json.loads(content)
                return len(data)
            else:
                # JSON Lines format
                return len(content.split('\n'))
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return 0

def run_until_count(output_file, target_count, resume=False):
    """Run the spider until it reaches the target count of items."""
    cmd = ["python", "run_spider.py", "--output", output_file]
    if resume:
        cmd.append("--resume")
    
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    print(f"{'Resuming' if resume else 'Starting'} crawl. Target count: {target_count} items")
    print(f"Process PID: {process.pid}")
    
    try:
        # We don't need to check the count ourselves anymore since the extension will show it
        # Just wait for the process to finish or for the user to interrupt
        process.wait()
        stdout, stderr = process.communicate()
        if stderr and stderr.strip():
            print(f"Errors: {stderr}")
    
    except KeyboardInterrupt:
        print("Manually interrupted. Pausing spider...")
        process.terminate()
        process.wait()
        print("Spider paused successfully")

def main():
    output_file = "example_apps.json"
    
    # First run: collect 10 items
    print("=== PHASE 1: Initial Crawl ===")
    run_until_count(output_file, 10)
    
    # Wait a bit before resuming
    print("\nWaiting 5 seconds before resuming...\n")
    time.sleep(5)
    
    # Second run: resume and collect 10 more items (20 total)
    print("=== PHASE 2: Resumed Crawl ===")
    run_until_count(output_file, 20, resume=True)
    
    print("\nExample completed successfully!")
    print(f"Check {output_file} for the scraped data.")

if __name__ == "__main__":
    main() 