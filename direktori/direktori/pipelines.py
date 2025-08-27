import re
import json
from datetime import datetime
from itemadapter import ItemAdapter
from scripts.utils import make_hash_id
from scripts.utils import convert_to_ymd
from db.utils import insert_data
class DeskripsiPutusanItemPipeline:
    def safe_retrieve(self, key,informasi=None, adapter=None):
        if informasi:
            return informasi[key] if key in informasi else ''
        elif adapter:
            return adapter[key] if key in adapter else ''
        else:
            return ''
        
    def process_item(self, item, spider):
        print("===PIPE===")
        adapter = ItemAdapter(item)
        informasi = adapter["description"]
        adapter["link_detail"] = adapter["url"]
        adapter["hash_id"] = make_hash_id(informasi.get("nomor"))
        adapter["timestamp"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # change to date type
        DATE_KEYS = ("tanggal_register", "tanggal_dibacakan", "tanggal_musyawarah")
        for k in DATE_KEYS:
            v = informasi.get(k)
            if v:
                informasi[k] = convert_to_ymd(v)
        
        # remove em dash
        for k in informasi.values():
            v = informasi.get(k)
            if v:
                informasi[k]=re.sub(r'—', '', v)

        insert_data(
            table="informasi_putusan",
            data={
                "hash_id":  self.safe_retrieve("hash_id",adapter=adapter),
                "link_detail":  self.safe_retrieve("url",adapter=adapter),
                "timestamp":  self.safe_retrieve("timestamp",adapter=adapter),
                "nomor": self.safe_retrieve("nomor",informasi=informasi),
                "tahun_putusan": self.safe_retrieve("tahun_putusan",informasi=informasi),
                "tingkat_proses": self.safe_retrieve("tingkat_proses",informasi=informasi),
                "jenis_lembaga_peradilan": self.safe_retrieve("jenis_lembaga_peradilan",informasi=informasi),
                "lembaga_peradilan": self.safe_retrieve("lembaga_peradilan",informasi=informasi),
                "klasifikasi": self.safe_retrieve("klasifikasi",informasi=informasi),
                "kaidah": self.safe_retrieve("kaidah",informasi=informasi),
                "kata_kunci": self.safe_retrieve("kata_kunci",informasi=informasi),
                "abstrak": self.safe_retrieve("abstrak",informasi=informasi),
                "amar": self.safe_retrieve("amar",informasi=informasi),
                "catatan_amar": self.safe_retrieve("catatan_amar",informasi=informasi),
                "hakim_ketua": self.safe_retrieve("hakim_ketua",informasi=informasi),
                "hakim_anggota": self.safe_retrieve("hakim_anggota",informasi=informasi),
                "panitera": self.safe_retrieve("panitera",informasi=informasi),
                "tanggal_register": self.safe_retrieve("tanggal_register",informasi=informasi),
                "tanggal_musyawarah": self.safe_retrieve("tanggal_musyawarah",informasi=informasi),
                "tanggal_dibacakan": self.safe_retrieve("tanggal_dibacakan",informasi=informasi),
                "jumlah_download": self.safe_retrieve("jumlah_download",informasi=informasi),
                "jumlah_view": self.safe_retrieve("jumlah_view",informasi=informasi),
                "link_pdf": self.safe_retrieve("link_pdf",informasi=informasi),
                "link_zip": self.safe_retrieve("link_zip",informasi=informasi),
                "putusan": str(self.safe_retrieve("link_zip",informasi=informasi)),
            },
            key="hash_id"
        )

        putusan_terkait = adapter["putusan_terkait"]
        insert_data(table="putusan_terkait",
                    data={
                        "pertama":putusan_terkait.get("pertama"),
                        "banding":putusan_terkait.get("banding"),
                        "kasasi":putusan_terkait.get("kasasi"),
                        "peninjauan_kembali":putusan_terkait.get("peninjauan_kembali"),
                        "link_pertama":putusan_terkait.get("link_pertama"),
                        "link_banding":putusan_terkait.get("link_banding"),
                        "link_kasasi":putusan_terkait.get("link_kasasi"),
                        "link_peninjauan_kembali":putusan_terkait.get("link_peninjauan_kembali")
                    },
                    key="kasasi")
        return dict(adapter)
    
    