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

    mass_iterations = 1
    rolling_iterations = 1
    aero_iterations = 1
    engine_iterations = 1

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        # Load the User Interface
        uic.loadUi('ALPHA GUI V4.ui', self)
        # Connect routines to events and any other needed initialization
        self.vehicle_type_select.currentIndexChanged.connect(self.displayvalue)
        self.validate_mass_reduction_button.clicked.connect(self.validate_mass_reduction)
        self.validate_rolling_reduction_button.clicked.connect(self.validate_rolling_reduction)
        self.validate_aero_reduction_button.clicked.connect(self.validate_aero_reduction)
        self.validate_engine_sizing_button.clicked.connect(self.validate_engine_sizing)
        self.calculate_iterations_button.clicked.connect(self.calculate111)

        # Initialize items
        # Hide validate road load button
        # self.validate_road_load_button.setVisible(0)
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

    # This function prevents invalid user selections on the Road Load UI page and then calculates
    # the possible step values given the valid max and min selections
    def validate_mass_reduction(self):
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

        global mass_iterations
        mass_iterations = (int(self.mass_reduction_max_select.value()) - int(self.mass_reduction_min_select.value()))
        if int(self.mass_reduction_step_select.currentText()) > 0:
            mass_iterations = mass_iterations / int(self.mass_reduction_step_select.currentText())
        mass_iterations = mass_iterations + 1

    def validate_rolling_reduction(self):
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

        global rolling_iterations
        rolling_iterations = int(self.rolling_reduction_max_select.value())
        rolling_iterations = rolling_iterations - int(self.rolling_reduction_min_select.value())
        if int(self.rolling_reduction_step_select.currentText()) > 0:
            rolling_iterations = rolling_iterations / int(self.rolling_reduction_step_select.currentText())
        rolling_iterations = rolling_iterations + 1

    def validate_aero_reduction(self):
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

        global aero_iterations
        aero_iterations = (int(self.aero_reduction_max_select.value()) - int(self.aero_reduction_min_select.value()))
        if int(self.aero_reduction_step_select.currentText()) > 0:
            aero_iterations = aero_iterations / int(self.aero_reduction_step_select.currentText())
        aero_iterations = aero_iterations + 1

    def validate_engine_sizing(self):
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

        global engine_iterations
        engine_iterations = int(self.engine_sizing_max_select.value())
        engine_iterations = engine_iterations - int(self.engine_sizing_min_select.value())
        if int(self.engine_sizing_step_select.currentText()) > 0:
            engine_iterations = engine_iterations / int(self.engine_sizing_step_select.currentText())
        engine_iterations = engine_iterations + 1

    def calculate111(self):
        global engine_iterations
        # engine_iterations = 1
        self.lineEdit.setText(str(engine_iterations))
        # b = 1


def main() -> object:
    app = QtWidgets.QApplication(sys.argv)
    main1 = MainWindow()
    main1.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()



