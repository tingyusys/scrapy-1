import scrapy
from ..items import Xm1Item

class XuNianShaSpider(scrapy.Spider):
    name = 'xu_nian_sha'
    # allowed_domains = ['xxx.com']
    start_urls = ['https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=58025142_oem_dg&rsv_dl=ns_pc&word=%E5%BE%90%E5%BF%B5%E6%B2%99&x_bfe_rqs=03E80&x_bfe_tjscore=0.100000&tngroupname=union&newVideo=12&pn=50']
    page_num=0
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'TESTSpider.middlewares.ProcessAllExceptionMiddleware': 120,
        },
        'DOWNLOAD_DELAY': 1,  # 延时最低为2s
        'AUTOTHROTTLE_ENABLED': True,  # 启动[自动限速]
        'AUTOTHROTTLE_DEBUG': True,  # 开启[自动限速]的debug
        'AUTOTHROTTLE_MAX_DELAY': 10,  # 设置最大下载延时
        'DOWNLOAD_TIMEOUT': 15,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 4  # 限制对该网站的并发请求数
    }

    def parse(self, response):
        if not response.url:  # 接收到url==''时
            print('500')
            yield Xm1Item(key=response.meta['key'], _str=500, alias='')
        elif 'exception' in response.url:
            print('exception')
            yield Xm1Item(key=response.meta['key'], _str='EXCEPTION', alias='')













        node_list=response.xpath('//div[@id="content_left"]/div/div[@class="result-op c-container xpath-log new-pmd"]')
        for  k,node in enumerate(node_list):
            if k==7:
                break
            # print(node)

            two_url=node.xpath('./div/h3/a/@href').extract()[0]
            title=node.xpath('./div/h3/a/text()').extract()
            media_type=node.xpath('./div/div/div[@class="c-span-last c-span9"]/div/span/text()').extract()
            digest=node.xpath('./div/div/div[@class="c-span-last c-span9"]/span/text()').extract()
            if not media_type or not digest :
                media_types = node.xpath('./div/div/div[@class="c-span-last c-span12"]/div/span/text()').extract()[0]
                if len(node.xpath('./div/div/div[@class="c-span-last c-span12"]/div/span/text()').extract())!=1:
                    time = node.xpath('./div/div/div[@class="c-span-last c-span12"]/div/span/text()').extract()[1]
                else:
                    time='查询'
                digests = node.xpath('./div/div/div[@class="c-span-last c-span12"]/span/text()').extract()
                # print(media_types,time,digests)
                if len(title)!=1:
                    title=title[0]+'徐念沙'+title[1]
                digests=digests[0]+'徐念沙'+digests[1]
                # print(digests)
                item_pop = Xm1Item()
                if time and two_url and title and media_types and digests:
                    item_pop['time'] = time
                    # print(two_url)

                    item_pop['title'] = title
                    # item_pop['media_types'] = media_types
                    item_pop['digests'] = digests
                print('数据开始回传')
                # print(two_url)
                if 'for=pc' in two_url:
                    if two_url:
                        item_pop['two_url'] = two_url
                        two_url = two_url.replace('for=pc', '')


                    # yield item_pop
                        yield scrapy.Request(two_url,callback=self.get_detail,meta={'info':item_pop})
                    print('数据回传成功')
            if media_type:
                # print('------------------------------------------------------------')
                # print(media_type,digest)
                # media_types = node.xpath('./div/div/div[@class="c-span-last c-span9"]/div/span/text()').extract()[0]
                # time = node.xpath('./div/div/div[@class="c-span-last c-span9"]/div/span/text()').extract()[1]
                # print(media_types,time,digest)
                # digests=digest[0]+'徐念沙'+digest[1]
                try:
                    if len(digest)!=1:
                        digest=digest[0]+'徐念沙'+digest[1]
                    else:
                        digest=digest[0]
                    item_pop = Xm1Item()
                    if len(media_type)==2:
                        item_pop['time'] = media_type[1]
                    else:
                        item_pop['time']='查询'

                    item_pop['title'] = title[0]
                    item_pop['media_types'] = media_type[0]
                    item_pop['digests'] = digest
                    if 'for=pc' in two_url:
                        if two_url:
                            item_pop['two_url'] = two_url
                            two_url=two_url.replace('for=pc','')
                            yield scrapy.Request(two_url,callback=self.get_detail,meta={'info':item_pop})
                except:
                    print('这是个视频')
        # page_url=['https://www.baidu.com/s?tn=58025142_oem_dg&rtt=4&bsst=1&cl=2&wd=%E5%BE%90%E5%BF%B5%E6%B2%99&medium=0&x_bfe_rqs=03E80&x_bfe_tjscore=0.100000&tngroupname=union&newVideo=12&rsv_dl=news_b_pn&pn=10'
        #     ,'https://www.baidu.com/s?tn=58025142_oem_dg&rtt=4&bsst=1&cl=2&wd=%E5%BE%90%E5%BF%B5%E6%B2%99&medium=0&x_bfe_rqs=03E80&x_bfe_tjscore=0.100000&tngroupname=union&newVideo=12&rsv_dl=news_b_pn&pn=20']
        # for i in page_url:
        #     yield scrapy.Request(i)


    def get_detail(self,response):

        item=Xm1Item()
        info=response.meta['info']
        item.update(info)
        # print(item['media_types'])
        print(item['two_url'])
        print(response)
        content = response.xpath('//div[@id="commentModule"]')
        if not content:
            content = response.xpath('//p/text()').extract()
            print(content)
        print(content)
        # picture=response.xpath('./a[@ class="news-title-font_1xS-F"]/@href').extract()[0]
        # if item['media_types']=='网易':
        #     print('开心')
        #     noto_list=response.xpath('//div[normalize-space(@class)="post_info"]')
        #     for noto in noto_list:
        #         content=noto.xpath('./span[@class="c-font-normal c-color-text"]').extract()[0]
        #         picture=noto.xpath('./a[@ class="news-title-font_1xS-F"]/@href').extract()[0]
        #         item['picture']=picture
        #         item['content']=content
        #         yield item
        # if item['media_types']=='网易':
        #     print('开心')
        #     noto_list=response.xpath('//div[normalize-space(@class)="post_info"]')
        #     for noto in noto_list:
        #         content=noto.xpath('./span[@class="c-font-normal c-color-text"]').extract()[0]
        #         picture=noto.xpath('./a[@ class="news-title-font_1xS-F"]/@href').extract()[0]
        #         item['picture']=picture
        #         item['content']=content
        #         yield item
        # if item['media_types']=='网易':
        #     print('开心')
        #     noto_list=response.xpath('//div[normalize-space(@class)="post_info"]')
        #     for noto in noto_list:
        #         content=noto.xpath('./span[@class="c-font-normal c-color-text"]').extract()[0]
        #         picture=noto.xpath('./a[@ class="news-title-font_1xS-F"]/@href').extract()[0]
        #         item['picture']=picture
        #         item['content']=content
        #         yield item
        # if item['media_types']=='网易':
        #     print('开心')
        #     noto_list=response.xpath('//div[normalize-space(@class)="post_info"]')
        #     for noto in noto_list:
        #         content=noto.xpath('./span[@class="c-font-normal c-color-text"]').extract()[0]
        #         picture=noto.xpath('./a[@ class="news-title-font_1xS-F"]/@href').extract()[0]
        #         item['picture']=picture
        #         item['content']=content
        #         yield item
        # if item['media_types']=='网易':
        #     print('开心')
        #     noto_list=response.xpath('//div[normalize-space(@class)="post_info"]')
        #     for noto in noto_list:
        #         content=noto.xpath('./span[@class="c-font-normal c-color-text"]').extract()[0]
        #         picture=noto.xpath('./a[@ class="news-title-font_1xS-F"]/@href').extract()[0]
        #         item['picture']=picture
        #         item['content']=content
        #         yield item
        # if item['media_types']=='网易':
        #     print('开心')
        #     noto_list=response.xpath('//div[normalize-space(@class)="post_info"]')
        #     for noto in noto_list:
        #         content=noto.xpath('./span[@class="c-font-normal c-color-text"]').extract()[0]
        #         picture=noto.xpath('./a[@ class="news-title-font_1xS-F"]/@href').extract()[0]
        #         item['picture']=picture
        #         item['content']=content
        #         yield item
        # if item['media_types']=='网易':
        #     print('开心')
        #     noto_list=response.xpath('//div[normalize-space(@class)="post_info"]')
        #     for noto in noto_list:
        #         content=noto.xpath('./span[@class="c-font-normal c-color-text"]').extract()[0]
        #         picture=noto.xpath('./a[@ class="news-title-font_1xS-F"]/@href').extract()[0]
        #         item['picture']=picture
        #         item['content']=content
        #         yield item
        # if item['media_types']=='网易':
        #     print('开心')
        #     noto_list=response.xpath('//div[normalize-space(@class)="post_info"]')
        #     for noto in noto_list:
        #         content=noto.xpath('./span[@class="c-font-normal c-color-text"]').extract()[0]
        #         picture=noto.xpath('./a[@ class="news-title-font_1xS-F"]/@href').extract()[0]
        #         item['picture']=picture
        #         item['content']=content
        #         yield item
        # if item['media_types']=='网易':
        #     print('开心')
        #     noto_list=response.xpath('//div[normalize-space(@class)="post_info"]')
        #     for noto in noto_list:
        #         content=noto.xpath('./span[@class="c-font-normal c-color-text"]').extract()[0]
        #         picture=noto.xpath('./a[@ class="news-title-font_1xS-F"]/@href').extract()[0]
        #         item['picture']=picture
        #         item['content']=content
        #         yield item
        # if item['media_types']=='网易':
        #     print('开心')
        #     noto_list=response.xpath('//div[normalize-space(@class)="post_info"]')
        #     for noto in noto_list:
        #         content=noto.xpath('./span[@class="c-font-normal c-color-text"]').extract()[0]
        #         picture=noto.xpath('./a[@ class="news-title-font_1xS-F"]/@href').extract()[0]
        #         item['picture']=picture
        #         item['content']=content
        #         yield item
        # if item['media_types']=='网易':
        #     print('开心')
        #     noto_list=response.xpath('//div[normalize-space(@class)="post_info"]')
        #     for noto in noto_list:
        #         content=noto.xpath('./span[@class="c-font-normal c-color-text"]').extract()[0]
        #         picture=noto.xpath('./a[@ class="news-title-font_1xS-F"]/@href').extract()[0]
        #         item['picture']=picture
        #         item['content']=content
        #         yield item
        # if item['media_types']=='网易':
        #     print('开心')
        #     noto_list=response.xpath('//div[normalize-space(@class)="post_info"]')
        #     for noto in noto_list:
        #         content=noto.xpath('./span[@class="c-font-normal c-color-text"]').extract()[0]
        #         picture=noto.xpath('./a[@ class="news-title-font_1xS-F"]/@href').extract()[0]
        #         item['picture']=picture
        #         item['content']=content
        #         yield item
        # if item['media_types']=='网易':
        #     print('开心')
        #     noto_list=response.xpath('//div[normalize-space(@class)="post_info"]')
        #     for noto in noto_list:
        #         content=noto.xpath('./span[@class="c-font-normal c-color-text"]').extract()[0]
        #         picture=noto.xpath('./a[@ class="news-title-font_1xS-F"]/@href').extract()[0]
        #         item['picture']=picture
        #         item['content']=content
        #         yield item


