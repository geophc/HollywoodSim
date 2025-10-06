#HollywoodSim/game/finance_view.py

from PySide6 import QtWidgets, QtCore


class FinanceView(QtWidgets.QWidget):
    def __init__(self, studio, ledger):
        super().__init__()
        self.studio = studio
        self.ledger = ledger
        self._setup_ui()

    def _setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        # --- Overview ---
        self.balance_label = QtWidgets.QLabel("💰 Balance: ...")
        self.earnings_label = QtWidgets.QLabel("📈 Total Earnings: ...")
        self.expenses_label = QtWidgets.QLabel("📉 Total Expenses: ...")
        self.highest_label = QtWidgets.QLabel("🎬 Highest Grossing: ...")

        for lbl in (self.balance_label, self.earnings_label, self.expenses_label, self.highest_label):
            lbl.setStyleSheet("font-weight: bold; font-size: 14px; color: #00bfa6;")
            layout.addWidget(lbl)

        # --- Ledger Table ---
        layout.addWidget(QtWidgets.QLabel("== Transaction Ledger =="))
        self.ledger_table = QtWidgets.QTableWidget()
        self.ledger_table.setColumnCount(4)
        self.ledger_table.setHorizontalHeaderLabels(["Date", "Description", "Amount (M)", "Balance (M)"])
        self.ledger_table.horizontalHeader().setStretchLastSection(True)
        self.ledger_table.setAlternatingRowColors(True)
        self.ledger_table.setStyleSheet("""
            QTableWidget {
                gridline-color: #3a3f47;
                font-family: monospace;
                font-size: 12px;
                alternate-background-color: #2a2e35;
                background-color: #1b1b1f;
                color: #e0e0e0;
            }
            QHeaderView::section {
                background-color: #293241;
                color: #f0f0f0;
                border: none;
                padding: 4px;
                font-weight: bold;
            }
            QTableWidget::item:selected {
                background-color: #00bfa6;
                color: #000000;
            }
        """)
        layout.addWidget(self.ledger_table)

        # --- Refresh ---
        self.refresh_view()

    def refresh_view(self):
        """Refresh overview and ledger details."""
        self.balance_label.setText(f"💰 Balance: ${self.studio.balance:.2f}M")
        self.earnings_label.setText(f"📈 Total Earnings: ${self.studio.total_earnings:.2f}M")
        self.expenses_label.setText(f"📉 Total Expenses: ${self.studio.total_expenses:.2f}M")

        if self.studio.highest_grossing:
            movie = self.studio.highest_grossing
            self.highest_label.setText(
                f"🎬 Highest Grossing: {movie['title']} (${movie.get('box_office', 0):.2f}M)"
            )
        else:
            self.highest_label.setText("🎬 Highest Grossing: N/A")

        # Populate ledger table
        self.ledger_table.setRowCount(len(self.ledger))
        for row, entry in enumerate(self.ledger):
            self.ledger_table.setItem(row, 0, QtWidgets.QTableWidgetItem(entry["date"]))
            self.ledger_table.setItem(row, 1, QtWidgets.QTableWidgetItem(entry["description"]))
            self.ledger_table.setItem(row, 2, QtWidgets.QTableWidgetItem(f"{entry['amount']:.2f}"))
            self.ledger_table.setItem(row, 3, QtWidgets.QTableWidgetItem(f"{entry['balance']:.2f}"))
