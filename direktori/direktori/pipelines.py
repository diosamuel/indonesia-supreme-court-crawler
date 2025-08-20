import re
from datetime import datetime
from itemadapter import ItemAdapter
from scripts.utils import make_hash_id
from scripts.utils import convert_to_ymd

class DeskripsiPutusanItemPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        desc = adapter["description"]
        adapter["link_detail"] = adapter["url"]
        adapter["hash_id"] = make_hash_id(desc.get("nomor") or adapter["nomor"])
        adapter["timestamp"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        DATE_KEYS = ("tanggal_register", "tanggal_dibacakan", "tanggal_musyawarah")
        for k in DATE_KEYS:
            v = desc.get(k)
            if v:
                desc[k] = convert_to_ymd(v)
        
        for k in desc.values():
            v = desc.get(k)
            if v:
                desc[k]=re.sub(r'—', '', v)

        # insertPutusan(adapter)
        return dict(adapter)
    
    