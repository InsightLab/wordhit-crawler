import scrapy
from scrapy.selector import Selector
from wordhit_crawler.items import WordhitItem

class WordHitSpider(scrapy.Spider):
	name = 'wordhitSpider'
	allowed_domains = ["www.google.com"]
	
	custom_settings = {
        'DOWNLOAD_DELAY': 0.1,
        'CONCURRENT_REQUESTS': 10
    }

	def start_requests(self):
		base_url = "https://www.bing.com/search?q=%s"
		
		with open('tuple_words.txt', 'rb') as f:
			lines = [line.strip() for line in f.read().decode('utf8').splitlines() if line.strip()]

		size = len(lines)

		for idx in range(size):
			words = lines[idx]

			completeUrl = base_url % (words)
			#completeUrl = completeUrl.encode('utf-8')


			yield scrapy.Request(url=completeUrl, callback=self.parse, meta={'words': words})

			
	def parse(self, response):

		wordItem = self.parse_bing(response)
		if(wordItem):
			yield wordItem

	def parse_bing(self, response):
		
		# Bing
		selector = '//*[@class="sb_count"]/text()'
		return self._parse(response, selector, 0)

	def hasResult(self, result, word):
		if(len(result) == 0):
			with open("words_missing.txt", "a") as myfile:
				myfile.write("%s\n" % word)
			return False

		return True

	def _parse(self, response, selector, hitPos):

		result = Selector(response).xpath(selector).extract()

		if( self.hasResult(result, response.meta['words']) ):

			hitsText = result[0]
			hits = hitsText.split(' ')[hitPos]
			word = response.meta['words']
		
			# print(hitsText)
			# print(hits)
			# print(word)

			wordItem = WordhitItem()
			wordItem['word'] = word
			wordItem['hits'] = hits

			return wordItem
		
		return None
		

		
