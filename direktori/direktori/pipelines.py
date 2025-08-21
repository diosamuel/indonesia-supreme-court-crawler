import re
import json
from datetime import datetime
from itemadapter import ItemAdapter
from scripts.utils import make_hash_id
from scripts.utils import convert_to_ymd
from db.utils import insert_data
class DeskripsiPutusanItemPipeline:
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
                "hash_id": adapter["hash_id"],
                "link_detail": adapter["url"],
                "timestamp":adapter["timestamp"],
                "nomor": informasi["nomor"],
                "tahun_putusan": informasi["tahun_putusan"],
                "tingkat_proses": informasi["tingkat_proses"],
                "jenis_lembaga_peradilan": informasi["jenis_lembaga_peradilan"],
                "lembaga_peradilan": informasi["lembaga_peradilan"],
                "klasifikasi": informasi["klasifikasi"],
                "kaidah": informasi["kaidah"],
                "kata_kunci": informasi["kata_kunci"],
                "abstrak": informasi["abstrak"],
                "amar": informasi["amar"],
                "catatan_amar": informasi["catatan_amar"],
                "hakim_ketua": informasi["hakim_ketua"],
                "hakim_anggota": informasi["hakim_anggota"],
                "panitera": informasi["panitera"],
                "tanggal_register": informasi["tanggal_register"],
                "tanggal_musyawarah": informasi["tanggal_musyawarah"],
                "tanggal_dibacakan": informasi["tanggal_dibacakan"],
                "jumlah_download": informasi["jumlah_download"],
                "jumlah_view": informasi["jumlah_view"],
                "link_pdf": informasi["link_pdf"],
                "link_zip": informasi["link_zip"],
                "putusan": str(informasi["putusan_terkait"]),
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
    
    