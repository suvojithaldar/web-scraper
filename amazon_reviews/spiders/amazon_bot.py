import scrapy

reviews_url = 'https://www.amazon.in/product-reviews/{}'
asin_list= ['B07BB3PYD8/']

class AmazonBotSpider(scrapy.Spider):
    name = 'amazon_bot'
    
    def start_requests(self):
        for asin in asin_list:
            url = reviews_url.format(asin)
            yield scrapy.Request(url)


    def parse(self, response):
        for review in response.css('[data-hook="review"]'):
            item = {
                'stars': review.css('[data-hook="review-star-rating"] span ::text').get(),
                'title': review.css('[data-hook="review-title"] span ::text').get(),
                'review': review.xpath('normalize-space(.//*[@data-hook="review-body"])').get()
            }
            yield item

        next_page = response.xpath('//a[text()= "Next page"]/@href').get()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page))
            

        
