from scrapy import Spider
from ..items import CompaniesItem
import scrapy


class CompaniesSpider(Spider):
    name = "companies"
    allowed_domains = ['startup.miami']
    # Defining the list of pages to scrape
    start_urls = ["http://startup.miami/category/startups/"]

    def parse(self, response):
        # getting link & name and sending item to parse_detail in meta
        rows = response.xpath('//*[@id="datafetch"]/article')
        for row in rows:
            link = row.xpath('.//@href').extract_first()
            location = row.xpath(
                './/*[@class="textoCoworking"]/text()').extract_first()
            name = row.xpath('.//header/h2/a/text()').extract_first()
            item = CompaniesItem()
            item['link'] = link
            item['name'] = name.strip()
            item['location'] = location.strip()
            yield scrapy.Request(link,
                                 callback=self.parse_detail,
                                 meta={'item': item})

        # getting the next page
        next_page = response.xpath(
            '//*[@class="next page-numbers"]/@href').extract_first()
        if next_page:
            yield scrapy.Request(next_page, callback=self.parse)

        # Getting details inside the links    
    def parse_detail(self, response):
        item = response.meta['item']
        founded = response.xpath('.//td[2]/p[3]/text()').extract_first()
        industry = response.xpath('.//*[@id="PostCoworking"]/table/tbody/tr[2]/td[2]/p[4]/text()').extract_first()
        url = response.xpath('.//p/a/@href').extract_first()

        item['founded'] = founded
        item['industry'] = industry
        item['url'] = url
        yield item