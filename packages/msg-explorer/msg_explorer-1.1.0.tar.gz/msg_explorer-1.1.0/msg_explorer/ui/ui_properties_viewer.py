# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'properties_viewer.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHeaderView, QSizePolicy,
    QTableWidget, QTableWidgetItem, QWidget)

class Ui_PropertiesViewer(object):
    def setupUi(self, PropertiesViewer):
        if not PropertiesViewer.objectName():
            PropertiesViewer.setObjectName(u"PropertiesViewer")
        PropertiesViewer.resize(800, 600)
        self.gridLayout = QGridLayout(PropertiesViewer)
        self.gridLayout.setObjectName(u"gridLayout")
        self.tableProps = QTableWidget(PropertiesViewer)
        if (self.tableProps.columnCount() < 3):
            self.tableProps.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableProps.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableProps.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableProps.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.tableProps.setObjectName(u"tableProps")
        self.tableProps.horizontalHeader().setDefaultSectionSize(100)
        self.tableProps.horizontalHeader().setStretchLastSection(True)
        self.tableProps.verticalHeader().setStretchLastSection(False)

        self.gridLayout.addWidget(self.tableProps, 0, 0, 1, 1)


        self.retranslateUi(PropertiesViewer)

        QMetaObject.connectSlotsByName(PropertiesViewer)
    # setupUi

    def retranslateUi(self, PropertiesViewer):
        PropertiesViewer.setWindowTitle(QCoreApplication.translate("PropertiesViewer", u"PropertiesViewer", None))
        ___qtablewidgetitem = self.tableProps.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("PropertiesViewer", u"ID", None));
        ___qtablewidgetitem1 = self.tableProps.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("PropertiesViewer", u"Type", None));
        ___qtablewidgetitem2 = self.tableProps.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("PropertiesViewer", u"Value", None));
    # retranslateUi

