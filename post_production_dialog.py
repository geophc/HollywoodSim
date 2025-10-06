# HollywoodSim/game/post_production_dialog.py

from PySide6 import QtWidgets, QtCore
from post_production import MARKETING_PLANS, RELEASE_STRATEGIES

class PostProductionDialog(QtWidgets.QDialog):
    def __init__(self, movie, studio_balance, parent=None):
        super().__init__(parent)
        self.movie = movie
        self.studio_balance = studio_balance
        self.setWindowTitle(f"Post-Production: {movie['title']}")
        self.setMinimumWidth(400)

        self.layout = QtWidgets.QVBoxLayout(self)
        
        # --- Marketing Section ---
        marketing_group = QtWidgets.QGroupBox("Marketing Campaign")
        marketing_layout = QtWidgets.QVBoxLayout()
        self.marketing_combo = QtWidgets.QComboBox()
        for plan, data in MARKETING_PLANS.items():
            self.marketing_combo.addItem(f"{plan} (${data['cost']}M) - +{data['buzz']} Buzz", userData=plan)
        marketing_layout.addWidget(self.marketing_combo)
        marketing_group.setLayout(marketing_layout)
        self.layout.addWidget(marketing_group)

        # --- Release Strategy Section ---
        release_group = QtWidgets.QGroupBox("Release Strategy")
        release_layout = QtWidgets.QVBoxLayout()
        self.release_combo = QtWidgets.QComboBox()
        for strategy, data in RELEASE_STRATEGIES.items():
            self.release_combo.addItem(f"{strategy} - {data['desc']}", userData=strategy)
        release_layout.addWidget(self.release_combo)
        release_group.setLayout(release_layout)
        self.layout.addWidget(release_group)

        # --- Dialog Buttons ---
        buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        self.layout.addWidget(buttons)

    def accept(self):
        """Check if the player can afford the marketing plan before closing."""
        selected_plan_name = self.marketing_combo.currentData()
        cost = MARKETING_PLANS[selected_plan_name]['cost']
        if cost > self.studio_balance:
            QtWidgets.QMessageBox.warning(self, "Insufficient Funds", f"You cannot afford the {selected_plan_name} marketing plan. It costs ${cost}M.")
            return # Prevent the dialog from closing
        super().accept() # Proceed with closing

    def get_choices(self):
        """Returns the selected plan and strategy."""
        return {
            "marketing_plan": self.marketing_combo.currentData(),
            "release_strategy": self.release_combo.currentData()
        }