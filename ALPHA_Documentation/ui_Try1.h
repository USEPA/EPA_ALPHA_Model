/********************************************************************************
** Form generated from reading UI file 'Try1nQEnEp.ui'
**
** Created by: Qt User Interface Compiler version 5.13.0
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef TRY1NQENEP_H
#define TRY1NQENEP_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QLabel>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QSpinBox>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QTextEdit>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QWidget *centralwidget;
    QTextEdit *price_box;
    QLabel *label;
    QSpinBox *tax_rate;
    QLabel *label_2;
    QPushButton *calc_tax_button;
    QTextEdit *results_window;
    QLabel *label_3;
    QMenuBar *menubar;
    QStatusBar *statusbar;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QString::fromUtf8("MainWindow"));
        MainWindow->resize(800, 600);
        centralwidget = new QWidget(MainWindow);
        centralwidget->setObjectName(QString::fromUtf8("centralwidget"));
        price_box = new QTextEdit(centralwidget);
        price_box->setObjectName(QString::fromUtf8("price_box"));
        price_box->setGeometry(QRect(160, 130, 104, 71));
        label = new QLabel(centralwidget);
        label->setObjectName(QString::fromUtf8("label"));
        label->setGeometry(QRect(80, 160, 47, 13));
        QFont font;
        font.setPointSize(10);
        label->setFont(font);
        tax_rate = new QSpinBox(centralwidget);
        tax_rate->setObjectName(QString::fromUtf8("tax_rate"));
        tax_rate->setGeometry(QRect(170, 260, 42, 22));
        tax_rate->setValue(20);
        label_2 = new QLabel(centralwidget);
        label_2->setObjectName(QString::fromUtf8("label_2"));
        label_2->setGeometry(QRect(70, 270, 47, 13));
        calc_tax_button = new QPushButton(centralwidget);
        calc_tax_button->setObjectName(QString::fromUtf8("calc_tax_button"));
        calc_tax_button->setGeometry(QRect(160, 320, 75, 23));
        results_window = new QTextEdit(centralwidget);
        results_window->setObjectName(QString::fromUtf8("results_window"));
        results_window->setGeometry(QRect(140, 390, 104, 71));
        label_3 = new QLabel(centralwidget);
        label_3->setObjectName(QString::fromUtf8("label_3"));
        label_3->setGeometry(QRect(170, 30, 261, 51));
        QFont font1;
        font1.setPointSize(22);
        label_3->setFont(font1);
        MainWindow->setCentralWidget(centralwidget);
        menubar = new QMenuBar(MainWindow);
        menubar->setObjectName(QString::fromUtf8("menubar"));
        menubar->setGeometry(QRect(0, 0, 800, 21));
        MainWindow->setMenuBar(menubar);
        statusbar = new QStatusBar(MainWindow);
        statusbar->setObjectName(QString::fromUtf8("statusbar"));
        MainWindow->setStatusBar(statusbar);

        retranslateUi(MainWindow);

        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QCoreApplication::translate("MainWindow", "MainWindow", nullptr));
        label->setText(QCoreApplication::translate("MainWindow", "Price", nullptr));
        label_2->setText(QCoreApplication::translate("MainWindow", "Tax Rate", nullptr));
        calc_tax_button->setText(QCoreApplication::translate("MainWindow", "Calculate Tax", nullptr));
        label_3->setText(QCoreApplication::translate("MainWindow", "Sales Tax Calculator", nullptr));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // TRY1NQENEP_H
