# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QLabel,
    QLayout, QMainWindow, QMenu, QMenuBar,
    QPushButton, QSizePolicy, QSpacerItem, QStatusBar,
    QTableWidget, QTableWidgetItem, QTextEdit, QTreeWidget,
    QTreeWidgetItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(812, 672)
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        MainWindow.setFont(font)
        MainWindow.setStyleSheet(u"")
        self.actionRes_temizle = QAction(MainWindow)
        self.actionRes_temizle.setObjectName(u"actionRes_temizle")
        self.actionDb_sifirla = QAction(MainWindow)
        self.actionDb_sifirla.setObjectName(u"actionDb_sifirla")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_6 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.btn_yeni_ders = QPushButton(self.centralwidget)
        self.btn_yeni_ders.setObjectName(u"btn_yeni_ders")

        self.horizontalLayout.addWidget(self.btn_yeni_ders)

        self.btn_yeni_konu = QPushButton(self.centralwidget)
        self.btn_yeni_konu.setObjectName(u"btn_yeni_konu")

        self.horizontalLayout.addWidget(self.btn_yeni_konu)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.tree_konular = QTreeWidget(self.centralwidget)
        self.tree_konular.setObjectName(u"tree_konular")

        self.verticalLayout.addWidget(self.tree_konular)


        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.btn_sinav_hazirla = QPushButton(self.centralwidget)
        self.btn_sinav_hazirla.setObjectName(u"btn_sinav_hazirla")

        self.horizontalLayout_4.addWidget(self.btn_sinav_hazirla)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.btn_yeni_soru = QPushButton(self.centralwidget)
        self.btn_yeni_soru.setObjectName(u"btn_yeni_soru")

        self.horizontalLayout_4.addWidget(self.btn_yeni_soru)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.table_sorular = QTableWidget(self.centralwidget)
        self.table_sorular.setObjectName(u"table_sorular")

        self.verticalLayout_2.addWidget(self.table_sorular)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.btn_soru_sil = QPushButton(self.centralwidget)
        self.btn_soru_sil.setObjectName(u"btn_soru_sil")

        self.horizontalLayout_3.addWidget(self.btn_soru_sil)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.btn_soru_kopyala = QPushButton(self.centralwidget)
        self.btn_soru_kopyala.setObjectName(u"btn_soru_kopyala")

        self.horizontalLayout_3.addWidget(self.btn_soru_kopyala)

        self.btn_soru_duzenle = QPushButton(self.centralwidget)
        self.btn_soru_duzenle.setObjectName(u"btn_soru_duzenle")

        self.horizontalLayout_3.addWidget(self.btn_soru_duzenle)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.txt_soru_detay = QTextEdit(self.centralwidget)
        self.txt_soru_detay.setObjectName(u"txt_soru_detay")
        font1 = QFont()
        font1.setFamilies([u"Times New Roman"])
        font1.setPointSize(12)
        self.txt_soru_detay.setFont(font1)
        self.txt_soru_detay.setReadOnly(True)

        self.horizontalLayout_5.addWidget(self.txt_soru_detay)

        self.lbl_resim_onizleme_main = QLabel(self.centralwidget)
        self.lbl_resim_onizleme_main.setObjectName(u"lbl_resim_onizleme_main")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_resim_onizleme_main.sizePolicy().hasHeightForWidth())
        self.lbl_resim_onizleme_main.setSizePolicy(sizePolicy)
        self.lbl_resim_onizleme_main.setMinimumSize(QSize(200, 200))
        self.lbl_resim_onizleme_main.setMaximumSize(QSize(200, 300))
        self.lbl_resim_onizleme_main.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_5.addWidget(self.lbl_resim_onizleme_main)

        self.horizontalLayout_5.setStretch(0, 8)
        self.horizontalLayout_5.setStretch(1, 2)

        self.verticalLayout_2.addLayout(self.horizontalLayout_5)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 3)

        self.horizontalLayout_6.addLayout(self.horizontalLayout_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 812, 22))
        self.menuAyarlar = QMenu(self.menubar)
        self.menuAyarlar.setObjectName(u"menuAyarlar")
        self.menuSistemi_Temizle = QMenu(self.menuAyarlar)
        self.menuSistemi_Temizle.setObjectName(u"menuSistemi_Temizle")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuAyarlar.menuAction())
        self.menuAyarlar.addAction(self.menuSistemi_Temizle.menuAction())
        self.menuSistemi_Temizle.addAction(self.actionRes_temizle)
        self.menuSistemi_Temizle.addAction(self.actionDb_sifirla)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionRes_temizle.setText(QCoreApplication.translate("MainWindow", u"Kullan\u0131lmayan resimleri temizle", None))
        self.actionDb_sifirla.setText(QCoreApplication.translate("MainWindow", u"Veri taban\u0131n\u0131 s\u0131f\u0131rla !", None))
        self.btn_yeni_ders.setText(QCoreApplication.translate("MainWindow", u"Ders Ekle", None))
        self.btn_yeni_konu.setText(QCoreApplication.translate("MainWindow", u"Konu Ekle", None))
        ___qtreewidgetitem = self.tree_konular.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"Ders ve konular", None));
        self.btn_sinav_hazirla.setText(QCoreApplication.translate("MainWindow", u"S\u0131nav Haz\u0131rla", None))
        self.btn_yeni_soru.setText(QCoreApplication.translate("MainWindow", u"Soru Ekle", None))
        self.btn_soru_sil.setText(QCoreApplication.translate("MainWindow", u"Soruyu Sil", None))
        self.btn_soru_kopyala.setText(QCoreApplication.translate("MainWindow", u"Soruyu Kopyala", None))
        self.btn_soru_duzenle.setText(QCoreApplication.translate("MainWindow", u"Soruyu D\u00fczenle", None))
        self.lbl_resim_onizleme_main.setText(QCoreApplication.translate("MainWindow", u"SORU RESM\u0130", None))
        self.menuAyarlar.setTitle(QCoreApplication.translate("MainWindow", u"Ayarlar", None))
        self.menuSistemi_Temizle.setTitle(QCoreApplication.translate("MainWindow", u"Veri taban\u0131", None))
    # retranslateUi

