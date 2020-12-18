"""Code1
   -----

   The ``code_1.py`` file demonstrates how to auto-document code.

   A full functional description of the file contents will be
   located here.

       ::

        A highlighted literal section may also be added here if needed.

    """


from PyQt5 import QtWidgets, uic
import sys
import threading


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        # Load the Use Interface
        uic.loadUi('try2.ui', self)
        # Connect routines to events and any other needed initialization
        self.calc_tax_button.clicked.connect(self.calculatetax)
        self.knob1.valueChanged.connect(self.calculateknob)
        self.knob1.setValue(10)

    def calculatetax(self):
        price = int(self.price_box.toPlainText())
        tax = (self.tax_rate.value())
        total_price = price + ((tax / 100) * price)
        total_price_string = "The total price with tax is: " + str(total_price)
        self.results_window.setText(total_price_string)

    def calculateknob(self):
        rotary = int(self.knob1.value())
        self.lcd.display(rotary)


def main() -> object:
    app = QtWidgets.QApplication(sys.argv)
    main1 = MainWindow()
    main1.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


