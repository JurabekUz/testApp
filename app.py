from PyQt6.QtCore import QCoreApplication, Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QFormLayout, QLineEdit, QPushButton,
    QFileDialog, QCheckBox, QLabel, QVBoxLayout, QHBoxLayout, QSpinBox, QComboBox, QMessageBox
)
import sys

from test_handler import generate_test_1, generate_test_2, generate_test_3, write_tests_to_pdf_1, write_tests_to_pdf_3


class TestGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Test Yaratuvchi Dastur")
        self.resize(500, 400)


        # Apply styles
        self.form_widget = FormWidget(self)
        self.setCentralWidget(self.form_widget)
        self.form_widget.setContentsMargins(10,20,10,20)
        # Apply styles
        self.setStyleSheet(self.load_styles())
        # Center the window on the screen with margins

    def load_styles(self):
        return """
                QMainWindow {
                    background-color: #f0f0f0;
                }
                QWidget {
                    font-size: 16px;
                    padding: 2px;
                }
                QLabel {
                    font-weight: bold;
                }
                QLineEdit, QSpinBox, QPushButton, QCheckBox {
                    padding: 5px 10px;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                }
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
                QCheckBox::indicator {
                    width: 20px;
                    height: 24px;
                }
                QCheckBox::indicator:checked {
                    background-color: #4CAF50;
                    border: 1px solid #4CAF50;
                }
                """


class FormWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QFormLayout()

        self.qlevels = [1, 2, 3, 4, 5]
        self.from_number = 1

        # Create and style the title label
        self.title_label = QLabel("Nazorat Teslarini Yaratish")
        self.title_font = QFont()
        self.title_font.setBold(True)
        self.title_font.setPointSize(20)  # Adjust the font size as needed
        self.title_label.setFont(self.title_font)
        self.title_label.setStyleSheet("text-align:center")

        self.title_layout = QVBoxLayout()
        self.title_layout.addWidget(self.title_label)
        self.title_layout.setContentsMargins(0, 0, 0, 20)
        self.title_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.layout.setLayout(0,  QFormLayout.ItemRole.SpanningRole, self.title_layout)

        self.test_type = QLabel(self)
        self.test_type.setObjectName("test_type")
        self.layout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.test_type)
        self.test_type_box = QComboBox(self)
        self.test_type_box.setObjectName("test_type_box")
        self.test_type_box.addItem("1")
        self.test_type_box.addItem("2")
        self.layout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.test_type_box)

        self.question_type = QLabel(self)
        self.question_type.setObjectName("question_type")
        self.layout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.question_type)
        self.question_type_box = QComboBox(self)
        self.question_type_box.setObjectName("question_type_box")
        self.question_type_box.addItem("")
        self.question_type_box.addItem("")
        self.layout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.question_type_box)

        # Science Name input
        self.science_name_input = QLineEdit(self)
        self.layout.addRow("Fan nomi:", self.science_name_input)

        # Teacher Name input
        self.teacher_name_input = QLineEdit(self)
        self.layout.addRow("O'qituvchi FIO:", self.teacher_name_input)

        # Excel File input
        self.student_file_input = QLineEdit(self)
        self.student_file_button = QPushButton("Tanlash...", self)
        self.student_file_button.clicked.connect(self.student_browse_file)
        self.layout.addRow("Talabalar Fayli:", self.create_student_file_input_layout())

        # Excel File input
        self.test_file_input = QLineEdit(self)
        self.test_file_button = QPushButton("Tanlash...", self)
        self.test_file_button.clicked.connect(self.test_browse_file)
        self.layout.addRow("Testlar Fayli:", self.create_test_file_input_layout())

        # Question Level input
        self.question_level_checkbox = QCheckBox("Darajali test", self)
        self.question_level_checkbox.stateChanged.connect(self.toggle_question_level_fields)
        self.layout.addRow(self.question_level_checkbox)

        # question count input
        self.question_count_input = QLineEdit(self)
        self.layout.addRow("Savollar soni:", self.question_count_input)

        # Dynamic From and To inputs container
        self.question_levels_layout = QVBoxLayout()
        self.add_question_level_button = QPushButton("Daraja qo'shish", self)
        self.add_question_level_button.clicked.connect(self.add_question_level_fields)

        self.layout.addRow(self.question_levels_layout)
        self.layout.addRow(self.add_question_level_button)

        self.add_question_level_button.hide()  # Initially hide the add button

        # Submit button
        self.submit_button = QPushButton("Yaratish", self)
        self.submit_button.clicked.connect(self.submit_form)
        self.layout.addRow(self.submit_button)

        self.setLayout(self.layout)
        self.retranslateUi()

    def create_test_file_input_layout(self):
        file_layout = QHBoxLayout()
        file_layout.addWidget(self.test_file_input)
        file_layout.addWidget(self.test_file_button)
        return file_layout

    def create_student_file_input_layout(self):
        file_layout = QHBoxLayout()
        file_layout.addWidget(self.student_file_input)
        file_layout.addWidget(self.student_file_button)
        return file_layout

    def test_browse_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Excel File", "", "Excel Files (*.xlsx *.xls)")
        if file_name:
            self.test_file_input.setText(file_name)

    def student_browse_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Excel File", "", "Excel Files (*.xlsx *.xls)")
        if file_name:
            self.student_file_input.setText(file_name)

    def toggle_question_level_fields(self):
        if self.question_level_checkbox.isChecked():
            self.question_count_input.hide()
            self.add_question_level_fields()
            self.add_question_level_button.show()
        else:
            self.clear_question_level_fields()
            self.add_question_level_button.hide()
            self.question_count_input.show()


    def add_question_level_fields(self):
        self.manage_qlevel()

        ql_box = QComboBox(self)
        for i in self.qlevels:
            ql_box.addItem(str(i))
        from_input = QSpinBox(self)
        from_input.setDisabled(True)
        to_input = QSpinBox(self)
        from_input.setRange(self.from_number, self.from_number + 100)
        to_input.setRange(self.from_number+1, self.from_number + 100)

        level_layout = QHBoxLayout(self)
        level_layout.addWidget(QLabel("Daraja:", self))
        level_layout.addWidget(ql_box)
        level_layout.addWidget(QLabel("Dan:", self))
        level_layout.addWidget(from_input)
        level_layout.addWidget(QLabel("Gacha:", self))
        level_layout.addWidget(to_input)
        self.question_levels_layout.addLayout(level_layout)

    def clear_question_level_fields(self):
        while self.question_levels_layout.count():
            child = self.question_levels_layout.takeAt(0)
            if child.layout():
                while child.layout().count():
                    sub_child = child.layout().takeAt(0)
                    if sub_child.widget():
                        sub_child.widget().deleteLater()
            elif child.widget():
                child.widget().deleteLater()

    def manage_qlevel(self):
        for i in range(self.question_levels_layout.count()):
            level_layout = self.question_levels_layout.itemAt(i).layout()
            level_input = level_layout.itemAt(1).widget()
            level_input.setDisabled(True)
            to_input = level_layout.itemAt(5).widget()
            to_input.setDisabled(True)
            if isinstance(to_input, QSpinBox):
                self.from_number = to_input.value() + 1
            if isinstance(level_input, QComboBox):
                try:
                    self.qlevels.remove(int(level_input.currentText()))
                except:
                    pass

    def submit_form(self):
        test_type = self.test_type_box.currentText()
        science_name = self.science_name_input.text()
        teacher_name = self.teacher_name_input.text()
        count = self.question_count_input.text()
        student_file_path = self.student_file_input.text()
        test_file_path = self.test_file_input.text()

        if self.question_level_checkbox.isChecked():
            question_levels = []
            for i in range(self.question_levels_layout.count()):
                level_layout = self.question_levels_layout.itemAt(i).layout()
                level_input = level_layout.itemAt(1).widget()
                from_input = level_layout.itemAt(3).widget()
                to_input = level_layout.itemAt(5).widget()
                if isinstance(from_input, QSpinBox) and isinstance(to_input, QSpinBox) and isinstance(level_input,
                                                                                                      QComboBox):
                    question_levels.append((
                        int(level_input.currentText()),
                        from_input.value(),
                        to_input.value()
                    ))
            result_tests, test_answers = generate_test_1(student_file_path, test_file_path, question_levels)
            pdf = write_tests_to_pdf_1(result_tests, test_answers, test_type, science_name, teacher_name, ql=True)
        elif self.question_type_box.currentText() == 'Variantli':
            result_tests, test_answers = generate_test_2(student_file_path, test_file_path, int(count))
            pdf = write_tests_to_pdf_1(result_tests, test_answers, test_type, science_name, teacher_name, ql=False)
        else:
            result_tests = generate_test_3(student_file_path, test_file_path, int(count))
            pdf = write_tests_to_pdf_3(result_tests, test_type, science_name, teacher_name)
        save_path, _ = QFileDialog.getSaveFileName(self, "Save PDF", "nazorat", "PDF Files (*.pdf)")
        if save_path:
            pdf.output(save_path)
            QMessageBox.information(self, "Test Muvaffaqiyatli yaratildi\n", f"PDF fayl manzili: {save_path}")

    def retranslateUi(self):
        _translate = QCoreApplication.translate

        self.test_type.setText(_translate("MainWindow", "Nazorat turi"))
        self.test_type_box.setItemText(0, _translate("MainWindow", "Oraliq"))
        self.test_type_box.setItemText(1, _translate("MainWindow", "Yakuniy"))

        self.question_type.setText(_translate("MainWindow", "Savollar turi"))
        self.question_type_box.setItemText(0, _translate("MainWindow", "Variantli"))
        self.question_type_box.setItemText(1, _translate("MainWindow", "Variantsiz(faqat savol)"))

def main():
    app = QApplication(sys.argv)
    main_window = TestGeneratorApp()
    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
