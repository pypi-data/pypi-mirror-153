# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'msg_tree_viewer.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QGridLayout, QHeaderView,
    QSizePolicy, QTreeWidget, QTreeWidgetItem, QWidget)

class Ui_MSGTreeViewer(object):
    def setupUi(self, MSGTreeViewer):
        if not MSGTreeViewer.objectName():
            MSGTreeViewer.setObjectName(u"MSGTreeViewer")
        MSGTreeViewer.resize(400, 300)
        self.gridLayout = QGridLayout(MSGTreeViewer)
        self.gridLayout.setObjectName(u"gridLayout")
        self.treeWidget = QTreeWidget(MSGTreeViewer)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"Name");
        self.treeWidget.setHeaderItem(__qtreewidgetitem)
        self.treeWidget.setObjectName(u"treeWidget")
        self.treeWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.treeWidget.setSortingEnabled(True)
        self.treeWidget.setHeaderHidden(False)
        self.treeWidget.header().setDefaultSectionSize(400)
        self.treeWidget.header().setStretchLastSection(True)

        self.gridLayout.addWidget(self.treeWidget, 0, 0, 1, 1)


        self.retranslateUi(MSGTreeViewer)

        QMetaObject.connectSlotsByName(MSGTreeViewer)
    # setupUi

    def retranslateUi(self, MSGTreeViewer):
        MSGTreeViewer.setWindowTitle(QCoreApplication.translate("MSGTreeViewer", u"Form", None))
    # retranslateUi

