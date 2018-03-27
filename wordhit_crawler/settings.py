# def load_lines(path):
# 	with open(path, 'rb') as f:
# 		return [line.strip() for line in
# 			f.read().decode('utf8').splitlines()
# 			if line.strip()]

# ROTATING_PROXY_LIST = load_lines('proxies.txt') 
# ROTATING_PROXY_PAGE_RETRY_TIMES = 1


DOWNLOADER_MIDDLEWARES = {
#     'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
#     'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
	'random_useragent.RandomUserAgentMiddleware': 400
}

# Select user-agents randomnly
USER_AGENT_LIST = "user-agents.txt"

# Just bot name
BOT_NAME = 'wordhit'

# Defining pipelines
ITEM_PIPELINES = {
	'wordhit_crawler.pipelines.MongoPipeline': 300
	#'wordhit_crawler.pipelines.MongoPipelineWords': 300
}

# Mongo configs
MONGODB_SERVER = 'localhost'
MONGODB_PORT = 27017
MONGODB_DB = 'opiniorizer'
MONGODB_COLLECTION = 'words_pair'
MONGODB_COLLECTION_TEST = 'wordstest'

