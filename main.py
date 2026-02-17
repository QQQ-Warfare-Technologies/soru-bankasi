# main.py
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
import os
from pathlib import Path
# Senin yazdığın mantık dosyasını çağırıyoruz
from ui.main_window import MainWindow


def resource_path(relative_path):
    """ PyInstaller ile paketlenmiş dosyaların gerçek yolunu bulur. """
    try:
        # PyInstaller dosyaları _MEIPASS içine çıkarır
        base_path = sys._MEIPASS
    except Exception:
        # Normal Python ile çalıştırılıyorsa
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def stilleri_yukle():
    """Belirtilen QSS dosyalarını okur ve tek bir metin olarak birleştirir."""

    # ÇÖZÜM BURADA: resource_path'ten gelen metni Path nesnesine çeviriyoruz!
    qss_klasoru = Path(resource_path("style"))

    # Yüklenecek dosyaların listesi
    qss_dosyalari = [
        "style.qss",
        "butonlar.qss"
    ]

    birlesik_qss = ""

    for dosya in qss_dosyalari:
        dosya_yolu = qss_klasoru / dosya  # Artık '/' operatörü sorunsuz çalışır

        if dosya_yolu.exists():  # Artık .exists() metodu çalışır
            with open(dosya_yolu, "r", encoding="utf-8") as f:
                birlesik_qss += f.read() + "\n\n"
        else:
            print(f"Uyarı: {dosya} bulunamadı!")

    return birlesik_qss


if __name__ == "__main__":
    # 1. Uygulama nesnesini yarat
    app = QApplication(sys.argv)

    app.setStyleSheet(stilleri_yukle())

    window = MainWindow()

    ikon_yolu = resource_path("lib.ico")
    app.setWindowIcon(QIcon(ikon_yolu))

    # 3. Pencereyi görünür yap
    window.show()

    # 4. Uygulama döngüsünü başlat (Kapatılana kadar çalışır)
    sys.exit(app.exec())
