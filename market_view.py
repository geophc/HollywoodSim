# HollywoodSim/game/market_view.py

from PySide6 import QtWidgets, QtCore
from library import get_script_resale_value

class MarketView(QtWidgets.QWidget):
    buy_script_signal = QtCore.Signal(dict)
    sign_talent_signal = QtCore.Signal(dict)

    # NEW: Library signals
    move_to_shelf_signal = QtCore.Signal(dict)   # script
    sell_script_signal = QtCore.Signal(dict)     # script
    sell_all_signal = QtCore.Signal()

    def __init__(self, market_pool, studio):
        super().__init__()
        self.market_pool = market_pool
        self.studio = studio

        # view caches to guarantee table row -> object mapping
        self._scripts_view = []
        self._actors_view = []
        self._directors_view = []
        self._writers_view = []
        self._staff_view = []
        self._library_view = []

        self._setup_ui()

    def _setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        # Tabs for categories
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane { border-top: 2px solid #444; }
            QTabBar::tab {
                background: #333;
                color: #ddd;
                font-family: monospace;
                font-weight: bold;
                padding: 6px 12px;
                border: 1px solid #444;
                border-bottom: none;
                min-width: 80px;
            }
            QTabBar::tab:selected {
                background: #2a2a2a;
                color: #fff;
                margin-bottom: -1px;
            }
            QTabBar::tab:!selected:hover {
                background: #454545;
            }
        """)

        self.scripts_table = self._create_table(["Title", "Genre", "Potential", "Value"])
        self.actors_table = self._create_table(["Name", "Fame", "Age", "Salary"])
        self.directors_table = self._create_table(["Name", "Fame", "Genre Focus", "Salary"])
        self.writers_table = self._create_table(["Name", "Fame", "Specialty", "Salary"])
        self.staff_table = self._create_table(["Name", "Role", "Experience", "Salary"])
        self.library_table = self._create_table(["Title", "Genre", "Potential", "Resale Value"])

        self.tabs.addTab(self.scripts_table, "Scripts")
        self.tabs.addTab(self.actors_table, "Actors")
        self.tabs.addTab(self.directors_table, "Directors")
        self.tabs.addTab(self.writers_table, "Writers")
        self.tabs.addTab(self.staff_table, "Staff")
        self.tabs.addTab(self.library_table, "Library")
        layout.addWidget(self.tabs)

        # Buttons
        btn_layout = QtWidgets.QHBoxLayout()
        self.btn_buy = QtWidgets.QPushButton("Buy Script")
        self.btn_sign = QtWidgets.QPushButton("Sign Talent")

        # NEW: Library buttons
        self.btn_move_to_shelf = QtWidgets.QPushButton("Move to Shelf")
        self.btn_sell_one = QtWidgets.QPushButton("Sell Script")
        self.btn_sell_all = QtWidgets.QPushButton("Sell All")

        for btn in [self.btn_buy, self.btn_sign,
                    self.btn_move_to_shelf, self.btn_sell_one, self.btn_sell_all]:
            btn_layout.addWidget(btn)

        layout.addLayout(btn_layout)

        # Connect
        self.btn_buy.clicked.connect(self.request_buy_script)
        self.btn_sign.clicked.connect(self.request_sign_talent)

        self.btn_move_to_shelf.clicked.connect(self.request_move_to_shelf)
        self.btn_sell_one.clicked.connect(self.request_sell_script)
        self.btn_sell_all.clicked.connect(self.request_sell_all)

        self.refresh_view()

    def _create_table(self, headers):
        table = QtWidgets.QTableWidget()
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.horizontalHeader().setStretchLastSection(True)
        table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        # Retro style polish
        table.setAlternatingRowColors(True)
        table.setStyleSheet("""
            QTableWidget {
                alternate-background-color: #2a2a2a;
                background-color: #1e1e1e;
                font-family: monospace;
                font-size: 12px;
                color: #ddd;
                gridline-color: #444;
            }
            QHeaderView::section {
                background-color: #333;
                color: #eee;
                font-weight: bold;
                padding: 4px;
            }
            QTableWidget::item {
                padding: 2px;
            }
        """)
        return table

    def refresh_view(self):
        # populate and cache the exact view lists used to render tables
        self._populate_scripts()

        # sort talent views by fame so UI is ordered predictably
        actors = list(getattr(self.market_pool, "actors", []))
        self._actors_view = sorted(actors, key=lambda t: -t.get("fame", 0))

        directors = list(getattr(self.market_pool, "directors", []))
        self._directors_view = sorted(directors, key=lambda t: -t.get("fame", 0))

        writers = list(getattr(self.market_pool, "writers", []))
        self._writers_view = sorted(writers, key=lambda t: -t.get("fame", 0))

        staff = list(getattr(self.market_pool, "staff", []))
        # staff might not have fame; keep original order or sort by experience/fame
        self._staff_view = sorted(staff, key=lambda t: -t.get("experience", 0))

        # populate tables from the cached views (keeps table <-> selection consistent)
        self._populate_talent(self.actors_table, self._actors_view, ["name", "fame", "age", "salary"])
        self._populate_talent(self.directors_table, self._directors_view, ["name", "fame", "genre_focus", "salary"])
        self._populate_talent(self.writers_table, self._writers_view, ["name", "fame", "specialty", "salary"])
        self._populate_talent(self.staff_table, self._staff_view, ["name", "role", "experience", "salary"])

        self._populate_library()

    def _populate_scripts(self):
        # Create the exact list shown in the Scripts table (market scripts first, then owned)
        scripts = list(getattr(self.market_pool, "scripts", [])) + list(getattr(self.studio, "scripts", []))
        self._scripts_view = scripts  # cache it so selection maps correctly
        if not scripts:
            self.scripts_table.setRowCount(1)
            self.scripts_table.setItem(0, 0, QtWidgets.QTableWidgetItem("No scripts available"))
            return

        self.scripts_table.setRowCount(len(scripts))
        for row, s in enumerate(scripts):
            values = [
                s.get("title", "Untitled"),
                s.get("genre", "Unknown"),
                str(s.get("potential_quality", 0)),
                f"${s.get('value', 0)}M"
            ]
            for col, v in enumerate(values):
                self.scripts_table.setItem(row, col, QtWidgets.QTableWidgetItem(str(v)))

    def _populate_library(self):
        shelf = list(getattr(self.studio, "script_library", []))
        self._library_view = shelf
        if not shelf:
            self.library_table.setRowCount(1)
            self.library_table.setItem(0, 0, QtWidgets.QTableWidgetItem("Shelf is empty"))
            return

        self.library_table.setRowCount(len(shelf))
        for row, s in enumerate(shelf):
            resale = get_script_resale_value(s, getattr(self, "calendar", None))
            values = [
                s.get("title", "Untitled"),
                s.get("genre", "Unknown"),
                str(s.get("potential_quality", 0)),
                f"${resale}M"
            ]
            for col, v in enumerate(values):
                self.library_table.setItem(row, col, QtWidgets.QTableWidgetItem(str(v)))

    def _populate_talent(self, table, talent_list, keys):
        if not isinstance(talent_list, list) or not talent_list:
            table.setRowCount(1)
            table.setItem(0, 0, QtWidgets.QTableWidgetItem("No candidates available"))
            return

        table.setRowCount(len(talent_list))
        for row, t in enumerate(talent_list):
            for col, key in enumerate(keys):
                value = t.get(key, "")
                if isinstance(value, (list, tuple)):
                    value = ", ".join(str(v) for v in value)
                table.setItem(row, col, QtWidgets.QTableWidgetItem(str(value)))

    # --- Selection handlers use the exact cached view lists --- #

    def request_buy_script(self):
        row = self.scripts_table.currentRow()
        if row >= 0 and row < len(self._scripts_view):
            script = self._scripts_view[row]
            # Only allow buying if the script is on the market (some displayed scripts are already owned)
            if script in getattr(self.market_pool, "scripts", []):
                self.buy_script_signal.emit(script)
            else:
                QtWidgets.QMessageBox.information(self, "Already Owned", f"'{script.get('title','Untitled')}' is already owned by your studio.")
            self.refresh_view()

    def request_sign_talent(self):
        current_tab = self.tabs.currentIndex()
        role_map = {1: "actors", 2: "directors", 3: "writers", 4: "staff"}
        if current_tab not in role_map:
            return

        table = self.tabs.widget(current_tab)
        row = table.currentRow()
        if row < 0:
            return

        role = role_map[current_tab]

        # Map the tab index to the cached view list
        view_map = {
            "actors": self._actors_view,
            "directors": self._directors_view,
            "writers": self._writers_view,
            "staff": self._staff_view
        }
        talent_view = view_map.get(role, [])
        if not talent_view or row >= len(talent_view):
            return

        talent = talent_view[row]

        # safe salary display
        salary = talent.get("salary", 1.0)
        # Optionally hide salary for staff if you prefer:
        if role == "staff":
            prompt = f"Months (1–12) for {talent.get('name','Unknown')}:"
        else:
            prompt = f"Months (1–12) for {talent.get('name','Unknown')} (Salary ${salary}M):"

        months, ok = QtWidgets.QInputDialog.getInt(
            self,
            "Contract Length",
            prompt,
            6, 1, 12
        )

        if ok:
            self.sign_talent_signal.emit({"talent": talent, "role": role, "months": months})
            self.refresh_view()

    # --- NEW: Library Requests --- #
    def request_move_to_shelf(self):
        row = self.scripts_table.currentRow()
        if row < 0 or row >= len(self._scripts_view):
            return
        script = self._scripts_view[row]
        # only move to shelf if we own it
        if script not in getattr(self.studio, "scripts", []):
            QtWidgets.QMessageBox.information(self, "Cannot Move", "You can only move scripts you own to the shelf.")
            return
        self.move_to_shelf_signal.emit(script)
        self.refresh_view()

    def request_sell_script(self):
        row = self.library_table.currentRow()
        if row >= 0 and row < len(self._library_view):
            script = self._library_view[row]
            self.sell_script_signal.emit(script)
            self.refresh_view()

    def request_sell_all(self):
        if self._library_view:
            self.sell_all_signal.emit()
            self.refresh_view()
