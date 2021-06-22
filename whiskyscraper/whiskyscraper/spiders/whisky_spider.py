import scrapy

class WhiskySpider (scrapy.Spider):
    name = 'whisky'
    start_urls = ['https://www.whiskyshop.com/scotch-whisky?item_availability=In+Stock']

    def parse(self, response):
        for product in response.xpath("//div[@class='product-item-info']"):
            try:
                yield {
                    'name': product.xpath(".//a[@class='product-item-link']/text()").get(),
                    'price(£)': product.xpath(".//span[@class='price']/text()").get().replace("£",""),
                    'link': product.xpath(".//a[@class='product-item-link']").attrib["href"]
                }
            except:
                yield {
                    'name': product.xpath(".//a[@class='product-item-link']/text()").get(),
                    'price(£)': "Sold Out",
                    'link': product.xpath(".//a[@class='product-item-link']").attrib["href"]
                }

        next_page = response.xpath("//a[@class ='action  next']").attrib["href"]
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)