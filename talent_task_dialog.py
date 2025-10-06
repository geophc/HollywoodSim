# HollywoodSim/game/talent_task_dialog.py

from PySide6 import QtWidgets
from talent_tasks import TASKS

class TalentTaskDialog(QtWidgets.QDialog):
    def __init__(self, contracts_by_type, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Assign Talent Task")
        self.setMinimumSize(400, 300)

        layout = QtWidgets.QVBoxLayout(self)

        # Pick role
        self.role_combo = QtWidgets.QComboBox()
        self.role_combo.addItems(contracts_by_type.keys())
        self.role_combo.currentTextChanged.connect(self.update_people)
        layout.addWidget(QtWidgets.QLabel("Select Role:"))
        layout.addWidget(self.role_combo)

        # Pick person
        self.person_combo = QtWidgets.QComboBox()
        layout.addWidget(QtWidgets.QLabel("Select Person:"))
        layout.addWidget(self.person_combo)

        # Pick task
        self.task_combo = QtWidgets.QComboBox()
        layout.addWidget(QtWidgets.QLabel("Select Task:"))
        layout.addWidget(self.task_combo)

        # Buttons
        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.contracts_by_type = contracts_by_type
        self.update_people()

    def update_people(self):
        role = self.role_combo.currentText()
        self.person_combo.clear()
        self.task_combo.clear()

        contracts = self.contracts_by_type.get(role, [])
        for c in contracts:
            if "person" in c:
                self.person_combo.addItem(c["person"]["name"], userData=c)

        for task in TASKS.get(role, []):
            self.task_combo.addItem(task["name"])

    def get_selection(self):
        contract = self.person_combo.currentData()
        task_name = self.task_combo.currentText()
        return contract, task_name
