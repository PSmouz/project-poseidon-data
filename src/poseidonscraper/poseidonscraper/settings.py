import time
# Scrapy settings for poseidonscraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "poseidonscraper"

SPIDER_MODULES = ["poseidonscraper.spiders"]
NEWSPIDER_MODULE = "poseidonscraper.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = "poseidonscraper (+http://www.yourdomain.com)"
# USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"

# FEED_EXPORT_BATCH_ITEM_COUNT = 50
# current_date = time.strftime('%Y_%m_%d')
FEEDS = {
    f'data/%(name)s/data_%(time)s.json': { #f'{BOT_NAME}/data/%(name)s/data_{current_date}.json'
        'format': 'json',
        'encoding': 'utf8',
    },
}

SCRAPEOPS_API_KEY = '9185667e-d82f-4786-aef2-db9a72d3ea47' # signup at https://scrapeops.io
SCRAPEOPS_FAKE_USER_AGENT_ENDPOINT = 'https://headers.scrapeops.io/v1/user-agents'
SCRAPEOPS_FAKE_USER_AGENT_ENABLED = True
SCRAPEOPS_NUM_RESULTS = 5

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
# REDIRECT_ENABLED = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "poseidonscraper.middlewares.PoseidonscraperSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
  #  "poseidonscraper.middlewares.PoseidonscraperDownloaderMiddleware": 543,
  'poseidonscraper.middlewares.FakeBrowserHeaderAgentMiddleware': 400,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html

IMAGES_STORE = f'H:\___FDRIVE\_resources\python\poseidonscraper\data\images' #"poseidonscraper/poseidonscraper/data/images"
IMAGES_RESULT_FIELD = 'images'
IMAGES_URLS_FIELD = 'images'

ITEM_PIPELINES = {
  # "poseidonscraper.pipelines.PoseidonscraperPipeline": 300,
  "poseidonscraper.pipelines.PoseidonscraperImagesPipeline": 1,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

# # Disable Scrapy's built-in log settings
# LOG_ENABLED = True
# LOG_STDOUT = True

# # Set the log level to a higher value to reduce verbosity
# LOG_LEVEL = 'INFO'  #  You can set it to 'WARNING', 'ERROR', or 'CRITICAL' for even less output

# # Optionally, you can configure a custom log format
# LOG_FORMAT = '%(asctime)s [%(name)s] %(levelname)s: %(message)s'
# LOG_DATEFORMAT = '%Y-%m-%d %H:%M:%S'

LOG_LEVEL = 'INFO'  # Set the desired log level, e.g., INFO, WARNING, ERROR
# LOG_APPEND = True  # Append to the file instead of overwriting
# LOG_FILE = f'H:/___FDRIVE/_resources/python/poseidonscraper/logs/log.txt'  # Specify the log file

# Exclude DEBUG messages from specific loggers
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'scrapy.pipelines.files': {
#             'level': 'INFO',  # Set to INFO or higher to exclude DEBUG messages
#         },
#         'PIL.TiffImagePlugin': {
#             'level': 'ERROR',  # Set to INFO or higher to exclude DEBUG messages
#         },
#     },
# }