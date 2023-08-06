# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'unhandled_exception.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QLabel,
    QPlainTextEdit, QSizePolicy, QWidget)

class Ui_UnhandledException(object):
    def setupUi(self, UnhandledException):
        if not UnhandledException.objectName():
            UnhandledException.setObjectName(u"UnhandledException")
        UnhandledException.resize(588, 479)
        self.gridLayout = QGridLayout(UnhandledException)
        self.gridLayout.setObjectName(u"gridLayout")
        self.traceback = QPlainTextEdit(UnhandledException)
        self.traceback.setObjectName(u"traceback")
        self.traceback.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.traceback.setReadOnly(True)

        self.gridLayout.addWidget(self.traceback, 1, 0, 1, 1)

        self.label = QLabel(UnhandledException)
        self.label.setObjectName(u"label")
        self.label.setWordWrap(True)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)


        self.retranslateUi(UnhandledException)

        QMetaObject.connectSlotsByName(UnhandledException)
    # setupUi

    def retranslateUi(self, UnhandledException):
        UnhandledException.setWindowTitle(QCoreApplication.translate("UnhandledException", u"Unhandled Exception", None))
        self.traceback.setPlainText("")
        self.label.setText(QCoreApplication.translate("UnhandledException", u"An unhandled exception has occured. Please report this to the developers.", None))
    # retranslateUi

