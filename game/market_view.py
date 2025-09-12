from PySide6 import QtWidgets, QtCore

class MarketView(QtWidgets.QWidget):
    buy_script_signal = QtCore.Signal(dict)
    sign_talent_signal = QtCore.Signal(dict)

    def __init__(self, market_pool, studio):
        super().__init__()
        self.market_pool = market_pool
        self.studio = studio
        self._setup_ui()

    def _setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        # Tabs for categories
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane { /* The container for the tab contents */
                border-top: 2px solid #444;
            }

            QTabBar::tab { /* The tab buttons */
                background: #333;
                color: #ddd;
                font-family: monospace;
                font-weight: bold;
                padding: 6px 12px;
                border: 1px solid #444;
                border-bottom: none; /* So it merges with the pane */
                min-width: 80px;
            }

            QTabBar::tab:selected {
                background: #2a2a2a; /* Match table's alternate color to look connected */
                color: #fff;
                margin-bottom: -1px; /* Makes selected tab merge with pane */
            }

            QTabBar::tab:!selected:hover {
                background: #454545; /* Hover effect for non-selected tabs */
            }
        """)
        
        self.scripts_table = self._create_table(["Title", "Genre", "Potential", "Value"])
        self.actors_table = self._create_table(["Name", "Fame", "Age", "Salary"])
        self.directors_table = self._create_table(["Name", "Fame", "Genre Focus", "Salary"])
        self.writers_table = self._create_table(["Name", "Fame", "Specialty", "Salary"])
        self.staff_table = self._create_table(["Name", "Role", "Experience", "Salary"])

        self.tabs.addTab(self.scripts_table, "Scripts")
        self.tabs.addTab(self.actors_table, "Actors")
        self.tabs.addTab(self.directors_table, "Directors")
        self.tabs.addTab(self.writers_table, "Writers")
        self.tabs.addTab(self.staff_table, "Staff")
        layout.addWidget(self.tabs)

        # Buttons
        btn_layout = QtWidgets.QHBoxLayout()
        self.btn_buy = QtWidgets.QPushButton("Buy Script")
        self.btn_sign = QtWidgets.QPushButton("Sign Talent")
        btn_layout.addWidget(self.btn_buy)
        btn_layout.addWidget(self.btn_sign)
        layout.addLayout(btn_layout)

        # Connect
        self.btn_buy.clicked.connect(self.request_buy_script)
        self.btn_sign.clicked.connect(self.request_sign_talent)

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
        self._populate_scripts()
        self._populate_talent(self.actors_table, self.market_pool.actors, ["name", "fame", "age", "salary"])
        self._populate_talent(self.directors_table, self.market_pool.directors, ["name", "fame", "genre_focus", "salary"])
        self._populate_talent(self.writers_table, self.market_pool.writers, ["name", "fame", "specialty", "salary"])
        self._populate_talent(self.staff_table, self.market_pool.staff, ["name", "role", "experience", "salary"])

    def _populate_scripts(self):
        scripts = self.market_pool.scripts
        if not scripts:
            self.scripts_table.setRowCount(1)
            self.scripts_table.setItem(0, 0, QtWidgets.QTableWidgetItem("No scripts available"))
            return

        self.scripts_table.setRowCount(len(scripts))
        for row, s in enumerate(scripts):
            values = [s["title"], s["genre"], str(s["potential_quality"]), f"${s.get('value', 0)}M"]
            for col, v in enumerate(values):
                self.scripts_table.setItem(row, col, QtWidgets.QTableWidgetItem(str(v)))

    def _populate_talent(self, table, talent_list, keys):
        if not talent_list:
            table.setRowCount(1)
            table.setItem(0, 0, QtWidgets.QTableWidgetItem("No candidates available"))
            return

        # Sort by fame, descending
        sorted_list = sorted(talent_list, key=lambda t: -t.get("fame", 0))

        table.setRowCount(len(sorted_list))
        for row, t in enumerate(sorted_list):
            for col, key in enumerate(keys):
                table.setItem(row, col, QtWidgets.QTableWidgetItem(str(t.get(key, ""))))

    def request_buy_script(self):
        row = self.scripts_table.currentRow()
        if row >= 0 and row < len(self.market_pool.scripts):
            self.buy_script_signal.emit(self.market_pool.scripts[row])
            self.refresh_view()  # auto-refresh

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
        talent_list = getattr(self.market_pool, role)
        if not talent_list:
            return

        # Make sure sorted by fame for consistency
        sorted_list = sorted(talent_list, key=lambda t: -t.get("fame", 0))
        if row >= len(sorted_list):
            return

        talent = sorted_list[row]
        months, ok = QtWidgets.QInputDialog.getInt(
            self,
            "Contract Length",
            f"Months (1–12) for {talent['name']} (Salary ${talent['salary']}M):",
            6, 1, 12
        )
        if ok:
            self.sign_talent_signal.emit({"talent": talent, "role": role, "months": months})
            self.refresh_view()  # auto-refresh
