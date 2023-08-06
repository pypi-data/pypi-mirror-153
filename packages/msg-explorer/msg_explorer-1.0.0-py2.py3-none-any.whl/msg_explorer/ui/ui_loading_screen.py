# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'loading_screen.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QProgressBar,
    QSizePolicy, QWidget)

class Ui_LoadingScreen(object):
    def setupUi(self, LoadingScreen):
        if not LoadingScreen.objectName():
            LoadingScreen.setObjectName(u"LoadingScreen")
        LoadingScreen.resize(400, 150)
        self.gridLayout = QGridLayout(LoadingScreen)
        self.gridLayout.setObjectName(u"gridLayout")
        self.loadingMessage = QLabel(LoadingScreen)
        self.loadingMessage.setObjectName(u"loadingMessage")
        self.loadingMessage.setLayoutDirection(Qt.LeftToRight)
        self.loadingMessage.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.loadingMessage, 0, 0, 1, 1)

        self.progressBar = QProgressBar(LoadingScreen)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setMaximum(0)
        self.progressBar.setValue(-1)

        self.gridLayout.addWidget(self.progressBar, 1, 0, 1, 1)


        self.retranslateUi(LoadingScreen)

        QMetaObject.connectSlotsByName(LoadingScreen)
    # setupUi

    def retranslateUi(self, LoadingScreen):
        LoadingScreen.setWindowTitle(QCoreApplication.translate("LoadingScreen", u"Loading...", None))
        self.loadingMessage.setText(QCoreApplication.translate("LoadingScreen", u"Loading MSG file, please wait...", None))
    # retranslateUi

