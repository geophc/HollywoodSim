# views.py
from PySide6 import QtWidgets, QtCore

class DashboardView(QtWidgets.QWidget):
    """
    Dashboard: Displays studio overview with date, balance, fame, scripts, roster, and quick actions.
    Styled with cinematic studio theme.
    """
    # Signals to communicate with the main window
    new_script_requested = QtCore.Signal()
    hire_talent_requested = QtCore.Signal()
    produce_movie_requested = QtCore.Signal()
    log_message_requested = QtCore.Signal(str) # New signal for logging

    def __init__(self, studio_model, calendar_model):
        super().__init__()
        self.studio = studio_model
        self.calendar = calendar_model

        layout = QtWidgets.QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # --- Row 1: Studio Info Cards ---
        info_layout = QtWidgets.QHBoxLayout()
        self.date_card = self._create_info_card("📽 Studio Date")
        self.balance_card = self._create_info_card("💵 Box Office Balance")
        self.fame_card = self._create_info_card("🌟 Studio Fame")
        info_layout.addWidget(self.date_card)
        info_layout.addWidget(self.balance_card)
        info_layout.addWidget(self.fame_card)
        layout.addLayout(info_layout)

        # --- Row 2: Financial Summary ---
        finance_layout = QtWidgets.QHBoxLayout()
        self.earnings_card = self._create_info_card("🎬 Total Earnings")
        self.expenses_card = self._create_info_card("💸 Total Expenses")
        finance_layout.addWidget(self.earnings_card)
        finance_layout.addWidget(self.expenses_card)
        layout.addLayout(finance_layout)

        # --- Row 3: Hot Genres ---
        self.trending_card = self._create_info_card("🔥 Trending Genres", wide=True)
        layout.addWidget(self.trending_card)

        # --- Row 4: Active Productions Table ---
        self.scripts_table = QtWidgets.QTableWidget()
        self.scripts_table.setColumnCount(4)
        self.scripts_table.setHorizontalHeaderLabels(["Title", "Genre", "Status", "Draft"])
        self.scripts_table.horizontalHeader().setStretchLastSection(True)
        self.scripts_table.setMinimumHeight(160)
        layout.addWidget(QtWidgets.QLabel("📚 Active Productions"))
        layout.addWidget(self.scripts_table)

        # --- Row 5: Talent Roster ---
        self.roster_list = QtWidgets.QListWidget()
        self.roster_list.setMinimumHeight(120)
        layout.addWidget(QtWidgets.QLabel("🎭 Talent Roster"))
        layout.addWidget(self.roster_list)

        # --- Row 6: Quick Studio Actions ---
        actions_layout = QtWidgets.QHBoxLayout()
        develop_btn = QtWidgets.QPushButton("✍️ Develop New Script")
        hire_btn = QtWidgets.QPushButton("🎬 Hire Talent")
        produce_btn = QtWidgets.QPushButton("🎞️ Produce Movie")

        develop_btn.clicked.connect(self.new_script_requested.emit)
        hire_btn.clicked.connect(self.hire_talent_requested.emit)
        produce_btn.clicked.connect(self.produce_movie_requested.emit)

        actions_layout.addWidget(develop_btn)
        actions_layout.addWidget(hire_btn)
        actions_layout.addWidget(produce_btn)
        layout.addLayout(actions_layout)

        layout.addStretch()

        self.scripts_table.itemDoubleClicked.connect(self._on_script_double_clicked)

    def _on_script_double_clicked(self, item):
        row = item.row()
        if row >= len(self.studio.scripts): return # Safety check
        script = self.studio.scripts[row]

        msg = QtWidgets.QMessageBox(self)
        msg.setWindowTitle("Manage Script")
        msg.setText(f"What do you want to do with '{script['title']}'?")
        finalize_btn = msg.addButton("Finalize", QtWidgets.QMessageBox.AcceptRole)
        rewrite_btn = msg.addButton("Rewrite", QtWidgets.QMessageBox.ActionRole)
        cancel_btn = msg.addButton("Cancel", QtWidgets.QMessageBox.RejectRole)
        msg.exec()

        button_clicked = msg.clickedButton()

        if button_clicked == finalize_btn:
            from scripts import finalize_script
            finalize_script(script, self.studio, self.calendar)
            self.log_message_requested.emit(f"Finalized script: {script['title']}")
        elif button_clicked == rewrite_btn:
            if not self.studio.contracts.get("writers"):
                QtWidgets.QMessageBox.warning(self, "No Writers", "You have no writers under contract to perform a rewrite.")
                return
            from scripts import rewrite_script
            # For now: pick first writer
            writer = self.studio.contracts["writers"][0]["person"]
            rewrite_script(script, writer, self.calendar)
            self.log_message_requested.emit(f"Rewritten script: {script['title']}")

        self.refresh_data() # Refresh view after action

    def _create_info_card(self, title, wide=False):
        """Create a cinematic-styled info card (QLabel)."""
        label = QtWidgets.QLabel(f"<h2>{title}</h2><p>...</p>")
        label.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Raised)
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setMinimumHeight(90)
        if wide:
            label.setMinimumWidth(400)
        label.setStyleSheet("""
            QLabel {
                background-color: #1c1c1c; border: 2px solid #ffcc00;
                border-radius: 10px; padding: 10px; color: #f5f5f5;
            }
            h2 {
                font-family: 'Cinematic'; color: #ffcc00; font-size: 16px;
                font-weight: bold;
            }
            p { font-size: 20px; font-weight: bold; }
        """)
        return label

    def refresh_data(self):
        """Refresh dashboard using studio and calendar models."""
        self.date_card.setText(f"<h2>📽 Studio Date</h2><p>{self.calendar.display()}</p>")

        balance_color = "#4CAF50" if self.studio.balance >= 0 else "#F44336"
        self.balance_card.setText(
            f"<h2>💵 Box Office Balance</h2><p style='color:{balance_color};'>${self.studio.balance:,.2f}M</p>"
        )

        self.fame_card.setText(f"<h2>🌟 Studio Fame</h2><p>{self.studio.prestige}</p>")
        self.earnings_card.setText(f"<h2>🎬 Total Earnings</h2><p>${self.studio.total_earnings:,.2f}M</p>")
        self.expenses_card.setText(f"<h2>💸 Total Expenses</h2><p>${self.studio.total_expenses:,.2f}M</p>")

        trending = ", ".join(self.calendar.trending_genres) or "None"
        self.trending_card.setText(f"<h2>🔥 Trending Genres</h2><p>{trending}</p>")

        # Scripts Table
        self.scripts_table.setRowCount(len(self.studio.scripts))
        for row, script in enumerate(self.studio.scripts):
            self.scripts_table.setItem(row, 0, QtWidgets.QTableWidgetItem(script["title"]))
            self.scripts_table.setItem(row, 1, QtWidgets.QTableWidgetItem(script["genre"]))
            self.scripts_table.setItem(row, 2, QtWidgets.QTableWidgetItem(script.get("status", "Draft")))
            self.scripts_table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(script.get("draft_number", 1))))

        # Talent Roster
        self.roster_list.clear()
        for role, contracts in self.studio.contracts.items():
            for contract in contracts:
                person = contract.get("person", {})
                self.roster_list.addItem(f"{role.capitalize()}: {person.get('name', 'Unknown')}")