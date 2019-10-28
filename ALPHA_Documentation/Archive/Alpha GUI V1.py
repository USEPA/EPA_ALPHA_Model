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


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        # Load the User Interface
        uic.loadUi('ALPHA GUI V4.ui', self)
        # Connect routines to events and any other needed initialization
        self.vehicle_type_select.currentIndexChanged.connect(self.displayvalue)
        # self.mass_reduction_step_select.valueChanged.connect(self.validate_road_load)
        self.validate_road_load_button.clicked.connect(self.validate_road_load)
        # self.calc_tax_button.clicked.connect(self.calculatetax)
        # self.knob1.valueChanged.connect(self.calculateknob)
        # self.knob1.setValue(10)

    def calculatetax(self):
        price = int(self.price_box.toPlainText())
        tax = (self.tax_rate.value())
        total_price = price + ((tax / 100) * price)
        total_price_string = "The total price with tax is: " + str(total_price)
        self.results_window.setText(total_price_string)

    def calculateknob(self):
        rotary = int(self.knob1.value())
        self.lcd.display(rotary)

    def displayvalue(self):
        # rotary = self.comboBox.currentText()
        self.textEdit.setText(self.vehicle_type_select.currentText())

    # This function calculates the possible step values given the max and min selections
    def validate_road_load(self):
        # Mass Reduction
        # Get selection range from ui
        selection_range = self.mass_reduction_max_select.value() - self.mass_reduction_min_select.value()
        # Clear the step selector on ui
        self.mass_reduction_step_select.clear()
        # Force selection ranges to be valid
        if self.mass_reduction_max_select.value() < self.mass_reduction_min_select.value():
            selection_range = 0
            self.mass_reduction_min_select.setValue(self.mass_reduction_max_select.value())
        #  Determine what step values are possible given the max and min selections in the ui
        for a in range(1, selection_range + 1):
            if selection_range/a == int(selection_range/a):
                self.mass_reduction_step_select.addItem(str(a))
        if selection_range == 0:
            self.mass_reduction_step_select.clear()
            self.mass_reduction_step_select.addItem("0")

        # Rolling Reduction
        # Get selection range from ui
        selection_range = self.rolling_reduction_max_select.value() - self.rolling_reduction_min_select.value()
        # Clear the step selector on ui
        self.rolling_reduction_step_select.clear()
        # Force selection ranges to be valid
        if self.rolling_reduction_max_select.value() < self.rolling_reduction_min_select.value():
            selection_range = 0
            self.rolling_reduction_min_select.setValue(self.rolling_reduction_max_select.value())
        #  Determine what step values are possible given the max and min selections in the ui
        for a in range(1, selection_range + 1):
            if selection_range/a == int(selection_range/a):
                self.rolling_reduction_step_select.addItem(str(a))
        if selection_range == 0:
            self.rolling_reduction_step_select.clear()
            self.rolling_reduction_step_select.addItem("0")

        # Aero Reduction
        # Get selection range from ui
        selection_range = self.aero_reduction_max_select.value() - self.aero_reduction_min_select.value()
        # Clear the step selector on ui
        self.aero_reduction_step_select.clear()
        # Force selection ranges to be valid
        if self.aero_reduction_max_select.value() < self.aero_reduction_min_select.value():
            selection_range = 0
            self.aero_reduction_min_select.setValue(self.aero_reduction_max_select.value())
        #  Determine what step values are possible given the max and min selections in the ui
        for a in range(1, selection_range + 1):
            if selection_range/a == int(selection_range/a):
                self.aero_reduction_step_select.addItem(str(a))
        if selection_range == 0:
            self.aero_reduction_step_select.clear()
            self.aero_reduction_step_select.addItem("0")

        # Engine Sizing
        # Get selection range from ui
        selection_range = self.engine_sizing_max_select.value() - self.engine_sizing_min_select.value()
        # Clear the step selector on ui
        self.engine_sizing_step_select.clear()
        # Force selection ranges to be valid
        if self.engine_sizing_max_select.value() < self.engine_sizing_min_select.value():
            selection_range = 0
            self.engine_sizing_min_select.setValue(self.engine_sizing_max_select.value())
        #  Determine what step values are possible given the max and min selections in the ui
        for a in range(1, selection_range + 1):
            if selection_range/a == int(selection_range/a):
                self.engine_sizing_step_select.addItem(str(a))
        if selection_range == 0:
            self.engine_sizing_step_select.clear()
            self.engine_sizing_step_select.addItem("0")


def main() -> object:
    app = QtWidgets.QApplication(sys.argv)
    main1 = MainWindow()
    main1.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()



