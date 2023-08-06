# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QMainWindow, QMenu,
    QMenuBar, QSizePolicy, QStatusBar, QTabWidget,
    QWidget)

from ..attachments_browser import AttachmentsBrowser
from ..msg_details_page import MSGDetailsPage
from ..msg_tree_viewer import MSGTreeViewer
from ..named_properties_viewer import NamedPropertiesViewer
from ..stream_viewer import StreamViewer

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1012, 615)
        self.actionLoad_Msg_File = QAction(MainWindow)
        self.actionLoad_Msg_File.setObjectName(u"actionLoad_Msg_File")
        self.actionClose_Current_File = QAction(MainWindow)
        self.actionClose_Current_File.setObjectName(u"actionClose_Current_File")
        self.actionOpen_Log = QAction(MainWindow)
        self.actionOpen_Log.setObjectName(u"actionOpen_Log")
        self.actionIncrease_Font = QAction(MainWindow)
        self.actionIncrease_Font.setObjectName(u"actionIncrease_Font")
        self.actionDecrease_Font = QAction(MainWindow)
        self.actionDecrease_Font.setObjectName(u"actionDecrease_Font")
        self.actionLoad_Parent_Msg = QAction(MainWindow)
        self.actionLoad_Parent_Msg.setObjectName(u"actionLoad_Parent_Msg")
        self.actionLoad_Parent_Msg.setEnabled(False)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.pageBasicInformation = MSGDetailsPage()
        self.pageBasicInformation.setObjectName(u"pageBasicInformation")
        self.tabWidget.addTab(self.pageBasicInformation, "")
        self.pageTreeView = MSGTreeViewer()
        self.pageTreeView.setObjectName(u"pageTreeView")
        self.tabWidget.addTab(self.pageTreeView, "")
        self.pageAttachments = AttachmentsBrowser()
        self.pageAttachments.setObjectName(u"pageAttachments")
        self.tabWidget.addTab(self.pageAttachments, "")
        self.pageNamedProperties = NamedPropertiesViewer()
        self.pageNamedProperties.setObjectName(u"pageNamedProperties")
        self.tabWidget.addTab(self.pageNamedProperties, "")
        self.pageStreamView = StreamViewer()
        self.pageStreamView.setObjectName(u"pageStreamView")
        self.tabWidget.addTab(self.pageStreamView, "")

        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1012, 21))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuTest = QMenu(self.menubar)
        self.menuTest.setObjectName(u"menuTest")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuTest.menuAction())
        self.menuFile.addAction(self.actionLoad_Msg_File)
        self.menuFile.addAction(self.actionLoad_Parent_Msg)
        self.menuFile.addAction(self.actionClose_Current_File)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionOpen_Log)
        self.menuTest.addAction(self.actionIncrease_Font)
        self.menuTest.addAction(self.actionDecrease_Font)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MSG Explorer", None))
        self.actionLoad_Msg_File.setText(QCoreApplication.translate("MainWindow", u"Load Msg File...", None))
        self.actionClose_Current_File.setText(QCoreApplication.translate("MainWindow", u"Close Current File", None))
        self.actionOpen_Log.setText(QCoreApplication.translate("MainWindow", u"Open Log", None))
        self.actionIncrease_Font.setText(QCoreApplication.translate("MainWindow", u"Increase Font", None))
        self.actionDecrease_Font.setText(QCoreApplication.translate("MainWindow", u"Decrease Font", None))
        self.actionLoad_Parent_Msg.setText(QCoreApplication.translate("MainWindow", u"Load Parent Msg", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.pageBasicInformation), QCoreApplication.translate("MainWindow", u"File Info", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.pageTreeView), QCoreApplication.translate("MainWindow", u"Tree", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.pageAttachments), QCoreApplication.translate("MainWindow", u"Attachments", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.pageNamedProperties), QCoreApplication.translate("MainWindow", u"Named Properties", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.pageStreamView), QCoreApplication.translate("MainWindow", u"Stream View", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuTest.setTitle(QCoreApplication.translate("MainWindow", u"Font", None))
    # retranslateUi

