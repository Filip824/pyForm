import sys
import os
from PySide2.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QListWidget, QListWidgetItem, QScrollArea,
    QFileDialog
)
from PySide2.QtCore import Qt


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Zadanie")
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        content_layout = QHBoxLayout()

        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel("Wybierz klasę:"))

        self.class_list_widget = QListWidget()
        self.load_class_list()

        scroll_area = QScrollArea()
        scroll_area.setFixedSize(100, 100)
        scroll_area.setWidget(self.class_list_widget)
        left_layout.addWidget(scroll_area)

        right_layout = QVBoxLayout()

        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Podaj nazwisko:"))
        self.name_edit = QLineEdit()
        name_layout.addWidget(self.name_edit)
        name_layout.addStretch()
        right_layout.addLayout(name_layout)

        first_name_layout = QHBoxLayout()
        first_name_layout.addWidget(QLabel("Podaj imię:"))
        self.first_name_edit = QLineEdit()
        first_name_layout.addWidget(self.first_name_edit)
        first_name_layout.addStretch()
        right_layout.addLayout(first_name_layout)
        right_layout.addStretch()

        extra_layout = QVBoxLayout()

        self.browse_button = QPushButton("Przeglądaj")
        self.browse_button.clicked.connect(self.browse_file)
        extra_layout.addWidget(self.browse_button, alignment=Qt.AlignTop)

        self.next_button = QPushButton("Dalej")
        self.next_button.clicked.connect(self.save_form_data)
        extra_layout.addWidget(self.next_button, alignment=Qt.AlignTop)

        content_layout.addLayout(left_layout)
        content_layout.addLayout(right_layout)
        content_layout.addLayout(extra_layout)

        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)

    def load_class_list(self):
        try:
            with open('class_list.txt', 'r') as file:
                for line in file:
                    self.class_list_widget.addItem(QListWidgetItem(line.strip()))
        except FileNotFoundError:
            print("Nie znaleziono pliku z listą klas")

    def browse_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)")
        if file_name:
            self.load_form_data(file_name)

    def load_form_data(self, file_name):
        try:
            with open(file_name, 'r') as file:
                lines = file.readlines()
                if len(lines) >= 3:
                    class_name = lines[0].strip()
                    last_name = lines[1].strip()
                    first_name = lines[2].strip()

                    self.name_edit.setText(last_name)
                    self.first_name_edit.setText(first_name)


                    items = self.class_list_widget.findItems(class_name, Qt.MatchExactly)
                    if items:
                        self.class_list_widget.setCurrentItem(items[0])
        except Exception as e:
            print(f"Nie udało się załadować danych z pliku: {e}")

    def save_form_data(self):
        class_item = self.class_list_widget.currentItem()
        class_name = class_item.text() if class_item else "Nie znane"
        last_name = self.name_edit.text()
        first_name = self.first_name_edit.text()

        data = f"{class_name}\n{last_name}\n{first_name}"
        try:
            with open('form_data.txt', 'w') as file:
                file.write(data)
            print("Zapis udany")
        except Exception as e:
            print(f"Zapis nieudany: {e}")


app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec_())
