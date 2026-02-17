from PySide6.QtWidgets import QMainWindow, QTreeWidgetItem, QTableWidgetItem, QHeaderView, QMessageBox, QAbstractItemView, QMenu, QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence, QShortcut, QCursor, QPixmap
from PySide6.QtCore import QTimer, QMimeData
from ui.forms.add_course import AddCourseDialog
from ui.forms.add_topic import AddTopicDialog
from ui.forms.add_question import AddQuestionDialog
from ui.forms.manage_exams import ManageExamsDialog
from ui.main_window_ui import Ui_MainWindow
from database.db_manager import DatabaseManager
import json
from pathlib import Path
import os
import base64
import shutil


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 1. Arayüzü Yükle
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("SORU BANKASI")
        # 2. Veritabanını Başlat
        self.db = DatabaseManager()
        self.tablo_ayarlari()
        # 3. Sol Menüyü Doldur (Program açılınca çalışsın)
        self.sol_menuyu_yukle()
        self.ui.actionRes_temizle.triggered.connect(
            self.gereksiz_resimleri_temizle)
        self.ui.actionDb_sifirla.triggered.connect(self.database_sil)
        self.ui.tree_konular.itemChanged.connect(self.tabloyu_guncelle)
        self.ui.tree_konular.itemClicked.connect(self.tree_item_tiklandi)
        self.ui.btn_yeni_ders.clicked.connect(self.yeni_ders_penceresini_ac)
        self.ui.btn_yeni_konu.clicked.connect(self.yeni_konu_penceresini_ac)
        self.ui.btn_yeni_soru.clicked.connect(self.yeni_soru_penceresini_ac)
        self.ui.btn_sinav_hazirla.clicked.connect(
            self.sinav_hazirla_penceresini_ac)
        self.ui.table_sorular.cellClicked.connect(
            self.satir_tiklandi)
        self.ui.tree_konular.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.tree_konular.customContextMenuRequested.connect(
            self.sag_tik_menu_ac)
        self.ui.btn_soru_sil.clicked.connect(self.sorulari_sil_tiklandi)
        self.shortcut_delete = QShortcut(
            QKeySequence("Delete"), self.ui.table_sorular)
        self.shortcut_delete.activated.connect(self.sorulari_sil_tiklandi)
        self.ui.btn_soru_kopyala.clicked.connect(self.soruyu_kopyala)
        self.ui.btn_soru_duzenle.clicked.connect(self.soru_duzenle_tiklandi)

    def tablo_ayarlari(self):
        # 4 Sütun olacağını sisteme bildiriyoruz
        basliklar = ["ID", "Soru Metni", "Şıklar", "Doğru Cevap"]
        self.ui.table_sorular.setColumnCount(len(basliklar))  # Burası 4 yapar
        self.ui.table_sorular.setHorizontalHeaderLabels(basliklar)

        # --- SÜTUN GENİŞLİK AYARLARI ---
        header = self.ui.table_sorular.horizontalHeader()

        # 1. Tüm sütunları "İnteraktif" yap (Kullanıcı fareyle değiştirebilsin)
        header.setSectionResizeMode(QHeaderView.Interactive)

        # 2. Başlangıç Genişliklerini Ayarla (Kullanıcı değiştirebilir ama ilk açılışta düzgün dursun)
        self.ui.table_sorular.setColumnHidden(0, True)

        # Soru Metni (Geniş olsun - Örn: 400 piksel)
        self.ui.table_sorular.setColumnWidth(1, 450)

        # Şıklar (Orta genişlik)
        self.ui.table_sorular.setColumnWidth(2, 250)

        # Doğru Cevap (Dar olsun)
        self.ui.table_sorular.setColumnWidth(3, 100)
        self.ui.table_sorular.setAlternatingRowColors(True)
        # 3. Son sütun, pencere büyürse boşluğu doldursun mu?
        # (Bunu True yaparsan son sütun sağa yapışır, False yaparsan boşluk kalır)
        header.setStretchLastSection(True)
        self.ui.table_sorular.setEditTriggers(
            QAbstractItemView.NoEditTriggers)  # Editlenemez yap
        # İpucu: Satırın tamamını seçtirmek için (Hücre değil, satır seçimi)
        self.ui.table_sorular.setSelectionBehavior(
            QAbstractItemView.SelectRows)

        # çoklu seçme mümkün
        self.ui.table_sorular.setSelectionMode(
            QAbstractItemView.ExtendedSelection)

    def sol_menuyu_yukle(self, hedef_agac=None):
        """Veritabanından dersleri ve konuları çekip belirtilen ağaca ekler."""

        # Eğer dışarıdan bir ağaç gönderilmezse, varsayılan olarak ana ekrandakini (tree_konular) kullan
        agac = hedef_agac if hedef_agac is not None else self.ui.tree_konular

        agac.blockSignals(True)  # Signal'leri geçici olarak kapat
        agac.clear()  # Önce temizle, üst üste binmesin

        # A. Dersleri Çek
        dersler = self.db.tum_dersleri_getir()

        for ders in dersler:
            # 1. Ana Dal (Ders) Oluştur -> Artık 'agac' değişkenini kullanıyoruz
            ders_item = QTreeWidgetItem(agac)
            ders_item.setText(0, ders['ad'])  # Ekranda görünen isim

            # GİZLİ VERİ SAKLAMA (ID'yi saklıyoruz)
            # 0. Sütuna, UserRole (Gizli bölme) içine ID'yi koy.
            ders_item.setData(0, Qt.ItemDataRole.UserRole, ders['id'])

            # Kutucuk (Checkbox) Ekle
            ders_item.setFlags(ders_item.flags(
            ) | Qt.ItemFlag.ItemIsAutoTristate | Qt.ItemFlag.ItemIsUserCheckable)
            ders_item.setCheckState(0, Qt.CheckState.Unchecked)

            # B. Bu dersin alt konularını çek
            konular = self.db.konulari_getir_by_ders_id(ders['id'])

            for konu in konular:
                # 2. Alt Dal (Konu) Oluştur -> Parent olarak 'ders_item' veriyoruz
                konu_item = QTreeWidgetItem(ders_item)
                konu_item.setText(0, konu['ad'])

                # Konu ID'sini gizle
                konu_item.setData(0, Qt.ItemDataRole.UserRole, konu['id'])

                # Kutucuk Ekle
                konu_item.setFlags(konu_item.flags() |
                                   Qt.ItemFlag.ItemIsUserCheckable)
                konu_item.setCheckState(0, Qt.CheckState.Unchecked)

            # (Opsiyonel) Ağacı açık halde göster
            ders_item.setExpanded(True)

        agac.blockSignals(False)  # Signal'leri tekrar aç

    def tree_item_tiklandi(self, item, column):
        """İsme tıklandığında checkbox durumunu değiştirir (Farklı ağaçlarda çalışabilir)."""

        # HARİKA Qt HİLESİ: Tıklanan item'ın hangi ağaca ait olduğunu kendisinden öğren!
        agac = item.treeWidget()

        # Artık 'self.ui.tree_konular' yerine bu dinamik 'agac' değişkenini kullanıyoruz
        fare_noktasi = agac.viewport().mapFromGlobal(QCursor.pos())

        # Bu sefer tüm satırın alanını alıyoruz (Kutu + Yazı)
        esya_alani = agac.visualItemRect(item)

        # Öğenin başlangıç X noktası (Yani kutunun en sol kenarı)
        baslangic_x = esya_alani.x()

        # KRİTİK KONTROL: Fare tıklaması, kutunun bitişinden (yaklaşık 25 piksel) daha sağda mı?
        # Eğer sağdaysa -> Yazıya tıklanmıştır. Biz işaretleyelim.
        # Eğer <= 25 ise -> Kutuya tıklanmıştır. Hiç dokunmayalım, Qt kendi işaretlesin.
        if fare_noktasi.x() > (baslangic_x + 25) or fare_noktasi.x() < (baslangic_x + 10):
            # Durumu tersine çevir
            if item.checkState(column) == Qt.CheckState.Checked:
                item.setCheckState(column, Qt.CheckState.Unchecked)
            else:
                item.setCheckState(column, Qt.CheckState.Checked)

    def tabloyu_guncelle(self):

        secili_id_listesi = []

        root = self.ui.tree_konular.invisibleRootItem()
        child_count = root.childCount()

        for i in range(child_count):
            ders_item = root.child(i)
            # Alt konuları gez
            for j in range(ders_item.childCount()):
                konu_item = ders_item.child(j)

                # CheckState kontrolü
                durum = konu_item.checkState(0)

                # Sadece işaretli olanları al
                if durum == Qt.CheckState.Checked:
                    k_id = konu_item.data(0, Qt.ItemDataRole.UserRole)

                    if k_id is not None:
                        secili_id_listesi.append(k_id)

        if not secili_id_listesi:

            self.ui.table_sorular.setRowCount(0)
            return

        sorular = self.db.sorulari_getir_filtreli(secili_id_listesi)

        self.ui.table_sorular.setRowCount(len(sorular))

        for satir_idx, soru in enumerate(sorular):
            self.ui.table_sorular.setItem(
                satir_idx, 0, QTableWidgetItem(str(soru['id'])))
            self.ui.table_sorular.setItem(
                satir_idx, 1, QTableWidgetItem(soru['metin']))

            try:
                siklar_dict = json.loads(soru['siklar_json'])
                # Görünüm: "A) Cevap1  B) Cevap2 ..."
                siklar_yazi = "  ".join(
                    [f"{k}) {v}" for k, v in siklar_dict.items()])
            except:
                siklar_yazi = "Şık verisi hatalı"

            self.ui.table_sorular.setItem(
                satir_idx, 2, QTableWidgetItem(siklar_yazi))

            # Doğru Cevap
            self.ui.table_sorular.setItem(
                satir_idx, 3, QTableWidgetItem(soru['dogru_cevap']))

    def yeni_ders_penceresini_ac(self):
        """Yeni ders ekleme penceresini açar. Hata durumunda tekrar dener."""
        while True:
            dialog = AddCourseDialog(self)

            # Kullanıcı iptal ettiyse çık
            if not dialog.exec():

                break

            yeni_isim = dialog.get_ders_adi()
            basarili = self.db.ders_ekle(yeni_isim)

            if basarili:
                QMessageBox.information(
                    self, "Başarılı", f"'{yeni_isim}' dersi eklendi.")
                self.sol_menuyu_yukle()
                # Döngü devam eder, yeni ders eklenebilir
            else:
                QMessageBox.critical(
                    self, "Hata", "Ders eklenirken bir sorun oluştu (İsim aynı olabilir).")
                # Döngü devam eder, dialog tekrar açılır

    def yeni_konu_penceresini_ac(self):
        """Yeni konu ekleme penceresini açar. Hata durumunda tekrar dener."""
        # Önce ders listesini kontrol et
        dersler = self.db.tum_dersleri_getir()

        if not dersler:
            QMessageBox.warning(
                self, "Uyarı", "Önce en az bir ders eklemelisiniz!")
            return

        secili_ders_id = None  # Son seçilen ders ID'sini takip et

        while True:
            # Dialog penceresini oluştur ve ders listesini gönder
            dialog = AddTopicDialog(dersler, secili_ders_id, self)

            # Kullanıcı iptal ettiyse çık
            if not dialog.exec():

                break

            # Kullanıcı 'Ekle' dediyse verileri al
            ders_id, konu_adi = dialog.get_data()
            secili_ders_id = ders_id  # Bir sonraki açılış için sakla

            # Veritabanına yaz
            basarili = self.db.alt_konu_ekle(ders_id, konu_adi)

            if basarili:
                QMessageBox.information(
                    self, "Başarılı", f"'{konu_adi}' konusu eklendi.")
                self.sol_menuyu_yukle()
                # Ders listesini güncelle (yeni ders eklenmiş olabilir)
                dersler = self.db.tum_dersleri_getir()
                # Döngü devam eder, yeni konu eklenebilir
            else:
                QMessageBox.critical(
                    self, "Hata", "Konu eklenirken bir sorun oluştu (Konu zaten mevcut olabilir).")
                # Döngü devam eder, dialog tekrar açılır

    def satir_tiklandi(self, row, column):
        """
        Tabloda bir satıra tıklandığında çalışır.
        row: Tıklanan satırın indeksi (0, 1, 2...)
        column: Tıklanan sütun (Bizim için önemsiz, satırdaki veriyi alacağız)
        """

        # Bizim tablomuzda:
        # 0. Sütun -> ID
        # 1. Sütun -> Soru Metni
        # 2. Sütun -> Şıklar
        # 3. Sütun -> Doğru Cevap

        soru_id_item = self.ui.table_sorular.item(row, 0)
        soru_item = self.ui.table_sorular.item(row, 1)
        siklar_item = self.ui.table_sorular.item(row, 2)
        cevap_item = self.ui.table_sorular.item(row, 3)

        if soru_item:
            soru_metni = soru_item.text()

            # Şıkları satır satır formatla
            siklar_text = ""
            if siklar_item:
                # Tablodaki format: "A) Cevap1  B) Cevap2 ..."
                # Bunu satır satır yapmak için split edelim
                siklar_raw = siklar_item.text()
                # "  " ile ayrılmış şıkları bul ve her birini yeni satıra koy
                siklar_parcalari = siklar_raw.split("  ")
                # Her şıkkı temizle (baştaki/sondaki boşlukları kaldır)
                siklar_parcalari = [s.strip()
                                    for s in siklar_parcalari if s.strip()]
                siklar_text = "\n".join(siklar_parcalari)
                cevap_text = "\nDoğru Cevap: " + cevap_item.text()
            # Text Area'ya soru + şıklar olarak yazdır
            tam_metin = f"{soru_metni}\n\n{siklar_text}\n{cevap_text}"
            self.ui.txt_soru_detay.setText(tam_metin)

            self.ui.lbl_resim_onizleme_main.clear()
            self.ui.lbl_resim_onizleme_main.setText(
                "SORU RESMİ")

            if soru_id_item:
                soru_id = int(soru_id_item.text())
                soru_data, _ = self.db.soru_detay_getir(soru_id)
                resim_adi = soru_data.get('resim_adi')
                if resim_adi:
                    appdata_klasoru = Path(
                        os.getenv('LOCALAPPDATA')) / "SoruBankasi" / "resimler"
                    resim_yolu = appdata_klasoru / resim_adi

                    # 4. Fiziksel olarak o dosya klasörde duruyor mu kontrol et
                    if resim_yolu.exists():
                        pixmap = QPixmap(str(resim_yolu))

                        # 5. Resmi Label'ın boyutlarına orantılı şekilde sığdır
                        sigdirilmis_pixmap = pixmap.scaled(
                            self.ui.lbl_resim_onizleme_main.size(),
                            Qt.AspectRatioMode.KeepAspectRatio,
                            Qt.TransformationMode.SmoothTransformation
                        )

                        self.ui.lbl_resim_onizleme_main.setPixmap(
                            sigdirilmis_pixmap)
                    else:
                        self.ui.lbl_resim_onizleme_main.setText(
                            "⚠️ Görsel dosyası kayıp!")

    def yeni_soru_penceresini_ac(self):
        konular = self.db.konu_var_mi()

        if not konular:
            QMessageBox.warning(
                self, "Uyarı", "Önce en az bir konu eklemelisiniz!")
            return

        while True:
            dialog = AddQuestionDialog(db_manager=self.db)

            # Kullanıcı iptal ettiyse çık
            if not dialog.exec():

                break

            # Dialog accept() ile kapandıysa (soru başarıyla eklendiyse)
            # Tabloyu güncelle ve döngüye devam et
            self.tabloyu_guncelle()

    def sinav_hazirla_penceresini_ac(self):
        # Dialog'u oluştururken veritabanı bağlantımızı (self.db) ona da gönderiyoruz
        dialog = ManageExamsDialog(self.db, self)
        dialog.exec()  # Pencereyi ekranda tut (Kapanana kadar arkaya tıklanmaz)

    def sag_tik_menu_ac(self, position):
        tiklanan_item = self.ui.tree_konular.itemAt(position)
        if not tiklanan_item:
            return

        # Öğe Ders mi Konu mu? (Parent'ı yoksa Derstir)
        is_konu = tiklanan_item.parent() is not None

        menu = QMenu()

        if is_konu:
            # --- KONU İŞLEMLERİ ---
            aksiyon_sil = menu.addAction("Bu Konuyu Sil")
            secilen_aksiyon = menu.exec(
                self.ui.tree_konular.mapToGlobal(position))

            if secilen_aksiyon == aksiyon_sil:
                self.konu_sil_onayi(tiklanan_item)

        else:
            # --- DERS İŞLEMLERİ ---
            aksiyon_ders_sil = menu.addAction("⚠️ Dersi ve Alt Konuları Sil")
            secilen_aksiyon = menu.exec(
                self.ui.tree_konular.mapToGlobal(position))

            if secilen_aksiyon == aksiyon_ders_sil:
                self.ders_sil_onayi(tiklanan_item)

    def konu_sil_onayi(self, item):
        konu_adi = item.text(0)
        konu_id = item.data(0, Qt.UserRole)  # Gizli ID'yi alıyoruz

        # 1. Bağlı soru sayısını kontrol et
        # (Bu fonksiyonu db_manager'a ekleyeceğiz, aşağıya bak)
        soru_sayisi = self.db.konuya_ait_soru_sayisi(konu_id)

        uyari_metni = f"'{konu_adi}' konusu silinecek."
        if soru_sayisi > 0:
            uyari_metni += f"\n\n⚠️ Bu konuya bağlı {soru_sayisi} adet soru var!\nSorular SİLİNMEYECEK, sadece 'Kategorisiz' kalacaklar."

        uyari_metni += "\n\nOnaylıyor musunuz?"

        cevap = QMessageBox.question(
            self, "Silme Onayı", uyari_metni,
            QMessageBox.Yes | QMessageBox.No
        )

        if cevap == QMessageBox.Yes:

            # Veritabanından sil
            if self.db.konuyu_sil(konu_id):
                QMessageBox.information(self, "Başarılı", "Konu silindi.")
                # Ağacı Yenile
                self.sol_menuyu_yukle()
                # Tabloyu Temizle
                self.ui.table_sorular.setRowCount(0)
            else:
                QMessageBox.critical(
                    self, "Hata", "Silme işlemi başarısız oldu.")

    def ders_sil_onayi(self, item):
        ders_adi = item.text(0)
        ders_id = item.data(0, Qt.UserRole)

        # Kaç konu gidecek?
        konu_sayisi = self.db.derse_ait_konu_sayisi(ders_id)

        # Korkutucu Uyarı Mesajı
        uyari_metni = (
            f"DİKKAT! '{ders_adi}' dersini silmek üzeresiniz.\n\n"
            f"Bu işlem sonucunda:\n"
            f"1. Bu derse ait {konu_sayisi} adet alt konu TAMAMEN SİLİNECEK.\n"
            f"2. Bu konulardaki sorular 'Kategorisiz' duruma düşecek.\n\n"
            f"Bu işlem geri alınamaz. Devam etmek istiyor musunuz?"
        )

        cevap = QMessageBox.question(
            self,
            "Ders Silme Onayı",
            uyari_metni,
            QMessageBox.Yes | QMessageBox.No
        )

        if cevap == QMessageBox.Yes:
            if self.db.dersi_sil(ders_id):
                QMessageBox.information(
                    self, "Bilgi", f"'{ders_adi}' ve tüm alt konuları silindi.")
                # Ekranları Yenile
                self.sol_menuyu_yukle()
                self.ui.table_sorular.setRowCount(0)
            else:
                QMessageBox.critical(
                    self, "Hata", "Ders silinirken bir sorun oluştu.")

    def sorulari_sil_tiklandi(self):
        # 1. Seçili satırları al (Model üzerinden indeksleri alıyoruz)
        secili_satirlar = self.ui.table_sorular.selectionModel().selectedRows()

        if not secili_satirlar:
            QMessageBox.warning(
                self, "Uyarı", "Lütfen silinecek soru(ları) seçiniz.")
            return

        # 2. Kullanıcıya ne sileceğini söyle (Dinamik Mesaj)
        soru_sayisi = len(secili_satirlar)
        mesaj = f"{soru_sayisi} adet soru silinecek.\nBu işlem geri alınamaz!"

        onay = QMessageBox.question(
            self, "Silme Onayı", mesaj, QMessageBox.Yes | QMessageBox.No)

        if onay == QMessageBox.No:
            return

        # 3. Seçili ID'leri topla
        silinecek_idler = []
        for index in secili_satirlar:
            # Tablomuzda ID 0. sütundaydı
            # row() satır numarasını verir, 0. sütundaki veriyi alacağız
            item = self.ui.table_sorular.item(index.row(), 0)
            if item:
                silinecek_idler.append(int(item.text()))

        # 4. Veritabanından Toplu Sil (Backend Fonksiyonu)
        # db_manager'a 'coklu_soru_sil' diye bir fonksiyon eklememiz gerekecek
        if self.db.coklu_soru_sil(silinecek_idler):
            QMessageBox.information(
                self, "Başarılı", "Seçilen sorular silindi.")

            # 5. Arayüzü güncelle (Filtreleme bozulmasın diye mevcut filtreyi tekrar çağır)
            self.tabloyu_guncelle()

            # Detay ekranını temizle
            self.ui.txt_soru_detay.clear()
        else:
            QMessageBox.critical(
                self, "Hata", "Silme işlemi sırasında bir sorun oluştu.")

    def soru_duzenle_tiklandi(self):
        # 1. Seçili satırı bul
        secili_satirlar = self.ui.table_sorular.selectionModel().selectedRows()

        if not secili_satirlar:
            QMessageBox.warning(
                self, "Uyarı", "Lütfen düzenlemek için bir soru seçiniz.")
            return

        if len(secili_satirlar) > 1:
            QMessageBox.warning(
                self, "Uyarı", "Aynı anda sadece bir soru düzenleyebilirsiniz.")
            return

        # 2. ID'yi al (0. sütun ID sütunumuzdu)
        row_index = secili_satirlar[0].row()
        soru_id = int(self.ui.table_sorular.item(row_index, 0).text())

        # 3. Pencereyi 'soru_id' ile aç (DÜZENLEME MODU)
        dialog = AddQuestionDialog(self.db, self, soru_id=soru_id)

        if dialog.exec():
            # Güncelleme yapıldıysa tabloyu yenile
            self.tabloyu_guncelle()
            # Detay ekranını da güncelle (belki o soru seçiliydi)
            self.satir_tiklandi(row_index, 0)

    def soruyu_kopyala(self):
        # 1. Text Area içindeki tüm yazıyı, boşluklarıyla beraber al
        icerik = self.ui.txt_soru_detay.toPlainText()

        if not icerik.strip():
            QMessageBox.warning(self, "Uyarı", "Kopyalanacak bir metin yok!")
            return

        secili_satir = self.ui.table_sorular.currentRow()
        soru_id = int(self.ui.table_sorular.item(secili_satir, 0).text())
        img_html = ""
        soru_data, _ = self.db.soru_detay_getir(soru_id)
        resim_adi = soru_data.get('resim_adi')
        if resim_adi:
            appdata_klasoru = Path(
                os.getenv('LOCALAPPDATA')) / "SoruBankasi" / "resimler"
            resim_yolu = appdata_klasoru / resim_adi

            if resim_yolu.exists():
                # Resmi byte (0 ve 1'ler) olarak oku
                with open(resim_yolu, "rb") as resim_dosyasi:
                    resim_bytes = resim_dosyasi.read()
                    # Base64 metnine çevir
                    resim_b64 = base64.b64encode(resim_bytes).decode('utf-8')
                    # Resmi HTML içine gömüyoruz (Word sayfasına sığması için width=500 sınırı koyduk)
                    img_html = f'<br><br><img src="data:image/png;base64,{resim_b64}" width="200">'

        html_satirlar = icerik.replace("\n", "<br>")
        html_icerik = f"""
            <html>
            <head>
            <style>
                /* Tüm gövdeyi Times New Roman yap ve satır yüksekliklerini sıfırla */
                body {{
                    font-family: 'Times New Roman', Times, serif;
                    font-size: 12pt;  /* Word standardı genelde 11 veya 12pt'dir */
                    line-height: 1.0; /* Satır aralığı: Tek (Single) */
                    margin: 0;
                    padding: 0;
                }}
                /* Paragraf boşluklarını tamamen ez */
                p {{
                    margin-top: 0pt;
                    margin-bottom: 0pt;
                    padding: 0;
                }}
            </style>
            </head>
            <body>
                {img_html}
                <p>{html_satirlar}</p>
            </body>
            </html>
        """
        pano = QApplication.clipboard()
        veri_paketi = QMimeData()
        veri_paketi.setHtml(html_icerik)
        veri_paketi.setText(icerik)
        pano.setMimeData(veri_paketi)
        # Eğer butonun üzerindeki yazıyı anlık değiştirip efekt vermek istersen:
        self.ui.btn_soru_kopyala.setText("Kopyalandı! ✔")
        # 1 saniye sonra eski haline dönsün
        QTimer.singleShot(
            1000, lambda: self.ui.btn_soru_kopyala.setText("Soruyu Kopyala"))

    def gereksiz_resimleri_temizle(self):
        """
        Veritabanında (soru tablosunda) referansı bulunmayan 
        kullanılmayan fiziksel resim dosyalarını AppData klasöründen siler.
        """

        # 1. Veritabanından aktif olarak kullanılan resimlerin isimlerini çek
        kullanilan_resimler = set()
        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            # Sadece resim_adi dolu olan kayıtları getiriyoruz
            cursor.execute(
                "SELECT resim_adi FROM sorular WHERE resim_adi IS NOT NULL AND resim_adi != ''")
            sonuclar = cursor.fetchall()

            # Hızlı arama yapabilmek için sonuçları bir 'Set' (küme) içine atıyoruz
            for row in sonuclar:
                kullanilan_resimler.add(row[0])

        except Exception as e:
            QMessageBox.critical(
                self, "Hata", f"Veritabanı okunurken hata oluştu:\n{str(e)}")
            return
        finally:
            conn.close()

        # 2. Resimlerin tutulduğu fiziksel klasörün yolunu belirle
        resim_klasoru = Path(os.getenv('LOCALAPPDATA')) / \
            "SoruBankasi" / "resimler"

        if not resim_klasoru.exists():
            QMessageBox.information(
                self, "Bilgi", "Resim klasörü henüz oluşturulmamış. Temizlenecek dosya yok.")
            return

        silinen_dosya_sayisi = 0
        kurtarilan_boyut_mb = 0.0

        # 3. Klasördeki tüm dosyaları tek tek tara
        for dosya in resim_klasoru.iterdir():
            if dosya.is_file():
                # Eğer dosyanın adı veritabanından gelen kümenin içinde YOKSA, bu yetim bir dosyadır
                if dosya.name not in kullanilan_resimler:
                    try:
                        # Silmeden önce dosya boyutunu bayt cinsinden al (kullanıcıya göstermek için)
                        boyut_bayt = dosya.stat().st_size

                        # Dosyayı fiziksel olarak diskten sil
                        dosya.unlink()

                        silinen_dosya_sayisi += 1
                        kurtarilan_boyut_mb += boyut_bayt / \
                            (1024 * 1024)  # MB'a çevir
                    except Exception as e:
                       pass

        # 4. Kullanıcıya işlemin sonucu hakkında detaylı bilgi ver
        if silinen_dosya_sayisi > 0:
            QMessageBox.information(
                self,
                "Temizlik Başarılı",
                f"Sistem başarıyla tarandı.\n\n"
                f"🗑️ Silinen Gereksiz Resim: {silinen_dosya_sayisi} adet\n"
                f"💾 Açılan Depolama Alanı: {kurtarilan_boyut_mb:.2f} MB"
            )
        else:
            QMessageBox.information(
                self,
                "Sistem Temiz",
                "Harika! Uygulamanızda gereksiz yer kaplayan hiçbir resim dosyası bulunmuyor."
            )

    def database_sil(self):
        """
        Kullanıcı onayı alarak veritabanını ve resimler klasörünü tamamen siler,
        ardından uygulamayı güvenli bir şekilde kapatır.
        """
        # 1. Özelleştirilmiş Mesaj Kutusunu Oluştur
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Sistemi Tamamen Sıfırla")
        msg_box.setText("DİKKAT! Bu işlem tüm sınavlarınızı, kayıtlı sorularınızı ve resimlerinizi KALICI OLARAK silecektir.\n\nBu işlem geri alınamaz. Uygulamayı sıfırlayıp kapatmak istediğinize emin misiniz?")
        msg_box.setIcon(QMessageBox.Icon.Warning)

        # 2. Kendi "Evet" ve "Hayır" Butonlarımızı Ekle
        evet_butonu = msg_box.addButton("Evet", QMessageBox.ButtonRole.YesRole)
        hayir_butonu = msg_box.addButton(
            "Hayır", QMessageBox.ButtonRole.NoRole)

        # Güvenlik için klavyeden 'Enter'a basıldığında kazara silinmesin diye
        # varsayılan butonu "Hayır" olarak ayarlıyoruz.
        msg_box.setDefaultButton(hayir_butonu)

        # 3. Ekranı Göster ve Kullanıcının Tıklamasını Bekle
        msg_box.exec()

        # Kullanıcı "Evet" butonuna tıklamadıysa işlemi iptal et
        if msg_box.clickedButton() != evet_butonu:
            return

        # --- BURADAN SONRASI SİLME İŞLEMİ (Aynı Kalıyor) ---
        try:
            # Veritabanı bağlantısını kapat
            if hasattr(self, 'db') and self.db:
                conn = self.db.get_connection()
                if conn:
                    conn.close()

            # Yolları belirle
            appdata_klasoru = Path(os.getenv('LOCALAPPDATA')) / "SoruBankasi"
            db_yolu = appdata_klasoru / "sorubankasi.db"
            resimler_klasoru = appdata_klasoru / "resimler"

            # Silme işlemleri
            if db_yolu.exists():
                db_yolu.unlink()

            if resimler_klasoru.exists():
                shutil.rmtree(resimler_klasoru)

            # Başarı mesajını da özelleştirelim (Tamamen Türkçe standart butonla)
            basari_msg = QMessageBox(self)
            basari_msg.setWindowTitle("Sıfırlama Başarılı")
            basari_msg.setText(
                "Tüm veriler başarıyla silindi. Uygulama şimdi kapatılacak.")
            basari_msg.setIcon(QMessageBox.Icon.Information)
            basari_msg.addButton("Tamam", QMessageBox.ButtonRole.AcceptRole)
            basari_msg.exec()

            QApplication.quit()

        except Exception as e:
            hata_msg = QMessageBox(self)
            hata_msg.setWindowTitle("Hata")
            hata_msg.setText(
                f"Sıfırlama sırasında beklenmeyen bir hata oluştu:\n{str(e)}")
            hata_msg.setIcon(QMessageBox.Icon.Critical)
            hata_msg.addButton("Tamam", QMessageBox.ButtonRole.AcceptRole)
            hata_msg.exec()
