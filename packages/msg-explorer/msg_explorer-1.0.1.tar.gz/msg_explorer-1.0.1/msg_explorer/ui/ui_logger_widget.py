# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'logger_widget.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QListWidget, QListWidgetItem,
    QSizePolicy, QWidget)

class Ui_LoggerWidget(object):
    def setupUi(self, LoggerWidget):
        if not LoggerWidget.objectName():
            LoggerWidget.setObjectName(u"LoggerWidget")
        LoggerWidget.resize(800, 600)
        self.gridLayout = QGridLayout(LoggerWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.listLog = QListWidget(LoggerWidget)
        self.listLog.setObjectName(u"listLog")

        self.gridLayout.addWidget(self.listLog, 0, 0, 1, 1)


        self.retranslateUi(LoggerWidget)

        QMetaObject.connectSlotsByName(LoggerWidget)
    # setupUi

    def retranslateUi(self, LoggerWidget):
        LoggerWidget.setWindowTitle(QCoreApplication.translate("LoggerWidget", u"LoggerWidget", None))
    # retranslateUi

