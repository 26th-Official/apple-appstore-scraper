#!/usr/bin/env python
import os
import sys
import time
import signal
import argparse
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from appstore_scraper.spiders.apps import AppsSpider

# Global flag to track if the spider should be paused
should_pause = False

def signal_handler(sig, frame):
    """Handle Ctrl+C (SIGINT) to gracefully pause the spider."""
    global should_pause
    if not should_pause:
        print("\nReceived interrupt signal. Pausing spider (this may take a moment)...")
        print("Press Ctrl+C again to force quit.")
        should_pause = True
    else:
        print("\nForce quitting...")
        sys.exit(1)

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Run the Apple App Store scraper with pause/resume functionality')
    parser.add_argument('--resume', action='store_true', help='Resume a previously paused crawl')
    parser.add_argument('--output', type=str, default='apps.json', help='Output file path (default: apps.json)')
    parser.add_argument('--format', type=str, default='json', help='Output format (default: json)')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose logging')
    args = parser.parse_args()
    
    # Register the signal handler for SIGINT (Ctrl+C)
    signal.signal(signal.SIGINT, signal_handler)
    
    # Get project settings
    settings = get_project_settings()
    
    # Override logging settings if verbose mode is not enabled
    if not args.verbose:
        settings.set('LOG_ENABLED', False)
        settings.set('LOG_LEVEL', 'ERROR')
    
    # Create the job directory if it doesn't exist
    job_dir = settings.get('JOBDIR')
    if job_dir and not os.path.exists(job_dir):
        os.makedirs(job_dir)
    
    # If not resuming, clear the job directory to start fresh
    if not args.resume and job_dir and os.path.exists(job_dir):
        print(f"Starting a new crawl. Clearing job directory: {job_dir}")
        for filename in os.listdir(job_dir):
            file_path = os.path.join(job_dir, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    import shutil
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Error clearing job directory: {e}")
    
    # Configure the crawler process
    process = CrawlerProcess(settings)
    
    # Add the spider to the process with the specified output
    process.crawl(
        AppsSpider,
        output_file=args.output,
        output_format=args.format
    )
    
    # Print minimal status message
    if args.resume:
        print(f"Resuming previous crawl. Output: {args.output}")
    else:
        print(f"Starting new crawl. Output: {args.output}")
    print("Press Ctrl+C once to pause the crawl.")
    
    # Start the crawling process
    try:
        process.start(stop_after_crawl=False)  # Don't stop reactor after crawl
    except KeyboardInterrupt:
        # This should not be reached due to the signal handler, but just in case
        print("\nCrawling paused. Run with --resume to continue.")
    
    # If the spider was paused, print a message
    if should_pause:
        print("\nCrawling paused. Run with --resume to continue.")
        print(f"To resume, run: python {sys.argv[0]} --resume --output {args.output} --format {args.format}")

if __name__ == "__main__":
    main() 