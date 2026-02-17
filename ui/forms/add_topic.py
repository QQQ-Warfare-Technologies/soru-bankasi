from PySide6.QtWidgets import QDialog, QMessageBox
from PySide6.QtCore import Qt
from ui.forms.add_topic_ui import Ui_Dialog


class AddTopicDialog(QDialog):
    def __init__(self, ders_listesi, secili_ders_id=None, parent=None):
        """
        ders_listesi: Veritabanından gelen [{'id': 1, 'ad': 'Matematik'}, ...] listesi
        secili_ders_id: Önceden seçili olan ders ID'si (opsiyonel)
        """
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Yeni Konu Ekle")

        # ComboBox'ı Doldur (İsim görünecek, ID saklanacak)
        self.combo_doldur(ders_listesi, secili_ders_id)

        self.ui.btn_ekle.clicked.connect(self.ekle_tiklandi)

    def combo_doldur(self, dersler, secili_ders_id=None):
        self.ui.cb_dersler.clear()
        secili_index = 0
        for i, ders in enumerate(dersler):
            # Ekrana İsmi Yaz, Arkaya ID'yi Sakla (UserData)
            self.ui.cb_dersler.addItem(ders['ad'], ders['id'])
            if secili_ders_id is not None and ders['id'] == secili_ders_id:
                secili_index = i

        # Önceki seçimi koru
        if secili_ders_id is not None:
            self.ui.cb_dersler.setCurrentIndex(secili_index)

    def ekle_tiklandi(self):
        konu_adi = self.ui.txt_konu_adi.text().strip()

        # 1. Doğrulama
        if not konu_adi:
            QMessageBox.warning(self, "Hata", "Lütfen konu adı giriniz!")
            return

        if self.ui.cb_dersler.currentIndex() == -1:
            QMessageBox.warning(self, "Hata", "Lütfen bir ders seçiniz!")
            return

        # 2. Onay (Pencereyi kapat ve 'Kabul' sinyali gönder)
        self.accept()

    def get_data(self):
        """Ana pencerenin veriyi alması için yardımcı fonksiyon"""
        # Seçili olan dersin saklanan ID'sini al
        secili_ders_id = self.ui.cb_dersler.currentData()
        girilen_konu_adi = self.ui.txt_konu_adi.text().strip()

        return secili_ders_id, girilen_konu_adi
