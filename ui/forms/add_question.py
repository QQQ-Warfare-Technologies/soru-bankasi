from PySide6.QtWidgets import QDialog, QMessageBox, QTreeWidgetItem, QApplication
from PySide6.QtCore import Qt
from ui.forms.add_question_ui import Ui_Dialog
from PySide6.QtGui import QShortcut, QKeySequence, QPixmap, QImage
import json
import uuid
from pathlib import Path
import os


class AddQuestionDialog(QDialog):
    def __init__(self, db_manager, parent=None, soru_id=None):
        """
        db_manager: Veritabanı nesnesini dışarıdan alıyoruz.
        """
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.db = db_manager
        self.soru_id = soru_id
        self.setWindowTitle("Yeni Soru Ekle")

        self.kisayol_yapistir = QShortcut(QKeySequence("Ctrl+V"), self)

        # 2. Kısayola basıldığında çalışacak fonksiyonu bağla
        self.kisayol_yapistir.activated.connect(self.panodan_resim_al)

        # 3. Resmi kaydederken kullanmak üzere hafızada tutacağımız değişken
        self.hafizadaki_resim = None
        self.mevcut_resim_adi = None  # Veritabanından gelen eski resmin adını tutar
        self.resim_degisti = False

        self.ui.btn_kaydet.clicked.connect(self.kaydet_tiklandi)
        self.ui.lbl_resim_onizleme.setFocusPolicy(Qt.FocusPolicy.ClickFocus)

        # 2. Label'a farenin sol tıkı ile basıldığında da yapıştırma fonksiyonunu çalıştır!
        self.ui.lbl_resim_onizleme.mousePressEvent = self.label_tiklandi

        self.ui.btn_resim_sil.setVisible(False)

        # Doğru cevap combobox'ını doldur
        self.ui.cb_dogru_cevap.addItems(["", "a", "b", "c", "d", "e"])

        # Ağacı doldur
        self.konulari_yukle()

        if self.soru_id is not None:
            self.setWindowTitle("Soruyu Düzenle")
            self.ui.btn_kaydet.setText("Güncelle")
            self.formu_doldur()  # <--- Mevcut verileri çekip kutulara yazar
        else:
            self.setWindowTitle("Yeni Soru Ekle")
            self.ui.btn_kaydet.setText("Kaydet")

        # Butona tıklandığında çalışacak fonksiyonu bağla
        self.ui.btn_resim_sil.clicked.connect(self.resmi_kaldir)

    def formu_doldur(self):
        """Veritabanından soruyu çekip arayüze yerleştirir."""
        soru_data, bagli_konular = self.db.soru_detay_getir(self.soru_id)

        # 1. Metni Yerleştir
        self.ui.txt_soru.setPlainText(soru_data['metin'])

        # 2. Şıkları Yerleştir
        siklar = json.loads(soru_data['siklar_json'])
        self.ui.txt_a.setText(siklar.get('a', ''))
        self.ui.txt_b.setText(siklar.get('b', ''))
        self.ui.txt_c.setText(siklar.get('c', ''))
        self.ui.txt_d.setText(siklar.get('d', ''))
        self.ui.txt_e.setText(siklar.get('e', ''))

        # 3. Doğru Cevabı Seç
        self.ui.cb_dogru_cevap.setCurrentText(soru_data['dogru_cevap'])

        # 4. Ağaçtaki İlgili Konuları İşaretle (ZOR KISIM BURASIYDI)
        root = self.ui.tree_konular.invisibleRootItem()
        # Tüm dersleri gez
        for i in range(root.childCount()):
            ders_item = root.child(i)
            # Tüm konuları gez
            for j in range(ders_item.childCount()):
                konu_item = ders_item.child(j)
                k_id = konu_item.data(0, Qt.ItemDataRole.UserRole)

                # Eğer bu konu, sorunun bağlı olduğu konulardan biriyse TİK AT
                if k_id in bagli_konular:
                    konu_item.setCheckState(0, Qt.CheckState.Checked)
                    ders_item.setExpanded(True)  # Bulunan dersi aç ki görünsün

        self.mevcut_resim_adi = soru_data.get('resim_adi')
        if self.mevcut_resim_adi:  # Eğer veritabanında bu soruya ait bir resim kaydı varsa
            appdata_klasoru = Path(
                os.getenv('LOCALAPPDATA')) / "SoruBankasi" / "resimler"
            resim_yolu = appdata_klasoru / self.mevcut_resim_adi

            # Gerçekten klasörde böyle bir dosya duruyor mu? (Kullanıcı yanlışlıkla silmiş olabilir)
            if resim_yolu.exists():
                # Resmi dosyadan oku
                pixmap = QPixmap(str(resim_yolu))

                # Label boyutuna sığdır
                sigdirilmis_pixmap = pixmap.scaled(
                    self.ui.lbl_resim_onizleme.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )

                # Ekrana yansıt ve sil butonunu görünür yap
                self.ui.lbl_resim_onizleme.setPixmap(sigdirilmis_pixmap)
               
                self.ui.btn_resim_sil.setVisible(True)
            else:
                pass
               

    def konulari_yukle(self):
        """Ders ve konuları Checkbox'lı olarak listeler."""
        self.ui.tree_konular.clear()
        dersler = self.db.tum_dersleri_getir()

        for ders in dersler:
            # Ana Dal (Ders)
            ders_item = QTreeWidgetItem(self.ui.tree_konular)
            ders_item.setText(0, ders['ad'])
            ders_item.setFlags(ders_item.flags() |
                               Qt.ItemFlag.ItemIsAutoTristate | Qt.ItemFlag.ItemIsUserCheckable)
            ders_item.setCheckState(0, Qt.CheckState.Unchecked)

            # Alt Dallar (Konular)
            konular = self.db.konulari_getir_by_ders_id(ders['id'])
            for konu in konular:
                konu_item = QTreeWidgetItem(ders_item)
                konu_item.setText(0, konu['ad'])
                # ID'yi gizli bölmeye sakla
                konu_item.setData(0, Qt.ItemDataRole.UserRole, konu['id'])

                konu_item.setFlags(konu_item.flags() |
                                   Qt.ItemFlag.ItemIsUserCheckable)
                konu_item.setCheckState(0, Qt.CheckState.Unchecked)

            ders_item.setExpanded(True)

    def kaydet_tiklandi(self):
        # 1. Soru Metni Kontrolü
        metin = self.ui.txt_soru.toPlainText().strip()
        if not metin:
            QMessageBox.warning(self, "Hata", "Soru metni boş olamaz!")
            return

        # 2. Şıkların Hazırlanması (JSON formatına çeviriyoruz)
        siklar = {
            "a": self.ui.txt_a.text().strip(),
            "b": self.ui.txt_b.text().strip(),
            "c": self.ui.txt_c.text().strip(),
            "d": self.ui.txt_d.text().strip(),
            "e": self.ui.txt_e.text().strip()
        }

        # Basit bir kontrol: En azından A ve B şıkkı dolu olsun
        if not siklar["a"] or not siklar["b"]:
            QMessageBox.warning(
                self, "Hata", "En az A ve B şıklarını doldurmalısınız!")
            return

        # 3. Doğru Cevap
        dogru_cevap = self.ui.cb_dogru_cevap.currentText()

        # 4. Seçili Konuların ID'lerini Topla
        secili_konu_idleri = []
        root = self.ui.tree_konular.invisibleRootItem()
        for i in range(root.childCount()):
            ders_item = root.child(i)
            for j in range(ders_item.childCount()):
                konu_item = ders_item.child(j)
                if konu_item.checkState(0) == Qt.CheckState.Checked:
                    secili_konu_idleri.append(
                        konu_item.data(0, Qt.ItemDataRole.UserRole))

        if not secili_konu_idleri:
            QMessageBox.warning(self, "Hata", "Lütfen en az bir konu seçiniz!")
            return

        resim_dosya_adi = self.mevcut_resim_adi

        if self.resim_degisti:
            if self.hafizadaki_resim is not None:
                # Kullanıcı yeni bir resim yapıştırdı, bunu klasöre kaydet
                appdata_klasoru = Path(
                    os.getenv('LOCALAPPDATA')) / "SoruBankasi" / "resimler"
                appdata_klasoru.mkdir(parents=True, exist_ok=True)

                resim_dosya_adi = f"{uuid.uuid4().hex}.png"
                kayit_yolu = appdata_klasoru / resim_dosya_adi

                self.hafizadaki_resim.save(str(kayit_yolu), "PNG")
                
            else:
                # Kullanıcı "Resmi Kaldır" butonuna bastı, veritabanına NULL gidecek
                resim_dosya_adi = None

        # 6. VERİTABANI İŞLEMLERİ
        if self.soru_id is not None:
            # GÜNCELLEME İŞLEMİ
            basarili = self.db.soru_guncelle(
                soru_id=self.soru_id,
                metin=metin,
                siklar_dict=siklar,
                dogru_cevap=dogru_cevap,
                alt_konu_idleri=secili_konu_idleri,
                resim_adi=resim_dosya_adi  # <-- Yeni parametreyi gönderiyoruz
            )
            if basarili:
                QMessageBox.information(
                    self, "Başarılı", "Soru başarıyla güncellendi.")
                self.accept()
            else:
                QMessageBox.critical(
                    self, "Hata", "Soru güncellenirken bir sorun oluştu.")
        else:
            # YENİ EKLEME İŞLEMİ
            basarili = self.db.soru_ekle(
                metin=metin,
                siklar_dict=siklar,
                dogru_cevap=dogru_cevap,
                resim_adi=resim_dosya_adi,  # <-- None'ı silip dinamik değişkenimizi koyduk
                alt_konu_idleri=secili_konu_idleri
            )

            if basarili:
                QMessageBox.information(
                    self, "Başarılı", "Soru başarıyla eklendi.")
                self.accept()
            else:
                QMessageBox.critical(
                    self, "Hata", "Soru eklenirken bir sorun oluştu.")

    def label_tiklandi(self, event):
        """Kullanıcı kesik çizgili alana fareyle tıkladığında çalışır."""
        # Eğer sol tıka basıldıysa panodan resim alma fonksiyonunu tetikle
        if event.button() == Qt.MouseButton.LeftButton:
           
            self.panodan_resim_al()

    def panodan_resim_al(self):
        """Panodaki resmi alır ve ekranda sabit boyutta gösterir."""
        pano = QApplication.clipboard()
        mime_data = pano.mimeData()

        if mime_data.hasImage():
            resim = pano.image()
            self.hafizadaki_resim = resim

            pixmap = QPixmap.fromImage(resim)

            # Artık label'ın boyutu Qt Designer'da sabitlendiği için resim sonsuza kadar büyümez.
            sigdirilmis_pixmap = pixmap.scaled(
                self.ui.lbl_resim_onizleme.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )

            self.ui.lbl_resim_onizleme.setPixmap(sigdirilmis_pixmap)
            self.resim_degisti = True
            # Resim başarıyla eklendiğine göre sil butonunu görünür yap!
            self.ui.btn_resim_sil.setVisible(True)

        else:
           pass

    def resmi_kaldir(self):
        """Eklenen resmi iptal eder ve arayüzü eski haline döndürür."""
        # 1. Hafızadaki resmi temizle
        self.hafizadaki_resim = None
        self.mevcut_resim_adi = None  # Eski resmi de veritabanından silmek için siliyoruz
        self.resim_degisti = True
        # 2. Label'ın içindeki resmi sil ve standart yazıyı geri getir
        self.ui.lbl_resim_onizleme.clear()
        self.ui.lbl_resim_onizleme.setText(
            "Resmi yapıştırmak için tıklayın")

        # 3. Resim kalmadığı için sil butonunu tekrar gizle
        self.ui.btn_resim_sil.setVisible(False)
