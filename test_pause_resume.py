#!/usr/bin/env python
"""
Test script to verify the pause and resume functionality of the Apple App Store scraper.
This script runs the spider for a short time, pauses it, and then resumes it.
"""

import os
import time
import subprocess
import shutil

def main():
    # Define the output file and job directory
    output_file = "test_apps.json"
    job_dir = "crawls/appstore-jobs"
    
    # Clean up any previous test files
    if os.path.exists(output_file):
        os.remove(output_file)
    if os.path.exists(job_dir):
        shutil.rmtree(job_dir)
    
    print("Step 1: Starting the spider...")
    # Start the spider in a subprocess
    process = subprocess.Popen(
        ["python", "run_spider.py", "--output", output_file],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Let it run for a few seconds
    print("Letting the spider run for 10 seconds...")
    time.sleep(10)
    
    # Send SIGINT to pause the spider
    print("Step 2: Pausing the spider...")
    process.terminate()
    stdout, stderr = process.communicate()
    
    # Only print errors if there are any
    if stderr and stderr.strip():
        print("Errors:")
        print(stderr)
    
    # Check if the job directory was created
    if os.path.exists(job_dir):
        print(f"Job directory '{job_dir}' was created successfully.")
    else:
        print(f"Error: Job directory '{job_dir}' was not created.")
        return
    
    # Check if the output file was created
    if os.path.exists(output_file):
        print(f"Output file '{output_file}' was created successfully.")
        with open(output_file, 'r') as f:
            content = f.read()
            print(f"Output file content length: {len(content)} characters")
    else:
        print(f"Error: Output file '{output_file}' was not created.")
        return
    
    # Wait a moment before resuming
    print("Waiting 3 seconds before resuming...")
    time.sleep(3)
    
    # Resume the spider
    print("Step 3: Resuming the spider...")
    resume_process = subprocess.Popen(
        ["python", "run_spider.py", "--resume", "--output", output_file],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Let it run for a few more seconds
    print("Letting the resumed spider run for 10 seconds...")
    time.sleep(10)
    
    # Stop the resumed spider
    print("Step 4: Stopping the resumed spider...")
    resume_process.terminate()
    resume_stdout, resume_stderr = resume_process.communicate()
    
    # Only print errors if there are any
    if resume_stderr and resume_stderr.strip():
        print("Errors:")
        print(resume_stderr)
    
    # Check the output file again
    if os.path.exists(output_file):
        with open(output_file, 'r') as f:
            new_content = f.read()
            print(f"Updated output file content length: {len(new_content)} characters")
            
        # Check if content was appended
        if len(new_content) > len(content):
            print("Success! The spider successfully resumed and added more data.")
        else:
            print("Warning: The resumed spider did not appear to add more data.")
    
    print("Test completed.")

if __name__ == "__main__":
    main() 