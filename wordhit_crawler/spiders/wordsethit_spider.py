import scrapy
from scrapy.selector import Selector
from wordhit_crawler.items import WordhitItem

class WordHitSpider(scrapy.Spider):
	name = 'wordhitSpider'
	#allowed_domains = ["www.google.com"]
	
	custom_settings = {
        'DOWNLOAD_DELAY': 0.05,
        'CONCURRENT_REQUESTS': 50
    }

	def start_requests(self):
		#base_url = "https://www.google.com/search?q=%s"
		base_url = "https://www.bing.com/search?q=%s"
		
		with open('words.txt', 'rb') as f:
			lines = [line.strip() for line in f.read().decode('utf8').splitlines() if line.strip()]

		sizeLines = len(lines)
		# print(sizeLines)

		for idx1 in range(301, 307):
			word1 = lines[idx1]
			
			for idx2 in range(idx1, sizeLines):
				word2 = lines[idx2]

				words = word1 + '+' + word2
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
		

	def parse_google(self, response):

		# Google
		selector = '//*[@id="resultStats"]/text()'
		return self._parse(response, selector, 1)
		


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