from PySide6.QtWidgets import QDialog, QMessageBox
from ui.forms.add_course_ui import Ui_Dialog


class AddCourseDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Yeni Ders Ekle")
        
        # Butona tıklandığında ne olacak?
        self.ui.btn_kaydet.clicked.connect(self.kaydet_tiklandi)

    def kaydet_tiklandi(self):
        # 1. Metni al ve boşlukları temizle
        ders_adi = self.ui.txt_ders_adi.text().strip()

        # 2. Boş mu kontrol et
        if not ders_adi:
            QMessageBox.warning(self, "Hata", "Lütfen bir ders adı giriniz!")
            return

        # 3. Her şey tamamsa pencereyi "Onaylandı" (Accepted) koduyla kapat
        self.accept()

    def get_ders_adi(self):
        """Dışarıdan girilen veriyi almak için yardımcı fonksiyon"""
        return self.ui.txt_ders_adi.text().strip()
