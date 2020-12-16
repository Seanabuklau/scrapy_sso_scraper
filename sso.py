import scrapy

class SsoSpider(scrapy.Spider):
    name = 'sso'
    allowed_domains = ['sso.agc.gov.sg']
    start_urls = ['https://sso.agc.gov.sg/Browse/Act/Current']


    def parse(self, response):
        acts = response.xpath("//table[@class='table browse-list']/tbody/tr")
 
        for act in acts:
            yield {

                'Act title': act.xpath(".//td[1]/a[@class='non-ajax']/text()").get(),
                'Short-hand code': act.xpath(".//td[1]/a[@class='non-ajax']/@href").get()
            }

        #relative_url = response.xpath('//div[@class="col-xs-7 col-sm-8 no-side-padding"]/a/@href').get()
        relative_url = response.xpath("//a[@aria-label='Next Page']/@href").get()
        next_page = response.urljoin(relative_url)

        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)

