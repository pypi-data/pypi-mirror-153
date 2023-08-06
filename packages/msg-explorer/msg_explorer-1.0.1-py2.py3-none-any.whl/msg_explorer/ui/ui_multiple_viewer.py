# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'multiple_viewer.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QListWidget, QListWidgetItem, QSizePolicy, QSpacerItem,
    QWidget)

class Ui_MultipleViewer(object):
    def setupUi(self, MultipleViewer):
        if not MultipleViewer.objectName():
            MultipleViewer.setObjectName(u"MultipleViewer")
        MultipleViewer.resize(800, 600)
        self.gridLayout = QGridLayout(MultipleViewer)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(MultipleViewer)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.labelType = QLabel(MultipleViewer)
        self.labelType.setObjectName(u"labelType")

        self.horizontalLayout.addWidget(self.labelType)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.listEntries = QListWidget(MultipleViewer)
        self.listEntries.setObjectName(u"listEntries")

        self.gridLayout.addWidget(self.listEntries, 1, 0, 1, 1)


        self.retranslateUi(MultipleViewer)

        QMetaObject.connectSlotsByName(MultipleViewer)
    # setupUi

    def retranslateUi(self, MultipleViewer):
        MultipleViewer.setWindowTitle(QCoreApplication.translate("MultipleViewer", u"MultipleViewer", None))
        self.label.setText(QCoreApplication.translate("MultipleViewer", u"Data Type:", None))
        self.labelType.setText("")
    # retranslateUi

