import sys
import time
from scrapy import signals
from scrapy.exceptions import NotConfigured

class InPlaceCounterExtension:
    """
    Extension to display an in-place counter of scraped items.
    """
    def __init__(self, stats):
        self.stats = stats
        self.items_scraped = 0
        self.start_time = time.time()
        
    @classmethod
    def from_crawler(cls, crawler):
        # Only enable the extension if it's enabled in settings
        if not crawler.settings.getbool('EXTENSIONS_ENABLED', True):
            raise NotConfigured
        
        # Instantiate the extension with the stats collector
        ext = cls(crawler.stats)
        
        # Connect the extension to the signals
        crawler.signals.connect(ext.item_scraped, signal=signals.item_scraped)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        
        return ext
    
    def item_scraped(self, item, spider):
        """Called when an item has been scraped."""
        self.items_scraped += 1
        elapsed_time = time.time() - self.start_time
        items_per_second = self.items_scraped / elapsed_time if elapsed_time > 0 else 0
        
        # Clear the current line and print the counter
        sys.stdout.write(f"\rItems scraped: {self.items_scraped} | Rate: {items_per_second:.2f} items/sec")
        sys.stdout.flush()
    
    def spider_closed(self, spider, reason):
        """Called when the spider is closed."""
        elapsed_time = time.time() - self.start_time
        items_per_second = self.items_scraped / elapsed_time if elapsed_time > 0 else 0
        
        # Print final stats with a newline
        sys.stdout.write(f"\rCompleted: {self.items_scraped} items | Total time: {elapsed_time:.2f}s | Avg rate: {items_per_second:.2f} items/sec\n")
        sys.stdout.flush() 