# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'named_properties_viewer.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QGridLayout,
    QHeaderView, QSizePolicy, QTableWidget, QTableWidgetItem,
    QWidget)

class Ui_NamedPropertiesViewer(object):
    def setupUi(self, NamedPropertiesViewer):
        if not NamedPropertiesViewer.objectName():
            NamedPropertiesViewer.setObjectName(u"NamedPropertiesViewer")
        NamedPropertiesViewer.resize(800, 600)
        self.gridLayout = QGridLayout(NamedPropertiesViewer)
        self.gridLayout.setObjectName(u"gridLayout")
        self.tableNamedProperties = QTableWidget(NamedPropertiesViewer)
        if (self.tableNamedProperties.columnCount() < 3):
            self.tableNamedProperties.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableNamedProperties.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableNamedProperties.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableNamedProperties.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.tableNamedProperties.setObjectName(u"tableNamedProperties")
        self.tableNamedProperties.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableNamedProperties.setSortingEnabled(True)
        self.tableNamedProperties.horizontalHeader().setDefaultSectionSize(300)

        self.gridLayout.addWidget(self.tableNamedProperties, 1, 0, 1, 1)

        self.comboBoxInstance = QComboBox(NamedPropertiesViewer)
        self.comboBoxInstance.setObjectName(u"comboBoxInstance")

        self.gridLayout.addWidget(self.comboBoxInstance, 0, 0, 1, 1)


        self.retranslateUi(NamedPropertiesViewer)

        QMetaObject.connectSlotsByName(NamedPropertiesViewer)
    # setupUi

    def retranslateUi(self, NamedPropertiesViewer):
        NamedPropertiesViewer.setWindowTitle(QCoreApplication.translate("NamedPropertiesViewer", u"NamedPropertiesViewer", None))
        ___qtablewidgetitem = self.tableNamedProperties.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("NamedPropertiesViewer", u"Property ID", None));
        ___qtablewidgetitem1 = self.tableNamedProperties.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("NamedPropertiesViewer", u"Named PID", None));
        ___qtablewidgetitem2 = self.tableNamedProperties.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("NamedPropertiesViewer", u"Data", None));
    # retranslateUi

