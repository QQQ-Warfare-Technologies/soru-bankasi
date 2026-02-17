import sqlite3
import json
import os
from pathlib import Path


class DatabaseManager:
    def __init__(self, db_name="sorubankasi.db"):

        self.appdata_klasoru = Path(os.getenv('LOCALAPPDATA')) / "SoruBankasi"
        self.resim_klasoru = self.appdata_klasoru / "resimler"
        self.appdata_klasoru.mkdir(parents=True, exist_ok=True)
        self.resim_klasoru.mkdir(parents=True, exist_ok=True)

        self.db_path = self.config_db_path(db_name)

        self.init_db()

    def config_db_path(self, db_name):
        
        kullanici_db_yolu = self.appdata_klasoru / db_name
        return str(kullanici_db_yolu)

    def get_connection(self):
        """Veritabanı bağlantısı oluşturur ve Foreign Key desteğini açar."""
        # timeout: Kilitli veritabanı için bekleme süresi (saniye)
        # check_same_thread: Farklı thread'lerden erişime izin ver
        conn = sqlite3.connect(self.db_path, timeout=10,
                               check_same_thread=False)
        # Verilere isimle erişmek için (row['ad'] gibi)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        # İlişkisel bütünlük için şart (her bağlantıda gerekli, varsayılan OFF)
        cursor.execute("PRAGMA foreign_keys = ON")
        return conn

    def init_db(self):
        """Tabloları oluşturur ve WAL modunu ayarlar."""
        conn = self.get_connection()
        cursor = conn.cursor()

        # WAL modu: Kalıcı ayar, bir kere çalıştırmak yeterli
        cursor.execute("PRAGMA journal_mode = WAL")

        # 1. Tablo: Dersler
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dersler (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ad TEXT NOT NULL UNIQUE
            )
        """)

        # 2. Tablo: Alt Konular (Derslere bağlı)
        # ders_id + ad kombinasyonu unique: Aynı derste aynı isimli konu olamaz
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alt_konular (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ders_id INTEGER,
                ad TEXT NOT NULL,
                FOREIGN KEY (ders_id) REFERENCES dersler (id) ON DELETE CASCADE,
                UNIQUE(ders_id, ad)
            )
        """)

        # 3. Tablo: Sorular (Resim ve Şıklar burada)
        # resim_adi: Sadece dosya ismi (örn: 'soru101.png'). Null olabilir.
        # siklar_json: '{"A": "5", "B": "10"}' formatında metin.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sorular (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metin TEXT NOT NULL,
                siklar_json TEXT NOT NULL,
                dogru_cevap TEXT NOT NULL,
                resim_adi TEXT
            )
        """)

        # 4. Tablo: İlişkiler (Junction Table)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS soru_konu_iliskisi (
                soru_id INTEGER,
                alt_konu_id INTEGER,
                PRIMARY KEY (soru_id, alt_konu_id),
                FOREIGN KEY (soru_id) REFERENCES sorular (id) ON DELETE CASCADE,
                FOREIGN KEY (alt_konu_id) REFERENCES alt_konular (id) ON DELETE CASCADE
            )
        """)

        # 5. Tablo: Sınavlar
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sinavlar (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ad TEXT NOT NULL        -- Örn: "2026 Güz Vize Sınavı"
            )
        """)

        # 6. Tablo: Sınav-Sorular
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sinav_soru (
            sinav_id INTEGER,
            soru_id INTEGER,
            -- İki ID'nin birleşimi benzersiz olmalı (Aynı soruyu aynı sınava iki kere eklememek için)
            PRIMARY KEY (sinav_id, soru_id),
            
            -- Sınav veya Soru silinirse, bu köprüdeki kayıt da otomatik silinsin (Çöp kalmasın)
            FOREIGN KEY(sinav_id) REFERENCES sinavlar(id) ON DELETE CASCADE,
            FOREIGN KEY(soru_id) REFERENCES sorular(id) ON DELETE CASCADE
        )
        """)

        conn.commit()
        conn.close()

    def ders_ekle(self, ders_adi):
        """Yeni bir ders ekler."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO dersler (ad) VALUES (?)", (ders_adi,))
            conn.commit()

            return True
        except Exception as e:

            return False
        finally:
            conn.close()

    def alt_konu_ekle(self, ders_id, konu_adi):
        """Seçilen derse yeni bir alt konu ekler."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO alt_konular (ders_id, ad) VALUES (?, ?)", (ders_id, konu_adi))
            conn.commit()

            return True
        except Exception as e:

            return False
        finally:
            conn.close()

    def soru_ekle(self, metin, siklar_dict, dogru_cevap, resim_adi=None, alt_konu_idleri=[]):
        """
        Soruyu ve ilişkilerini veritabanına ekler.
        siklar_dict: Python sözlüğü olmalı -> {'A': 'Cevap1', 'B': 'Cevap2'}
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            # 1. Sözlüğü JSON metnine çevir (Türkçe karakter sorunu olmasın diye ensure_ascii=False)
            siklar_json = json.dumps(siklar_dict, ensure_ascii=False)

            # 2. Soruyu Ekle
            cursor.execute("""
                INSERT INTO sorular (metin, siklar_json, dogru_cevap, resim_adi) 
                VALUES (?, ?, ?, ?)
            """, (metin, siklar_json, dogru_cevap, resim_adi))

            yeni_soru_id = cursor.lastrowid

            # 3. İlişkileri Ekle (Hangi alt konulara ait?)
            for kid in alt_konu_idleri:
                cursor.execute("""
                    INSERT INTO soru_konu_iliskisi (soru_id, alt_konu_id) VALUES (?, ?)
                """, (yeni_soru_id, kid))

            conn.commit()

            return yeni_soru_id

        except Exception as e:
            conn.rollback()  # Hata olursa işlemi geri al

            return None
        finally:
            conn.close()

    def tum_dersleri_getir(self):
        """Ders listesini döndürür."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM dersler ORDER BY ad ASC")
        sonuclar = cursor.fetchall()  # Liste içinde sözlük gibi döner
        conn.close()
        return sonuclar

    def konulari_getir_by_ders_id(self, ders_id):
        """Verilen derse ait alt konuları döndürür."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM alt_konular WHERE ders_id = ? ORDER BY ad ASC", (ders_id,))
        sonuclar = cursor.fetchall()
        conn.close()
        return sonuclar

    def sorulari_getir_filtreli(self, konu_id_listesi):
        """
        Verilen alt_konu_id listesine ait soruları getirir.
        Örn: konu_id_listesi = [1, 5, 8]
        """
        if not konu_id_listesi:
            return []  # Liste boşsa boş dön

        conn = self.get_connection()
        cursor = conn.cursor()

        # SQL'de dinamik olarak (?, ?, ?) yapısını oluşturuyoruz
        soru_isaretleri = ','.join(['?'] * len(konu_id_listesi))

        # DISTINCT kullanıyoruz ki bir soru iki farklı konuda varsa tabloda iki kere çıkmasın
        sorgu = f"""
        SELECT DISTINCT s.id, s.metin, s.siklar_json, s.dogru_cevap, s.resim_adi 
        FROM sorular s
        JOIN soru_konu_iliskisi ski ON s.id = ski.soru_id
        WHERE ski.alt_konu_id IN ({soru_isaretleri})
        ORDER BY s.id ASC
        """

        cursor.execute(sorgu, konu_id_listesi)
        sonuclar = cursor.fetchall()
        conn.close()
        return sonuclar

    def konu_var_mi(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        sorgu = f"""
        SELECT 1 WHERE EXISTS (SELECT 1 FROM alt_konular);
        """
        cursor.execute(sorgu)
        sonuclar = cursor.fetchall()
        conn.close()
        return sonuclar

    def konuya_ait_soru_sayisi(self, konu_id):
        """Bir konuya bağlı kaç soru olduğunu sayar."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM soru_konu_iliskisi WHERE alt_konu_id = ?", (konu_id,))
        sayi = cursor.fetchone()[0]
        conn.close()
        return sayi

    def konuyu_sil(self, konu_id):
        """Konuyu ve ilişkilerini siler (Sorulara dokunmaz)."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            # 1. İlişkileri sil (Bağları kopar)
            cursor.execute(
                "DELETE FROM soru_konu_iliskisi WHERE alt_konu_id = ?", (konu_id,))

            # 2. Konuyu sil
            cursor.execute("DELETE FROM alt_konular WHERE id = ?", (konu_id,))

            conn.commit()
            return True
        except Exception as e:

            return False
        finally:
            conn.close()

    def dersi_sil(self, ders_id):
        """
        Dersi ve ona bağlı tüm alt konuları siler.
        NOT: Sorular silinmez, sadece bu dersten boşa çıkar (Kategorisiz kalır).
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            # 1. Önce bu derse ait alt konuların ID'lerini bulalım
            cursor.execute(
                "SELECT id FROM alt_konular WHERE ders_id = ?", (ders_id,))
            konu_idleri = [row[0] for row in cursor.fetchall()]

            if konu_idleri:
                # 2. Bu konulara ait soru ilişkilerini temizle (soru_konu_iliskisi tablosundan)
                # (SQL'de liste vermek için dinamik soru işareti oluşturuyoruz)
                placeholder = ','.join('?' for _ in konu_idleri)
                cursor.execute(
                    f"DELETE FROM soru_konu_iliskisi WHERE alt_konu_id IN ({placeholder})", konu_idleri)

                # 3. Alt konuları sil
                cursor.execute(
                    "DELETE FROM alt_konular WHERE ders_id = ?", (ders_id,))

            # 4. En son Dersi sil
            cursor.execute("DELETE FROM dersler WHERE id = ?", (ders_id,))

            conn.commit()
            return True
        except Exception as e:

            return False
        finally:
            conn.close()

    def derse_ait_konu_sayisi(self, ders_id):
        """Uyarı mesajı için alt konu sayısını getirir."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM alt_konular WHERE ders_id = ?", (ders_id,))
        sayi = cursor.fetchone()[0]
        conn.close()
        return sayi

    def coklu_soru_sil(self, id_listesi):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            # SQL: DELETE FROM sorular WHERE id IN (1, 5, 8)
            placeholder = ','.join('?' for _ in id_listesi)
            cursor.execute(
                f"DELETE FROM sorular WHERE id IN ({placeholder})", id_listesi)

            # İlişki tablosundan da temizlemeyi unutma (Eğer CASCADE yoksa)
            cursor.execute(
                f"DELETE FROM soru_konu_iliskisi WHERE soru_id IN ({placeholder})", id_listesi)

            conn.commit()
            return True
        except Exception as e:

            return False
        finally:
            conn.close()

    def soru_guncelle(self, soru_id, metin, siklar_dict, dogru_cevap, alt_konu_idleri, resim_adi):
        """Mevcut bir soruyu ve konu ilişkilerini günceller."""
        import json
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            # 1. Sorunun metnini ve şıklarını güncelle
            siklar_json = json.dumps(siklar_dict, ensure_ascii=False)
            cursor.execute("""
                UPDATE sorular 
                SET metin = ?, siklar_json = ?, dogru_cevap = ?, resim_adi = ?
                WHERE id = ?
            """, (metin, siklar_json, dogru_cevap, resim_adi, soru_id))

            # 2. İLİŞKİLERİ GÜNCELLE (Strateji: Eskileri sil, yenileri ekle)
            # A. Önce bu soruya ait eski tüm konu bağlarını kopar
            cursor.execute(
                "DELETE FROM soru_konu_iliskisi WHERE soru_id = ?", (soru_id,))

            # B. Yeni seçilen konuları ekle
            for kid in alt_konu_idleri:
                cursor.execute(
                    "INSERT INTO soru_konu_iliskisi (soru_id, alt_konu_id) VALUES (?, ?)", (soru_id, kid))

            conn.commit()

            return True
        except Exception as e:

            conn.rollback()
            return False
        finally:
            conn.close()

    def soru_detay_getir(self, soru_id):
        """Düzenleme ekranını doldurmak için tek bir sorunun tüm detaylarını ve bağlı olduğu konuları getirir."""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Soru Bilgileri
        cursor.execute("SELECT * FROM sorular WHERE id = ?", (soru_id,))
        soru = cursor.fetchone()  # Row nesnesi döner

        # Bağlı olduğu Konu ID'leri
        cursor.execute(
            "SELECT alt_konu_id FROM soru_konu_iliskisi WHERE soru_id = ?", (soru_id,))
        konu_idleri = [row[0] for row in cursor.fetchall()]

        conn.close()
        return dict(soru), konu_idleri

    def sinav_ekle(self, sinav_adi):
        """Kullanıcının girdiği isimle yeni bir sınav kaydı oluşturur."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            # Sınav oluşturulma tarihini sistemden otomatik alıyoruz (Örn: 2026-02-15)

            # SQL Sorgusu: ID otomatik artar, biz sadece ad ve tarihi göndeririz
            cursor.execute("""
                INSERT INTO sinavlar (ad) 
                VALUES (?)
            """, [sinav_adi])

            conn.commit()
            
            return True

        except Exception as e:
           
            return False
        finally:
            conn.close()

    def tum_sinavlari_getir(self):
        """Kayıtlı tüm sınavları en yeni en üstte olacak şekilde getirir."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            # ORDER BY id DESC ile en son eklenen sınavı listenin en başına alıyoruz
            cursor.execute(
                "SELECT id, ad FROM sinavlar ORDER BY id DESC")
            kayitlar = cursor.fetchall()

            sinavlar = []
          
            for kayit in kayitlar:
                sinavlar.append({
                    'id': kayit[0],
                    'ad': kayit[1]
                })
            conn.close()
            return sinavlar

        except Exception as e:
         
            return []

    def sinav_sorularini_getir(self, sinav_id):
        """Belirli bir sınava ait tüm soruları güvenli bir şekilde getirir."""
        # Bağlantıyı her seferinde taze açıyoruz
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            sorgu = """
                SELECT s.id, s.metin, s.siklar_json, s.resim_adi
                FROM sorular s
                JOIN sinav_soru ss ON s.id = ss.soru_id
                WHERE ss.sinav_id = ?
                ORDER BY ss.rowid ASC -- Eklenme sırasına göre getirir
            """
            cursor.execute(sorgu, (sinav_id,))
            sonuclar = cursor.fetchall()
            return sonuclar
        except Exception as e:
           
            return []
        finally:
            # Bağlantıyı işimiz bitince kapatıyoruz ki 'leak' olmasın
            conn.close()

    def sinav_sorularini_kaydet(self, sinav_id, soru_id_listesi):
        """Sınav ve sorular arasındaki ilişkiyi toplu olarak (Batch) kaydeder."""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            # 1. Önce bu sınavın mevcut (eski) tüm ilişkilerini sil (Temiz bir sayfa)
            cursor.execute(
                "DELETE FROM sinav_soru WHERE sinav_id = ?", (sinav_id,))

            # 2. Yeni listeyi hazırla: [(sinav_id, soru_id1), (sinav_id, soru_id2), ...]
            kayit_verisi = [(sinav_id, soru_id) for soru_id in soru_id_listesi]

            # 3. TOPLU EKLEME (executemany milisaniyeler sürer)
            cursor.executemany("""
                INSERT INTO sinav_soru (sinav_id, soru_id) 
                VALUES (?, ?)
            """, kayit_verisi)

            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
          
            return False
        finally:
            conn.close()

    def sinav_veritabanindan_sil(self, sinav_id):
        """Belirtilen ID'ye sahip sınavı ve tüm ilişkilerini siler."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            # Sınavı sil (CASCADE sayesinde sinav_soru tablosu otomatik temizlenir)
            cursor.execute("DELETE FROM sinavlar WHERE id = ?", (sinav_id,))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            
            return False
        finally:
            conn.close()