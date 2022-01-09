'''
in terminal under the same folder as the program type:(under spiders)
scrapy runspider webScrape.py -o quotes.jl
-o quotes.jl is to write a file named quotes.jl
'''
import scrapy
class MoviesSpider(scrapy.Spider):
    name = 'movies'
    allowed_domains = ['stackoverflow.com']
    start_urls = ['https://stackoverflow.com/questions?sort=MostVotes&edited=true']

    def parse(self, response):
        for quote in response.css('div.summary'):
            
            
            yield{
                'question': quote.xpath('h3/a/text()').get(),
                
                
            }
        for quote2 in response.css('div.statscontainer'):
           
            
            yield{
                'views':quote2.xpath('div[2]/text()').get().strip()
                
            }
        for quote2 in response.css('div.statscontainer'):
            
            
            yield{
                'answers':quote2.xpath('div/div[2]/strong/text()').get()
                
                #get each text between <span class="text"...>(...)
            }
        
        for quote1 in response.css('div.votes'):
           
            
            yield{
                'votes': quote1.xpath('span/strong/text()').get(),
                
            }
        for quote1 in response.css('div.flex--item'):
           
            
            yield{
                'languages': quote1.xpath('div[1]/a/text()').getall(),
                
                }
        next_page = response.css('li.next a::attr("href")').get()
        #get next page
        if next_page is not None:
            yield response.follow(next_page, self.parse)
            
       