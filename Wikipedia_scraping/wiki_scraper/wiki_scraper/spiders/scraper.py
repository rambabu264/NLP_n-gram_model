import scrapy
from functools import reduce
import nltk
import random
import re
nltk.download('punkt')

class Extract_wiki(scrapy.Spider):

    name = "extract"
    page_no= 2
    start_urls = ['https://en.wikipedia.org/wiki/Language_model']

    def parse(self, response):
        # Extracting all the text from the page and converting it into a single list
        # i.e flattening the 2-D list into 1-D
        content = reduce(lambda x, y: x+y, response.css('p ::text').extract())
        # Joining the list to a string
        content = ''.join([str(sent) for sent in content])

        # Sentence tokenizing the string
        content_tokens = nltk.sent_tokenize(content)

        # Creating list of all escape characters to be removed
        escapes = ''.join([chr(char) for char in range(1, 32)])

        # Removing all escape characters
        translator = str.maketrans(' ', ' ', escapes)
        content_tokens_wo_escape = [sent.translate(translator) for sent in content_tokens]

        # Removing all special characters
        scraped_info = [re.sub('[^A-Za-z0-9]+', ' ', tokens) for tokens in content_tokens_wo_escape]

        see_also_web = response.css('#mw-content-text li > a::attr(href)').extract()
        url = 'https://en.wikipedia.org'+random.choice(see_also_web)

        # Returning the tokenized list
        yield {url: scraped_info}

        Extract_wiki.page_no += 1
        if url is not None and Extract_wiki.page_no < 11:
            print(url)
            yield response.follow(url, callback=self.parse)
