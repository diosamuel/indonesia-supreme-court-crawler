import scrapy
import os
import json
import re
import logging
from datetime import datetime
from direktori.items import DeskripsiPutusanItem, PutusanTerkaitItem
from db.utils import retrieve_data
from scripts.utils import make_hash_id
"""
Retrieve link_detail from list_putusan table and scrape each one by one
Store into informasi_putusan
"""
class PageInformationScrape(scrapy.Spider):
    putusan = {}
    name = "scrape_details"
    allowed_domains = ["putusan3.mahkamahagung.go.id"]
    start_urls = list(map(lambda x:x[0],retrieve_data(table="list_putusan",column="link_detail")))

    custom_settings = {
        'ITEM_PIPELINES': {
            'direktori.pipelines.DeskripsiPutusanItemPipeline': 100,
        },
        'DOWNLOAD_DELAY':1
    }

    def parse(self, response):
        global item
        item = DeskripsiPutusanItem()
        url_putusan = response.request.url
        title = response.css("h2 strong::text").get(default="").strip()
        view_count = response.css('div[title="Jumlah view"]::text').get()
        download_count = response.css('div[title="Jumlah download"]::text').get()

        putusan_terkait_item = self.handleRelatedPutusan(response)

        # Each putusan has different keys and values, so create a dynamic scraper based on the table's keys and attributes
        for row in response.css("table tr"):
            tds = row.css("td")
            if len(tds) == 2:
                key = tds[0].css("::text").get(default="").strip().replace(":", "").replace(" ","_").lower()
                value = tds[1].xpath("normalize-space(string())").get(default="").strip()
                if key:
                    if key == "tahun":
                        key="tahun_putusan"
                    item[key] = value
        
        item["putusan_terkait"] = putusan_terkait_item
        item["jumlah_view"] = view_count
        item["jumlah_download"] = download_count
        
        file = response.css("#collapseThree a::attr(href)").getall()
        if len(file) != 0:
            item["link_zip"], item["link_pdf"] = response.css("#collapseThree a::attr(href)").getall()

        yield {
            "url":url_putusan,
            "title": title,
            "description": item,
            "putusan_terkait": putusan_terkait_item
        }

    def handleRelatedPutusan(self,response):
        putusan_terkait_item = PutusanTerkaitItem()
        laws = list(set(map(lambda res:re.sub(r':','',res.strip()),response.css("ul.portfolio-meta.nobottommargin")[2].css("::text").getall())))
        if len(laws) > 10: #If the length is greater than 10, the HTML element indicates an overflow and needs to be handled differently depending on the case.
            putusan_type = response.css("ul.portfolio-meta.nobottommargin")[2].css("strong::text").getall()
            
            # 'Putusan' will serve as the separator for the scraped results.
            if 'Putusan' in putusan_type: 
                putusan_type = putusan_type[0:putusan_type.index('Putusan')]
            putusan_type = list(map(lambda val:re.sub(r":","",val),putusan_type))
            # putusan_type = [item.strip() for item in putusan_type if item.strip()]

            putusan_number = response.css("ul.portfolio-meta.nobottommargin")[2].css("a[href]::text").getall()
            putusan_link = response.css("ul.portfolio-meta.nobottommargin")[2].css("a[href]::attr(href)").getall()
            
            # 'Putusan' will serve as the separator for the scraped results.
            if 'Putusan' in putusan_number:
                loc = putusan_number.index('Putusan')
                putusan_number = putusan_number[0:loc]
                putusan_link = putusan_link[0:loc]
            
            cleaned_putusan_type = [x.strip() for x in putusan_type if x.strip()]
            cleaned_putusan_number = [x.strip() for x in putusan_number if x.strip()]

            # The output will be two arrays, which are expected to have the same length so they can be paired
            if len(cleaned_putusan_type) == len(cleaned_putusan_number):
                for index in range(len(cleaned_putusan_type)):
                    putusan = (cleaned_putusan_type[index]).lower().replace(" ","_") # peninjauan kembali -> peninjauan_kembali
                    putusan_terkait_item[putusan] = cleaned_putusan_number[index]
                    putusan_terkait_item["link_"+putusan] = putusan_link[index]

                print(putusan_terkait_item)
        else:
            print("==================")
            print(laws)
            print("==================")
            # for index in range(1,len(laws[1:]),2):
            #     self.putusan[laws[index]]=laws[index+1]

        return putusan_terkait_item