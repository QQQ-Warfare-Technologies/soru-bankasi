# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'add_question.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QGridLayout,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QTextEdit, QTreeWidget,
    QTreeWidgetItem, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(557, 462)
        font = QFont()
        font.setPointSize(12)
        Dialog.setFont(font)
        self.horizontalLayout = QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.txt_e = QLineEdit(Dialog)
        self.txt_e.setObjectName(u"txt_e")

        self.gridLayout.addWidget(self.txt_e, 12, 1, 1, 1)

        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 6, 0, 1, 1)

        self.txt_soru = QTextEdit(Dialog)
        self.txt_soru.setObjectName(u"txt_soru")

        self.gridLayout.addWidget(self.txt_soru, 3, 0, 1, 2)

        self.label_4 = QLabel(Dialog)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 7, 0, 2, 1)

        self.label_5 = QLabel(Dialog)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 9, 0, 1, 1)

        self.txt_a = QLineEdit(Dialog)
        self.txt_a.setObjectName(u"txt_a")

        self.gridLayout.addWidget(self.txt_a, 5, 1, 3, 1)

        self.btn_resim_sil = QPushButton(Dialog)
        self.btn_resim_sil.setObjectName(u"btn_resim_sil")

        self.gridLayout.addWidget(self.btn_resim_sil, 1, 0, 1, 1)

        self.label_6 = QLabel(Dialog)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 10, 0, 2, 1)

        self.cb_dogru_cevap = QComboBox(Dialog)
        self.cb_dogru_cevap.setObjectName(u"cb_dogru_cevap")

        self.gridLayout.addWidget(self.cb_dogru_cevap, 13, 1, 1, 1)

        self.label_7 = QLabel(Dialog)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        self.gridLayout.addWidget(self.label_7, 12, 0, 1, 1)

        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 13, 0, 1, 1)

        self.txt_b = QLineEdit(Dialog)
        self.txt_b.setObjectName(u"txt_b")

        self.gridLayout.addWidget(self.txt_b, 8, 1, 1, 1)

        self.txt_d = QLineEdit(Dialog)
        self.txt_d.setObjectName(u"txt_d")

        self.gridLayout.addWidget(self.txt_d, 10, 1, 1, 1)

        self.txt_c = QLineEdit(Dialog)
        self.txt_c.setObjectName(u"txt_c")

        self.gridLayout.addWidget(self.txt_c, 9, 1, 1, 1)

        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        font1 = QFont()
        font1.setPointSize(12)
        font1.setBold(True)
        self.label.setFont(font1)
        self.label.setAlignment(Qt.AlignmentFlag.AlignBottom|Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft)

        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)

        self.lbl_resim_onizleme = QLabel(Dialog)
        self.lbl_resim_onizleme.setObjectName(u"lbl_resim_onizleme")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_resim_onizleme.sizePolicy().hasHeightForWidth())
        self.lbl_resim_onizleme.setSizePolicy(sizePolicy)
        self.lbl_resim_onizleme.setMinimumSize(QSize(100, 100))

        self.gridLayout.addWidget(self.lbl_resim_onizleme, 1, 1, 2, 1)


        self.horizontalLayout.addLayout(self.gridLayout)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_8 = QLabel(Dialog)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setFont(font1)
        self.label_8.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label_8.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label_8)

        self.tree_konular = QTreeWidget(Dialog)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.tree_konular.setHeaderItem(__qtreewidgetitem)
        self.tree_konular.setObjectName(u"tree_konular")
        self.tree_konular.setHeaderHidden(True)

        self.verticalLayout.addWidget(self.tree_konular)

        self.btn_kaydet = QPushButton(Dialog)
        self.btn_kaydet.setObjectName(u"btn_kaydet")

        self.verticalLayout.addWidget(self.btn_kaydet)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.horizontalLayout.setStretch(0, 3)
        self.horizontalLayout.setStretch(1, 1)
        QWidget.setTabOrder(self.txt_soru, self.txt_a)
        QWidget.setTabOrder(self.txt_a, self.txt_b)
        QWidget.setTabOrder(self.txt_b, self.txt_c)
        QWidget.setTabOrder(self.txt_c, self.txt_d)
        QWidget.setTabOrder(self.txt_d, self.txt_e)
        QWidget.setTabOrder(self.txt_e, self.cb_dogru_cevap)
        QWidget.setTabOrder(self.cb_dogru_cevap, self.tree_konular)
        QWidget.setTabOrder(self.tree_konular, self.btn_kaydet)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"a)", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"b)", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"c)", None))
        self.btn_resim_sil.setText(QCoreApplication.translate("Dialog", u"Resmi Sil", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"d)", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"e)", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Cevap", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Soru Metni", None))
        self.lbl_resim_onizleme.setText(QCoreApplication.translate("Dialog", u"Resmi yap\u0131\u015ft\u0131rmak i\u00e7in t\u0131klay\u0131n", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"Konu/ Konular\u0131 Se\u00e7in", None))
        self.btn_kaydet.setText(QCoreApplication.translate("Dialog", u"Soruyu Kaydet", None))
    # retranslateUi

