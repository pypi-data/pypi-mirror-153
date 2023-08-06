# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'attachments_browser.ui'
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
    QSizePolicy, QTableWidget, QTableWidgetItem, QWidget)

class Ui_AttachmentsBrowser(object):
    def setupUi(self, AttachmentsBrowser):
        if not AttachmentsBrowser.objectName():
            AttachmentsBrowser.setObjectName(u"AttachmentsBrowser")
        AttachmentsBrowser.resize(800, 600)
        self.gridLayout = QGridLayout(AttachmentsBrowser)
        self.gridLayout.setObjectName(u"gridLayout")
        self.tableAttachments = QTableWidget(AttachmentsBrowser)
        if (self.tableAttachments.columnCount() < 7):
            self.tableAttachments.setColumnCount(7)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableAttachments.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableAttachments.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableAttachments.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableAttachments.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableAttachments.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableAttachments.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableAttachments.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        self.tableAttachments.setObjectName(u"tableAttachments")
        self.tableAttachments.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableAttachments.setSortingEnabled(True)
        self.tableAttachments.horizontalHeader().setDefaultSectionSize(150)
        self.tableAttachments.verticalHeader().setVisible(False)

        self.gridLayout.addWidget(self.tableAttachments, 0, 0, 1, 1)


        self.retranslateUi(AttachmentsBrowser)

        QMetaObject.connectSlotsByName(AttachmentsBrowser)
    # setupUi

    def retranslateUi(self, AttachmentsBrowser):
        AttachmentsBrowser.setWindowTitle(QCoreApplication.translate("AttachmentsBrowser", u"AttachmentsBrowser", None))
        ___qtablewidgetitem = self.tableAttachments.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("AttachmentsBrowser", u"ID", None));
        ___qtablewidgetitem1 = self.tableAttachments.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("AttachmentsBrowser", u"Status", None));
        ___qtablewidgetitem2 = self.tableAttachments.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("AttachmentsBrowser", u"Short Name", None));
        ___qtablewidgetitem3 = self.tableAttachments.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("AttachmentsBrowser", u"Long Name", None));
        ___qtablewidgetitem4 = self.tableAttachments.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("AttachmentsBrowser", u"Content ID", None));
        ___qtablewidgetitem5 = self.tableAttachments.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("AttachmentsBrowser", u"Mime Type", None));
        ___qtablewidgetitem6 = self.tableAttachments.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("AttachmentsBrowser", u"Rendering Position", None));
    # retranslateUi

