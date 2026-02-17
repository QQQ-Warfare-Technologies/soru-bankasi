# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'manage_exams.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QDialog,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QTableWidget,
    QTableWidgetItem, QTextEdit, QTreeWidget, QTreeWidgetItem,
    QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(738, 571)
        self.verticalLayout_7 = QVBoxLayout(Dialog)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.btn_sinav_arti = QPushButton(Dialog)
        self.btn_sinav_arti.setObjectName(u"btn_sinav_arti")

        self.horizontalLayout.addWidget(self.btn_sinav_arti)

        self.cb_sinavlar = QComboBox(Dialog)
        self.cb_sinavlar.setObjectName(u"cb_sinavlar")

        self.horizontalLayout.addWidget(self.cb_sinavlar)

        self.lbl_yeni_sinav = QLabel(Dialog)
        self.lbl_yeni_sinav.setObjectName(u"lbl_yeni_sinav")

        self.horizontalLayout.addWidget(self.lbl_yeni_sinav)

        self.txt_yeni_sinav_adi = QLineEdit(Dialog)
        self.txt_yeni_sinav_adi.setObjectName(u"txt_yeni_sinav_adi")

        self.horizontalLayout.addWidget(self.txt_yeni_sinav_adi)

        self.btn_sinav_kaydet = QPushButton(Dialog)
        self.btn_sinav_kaydet.setObjectName(u"btn_sinav_kaydet")

        self.horizontalLayout.addWidget(self.btn_sinav_kaydet)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout_7.addLayout(self.horizontalLayout)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.verticalLayout_3.addWidget(self.label)

        self.tree_filtre = QTreeWidget(Dialog)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.tree_filtre.setHeaderItem(__qtreewidgetitem)
        self.tree_filtre.setObjectName(u"tree_filtre")

        self.verticalLayout_3.addWidget(self.tree_filtre)


        self.horizontalLayout_6.addLayout(self.verticalLayout_3)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_2.addWidget(self.label_2)

        self.table_all_questions = QTableWidget(Dialog)
        self.table_all_questions.setObjectName(u"table_all_questions")

        self.verticalLayout_2.addWidget(self.table_all_questions)


        self.horizontalLayout_4.addLayout(self.verticalLayout_2)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.btn_ekle_sinava = QPushButton(Dialog)
        self.btn_ekle_sinava.setObjectName(u"btn_ekle_sinava")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_ekle_sinava.sizePolicy().hasHeightForWidth())
        self.btn_ekle_sinava.setSizePolicy(sizePolicy)
        self.btn_ekle_sinava.setMinimumSize(QSize(55, 25))
        self.btn_ekle_sinava.setMaximumSize(QSize(25, 25))

        self.verticalLayout_4.addWidget(self.btn_ekle_sinava)

        self.btn_cikar = QPushButton(Dialog)
        self.btn_cikar.setObjectName(u"btn_cikar")
        sizePolicy.setHeightForWidth(self.btn_cikar.sizePolicy().hasHeightForWidth())
        self.btn_cikar.setSizePolicy(sizePolicy)
        self.btn_cikar.setMinimumSize(QSize(55, 25))
        self.btn_cikar.setMaximumSize(QSize(25, 25))

        self.verticalLayout_4.addWidget(self.btn_cikar)


        self.horizontalLayout_4.addLayout(self.verticalLayout_4)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.lbl_sinav_sorulari = QLabel(Dialog)
        self.lbl_sinav_sorulari.setObjectName(u"lbl_sinav_sorulari")

        self.verticalLayout_5.addWidget(self.lbl_sinav_sorulari)

        self.table_exam_questions = QTableWidget(Dialog)
        self.table_exam_questions.setObjectName(u"table_exam_questions")
        self.table_exam_questions.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.verticalLayout_5.addWidget(self.table_exam_questions)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")

        self.verticalLayout_5.addLayout(self.horizontalLayout_2)


        self.horizontalLayout_4.addLayout(self.verticalLayout_5)


        self.verticalLayout_6.addLayout(self.horizontalLayout_4)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.btn_soru_kopyala = QPushButton(Dialog)
        self.btn_soru_kopyala.setObjectName(u"btn_soru_kopyala")

        self.horizontalLayout_5.addWidget(self.btn_soru_kopyala)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)

        self.btn_word_olustur = QPushButton(Dialog)
        self.btn_word_olustur.setObjectName(u"btn_word_olustur")

        self.horizontalLayout_5.addWidget(self.btn_word_olustur)

        self.btn_sorulari_kaydet = QPushButton(Dialog)
        self.btn_sorulari_kaydet.setObjectName(u"btn_sorulari_kaydet")

        self.horizontalLayout_5.addWidget(self.btn_sorulari_kaydet)

        self.btn_sinav_sil = QPushButton(Dialog)
        self.btn_sinav_sil.setObjectName(u"btn_sinav_sil")

        self.horizontalLayout_5.addWidget(self.btn_sinav_sil)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.txt_onizleme = QTextEdit(Dialog)
        self.txt_onizleme.setObjectName(u"txt_onizleme")
        self.txt_onizleme.setEnabled(True)
        self.txt_onizleme.setMaximumSize(QSize(500, 500))
        self.txt_onizleme.setReadOnly(True)

        self.horizontalLayout_3.addWidget(self.txt_onizleme)

        self.lbl_resim_sinav = QLabel(Dialog)
        self.lbl_resim_sinav.setObjectName(u"lbl_resim_sinav")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.lbl_resim_sinav.sizePolicy().hasHeightForWidth())
        self.lbl_resim_sinav.setSizePolicy(sizePolicy1)
        self.lbl_resim_sinav.setMinimumSize(QSize(150, 100))
        self.lbl_resim_sinav.setMaximumSize(QSize(150, 100))

        self.horizontalLayout_3.addWidget(self.lbl_resim_sinav)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.verticalLayout_6.addLayout(self.verticalLayout)


        self.horizontalLayout_6.addLayout(self.verticalLayout_6)

        self.horizontalLayout_6.setStretch(0, 1)
        self.horizontalLayout_6.setStretch(1, 3)

        self.verticalLayout_7.addLayout(self.horizontalLayout_6)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.btn_sinav_arti.setText(QCoreApplication.translate("Dialog", u"+", None))
        self.lbl_yeni_sinav.setText(QCoreApplication.translate("Dialog", u"Yeni S\u0131nav\u0131n Ad\u0131:", None))
        self.btn_sinav_kaydet.setText(QCoreApplication.translate("Dialog", u"Olu\u015ftur", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Ders/Konular", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"T\u00fcm Sorular", None))
        self.btn_ekle_sinava.setText(QCoreApplication.translate("Dialog", u">>", None))
        self.btn_cikar.setText(QCoreApplication.translate("Dialog", u"<<", None))
        self.lbl_sinav_sorulari.setText(QCoreApplication.translate("Dialog", u"S\u0131nav Sorular\u0131", None))
        self.btn_soru_kopyala.setText(QCoreApplication.translate("Dialog", u"Soruyu Kopyala", None))
        self.btn_word_olustur.setText(QCoreApplication.translate("Dialog", u"Word Dosyas\u0131 Olu\u015ftur", None))
        self.btn_sorulari_kaydet.setText(QCoreApplication.translate("Dialog", u"S\u0131nav\u0131 Kaydet", None))
        self.btn_sinav_sil.setText(QCoreApplication.translate("Dialog", u"S\u0131nav\u0131 sil", None))
        self.lbl_resim_sinav.setText(QCoreApplication.translate("Dialog", u"Soru Resmi", None))
    # retranslateUi

