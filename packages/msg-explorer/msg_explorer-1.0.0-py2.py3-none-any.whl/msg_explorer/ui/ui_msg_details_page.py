# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'msg_details_page.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QLineEdit,
    QSizePolicy, QSpacerItem, QWidget)

class Ui_MSGDetailsPage(object):
    def setupUi(self, MSGDetailsPage):
        if not MSGDetailsPage.objectName():
            MSGDetailsPage.setObjectName(u"MSGDetailsPage")
        MSGDetailsPage.resize(800, 600)
        self.gridLayout = QGridLayout(MSGDetailsPage)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_6 = QLabel(MSGDetailsPage)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 7, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 9, 1, 1, 1)

        self.labelSubject = QLabel(MSGDetailsPage)
        self.labelSubject.setObjectName(u"labelSubject")

        self.gridLayout.addWidget(self.labelSubject, 7, 1, 1, 1)

        self.labelPath = QLineEdit(MSGDetailsPage)
        self.labelPath.setObjectName(u"labelPath")
        self.labelPath.setReadOnly(True)

        self.gridLayout.addWidget(self.labelPath, 0, 1, 1, 1)

        self.label_4 = QLabel(MSGDetailsPage)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 6, 0, 1, 1)

        self.labelEncoding = QLabel(MSGDetailsPage)
        self.labelEncoding.setObjectName(u"labelEncoding")

        self.gridLayout.addWidget(self.labelEncoding, 4, 1, 1, 1)

        self.label_5 = QLabel(MSGDetailsPage)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)

        self.labelAttachCount = QLabel(MSGDetailsPage)
        self.labelAttachCount.setObjectName(u"labelAttachCount")

        self.gridLayout.addWidget(self.labelAttachCount, 5, 1, 1, 1)

        self.label = QLabel(MSGDetailsPage)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.label_2 = QLabel(MSGDetailsPage)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 5, 0, 1, 1)

        self.labelClassType = QLabel(MSGDetailsPage)
        self.labelClassType.setObjectName(u"labelClassType")

        self.gridLayout.addWidget(self.labelClassType, 3, 1, 1, 1)

        self.label_3 = QLabel(MSGDetailsPage)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1)

        self.labelClass = QLabel(MSGDetailsPage)
        self.labelClass.setObjectName(u"labelClass")

        self.gridLayout.addWidget(self.labelClass, 2, 1, 1, 1)

        self.labelRecipCount = QLabel(MSGDetailsPage)
        self.labelRecipCount.setObjectName(u"labelRecipCount")

        self.gridLayout.addWidget(self.labelRecipCount, 6, 1, 1, 1)

        self.label_9 = QLabel(MSGDetailsPage)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout.addWidget(self.label_9, 3, 0, 1, 1)

        self.label_7 = QLabel(MSGDetailsPage)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 1, 0, 1, 1)

        self.labelPrefix = QLineEdit(MSGDetailsPage)
        self.labelPrefix.setObjectName(u"labelPrefix")
        self.labelPrefix.setReadOnly(True)

        self.gridLayout.addWidget(self.labelPrefix, 1, 1, 1, 1)


        self.retranslateUi(MSGDetailsPage)

        QMetaObject.connectSlotsByName(MSGDetailsPage)
    # setupUi

    def retranslateUi(self, MSGDetailsPage):
        MSGDetailsPage.setWindowTitle(QCoreApplication.translate("MSGDetailsPage", u"MSGDetailsPage", None))
        self.label_6.setText(QCoreApplication.translate("MSGDetailsPage", u"Subject:", None))
        self.labelSubject.setText("")
        self.label_4.setText(QCoreApplication.translate("MSGDetailsPage", u"Recipients:", None))
        self.labelEncoding.setText("")
        self.label_5.setText(QCoreApplication.translate("MSGDetailsPage", u"Class:", None))
        self.labelAttachCount.setText("")
        self.label.setText(QCoreApplication.translate("MSGDetailsPage", u"Path:", None))
        self.label_2.setText(QCoreApplication.translate("MSGDetailsPage", u"Attachments:", None))
        self.labelClassType.setText("")
        self.label_3.setText(QCoreApplication.translate("MSGDetailsPage", u"Encoding:", None))
        self.labelClass.setText("")
        self.labelRecipCount.setText("")
        self.label_9.setText(QCoreApplication.translate("MSGDetailsPage", u"Class Type:", None))
        self.label_7.setText(QCoreApplication.translate("MSGDetailsPage", u"Prefix:", None))
    # retranslateUi

