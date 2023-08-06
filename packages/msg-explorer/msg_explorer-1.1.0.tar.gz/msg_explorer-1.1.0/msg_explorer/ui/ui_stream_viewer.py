# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'stream_viewer.ui'
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
    QRadioButton, QSizePolicy, QSpacerItem, QStackedWidget,
    QWidget)

from ..guid_viewer import GuidViewer
from ..hex_viewer import HexViewer
from ..multiple_binary_viewer import MultipleBinaryViewer
from ..multiple_viewer import MultipleViewer
from ..properties_viewer import PropertiesViewer
from ..string_viewer import StringViewer

class Ui_StreamViewer(object):
    def setupUi(self, StreamViewer):
        if not StreamViewer.objectName():
            StreamViewer.setObjectName(u"StreamViewer")
        StreamViewer.resize(800, 600)
        self.gridLayout = QGridLayout(StreamViewer)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.buttonParsedView = QRadioButton(StreamViewer)
        self.buttonParsedView.setObjectName(u"buttonParsedView")
        self.buttonParsedView.setChecked(True)

        self.horizontalLayout.addWidget(self.buttonParsedView)

        self.buttonHexView = QRadioButton(StreamViewer)
        self.buttonHexView.setObjectName(u"buttonHexView")
        self.buttonHexView.setChecked(False)

        self.horizontalLayout.addWidget(self.buttonHexView)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.gridLayout.addLayout(self.horizontalLayout, 4, 0, 1, 1)

        self.stackedWidget = QStackedWidget(StreamViewer)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.pageParsedNoData = QWidget()
        self.pageParsedNoData.setObjectName(u"pageParsedNoData")
        self.gridLayout_3 = QGridLayout(self.pageParsedNoData)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label = QLabel(self.pageParsedNoData)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)

        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.pageParsedNoData)
        self.pageParsedString = StringViewer()
        self.pageParsedString.setObjectName(u"pageParsedString")
        self.stackedWidget.addWidget(self.pageParsedString)
        self.pageParsedMultiple = MultipleViewer()
        self.pageParsedMultiple.setObjectName(u"pageParsedMultiple")
        self.stackedWidget.addWidget(self.pageParsedMultiple)
        self.pageParsedMultipleBinary = MultipleBinaryViewer()
        self.pageParsedMultipleBinary.setObjectName(u"pageParsedMultipleBinary")
        self.stackedWidget.addWidget(self.pageParsedMultipleBinary)
        self.pageParsedProperties = PropertiesViewer()
        self.pageParsedProperties.setObjectName(u"pageParsedProperties")
        self.stackedWidget.addWidget(self.pageParsedProperties)
        self.pageParsedGuidViewer = GuidViewer()
        self.pageParsedGuidViewer.setObjectName(u"pageParsedGuidViewer")
        self.stackedWidget.addWidget(self.pageParsedGuidViewer)
        self.pageHexViewer = HexViewer()
        self.pageHexViewer.setObjectName(u"pageHexViewer")
        self.stackedWidget.addWidget(self.pageHexViewer)

        self.gridLayout.addWidget(self.stackedWidget, 5, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_2 = QLabel(StreamViewer)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_3.addWidget(self.label_2)

        self.labelStreamName = QLabel(StreamViewer)
        self.labelStreamName.setObjectName(u"labelStreamName")

        self.horizontalLayout_3.addWidget(self.labelStreamName)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)


        self.gridLayout.addLayout(self.horizontalLayout_3, 3, 0, 1, 1)


        self.retranslateUi(StreamViewer)

        QMetaObject.connectSlotsByName(StreamViewer)
    # setupUi

    def retranslateUi(self, StreamViewer):
        StreamViewer.setWindowTitle(QCoreApplication.translate("StreamViewer", u"StreamViewer", None))
        self.buttonParsedView.setText(QCoreApplication.translate("StreamViewer", u"Parsed View", None))
        self.buttonHexView.setText(QCoreApplication.translate("StreamViewer", u"Hex View", None))
        self.label.setText(QCoreApplication.translate("StreamViewer", u"No stream has been loaded. Try double clicking one in the tree view.", None))
        self.label_2.setText(QCoreApplication.translate("StreamViewer", u"Current Stream:", None))
        self.labelStreamName.setText(QCoreApplication.translate("StreamViewer", u"None", None))
    # retranslateUi

