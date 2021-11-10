import json
import scrapy
from scrapy.crawler import CrawlerProcess


class aldi2(scrapy.Spider):
    name = 'final'
    start_urls = ['https://www.aldi.nl/producten.html']

    def parse(self, response,**kwargs):
        for category_url in response.css('div.mod-content-tile__content a::attr(href)').getall():
            yield response.follow('https://www.aldi.nl' + category_url, callback=self.parse_page)
        pass

    def parse_page(self, response):
        for subcategory_url in response.css('div.mod-content-tile__content a::attr(href)').getall():
            yield response.follow('https://www.aldi.nl' + subcategory_url, callback=self.parse_products)
        pass

    def parse_products(self, response):
        for product_url in response.css('.mod-article-tile__action::attr(href)').getall():
            yield response.follow('https://www.aldi.nl/' + product_url, callback=self.productsdisplay)

    def productsdisplay(self, response):
        script = response.css('.mod.mod-article-intro.ct-backwaren::attr(data-article)').get()
       # or response.xpath("//div[contains(@data-t-name, 'ArticleIntro')]").get()
        json_data = json.loads(script)
        yield {
            'name': json_data['productInfo']['productName'],
            'price': json_data['productInfo']['priceWithTax'],
            'id': json_data['productInfo']['productID'],
            'quantity': json_data['productInfo']['quantity'],
            'primary_category': json_data['productCategory']['primaryCategory'],
            'sub_category1' : json_data['productCategory']['subCategory1'],
            'sub_category2' : json_data['productCategory']['subCategory2']
        }

if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(aldi2)
    process.start()
