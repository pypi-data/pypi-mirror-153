# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'guid_viewer.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QSizePolicy,
    QWidget)

class Ui_GuidViewer(object):
    def setupUi(self, GuidViewer):
        if not GuidViewer.objectName():
            GuidViewer.setObjectName(u"GuidViewer")
        GuidViewer.resize(800, 600)
        self.gridLayout = QGridLayout(GuidViewer)
        self.gridLayout.setObjectName(u"gridLayout")
        self.labelGuid = QLabel(GuidViewer)
        self.labelGuid.setObjectName(u"labelGuid")
        self.labelGuid.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.labelGuid, 0, 0, 1, 1)


        self.retranslateUi(GuidViewer)

        QMetaObject.connectSlotsByName(GuidViewer)
    # setupUi

    def retranslateUi(self, GuidViewer):
        GuidViewer.setWindowTitle(QCoreApplication.translate("GuidViewer", u"GuidViewer", None))
        self.labelGuid.setText(QCoreApplication.translate("GuidViewer", u"TextLabel", None))
    # retranslateUi

