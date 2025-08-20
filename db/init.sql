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
    hash_id String,                -- PK (konseptual)
    nomor Int32,
    link_detail String,
    tingkat_proses String,
    klasifikasi String,
    kata_kunci String,
    lembaga_peradilan String,
    jenis_lembaga_peradilan String,
    hakim_ketua String,
    hakim_anggota String,
    panitera String,
    amar String,
    amar_lainnya String,
    catatan_amar String,
    kaidah String,
    abstrak String,
    putusan String,
    tahun_putusan Int32,
    tanggal_register Date,
    tanggal_musyawarah Date,
    tanggal_dibacakan Date,
    jumlah_view Int32,
    jumlah_download Int32,
    link_zip String,
    link_pdf String,
    timestamp Date
)
ENGINE = MergeTree
ORDER BY hash_id;

-- ============================================================
-- TABEL: putusan_terkait
-- Ref: putusan_terkait.hash_id -> informasi_putusan.hash_id (non-enforced)
-- ============================================================
CREATE TABLE IF NOT EXISTS putusan_terkait (
    hash_id String,   -- PK (konseptual)
    pertama String,
    banding String,
    kasasi String,
    peninjauan_kembali String
)
ENGINE = MergeTree
ORDER BY hash_id;

-- ============================================================
-- TABEL: list_putusan
-- Ref: list_putusan.hash_id -> informasi_putusan.hash_id (non-enforced)
-- ============================================================
CREATE TABLE IF NOT EXISTS list_putusan (
    hash_id String,   -- PK (konseptual)
    upload Date,
    link_detail String,
    nomor String,
    timestamp String
)
ENGINE = MergeTree
ORDER BY (nomor, upload);

-- ============================================================
-- TABEL: ekstraksi_pdf
-- Ref: ekstraksi_pdf.hash_id -> informasi_putusan.hash_id (non-enforced)
-- ============================================================
CREATE TABLE IF NOT EXISTS ekstraksi_pdf (
    hash_id String,   -- PK (konseptual)
    link_pdf String,
    peran_pihak String,
    tempat_lahir String,
    tanggal_lahir String,
    usia Int32,
    jenis_kelamin String,
    pekerjaan String,
    agama String,
    nomor_ktp String,
    nomor_kk String,
    nomor_akta_kelahiran String,
    nomor_paspor String
)
ENGINE = MergeTree
ORDER BY hash_id;

-- ============================================================
-- (Opsional) Indeks/Tuning bisa ditambahkan nanti sesuai kebutuhan query
-- ============================================================
