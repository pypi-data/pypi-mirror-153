# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'hex_viewer.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QPlainTextEdit, QSizePolicy,
    QWidget)

class Ui_HexViewer(object):
    def setupUi(self, HexViewer):
        if not HexViewer.objectName():
            HexViewer.setObjectName(u"HexViewer")
        HexViewer.resize(800, 600)
        self.gridLayout = QGridLayout(HexViewer)
        self.gridLayout.setObjectName(u"gridLayout")
        self.hexViewer = QPlainTextEdit(HexViewer)
        self.hexViewer.setObjectName(u"hexViewer")
        font = QFont()
        font.setFamilies([u"Consolas"])
        font.setPointSize(9)
        self.hexViewer.setFont(font)
        self.hexViewer.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.hexViewer.setReadOnly(True)

        self.gridLayout.addWidget(self.hexViewer, 0, 0, 1, 1)


        self.retranslateUi(HexViewer)

        QMetaObject.connectSlotsByName(HexViewer)
    # setupUi

    def retranslateUi(self, HexViewer):
        HexViewer.setWindowTitle(QCoreApplication.translate("HexViewer", u"HexViewer", None))
    # retranslateUi

