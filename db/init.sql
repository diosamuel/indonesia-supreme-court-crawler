-- ============================================================
-- Database
-- ============================================================
CREATE DATABASE IF NOT EXISTS putusan;

USE putusan;

-- ============================================================
-- TABEL: informasi_putusan
-- Catatan: PK konseptual = hash_id (ClickHouse pakai ORDER BY)
-- ============================================================
CREATE TABLE IF NOT EXISTS informasi_putusan (
    hash_id String,                              -- PK (konseptual, tetap wajib)
    nomor Nullable(Int32),
    link_detail Nullable(String),
    tingkat_proses Nullable(String),
    klasifikasi Nullable(String),
    kata_kunci Nullable(String),
    lembaga_peradilan Nullable(String),
    jenis_lembaga_peradilan Nullable(String),
    hakim_ketua Nullable(String),
    hakim_anggota Nullable(String),
    panitera Nullable(String),
    amar Nullable(String),
    amar_lainnya Nullable(String),
    catatan_amar Nullable(String),
    kaidah Nullable(String),
    abstrak Nullable(String),
    putusan Nullable(String),
    tahun_putusan Nullable(Int32),
    tanggal_register Nullable(String),
    tanggal_musyawarah Nullable(String),
    tanggal_dibacakan Nullable(String),
    jumlah_view Nullable(Int32),
    jumlah_download Nullable(Int32),
    link_zip Nullable(String),
    link_pdf Nullable(String),
    timestamp Nullable(String)
)
ENGINE = MergeTree
ORDER BY hash_id;

-- ============================================================
-- TABEL: putusan_terkait
-- Ref: putusan_terkait.hash_id -> informasi_putusan.hash_id (non-enforced)
-- ============================================================
CREATE TABLE IF NOT EXISTS putusan_terkait (
    id UUID DEFAULT generateUUIDv4(),
    pertama Nullable(String),
    banding Nullable(String),
    kasasi Nullable(String),
    peninjauan_kembali Nullable(String),
    link_pertama Nullable(String),
    link_banding Nullable(String),
    link_kasasi Nullable(String),
    link_peninjauan_kembali Nullable(String)
)
ENGINE = MergeTree
ORDER BY id;

-- ============================================================
-- TABEL: list_putusan
-- Ref: list_putusan.hash_id -> informasi_putusan.hash_id (non-enforced)
-- ============================================================
CREATE TABLE IF NOT EXISTS list_putusan (
    upload Nullable(Date),
    link_detail Nullable(String),
    nomor Nullable(String),
    timestamp Nullable(String)
)
ENGINE = MergeTree
ORDER BY (nomor, upload);

-- ============================================================
-- TABEL: ekstraksi_pdf
-- Ref: ekstraksi_pdf.hash_id -> informasi_putusan.hash_id (non-enforced)
-- ============================================================
CREATE TABLE IF NOT EXISTS ekstraksi_pdf (
    hash_id String,        -- PK (konseptual)
    link_pdf Nullable(String),
    peran_pihak Nullable(String),
    tempat_lahir Nullable(String),
    tanggal_lahir Nullable(String),
    usia Nullable(Int32),
    jenis_kelamin Nullable(String),
    pekerjaan Nullable(String),
    agama Nullable(String),
    nomor_ktp Nullable(String),
    nomor_kk Nullable(String),
    nomor_akta_kelahiran Nullable(String),
    nomor_paspor Nullable(String)
)
ENGINE = MergeTree
ORDER BY hash_id;
