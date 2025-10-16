import scrapy
import re
import logging
import json
from db.utils import insert_data,retrieve_data
"""
Generate big tree combination putusan MA and store it into crawl_populate.json
tree = {
    {{jenis direktori}}:{
        {{jenis klasifikasi}}:{
            {{jenis pengadilan}}:{
                {{list upload}}:{{list years}}
            }
        }
    }
}
"""
class GenerateTree(scrapy.Spider):
    name = "generate_tree"
    allowed_domains = ["putusan3.mahkamahagung.go.id"]
    start_urls = [ "ht  tps://putusan3.mahkamahagung.go.id/direktori.html" ]
    tree = {}
    def parse(self, response):
        traverseDirektori = response.xpath('(//*[@aria-labelledby="headingOne"])[1]//a/@href').getall()
        traverseDirektori.remove("https://putusan3.mahkamahagung.go.id/direktori.html")
        for i, direktori in enumerate(traverseDirektori):
            self.tree[direktori] = {}
            retrieveCount = retrieve_data(column="count(*)",table="tree_direktori")
            if len(retrieveCount) > 0:
                totalData = int(retrieveCount[0][0]) # total yang sudah diambil
            if totalData != len(traverseDirektori):                    
                insert_data(table="tree_direktori",data={
                    "link_detail":direktori,
                    "level":1,
                    "tipe":"direktori",
                    "parent":''
                },key="link_detail")
            else:
                logging.info("Direktori already exists")
                pass
            yield scrapy.Request(
                direktori, 
                callback=self.parseTraverseKlasifikasi,
                cb_kwargs={'direktori': direktori},
            )

    def parseTraverseKlasifikasi(self, response, direktori):
        traverseKlasifikasi = response.xpath('(//*[@aria-labelledby="headingOne"])[2]//a/@href').getall()
        traverseKlasifikasiTotal = response.xpath('(//*[@aria-labelledby="headingOne"])[2]//span/text()').getall()
        for index,klasifikasi in enumerate(traverseKlasifikasi):
            if len(klasifikasi) > 0: # check validity of klasifikasi
                self.tree[direktori][klasifikasi] = {}
                insert_data(table="tree_klasifikasi",data={
                    "link_detail":klasifikasi,
                    "level":2,
                    "tipe":"klasifikasi",
                    "parent":direktori
                },key="link_detail")
                if int(traverseKlasifikasiTotal[index]) < 10000: # limit
                    pass
                else:
                    yield scrapy.Request(klasifikasi, callback=self.parseTraversePengadilan,cb_kwargs={
                        'direktori':direktori,
                        'klasifikasi':klasifikasi,
                    })
    
        with open("logger.log",'w') as f:
            f.write(f"{direktori} - {klasifikasi}")

        with open("crawl_populate.json","w") as f:
            f.write(json.dumps(self.tree)) 
    
    def parseTraversePengadilan(self,response,direktori,klasifikasi):
        traversePengadilan = response.xpath('(//*[@aria-labelledby="headingOne"])[3]//a/@href').getall()
        traversePengadilanTotal = response.xpath('(//*[@aria-labelledby="headingOne"])[3]//span/text()').getall()
        for index,pengadilan in enumerate(traversePengadilan):
            if len(pengadilan) > 0:# check validity of pengadilan
                self.tree[direktori][klasifikasi][pengadilan] = {}
                
                insert_data(table="tree_pengadilan",data={
                    "link_detail":pengadilan,
                    "level":3,
                    "tipe":"pengadilan",
                    "parent":klasifikasi
                },key="link_detail")

                if int(traversePengadilanTotal[index]) < 10000:
                    pass
                else:
                    yield scrapy.Request(pengadilan, callback=self.findYear,cb_kwargs={
                        'direktori':direktori,
                        'klasifikasi':klasifikasi,
                        'pengadilan':pengadilan
                    })
        # with open("logger.log",'w') as f:
        #     f.write(f"{direktori} - {klasifikasi} - {pengadilan}")

        with open("crawl_populate.json","w") as f:
            f.write(json.dumps(self.tree))            

    def findYear(self,response,direktori,klasifikasi,pengadilan):
        findUpload = response.xpath('(//*[@aria-labelledby="headingOne"])[4]//a/@href').getall()[-1] # get last value
        yield scrapy.Request(findUpload, callback=self.parseTraverseTahun,cb_kwargs={
            'direktori':direktori,
            'klasifikasi':klasifikasi,
            'pengadilan':pengadilan,
        })

    def parseTraverseTahun(self,response,direktori,klasifikasi,pengadilan):
        traverseTahun = set(response.xpath('//tbody/tr/td/a/@href').getall())
        self.tree[direktori][klasifikasi][pengadilan]["upload"] = list(traverseTahun)

        for tahun in list(traverseTahun):
            insert_data(table="tree_upload",data={
                "link_detail":tahun,
                "level":4,
                "tipe":"upload",
                "parent":pengadilan
            },key="link_detail")
    
        with open("crawl_populate.json","w") as f:
            f.write(json.dumps(self.tree))
        
        yield {
            "direktori":direktori,
            "klasifikasi":klasifikasi,
            "pengadilan":pengadilan,
            "upload":traverseTahun
        }

