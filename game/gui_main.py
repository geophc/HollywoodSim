# gui_main.py
import sys
from PySide6 import QtWidgets, QtCore

# Import your game logic classes and functions
from views import DashboardView
from studio import Studio
from calendar import GameCalendar
from market import init_market, refresh_market
from market_view import MarketView
from personnel import CastingPool
from scripts_view import ScriptsView
from contracts import create_contract
# ✅ ADDED: Import script logic functions
from scripts import generate_script, finalize_script, rewrite_script


# Main Window Class
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Movie Studio Tycoon")
        self.setGeometry(100, 100, 1200, 800)

        # Initialize models
        self.studio = Studio()
        self.calendar = GameCalendar()
        self.market_pool = init_market()
        self.casting_pool = CastingPool()

        # UI
        self._apply_stylesheet()
        self._setup_ui()
        
        # Initial state
        self.log_message("Welcome to Movie Studio Tycoon!")
        self.update_all_views()


    def _apply_stylesheet(self):
        self.setStyleSheet("""
            QWidget { background-color: #2b2b2b; color: #f0f0f0; font-family: 'Segoe UI'; font-size: 14px; }
            QPushButton { background-color: #555; border: 1px solid #666; padding: 8px; border-radius: 4px; }
            QPushButton:hover { background-color: #6a6a6a; }
            QPushButton:pressed { background-color: #4a4a4a; }
            QTextEdit, QTableWidget, QListView { background-color: #3c3c3c; border: 1px solid #555; border-radius: 4px; }
            QHeaderView::section { background-color: #4a4a4a; padding: 4px; border: 1px solid #555; }
        """)

    def _setup_ui(self):
        main_widget = QtWidgets.QWidget()
        main_layout = QtWidgets.QGridLayout(main_widget)
        self.setCentralWidget(main_widget)

        # --- Create Views (instantiate each view only once) ---
        self.dashboard_page = DashboardView(self.studio, self.calendar)
        self.market_page = MarketView(self.market_pool, self.studio)
        self.scripts_page = ScriptsView(self.studio, self.calendar, self.casting_pool)

        # --- Main content area (Stacked Widget) ---
        self.main_content_area = QtWidgets.QStackedWidget()
        self.main_content_area.addWidget(self.dashboard_page)  # index 0
        self.main_content_area.addWidget(self.market_page)     # index 1
        self.main_content_area.addWidget(self.scripts_page)    # index 2

        # --- Side navigation ---
        nav_widget = QtWidgets.QWidget()
        nav_layout = QtWidgets.QVBoxLayout(nav_widget)
        nav_widget.setFixedWidth(150)

        nav_buttons = {
            "Dashboard": 0,
            "Market": 1,
            "Scripts": 2,
        }
        for name, index in nav_buttons.items():
            button = QtWidgets.QPushButton(name)
            button.clicked.connect(lambda checked=False, i=index: self.main_content_area.setCurrentIndex(i))
            nav_layout.addWidget(button)
        nav_layout.addStretch()

        # --- Log ---
        self.log_output = QtWidgets.QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setMaximumHeight(150)

        # --- Advance month button ---
        self.advance_month_btn = QtWidgets.QPushButton("Advance Month ➡️")
        self.advance_month_btn.setFixedHeight(50)
        self.advance_month_btn.setStyleSheet("font-size: 18px; background-color: #006400;")

        # --- Layout placement ---
        main_layout.addWidget(nav_widget, 0, 0, 2, 1)
        main_layout.addWidget(self.main_content_area, 0, 1)
        main_layout.addWidget(self.log_output, 1, 1)
        main_layout.addWidget(self.advance_month_btn, 2, 0, 1, 2)
        main_layout.setColumnStretch(1, 1)

        # --- Connect Signals ---
        self.advance_month_btn.clicked.connect(self.run_monthly_turn)

        # Market signals
        self.market_page.buy_script_signal.connect(self.handle_buy_script)
        self.market_page.sign_talent_signal.connect(self.handle_sign_talent)
        
        # ✅ ADDED: Scripts signals
        self.scripts_page.new_script_requested.connect(self.handle_new_script)
        self.scripts_page.finalize_script_requested.connect(self.handle_finalize_script)
        self.scripts_page.rewrite_script_requested.connect(self.handle_rewrite_script)


    def log_message(self, msg):
        timestamp = self.calendar.display()
        self.log_output.append(f"[{timestamp}] {msg}")
        self.log_output.verticalScrollBar().setValue(self.log_output.verticalScrollBar().maximum())

    def update_all_views(self):
        """Refreshes the data in all UI views."""
        self.dashboard_page.refresh_data()
        self.market_page.refresh_view()
        self.scripts_page.refresh_view()
        self.log_message("UI views updated.")

    def run_monthly_turn(self):
        self.calendar.advance()
        refresh_market(self.market_pool, self.casting_pool, self.calendar, self.studio)
        self.update_all_views()
        self.log_message("Advanced to new month.")

    # --- Handler Methods for Game Logic ---

    def handle_buy_script(self, script):
        """Handles the logic for buying a script from the market."""
        cost = script.get("value", 0)
        if self.studio.balance >= cost:
            self.studio.balance -= cost
            self.studio.scripts.append(script)
            self.market_pool.scripts.remove(script)
            self.log_message(f"✅ Purchased script '{script['title']}' for ${cost}M.")
            self.update_all_views()
        else:
            QtWidgets.QMessageBox.warning(self, "Insufficient Funds", f"Not enough funds to buy '{script['title']}'.")
            
    def handle_sign_talent(self, data):
        """Handles the logic for signing talent to a contract."""
        talent, role, months = data['talent'], data['role'], data['months']
        contract = create_contract(talent, role, months, talent.get("salary", 1.0))
        self.studio.contracts[role].append(contract)
        self.studio.hire(talent)
        
        # Remove from the correct market pool list
        if role in ["actors", "directors", "writers", "staff"]:
             getattr(self.market_pool, role).remove(talent)

        self.log_message(f"✅ Signed {talent['name']} as a {role[:-1]} for {months} months.")
        self.update_all_views()

    def handle_new_script(self, writer):
        """Handles the logic for generating a new script with a contracted writer."""
        script = generate_script(self.calendar, writer)
        self.studio.scripts.append(script)
        self.log_message(f"📝 New script '{script['title']}' created by {writer['name']}.")
        self.update_all_views()
        
    def handle_finalize_script(self, script):
        """Handles the logic for finalizing a script."""
        final_script = finalize_script(script, self.studio, self.calendar, self.studio.scripts)
        # Replace the old script dict with the updated one
        for i, s in enumerate(self.studio.scripts):
            if s['title'] == final_script['title']:
                self.studio.scripts[i] = final_script
                break
        self.log_message(f"✅ Finalized '{final_script['title']}'. Quality: {final_script['quality']}.")
        self.update_all_views()


    def handle_rewrite_script(self, script):
        """Handles the logic for rewriting a script."""
        # For simplicity, we'll use the first available writer
        writer = [c["person"] for c in self.studio.contracts.get("writers", []) if "person" in c][0]
        rewritten_script = rewrite_script(script, writer, self.calendar)
        for i, s in enumerate(self.studio.scripts):
            if s['title'] == rewritten_script['title']:
                self.studio.scripts[i] = rewritten_script
                break
        self.log_message(f"✍️ Rewrote '{rewritten_script['title']}'. Potential Quality: {rewritten_script['potential_quality']}.")
        self.update_all_views()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())