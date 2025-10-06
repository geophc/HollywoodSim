# HollywoodSim/game/dashboard_view.py

from PySide6 import QtWidgets, QtCore
from library import get_script_resale_value
import calendar_1 as calendar


class DashboardView(QtWidgets.QWidget):
    # === Signals to request actions from the main window ===
    new_script_requested = QtCore.Signal()
    rewrite_script_requested = QtCore.Signal(object)
    finalize_script_requested = QtCore.Signal(object)
    start_production_requested = QtCore.Signal(object)
    open_post_production_requested = QtCore.Signal(object)

    # Script Shelf
    move_to_shelf_requested = QtCore.Signal(object)
    sell_script_requested = QtCore.Signal(object)
    sell_all_requested = QtCore.Signal()

    # Talent Tasks
    assign_task_requested = QtCore.Signal()

    def __init__(self, studio, calendar):
        super().__init__()
        self.studio = studio
        self.calendar = calendar
        self._setup_ui()

    # === UI Setup ===
    def _setup_ui(self):
        main_layout = QtWidgets.QHBoxLayout(self)

        # --- Left Column ---
        left_column_layout = QtWidgets.QVBoxLayout()

        # Studio Overview
        self.date_label = QtWidgets.QLabel("📅 Date: ...")
        self.balance_label = QtWidgets.QLabel("💰 Balance: ...")
        self.prestige_label = QtWidgets.QLabel("👑 Prestige: ...")
        for lbl in (self.date_label, self.balance_label, self.prestige_label):
            lbl.setStyleSheet("font-weight: bold; font-size: 14px; color: #00bfa6;")
            left_column_layout.addWidget(lbl)

        # Script Development
        left_column_layout.addWidget(QtWidgets.QLabel("== Script Development =="))
        self.scripts_table = self._create_table(["Title", "Genre", "Status", "Quality", "Potential"])
        left_column_layout.addWidget(self.scripts_table)

        script_btn_layout = QtWidgets.QHBoxLayout()
        for text, handler in [
            ("New", self.on_new_script),
            ("Rewrite", self.on_rewrite_script),
            ("Finalize", self.on_finalize_script),
        ]:
            btn = QtWidgets.QPushButton(text)
            btn.setFixedWidth(80)
            btn.setStyleSheet("""
                QPushButton {
                    background: #293241;
                    border: 1px solid #00bfa6;
                    border-radius: 4px;
                    padding: 4px;
                    color: #e0e0e0;
                }
                QPushButton:hover { background: #3d4a5a; }
            """)
            btn.clicked.connect(handler)
            script_btn_layout.addWidget(btn)
        left_column_layout.addLayout(script_btn_layout)

        # Script Shelf
        left_column_layout.addWidget(QtWidgets.QLabel("== Script Shelf =="))
        self.shelf_table = self._create_table(["Title", "Genre", "Potential", "Resale Value"])
        left_column_layout.addWidget(self.shelf_table)

        shelf_btn_layout = QtWidgets.QHBoxLayout()
        for text, handler in [
            ("Move", self.on_move_to_shelf),
            ("Sell", self.on_sell_from_shelf),
            ("Sell All", self.on_sell_all),
        ]:
            btn = QtWidgets.QPushButton(text)
            btn.setFixedWidth(80)
            btn.setStyleSheet("""
                QPushButton {
                    background: #222;
                    border: 1px solid #00bfa6;
                    border-radius: 4px;
                    padding: 4px;
                    color: #e0e0e0;
                }
                QPushButton:hover { background: #333; }
            """)
            btn.clicked.connect(handler)
            shelf_btn_layout.addWidget(btn)
        left_column_layout.addLayout(shelf_btn_layout)

        # Studio Roster (with tasks)
        left_column_layout.addWidget(QtWidgets.QLabel("== Studio Roster =="))
        self.roster_table = self._create_table(["Name", "Role", "Fame", "Salary", "Task"])
        left_column_layout.addWidget(self.roster_table)

        # Assign Task Button
        self.assign_task_btn = QtWidgets.QPushButton("Assign Task")
        self.assign_task_btn.setFixedWidth(120)
        self.assign_task_btn.setStyleSheet("""
            QPushButton {
                background: #2b2b2b;
                border: 1px solid #00bfa6;
                border-radius: 4px;
                padding: 4px;
                color: #e0e0e0;
            }
            QPushButton:hover { background: #3a3a3a; }
        """)
        self.assign_task_btn.clicked.connect(self.assign_task_requested.emit)
        left_column_layout.addWidget(self.assign_task_btn)

        # --- Right Column ---
        right_column_layout = QtWidgets.QVBoxLayout()
        right_column_layout.addWidget(QtWidgets.QLabel("== Production Pipeline =="))
        self.movies_table = self._create_table(["Title", "Status", "Director", "Actor", "Release"])
        right_column_layout.addWidget(self.movies_table)

        prod_btn_layout = QtWidgets.QHBoxLayout()
        for text, handler in [
            ("Start", self.on_start_production),
            ("Marketing", self.on_set_marketing),
        ]:
            btn = QtWidgets.QPushButton(text)
            btn.setFixedWidth(100)
            btn.setStyleSheet("""
                QPushButton { background: #333; border: none; padding: 4px; }
                QPushButton:hover { background: #444; }
            """)
            btn.clicked.connect(handler)
            prod_btn_layout.addWidget(btn)
        right_column_layout.addLayout(prod_btn_layout)

        # Combine both columns
        main_layout.addLayout(left_column_layout, 1)
        main_layout.addLayout(right_column_layout, 1)

    # === Utilities ===
    def _create_table(self, headers):
        table = QtWidgets.QTableWidget()
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.setAlternatingRowColors(True)
        table.setStyleSheet("""
            QTableWidget {
                gridline-color: #3a3f47;
                font-family: monospace;
                font-size: 13px;
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
        table.horizontalHeader().setStretchLastSection(True)
        table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        return table

    # === Refresh Methods ===
    def refresh_data(self):
        # --- Update Studio Overview ---
        self.date_label.setText(
            f"📅 Date: {self.calendar.month_name()} {self.calendar.year}"
        )
        self.balance_label.setText(f"💰 Balance: ${self.studio.balance:,.2f}M")
        self.prestige_label.setText(f"👑 Prestige: {self.studio.prestige}")

        # --- Update Tables ---
        self._refresh_scripts_table()
        self._refresh_shelf_table()
        self._refresh_roster_table()
        self._refresh_movies_table()



    def _refresh_scripts_table(self):
        scripts_in_dev = [s for s in self.studio.scripts if s.get("status") in ["first_draft", "rewritten", "approved"]]
        self.scripts_table.setRowCount(len(scripts_in_dev))
        for row, s in enumerate(scripts_in_dev):
            self.scripts_table.setItem(row, 0, QtWidgets.QTableWidgetItem(s["title"]))
            self.scripts_table.setItem(row, 1, QtWidgets.QTableWidgetItem(s["genre"]))
            self.scripts_table.setItem(row, 2, QtWidgets.QTableWidgetItem(s.get("status", "Draft")))
            self.scripts_table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(s.get("quality", 0))))
            self.scripts_table.setItem(row, 4, QtWidgets.QTableWidgetItem(str(s.get("potential_quality", 0))))

    def _refresh_shelf_table(self):
        shelf = getattr(self.studio, "script_library", [])
        self.shelf_table.setRowCount(len(shelf))
        for row, s in enumerate(shelf):
            resale = get_script_resale_value(s, self.calendar)
            values = [s["title"], s["genre"], str(s.get("potential_quality", 0)), f"${resale}M"]
            for col, v in enumerate(values):
                self.shelf_table.setItem(row, col, QtWidgets.QTableWidgetItem(str(v)))

    def _refresh_roster_table(self):
        """Rebuild the roster table with live contract data."""
        roster = []
        for role, contracts in self.studio.contracts.items():
            for contract in contracts:
                person = contract.get("person", {})
                task = contract.get("task")

                roster.append({
                    "name": person.get("name", "Unknown"),
                    "role": role.capitalize()[:-1],
                    "fame": person.get("fame", 0),
                    "salary": contract.get("salary", 0),
                    "specialty": person.get("specialty", {}).get("name") 
                                if isinstance(person.get("specialty"), dict)
                                else person.get("specialty", "-"),
                    "task": f"{task['name']} ({task['remaining']}m)" if task else "Idle",
                    "duration": contract.get("duration", "∞")
                })

        # Update table
        headers = ["Name", "Role", "Fame", "Salary", "Specialty", "Task", "Contract (mths)"]
        self.roster_table.setColumnCount(len(headers))
        self.roster_table.setHorizontalHeaderLabels(headers)
        self.roster_table.setRowCount(len(roster))

        for row, person in enumerate(roster):
            self.roster_table.setItem(row, 0, QtWidgets.QTableWidgetItem(person["name"]))
            self.roster_table.setItem(row, 1, QtWidgets.QTableWidgetItem(person["role"]))
            self.roster_table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(person["fame"])))
            self.roster_table.setItem(row, 3, QtWidgets.QTableWidgetItem(f"${person['salary']:.2f}M"))
            self.roster_table.setItem(row, 4, QtWidgets.QTableWidgetItem(str(person["specialty"])))
            self.roster_table.setItem(row, 5, QtWidgets.QTableWidgetItem(person["task"]))
            self.roster_table.setItem(row, 6, QtWidgets.QTableWidgetItem(str(person["duration"])))


    def _refresh_movies_table(self):
        movies = self.studio.scheduled_movies + self.studio.released_movies
        self.movies_table.setRowCount(len(movies))
        for row, movie in enumerate(movies):
            release_date = movie.get("release_date", ("?", "?"))
            release_str = f"{release_date[1]}/{release_date[0]}"
            director = movie.get("director", {})
            director_name = director.get("name", "N/A") if isinstance(director, dict) else "N/A"

            cast = movie.get("cast", [])
            if isinstance(cast, list):
                actor_name = ", ".join([a.get("name", "N/A") for a in cast])
            elif isinstance(cast, dict):
                actor_name = cast.get("name", "N/A")
            else:
                actor_name = "N/A"

            self.movies_table.setItem(row, 0, QtWidgets.QTableWidgetItem(movie["title"]))
            self.movies_table.setItem(row, 1, QtWidgets.QTableWidgetItem(movie.get("status", "Scheduled")))
            self.movies_table.setItem(row, 2, QtWidgets.QTableWidgetItem(director_name))
            self.movies_table.setItem(row, 3, QtWidgets.QTableWidgetItem(actor_name))
            self.movies_table.setItem(row, 4, QtWidgets.QTableWidgetItem(release_str))

    # === Signal Emitters ===
    def on_new_script(self):
        self.new_script_requested.emit()

    def on_rewrite_script(self):
        selected_row = self.scripts_table.currentRow()
        if selected_row >= 0:
            script = [s for s in self.studio.scripts if s.get("status") in ["first_draft", "rewritten", "approved"]][selected_row]
            self.rewrite_script_requested.emit(script)
        else:
            QtWidgets.QMessageBox.information(self, "Selection", "Please select a script to rewrite.")

    def on_finalize_script(self):
        selected_row = self.scripts_table.currentRow()
        if selected_row >= 0:
            script = [s for s in self.studio.scripts if s.get("status") in ["first_draft", "rewritten", "approved"]][selected_row]
            if script.get("status") == "approved":
                QtWidgets.QMessageBox.information(self, "Action", f"'{script['title']}' is already finalized.")
                return
            self.finalize_script_requested.emit(script)
        else:
            QtWidgets.QMessageBox.information(self, "Selection", "Please select a script to finalize.")

    def on_start_production(self):
        selected_row = self.shelf_table.currentRow()
        if selected_row >= 0 and selected_row < len(self.studio.script_library):
            script = self.studio.script_library[selected_row]
            if script.get("status") != "approved":
                QtWidgets.QMessageBox.information(
                    self, "Action", "You must finalize a script before starting production."
                )
                return
            self.start_production_requested.emit(script)
        else:
            QtWidgets.QMessageBox.information(
                self, "Selection", "Please select a finalized script from the shelf to put into production."
            )

    def on_set_marketing(self):
        selected_row = self.movies_table.currentRow()
        if selected_row >= 0:
            movie = (self.studio.scheduled_movies + self.studio.released_movies)[selected_row]
            if movie.get("status") != "in_production":
                QtWidgets.QMessageBox.information(self, "Action", "You can only set marketing for a movie in production.")
                return
            self.open_post_production_requested.emit(movie)
        else:
            QtWidgets.QMessageBox.information(self, "Selection", "Please select a movie to set its marketing.")

    def on_move_to_shelf(self):
        selected_row = self.scripts_table.currentRow()
        if selected_row >= 0:
            script = [s for s in self.studio.scripts if s.get("status") != "released"][selected_row]
            self.move_to_shelf_requested.emit(script)

    def on_sell_from_shelf(self):
        selected_row = self.shelf_table.currentRow()
        if selected_row >= 0 and selected_row < len(self.studio.script_library):
            script = self.studio.script_library[selected_row]
            self.sell_script_requested.emit(script)

    def on_sell_all(self):
        if self.studio.script_library:
            self.sell_all_requested.emit()
