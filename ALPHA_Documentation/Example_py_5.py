from PyQt5 import QtWidgets, uic
import sys


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        # Load the UI Page
        uic.loadUi('try1.ui', self)
        self.calc_tax_button.clicked.connect(self.calculatetax)

    def calculatetax(self):
        price = int(self.price_box.toPlainText())
        tax = (self.tax_rate.value())
        total_price = price + ((tax / 100) * price)
        total_price_string = "The total price with tax is: " + str(total_price)
        self.results_window.setText(total_price_string)


def main():
    app = QtWidgets.QApplication(sys.argv)
    main1 = MainWindow()
    main1.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

