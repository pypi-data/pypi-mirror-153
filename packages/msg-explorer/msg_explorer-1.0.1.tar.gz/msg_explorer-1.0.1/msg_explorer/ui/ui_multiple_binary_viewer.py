# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'multiple_binary_viewer.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QHBoxLayout,
    QLabel, QSizePolicy, QSpacerItem, QWidget)

from ..hex_viewer import HexViewer

class Ui_MultipleBinaryViewer(object):
    def setupUi(self, MultipleBinaryViewer):
        if not MultipleBinaryViewer.objectName():
            MultipleBinaryViewer.setObjectName(u"MultipleBinaryViewer")
        MultipleBinaryViewer.resize(800, 600)
        self.gridLayout = QGridLayout(MultipleBinaryViewer)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(MultipleBinaryViewer)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.label_2 = QLabel(MultipleBinaryViewer)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.comboBoxEntries = QComboBox(MultipleBinaryViewer)
        self.comboBoxEntries.setObjectName(u"comboBoxEntries")

        self.horizontalLayout.addWidget(self.comboBoxEntries)


        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.hexViewer = HexViewer(MultipleBinaryViewer)
        self.hexViewer.setObjectName(u"hexViewer")

        self.gridLayout.addWidget(self.hexViewer, 1, 0, 1, 1)


        self.retranslateUi(MultipleBinaryViewer)

        QMetaObject.connectSlotsByName(MultipleBinaryViewer)
    # setupUi

    def retranslateUi(self, MultipleBinaryViewer):
        MultipleBinaryViewer.setWindowTitle(QCoreApplication.translate("MultipleBinaryViewer", u"MultipleBinaryViewer", None))
        self.label.setText(QCoreApplication.translate("MultipleBinaryViewer", u"Data Type:", None))
        self.label_2.setText(QCoreApplication.translate("MultipleBinaryViewer", u"Multiple Binary", None))
    # retranslateUi

