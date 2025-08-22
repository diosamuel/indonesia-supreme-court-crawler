import scrapy
import datetime as datetime
import re
from scripts.utils import make_hash_id
from direktori.items import PutusanItem
import logging
from db.utils import insert_data
class LatestSpider(scrapy.Spider):
    stop_crawling = False
    currentPage = 1
    lastPage = 1
    name = "latest"
    CURRENT_DATE = datetime.datetime.now().strftime("%Y-%m-%d")
    allowed_domains = ["putusan3.mahkamahagung.go.id"]
    start_urls = [
        f"https://putusan3.mahkamahagung.go.id/direktori/index/page/{currentPage}.html"
    ]

    def parse(self,response):
        print(self.start_urls)
        checktotalPage = response.css('.pagination.justify-content-center a::attr(href)').getall()
        if len(checktotalPage) < 1:
            self.lastPage = 1
        else:
            totalPage = int(checktotalPage[-1].split('/')[-1].split('.html')[0])
            self.lastPage = totalPage

        if self.currentPage < self.lastPage:
            posts = response.css('#tabs-1 #popular-post-list-sidebar .spost')
            for post in posts:
                item = PutusanItem()
                upload = 'Upload :' in post.css('.small:nth-child(2) strong::text').getall()      
                if upload:
                    uploadText = post.css('.small:nth-child(2)').get().split("Upload :")[1]
                    uploadDateMatch = re.search(r'\b\d{2}-\d{2}-\d{4}\b', uploadText)
                    if uploadDateMatch:
                        rawDate = datetime.datetime.strptime(uploadDateMatch.group(), "%d-%m-%Y")
                        formmatedDateUpload = rawDate.strftime("%Y-%m-%d")
                        item['upload'] = formmatedDateUpload
                        
                        # Check current date
                        if item['upload'] and item['upload'] < self.CURRENT_DATE:
                            self.stop_crawling = True
                            break

                title_elem = post.css('strong a')
                title_href = title_elem.css('::attr(href)').get()
                item['link_detail'] = response.urljoin(title_href)
                
                title_text = post.css('strong a::text').get()
                if title_text:
                    parts = title_text.split("Nomor")
                    item['nomor'] = parts[1].strip() if len(parts) > 1 else ''
                    item['hash_id'] = make_hash_id(item['nomor'])

                info_text = post.css('div > div:nth-child(4)::text').get()
                if info_text:
                    lines = info_text.strip().split('—')
                    print(lines)
                    item['upload'] = lines[0].replace('Tanggal', '').strip()
                item["timestamp"] = datetime.datetime.now().strftime("%c")
                try:
                    insert_data(table='list_putusan',
                                data={
                                    'upload':item["upload"],
                                    'timestamp':item["timestamp"],
                                    'link_detail':item["link_detail"],
                                    'nomor':item['nomor'],
                                    'hash_id':item['hash_id']
                                },
                                key="hash_id")
                    logging.info(item)
                except Exception as e:
                    logging.error(f"SQL Error: {str(e)}")
                    raise Exception(f"Failed to insert data into database: {str(e)}")
            
            # Next pagination
            if not self.stop_crawling and self.currentPage < self.lastPage:
                self.currentPage += 1
                next_page = f"https://putusan3.mahkamahagung.go.id/direktori/index/page/{self.currentPage}.html"
                yield scrapy.Request(next_page, callback=self.parse)

