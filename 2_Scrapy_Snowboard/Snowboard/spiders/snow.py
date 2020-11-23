# -*- coding: utf-8 -*-
import scrapy



class SnowSpider(scrapy.Spider):
    name = 'blue-tomato'
    allowed_domains = ['blue-tomato.com']
    start_urls = ['https://www.blue-tomato.com/de-DE/products/categories/Snowboard+Shop-00000000/']
    def __init__(self):
        self.page_n = 0


    def parse(self, response):
        ur = response.url
        print('Url is **********  : ' , ur)
        base_url = 'https://www.blue-tomato.com'

        total_products_info = response.xpath('//*[@class="catHeadline"]/span[@class="count"]//text()').extract()
        total_products = int(total_products_info[0].strip().replace(')','').replace('(','').replace(',',''))
        total_pages = int(response.xpath('//*[@id="searchPanes"]/div/div[2]/section[1]/div[2]/nav/ul/li[2]//text()').extract()[0].split('/')[1])
        try:
            next_page_link_info = response.xpath('//li[@class="next browse"]/a/@href').extract()[0]
            next_page_link = base_url + next_page_link_info
        except:
            next_page_link = ''


        total_products_on_current_page = len(response.css('section#productList > ul >li.productcell '))
        data = response.css('span.productdesc')
        product_image_data = response.css('li.productcell ')
        product_name = data.xpath('./a[@data-action="click-producttile"]/@data-productname')
        product_brand = data.xpath('./a[@data-action="click-producttile"]/@data-brand')
        product_price = data.xpath('./span[1]//text()')
        product_url = data.xpath('./a[@data-action="click-producttile"]/@href')
        product_img_url = product_image_data.xpath('./span[1]/img/@src')


        for i in range(len(product_name)):
            if(product_price[i].extract().strip().replace('\xa0',' ').replace(',','') ==''):
                sale_price = data.xpath('//*[@id="p{}"]/span[2]/span[1]//text()'.format(i))
                price = sale_price.extract()[0].strip().replace('\xa0',' ').replace(',','').replace('statt ','')

            else:
                price = product_price[i].extract().strip().replace('\xa0',' ').replace(',','').replace('statt ','')
            yield{
            'Product_Name': product_name[i].extract(),
            'Product_Brand':product_brand[i].extract(),
            'Product_Price':price,
            'Product_Image_Url':'https:' + product_img_url[i].extract(),
            'Product_Url' : base_url + product_url[i].extract(),
            }

        if(len(next_page_link)>0):
            yield scrapy.Request(url=next_page_link,
                   callback=self.parse,
                   headers={'User-Agent': 'Mozilla/5.0'})


