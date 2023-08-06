# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'string_viewer.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QPlainTextEdit,
    QSizePolicy, QWidget)

class Ui_StringViewer(object):
    def setupUi(self, StringViewer):
        if not StringViewer.objectName():
            StringViewer.setObjectName(u"StringViewer")
        StringViewer.resize(800, 600)
        self.gridLayout = QGridLayout(StringViewer)
        self.gridLayout.setObjectName(u"gridLayout")
        self.labelType = QLabel(StringViewer)
        self.labelType.setObjectName(u"labelType")

        self.gridLayout.addWidget(self.labelType, 0, 0, 1, 1)

        self.textDisplay = QPlainTextEdit(StringViewer)
        self.textDisplay.setObjectName(u"textDisplay")
        self.textDisplay.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.textDisplay.setReadOnly(True)

        self.gridLayout.addWidget(self.textDisplay, 1, 0, 1, 1)


        self.retranslateUi(StringViewer)

        QMetaObject.connectSlotsByName(StringViewer)
    # setupUi

    def retranslateUi(self, StringViewer):
        StringViewer.setWindowTitle(QCoreApplication.translate("StringViewer", u"StringViewer", None))
        self.labelType.setText("")
    # retranslateUi

