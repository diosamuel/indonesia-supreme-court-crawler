import clickhouse_connect
import datetime
import json
import logging
import datetime
import os
from dotenv import load_dotenv
load_dotenv()

client = clickhouse_connect.get_client(
    host=os.getenv("CLICKHOUSE_HOST", "localhost"),
    username=os.getenv("CLICKHOUSE_USER", "default"),
    password=os.getenv("CLICKHOUSE_PASSWORD", "default"),
    port=os.getenv("CLICKHOUSE_HTTP_PORT", "8123")
)

def insert_data(data, table, columns):
    try:
        data["upload"] = datetime.datetime.strptime(data["upload"], "%Y-%m-%d").date()
        check_dup = client.query(f"""
            SELECT count(*) from {table} where hash_id = '{data["hash_id"]}'
        """)
        if check_dup.result_rows[0][0] >= 1:
            logging.warning(f"Duplicate {data['hash_id']}, Skip")
        else:
            insertedData = [list(data.values())]
            client.insert(table, insertedData, column_names=columns)
            logging.info(f"Successfully insert {data['hash_id']}")
    except Exception as e:
        logging.error(e)


def retrieve_data(column,table):
    try:
        retrieve = client.query(f"SELECT {column} from {table}")
        return retrieve
    except Exception as e:
        logging.error(e)

def insertPutusan(scraped_json):
    desc = scraped_json.get('description', {})
    DEFAULT_DATE = datetime.date(1970, 1, 1)

    def safeDate(date_str):
        if not date_str:
            return DEFAULT_DATE
        try:
            return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except Exception:
            return DEFAULT_DATE
    def safeStr(val):
        return val if (val is not None and isinstance(val, str)) else ''
    
    data = {
        'link_detail':scraped_json.get('url'),
        'update_at':datetime.datetime.now().strftime("%c"),
        'hash_id': safeStr(scraped_json.get('hash_id')),
        'nomor': safeStr(desc.get('nomor')),
        'tingkat_proses': safeStr(desc.get('tingkat_proses')),
        'klasifikasi': safeStr(desc.get('klasifikasi')),
        'kata_kunci': safeStr(desc.get('kata_kunci')),
        'tahun': int(desc.get('tahun')) if desc.get('tahun') else None,
        'tanggal_register': safeDate(desc.get('tanggal_register')),
        'lembaga_peradilan': safeStr(desc.get('lembaga_peradilan')),
        'jenis_lembaga_peradilan': safeStr(desc.get('jenis_lembaga_peradilan')),
        'hakim_ketua': safeStr(desc.get('hakim_ketua')),
        'hakim_anggota': safeStr(desc.get('hakim_anggota')),
        'panitera': safeStr(desc.get('panitera')),
        'amar': safeStr(desc.get('amar')),
        'amar_lainnya': safeStr(desc.get('amar_lainnya')),
        'catatan_amar': safeStr(desc.get('catatan_amar')),
        'kaidah': safeStr(desc.get('kaidah')),
        'abstrak': safeStr(desc.get('abstrak')),
        'putusan': json.dumps(desc.get('putusan', {})),
        'view': int(desc.get('view')) if desc.get('view') else 0,
        'download': int(desc.get('download')) if desc.get('download') else 0,
        'zip': safeStr(desc.get('zip')),
        'pdf': safeStr(desc.get('pdf')),
        'tanggal_musyawarah': safeDate(desc.get('tanggal_musyawarah')),
        'tanggal_dibacakan': safeDate(desc.get('tanggal_dibacakan')),
    }
    check_dup = client.query(f"""
        SELECT count(*) from informasi_putusan where hash_id = '{data["hash_id"]}'
    """)
    if check_dup.result_rows[0][0] >= 1:
        logging.warning(f"Skip {data['hash_id']}")
    else:
        client.insert("informasi_putusan", [list(data.values())], column_names=list(data.keys()))
        logging.warning(f"Success Insert {data['hash_id']}")