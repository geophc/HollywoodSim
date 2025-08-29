# scripts_view.py
from PySide6 import QtWidgets, QtCore
# Logic imports are no longer needed here, they will be handled by MainWindow
# from scripts import finalize_script, rewrite_script, generate_script

class ScriptsView(QtWidgets.QWidget):
    # Signals to REQUEST actions from MainWindow
    new_script_requested = QtCore.Signal(object)      # emits the writer object
    finalize_script_requested = QtCore.Signal(object) # emits the script object to finalize
    rewrite_script_requested = QtCore.Signal(object)  # emits the script object to rewrite

    def __init__(self, studio, calendar, casting_pool):
        super().__init__()
        self.studio = studio
        self.calendar = calendar
        self.casting_pool = casting_pool

        layout = QtWidgets.QVBoxLayout(self)

        # Table of scripts
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Title", "Genre", "Status", "Quality", "Potential", "Writer", "Buzz"
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        # Ensure only one row can be selected at a time
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        layout.addWidget(self.table)

        # Buttons
        btn_layout = QtWidgets.QHBoxLayout()
        self.btn_new = QtWidgets.QPushButton("📝 New Script")
        self.btn_finalize = QtWidgets.QPushButton("✅ Finalize")
        self.btn_rewrite = QtWidgets.QPushButton("✍️ Rewrite")
        btn_layout.addWidget(self.btn_new)
        btn_layout.addWidget(self.btn_finalize)
        btn_layout.addWidget(self.btn_rewrite)
        layout.addLayout(btn_layout)

        # Connect buttons
        self.btn_new.clicked.connect(self.request_new_script)
        self.btn_finalize.clicked.connect(self.request_finalize)
        self.btn_rewrite.clicked.connect(self.request_rewrite)

    def refresh_view(self):
        """Refreshes the table with current studio scripts."""
        scripts = self.studio.scripts
        self.table.setRowCount(len(scripts))
        for row, s in enumerate(scripts):
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(s["title"]))
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(s["genre"]))
            self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(s.get("status", "Draft")))
            self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(s.get("quality", 0))))
            self.table.setItem(row, 4, QtWidgets.QTableWidgetItem(str(s.get("potential_quality", 0))))
            writer_name = s.get("writer", {}).get("name", "Unknown")
            self.table.setItem(row, 5, QtWidgets.QTableWidgetItem(writer_name))
            self.table.setItem(row, 6, QtWidgets.QTableWidgetItem(str(s.get("buzz", 0))))
            
    def request_new_script(self):
        """Requests that a new script be created."""
        writers = [c["person"] for c in self.studio.contracts.get("writers", []) if "person" in c]
        if not writers:
            QtWidgets.QMessageBox.warning(self, "No Writers", "You must contract a writer before creating scripts.")
            return
        # Simple: just pick the first writer for now
        writer = writers[0]
        self.new_script_requested.emit(writer)

    def request_finalize(self):
        """Requests that the selected script be finalized."""
        row = self.table.currentRow()
        if row < 0:
            QtWidgets.QMessageBox.information(self, "No Selection", "Please select a script to finalize.")
            return
        script = self.studio.scripts[row]
        
        if script.get("status", "Draft") not in ["first_draft", "rewritten"]:
            QtWidgets.QMessageBox.information(self, "Finalize", f"'{script['title']}' is already finalized or in production.")
            return

        self.finalize_script_requested.emit(script)

    def request_rewrite(self):
        """Requests that the selected script be rewritten."""
        row = self.table.currentRow()
        if row < 0:
            QtWidgets.QMessageBox.information(self, "No Selection", "Please select a script to rewrite.")
            return
        
        writers = [c["person"] for c in self.studio.contracts.get("writers", []) if "person" in c]
        if not writers:
            QtWidgets.QMessageBox.warning(self, "No Writers", "You must contract a writer to rewrite scripts.")
            return

        script = self.studio.scripts[row]
        self.rewrite_script_requested.emit(script)