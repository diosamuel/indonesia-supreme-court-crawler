import scrapy
# ==========================
# Tabel: list_putusan
# ==========================
class PutusanItem(scrapy.Item):
    hash_id = scrapy.Field()       
    upload = scrapy.Field()        
    link_detail = scrapy.Field()   
    nomor = scrapy.Field()         
    timestamp = scrapy.Field()     

# ==========================
# Tabel: informasi_putusan
# ==========================

class DeskripsiPutusanItem(scrapy.Item):
    hash_id = scrapy.Field()                 
    nomor = scrapy.Field()                   
    link_detail = scrapy.Field()             
    tingkat_proses = scrapy.Field()          
    klasifikasi = scrapy.Field()             
    kata_kunci = scrapy.Field()              
    lembaga_peradilan = scrapy.Field()       
    jenis_lembaga_peradilan = scrapy.Field() 
    hakim_ketua = scrapy.Field()             
    hakim_anggota = scrapy.Field()           
    panitera = scrapy.Field()                
    amar = scrapy.Field()                    
    amar_lainnya = scrapy.Field()            
    catatan_amar = scrapy.Field()            
    kaidah = scrapy.Field()                  
    abstrak = scrapy.Field()                 
    putusan_terkait = scrapy.Field()                 
    tahun_putusan = scrapy.Field()           
    tanggal_register = scrapy.Field()        
    tanggal_musyawarah = scrapy.Field()      
    tanggal_dibacakan = scrapy.Field()       
    jumlah_view = scrapy.Field()             
    jumlah_download = scrapy.Field()         
    link_zip = scrapy.Field()                
    link_pdf = scrapy.Field()                
    timestamp = scrapy.Field()               

# ==========================
# Tabel: putusan_terkait
# ==========================
class PutusanTerkaitItem(scrapy.Item):
    hash_id = scrapy.Field()             
    pertama = scrapy.Field()             
    banding = scrapy.Field()             
    kasasi = scrapy.Field()              
    peninjauan_kembali = scrapy.Field()  

# ==========================
# Tabel: ekstraksi_pdf
# ==========================
class EkstraksiPDFItem(scrapy.Item):
    hash_id = scrapy.Field()                
    link_pdf = scrapy.Field()               
    peran_pihak = scrapy.Field()            
    tempat_lahir = scrapy.Field()           
    tanggal_lahir = scrapy.Field()          
    usia = scrapy.Field()                   
    jenis_kelamin = scrapy.Field()          
    pekerjaan = scrapy.Field()              
    agama = scrapy.Field()                  
    nomor_ktp = scrapy.Field()              
    nomor_kk = scrapy.Field()               
    nomor_akta_kelahiran = scrapy.Field()   
    nomor_paspor = scrapy.Field()           
