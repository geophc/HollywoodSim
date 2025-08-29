# market_view.py
from PySide6 import QtWidgets, QtCore

class MarketView(QtWidgets.QWidget):
    buy_script_signal = QtCore.Signal(dict)
    sign_talent_signal = QtCore.Signal(dict)

    def __init__(self, market_pool, studio):
        super().__init__()
        self.market_pool = market_pool
        self.studio = studio

        layout = QtWidgets.QVBoxLayout(self)

        self.display = QtWidgets.QTextEdit()
        self.display.setReadOnly(True)
        self.display.setStyleSheet("font-family: monospace; font-size: 12pt;")

        # --- Command buttons ---
        self.btn_scripts = QtWidgets.QPushButton("[1] View Scripts")
        self.btn_actors = QtWidgets.QPushButton("[2] View Actors")
        self.btn_directors = QtWidgets.QPushButton("[3] View Directors")
        self.btn_writers = QtWidgets.QPushButton("[4] View Writers")
        self.btn_staff = QtWidgets.QPushButton("[5] View Staff")

        # connect signals
        self.btn_scripts.clicked.connect(self.request_buy_script)
        self.btn_actors.clicked.connect(lambda: self.request_sign_talent("actors"))
        self.btn_directors.clicked.connect(lambda: self.request_sign_talent("directors"))
        self.btn_writers.clicked.connect(lambda: self.request_sign_talent("writers"))
        self.btn_staff.clicked.connect(lambda: self.request_sign_talent("staff"))

        # layout
        layout.addWidget(self.display)
        btn_layout = QtWidgets.QGridLayout()
        btn_layout.addWidget(self.btn_scripts, 0, 0)
        btn_layout.addWidget(self.btn_actors, 1, 0)
        btn_layout.addWidget(self.btn_directors, 1, 1)
        btn_layout.addWidget(self.btn_writers, 2, 0)
        btn_layout.addWidget(self.btn_staff, 2, 1)
        layout.addLayout(btn_layout)

        self.refresh_view()

    def request_buy_script(self):
        """Shows available scripts and emits the chosen one."""
        scripts = self.market_pool.scripts
        if not scripts:
            QtWidgets.QMessageBox.information(self, "Market", "No scripts available for purchase this month.")
            return

        items = [
            f"{s['title']} ({s['genre']}) - Potential: {s['potential_quality']}, Price: ${s.get('value',0)}M"
            for s in scripts
        ]
        item, ok = QtWidgets.QInputDialog.getItem(self, "Buy Script", "Select a script:", items, 0, False)
        if ok and item:
            index = items.index(item)
            self.buy_script_signal.emit(scripts[index]) # 🔧 MODIFIED: Just emit the signal

    def request_sign_talent(self, role):
        """Shows available talent and emits the chosen person, role, and contract length."""
        pool_map = {
            "actors": self.market_pool.actors, "directors": self.market_pool.directors,
            "writers": self.market_pool.writers, "staff": self.market_pool.staff,
        }
        candidates = pool_map[role]
        if not candidates:
            QtWidgets.QMessageBox.information(self, "Market", f"No {role} available for hire this month.")
            return
        
        items = [f"{t['name']} (Fame: {t.get('fame',0)}, Salary: ${t.get('salary',0)}M)" for t in candidates]
        item, ok = QtWidgets.QInputDialog.getItem(self, f"Sign {role.title()}", "Select talent:", items, 0, False)
        if not ok or not item:
            return

        idx = items.index(item)
        selected_talent = candidates[idx]

        months, ok = QtWidgets.QInputDialog.getInt(self, "Contract Length", "Months (1–12):", 6, 1, 12)
        if not ok:
            return

        # 🔧 MODIFIED: Emit all necessary data in a dictionary
        self.sign_talent_signal.emit({
            "talent": selected_talent,
            "role": role,
            "months": months
        })

    def refresh_view(self):
        self.display.setPlainText(f"🛒 Welcome to the Free Market. Studio Balance: ${self.studio.balance:.2f}M\nChoose an option below...")