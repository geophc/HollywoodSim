# HollywoodSim/game/gui_main.py
# Main GUI application for HollywoodSim using PySide6.
# Handles window setup, navigation, UI integration, and core game loop.

import sys
import os
import traceback
from PySide6 import QtWidgets, QtGui, QtCore

# --- Game Logic Imports ---
from studio import Studio
from calendar_1 import GameCalendar
from market import init_market, refresh_market, adjust_market_prices, populate_initial_market
from contracts import create_contract
from scripts import generate_script, rewrite_script
from rivals import RivalStudio
from auction_dialog import AuctionDialog
from personnel import CastingPool
from library import get_script_resale_value
from draft_production import draft_production
from talent_tasks import assign_task, progress_tasks, TASKS
from post_production import MARKETING_PLANS, RELEASE_STRATEGIES
import events

# --- UI Imports ---
from dashboard_view import DashboardView
from market_view import MarketView
from calendar_view import CalendarView
from finance_view import FinanceView
from released_movies_view import ReleasedMoviesView
from post_production_dialog import PostProductionDialog
from end_of_year_dialog import EndOfYearDialog


class MainWindow(QtWidgets.QMainWindow):
    """Main application window for HollywoodSim."""

    # === Initialization & Setup ===
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Movie Studio Tycoon")
        self.setGeometry(100, 100, 1400, 900)

        # Initialize models
        self.studio = Studio()
        self.calendar = GameCalendar()
        self.market_pool = init_market()
        self.casting_pool = CastingPool()
        self.ledger = []  # Tracks financial records

        # Populate initial market & rivals
        populate_initial_market(self.market_pool, self.calendar)
        self.rival_studios = [
            RivalStudio("Silver Screen Studios", balance=150, prestige=10),
            RivalStudio("Golden Gate Films", balance=120, prestige=8),
            RivalStudio("Sunset Pictures", balance=100, prestige=5),
        ]

        # UI setup
        self._apply_stylesheet()
        self._load_font()
        self._setup_ui()

        # Initial log
        self.log_message("Welcome to Movie Studio Tycoon!")
        self.log_message(f"Competing against: {', '.join(r.name for r in self.rival_studios)}")
        self.update_all_views()

    def _load_font(self):
        """Load the game’s custom monospace font if available."""
        font_path = os.path.join("assets", "fonts", "SourceCodePro-Regular.ttf")
        font_id = QtGui.QFontDatabase.addApplicationFont(font_path)
        if font_id >= 0:
            family = QtGui.QFontDatabase.applicationFontFamilies(font_id)[0]
            QtWidgets.QApplication.setFont(QtGui.QFont(family, 10))
        else:
            print("⚠️ Pixel font failed to load.")

    def _apply_stylesheet(self):
        """Apply dark theme styling to the entire application."""
        self.setStyleSheet("""
            QWidget {
                background-color: #000000;
                color: #e0e0e0;
                font-size: 12px;
            }
            QPushButton {
                background-color: #111111;
                border: 2px solid #888888;
                padding: 4px 8px;
                color: #f5f5f5;
            }
            QPushButton:hover {
                background-color: #222222;
            }
            QHeaderView::section {
                background-color: #111111;
                color: #ffffff;
                border: 1px solid #555555;
            }
            QTableWidget {
                gridline-color: #555555;
                selection-background-color: #444444;
                selection-color: #ffffff;
                alternate-background-color: #1a1a1a;
                background-color: #0d0d0d;
            }
        """)

    def _setup_ui(self):
        """Create main layout with navigation, content area, logs, and controls."""
        main_widget = QtWidgets.QWidget()
        main_layout = QtWidgets.QGridLayout(main_widget)
        self.setCentralWidget(main_widget)

        # Core pages
        self.main_content_area = QtWidgets.QStackedWidget()
        self.dashboard_page = DashboardView(self.studio, self.calendar)
        self.market_page = MarketView(self.market_pool, self.studio)
        self.calendar_page = CalendarView(self.calendar)
        self.finance_page = FinanceView(self.studio, self.ledger)
        self.released_page = ReleasedMoviesView(self.studio)

        # Menubar & pages
        self._create_menubar()
        self.main_content_area.addWidget(self.dashboard_page)
        self.main_content_area.addWidget(self.market_page)
        self.main_content_area.addWidget(self.calendar_page)
        self.main_content_area.addWidget(self.finance_page)
        self.main_content_area.addWidget(self.released_page)

        # Navigation / Logs / Controls
        nav_widget = self._create_navigation_panel()
        self.log_output = self._create_log_output()
        self.advance_month_btn = self._create_advance_month_button()

        # Layout placement
        main_layout.addWidget(nav_widget, 0, 0, 2, 1)
        main_layout.addWidget(self.main_content_area, 0, 1)
        main_layout.addWidget(self.log_output, 1, 1)
        main_layout.addWidget(self.advance_month_btn, 2, 0, 1, 2)
        main_layout.setColumnStretch(1, 1)

        # Connect signals
        self._connect_signals()

    # === Navigation & Menus ===
    def _create_navigation_panel(self):
        """Build left-hand navigation with buttons for main pages."""
        nav_widget = QtWidgets.QWidget()
        nav_layout = QtWidgets.QVBoxLayout(nav_widget)
        nav_widget.setFixedWidth(150)

        nav_buttons = {
            "Dashboard": 0,
            "Market": 1,
            "Calendar": 2,
            "Finance": 3,
            "Released": 4
        }
        for name, index in nav_buttons.items():
            button = QtWidgets.QPushButton(name)
            button.clicked.connect(lambda checked=False, i=index: self.main_content_area.setCurrentIndex(i))
            nav_layout.addWidget(button)

        nav_layout.addStretch()
        return nav_widget

    def _create_menubar(self):
        """Set up menubar with reports and talent management actions."""
        menubar = self.menuBar()

        # Reports
        reports_menu = menubar.addMenu("Reports")
        end_of_year_action = QtGui.QAction("Show End of Year Report", self)
        end_of_year_action.triggered.connect(self._handle_end_of_year)
        reports_menu.addAction(end_of_year_action)

        # Talent
        talent_menu = menubar.addMenu("Talent")
        assign_task_action = QtGui.QAction("Assign Task", self)
        assign_task_action.triggered.connect(self._handle_assign_task)
        talent_menu.addAction(assign_task_action)

    def _create_log_output(self):
        """Bottom log window for showing in-game events."""
        log_output = QtWidgets.QTextEdit()
        log_output.setReadOnly(True)
        log_output.setMaximumHeight(150)
        return log_output

    def _create_advance_month_button(self):
        """Create the big 'Advance Month' button."""
        button = QtWidgets.QPushButton("Advance Month ➡️")
        button.setFixedHeight(50)
        button.setStyleSheet("font-size: 18px; background-color: #006400;")
        return button

    def _connect_signals(self):
        """Connect UI actions to handlers."""
        self.advance_month_btn.clicked.connect(self.run_monthly_turn)

        # Dashboard signals
        self.dashboard_page.new_script_requested.connect(self.handle_new_script)
        self.dashboard_page.rewrite_script_requested.connect(self.handle_rewrite_script)
        self.dashboard_page.finalize_script_requested.connect(self.handle_finalize_script)
        self.dashboard_page.start_production_requested.connect(self.handle_start_production)
        self.dashboard_page.open_post_production_requested.connect(self.handle_open_post_production)
        self.dashboard_page.move_to_shelf_requested.connect(self.handle_move_to_shelf)
        self.dashboard_page.sell_script_requested.connect(self.handle_sell_script)
        self.dashboard_page.sell_all_requested.connect(self.handle_sell_all_scripts)
        self.dashboard_page.assign_task_requested.connect(self._handle_assign_task)

        # Market signals
        self.market_page.buy_script_signal.connect(self.handle_buy_script)
        self.market_page.sign_talent_signal.connect(self.handle_sign_talent)
        self.market_page.move_to_shelf_signal.connect(self.handle_move_to_shelf)
        self.market_page.sell_script_signal.connect(self.handle_sell_script)
        self.market_page.sell_all_signal.connect(self.handle_sell_all_scripts)

    # === Handlers (UI Actions) ===
    def handle_buy_script(self, script):
        dialog = AuctionDialog(script, self.studio, self.rival_studios, self)
        if dialog.exec():
            winner, price = dialog.get_result()
            if winner == self.studio.name:
                self.studio.balance -= price
                self.studio.scripts.append(script)
                if script in self.market_pool.scripts:
                    self.market_pool.scripts.remove(script)
                self.log_message(f"🏆 You won '{script['title']}' for ${price}M at auction!")
            else:
                self.market_pool.scripts.remove(script)
                self.log_message(f"🏢 {winner} won '{script['title']}' at ${price}M.")
        self.update_all_views()

    def handle_sign_talent(self, data):
        talent, role, months = data['talent'], data['role'], data['months']
        contract = create_contract(talent, role, months, talent.get("salary", 1.0))
        self.studio.contracts[role].append(contract)
        self.studio.hire(talent)
        if role in ["actors", "directors", "writers", "staff"]:
            getattr(self.market_pool, role).remove(talent)
        self.log_message(f"✅ Signed {talent['name']} as a {role[:-1]} for {months} months.")
        self.update_all_views()

    def handle_new_script(self):
        writers = [c["person"] for c in self.studio.contracts.get("writers", []) if "person" in c]
        if not writers:
            QtWidgets.QMessageBox.warning(self, "No Writers", "You must have a writer under contract to create a new script.")
            return

        writer_names = [w['name'] for w in writers]
        writer_name, ok = QtWidgets.QInputDialog.getItem(self, "Select Writer", "Choose a writer:", writer_names, 0, False)
        if ok and writer_name:
            writer = next(w for w in writers if w['name'] == writer_name)
            script = generate_script(self.calendar, writer)
            self.studio.scripts.append(script)
            self.log_message(f"📝 New script '{script['title']}' created by {writer['name']}.")
            self.update_all_views()

    def handle_finalize_script(self, script):
        script['status'] = 'approved'
        if script in self.studio.scripts:
            self.studio.scripts.remove(script)
        self.studio.script_library.append(script)
        self.log_message(f"📦 '{script['title']}' finalized and moved to the shelf.")
        self.update_all_views()

    def handle_rewrite_script(self, script):
        writer_contracts = self.studio.contracts.get("writers", [])
        if not writer_contracts:
            self.log_message("Cannot rewrite: No writers under contract.", is_error=True)
            return
        writer = writer_contracts[0]["person"]
        rewritten_script = rewrite_script(script, writer, self.calendar)
        for i, s in enumerate(self.studio.scripts):
            if s['title'] == rewritten_script['title']:
                self.studio.scripts[i] = rewritten_script
                break
        self.log_message(f"✍️ Rewrote '{rewritten_script['title']}'. Potential Quality: {rewritten_script['potential_quality']}.")
        self.update_all_views()

    def handle_start_production(self, script):
        actors = self.studio.list_signed_talent("actors")
        directors = self.studio.list_signed_talent("directors")
        if not actors or not directors:
            QtWidgets.QMessageBox.warning(self, "Missing Talent", "You need at least one actor and one director under contract.")
            return

        actor_contract = self._select_talent_dialog(actors, "Actor")
        if not actor_contract:
            return
        director_contract = self._select_talent_dialog(directors, "Director")
        if not director_contract:
            return

        actor = actor_contract["person"]
        director = director_contract["person"]

        if script not in self.studio.script_library:
            QtWidgets.QMessageBox.warning(self, "Invalid Script", "This script must be taken from your shelf to start production.")
            return

        movie = self.studio.produce_movie(script, [actor], director, self.calendar, months_ahead=6)
        if movie:
            movie["status"] = "in_production"
            movie["production_end_turn"] = self._get_turn_number() + 3
            self.studio.script_library.remove(script)
            lead_name = actor['name'] if actor else "Unknown"
            self.log_message(f"🎬 Production started for '{movie['title']}' starring {lead_name}.")
            self.update_all_views()

    def _select_talent_dialog(self, talent_contracts, role_name):
        names = [c["person"]["name"] for c in talent_contracts]
        selected_name, ok = QtWidgets.QInputDialog.getItem(self, f"Select {role_name}", f"Choose {role_name.lower()}:", names, 0, False)
        if ok and selected_name:
            return next(c for c in talent_contracts if c["person"]["name"] == selected_name)
        return None

    def handle_open_post_production(self, movie):
        dialog = PostProductionDialog(movie, self.studio.balance, self)
        if dialog.exec():
            choices = dialog.get_choices()
            plan_name = choices['marketing_plan']
            plan_data = MARKETING_PLANS.get(plan_name, MARKETING_PLANS["None"])  # fallback
            cost = plan_data['cost']

            # Apply plan
            self.studio.balance -= cost
            movie["buzz"] = movie.get("buzz", 0) + plan_data['buzz']
            movie["marketing_spend"] = cost
            movie["marketing_plan"] = plan_name
            movie["release_strategy"] = choices['release_strategy']
            movie["status"] = "scheduled"

            self.log_message(
                f"'{movie['title']}' marketing plan set to '{plan_name}'. "
                f"Release: '{choices['release_strategy']}'."
            )
            self.update_all_views()


    def handle_move_to_shelf(self, script):
        if script in self.market_pool.scripts:
            self.market_pool.scripts.remove(script)
        elif script in self.studio.scripts:
            self.studio.scripts.remove(script)
        self.studio.script_library.append(script)
        self.log_message(f"📦 Moved '{script['title']}' to the shelf.")
        self.update_all_views()

    def handle_sell_script(self, script):
        if script not in self.studio.script_library:
            return
        value = get_script_resale_value(script, self.calendar)
        self.studio.script_library.remove(script)
        self.studio.balance += value
        self.log_message(f"💰 Sold '{script['title']}' for ${value:.2f}M.")
        self.update_all_views()

    def handle_sell_all_scripts(self):
        if not self.studio.script_library:
            return
        total = sum(get_script_resale_value(s, self.calendar) for s in self.studio.script_library)
        count = len(self.studio.script_library)
        self.studio.balance += total
        self.studio.script_library.clear()
        self.log_message(f"💰 Sold {count} scripts from the shelf for a total of ${total:.2f}M.")
        self.update_all_views()

    def _handle_assign_task(self):
        from talent_task_dialog import TalentTaskDialog
        dialog = TalentTaskDialog(self.studio.contracts, self)
        if dialog.exec():
            contract, task_name = dialog.get_selection()
            if contract and task_name:
                if contract.get("task"):
                    QtWidgets.QMessageBox.warning(self, "Already Busy", f"{contract['person']['name']} is already working on '{contract['task']['name']}' ({contract['task']['remaining']} month(s) left).")
                    return
                try:
                    assign_task(contract, task_name)
                    self.log_message(f"📝 Assigned {contract['person']['name']} to {task_name}.")
                    self.update_all_views()
                except Exception as e:
                    QtWidgets.QMessageBox.warning(self, "Error", str(e))

    # === Game Loop ===
    def run_monthly_turn(self):
        try:
            if not self._check_bankruptcy():
                return
            self._advance_time()
            self._update_market()
            self._process_rival_turns()
            self._update_productions()
            self._process_movie_releases()
            self._update_finances()
            self._update_talent_tasks()
            self._run_random_events()
            self._finalize_month()
            if self.calendar.month == 12:
                self._handle_end_of_year()
        except Exception as e:
            error_message = f"An unexpected error occurred: {e}"
            traceback_info = traceback.format_exc()
            self.log_message(error_message, is_error=True)
            print(traceback_info)
            QtWidgets.QMessageBox.critical(self, "Error", f"{error_message}\n\nSee console for details.")

    # === Monthly Turn Phases ===
    def _check_bankruptcy(self):
        if self.studio.is_bankrupt():
            QtWidgets.QMessageBox.information(self, "Game Over", "💀 Your studio is bankrupt! You can no longer continue.")
            self.advance_month_btn.setEnabled(False)
            self.advance_month_btn.setText("Game Over")
            return False
        return True

    def _advance_time(self):
        self.calendar.advance()
        self.log_message(f"📅 A new month begins: {self.calendar.display()}")

    def _update_market(self):
        refresh_market(self.market_pool, self.casting_pool, self.calendar, self.studio)
        self.log_message("🛒 Market refreshed with new scripts and talent.")
        adjust_market_prices(self.market_pool, self.calendar)
        self.log_message("📉 Market prices adjusted based on supply & demand.")

    def _process_rival_turns(self):
        self.log_message("🏢 Rival studios are making their moves...")
        for rival in self.rival_studios:
            actions = rival.act_month(self.market_pool, self.calendar)
            for action in actions:
                self.log_message(f"   - {action}")

    def _update_productions(self):
        for movie in self.studio.scheduled_movies:
            if movie.get("status") == "in_production":
                if self._get_turn_number() >= movie.get("production_end_turn", 0):
                    movie["status"] = "post_production"
                    self.log_message(f"'{movie['title']}' has finished photography and is in post-production.")

    def _process_movie_releases(self):
        released_this_month = self.studio.check_for_releases(self.calendar)
        for movie in released_this_month:
            score, review = self.studio.generate_review(movie)
            cast = movie.get("cast", [])
            lead = cast[0]['name'] if cast else "Unknown"
            self.log_message(f"🎉 '{movie['title']}' released! Lead: {lead}. Critics score: {score}/100. {review}")

    def _update_finances(self):
        before_balance = self.studio.balance
        self.studio.update_revenue()
        revenue = self.studio.balance - before_balance
        total_salaries = sum(c.get("salary", 1.0) for contracts in self.studio.contracts.values() for c in contracts)
        if total_salaries > 0:
            self.studio.balance -= total_salaries
            self.log_message(f"💰 Paid salaries: ${total_salaries:.2f}M.")
        self.studio.record_financials(self.calendar, revenue=revenue, expenses=total_salaries, note="Monthly operations")

    def _update_talent_tasks(self):
        completed = progress_tasks(self.studio.contracts, self.studio)
        for result in completed:
            person = result['person']['name']
            task = result['task']
            for outcome in result['outcome']:
                self.log_message(f"📝 Task complete: {person} finished {task}. {outcome}")

    def _run_random_events(self):
        initial_news_count = len(self.studio.newsfeed)
        events.run_random_events(self.studio, self.calendar)
        if len(self.studio.newsfeed) > initial_news_count:
            self.log_message("📰 Hollywood News:")
            for story in self.studio.newsfeed[initial_news_count:]:
                self.log_message(f"• {story}")

    def _finalize_month(self):
        self.studio.renew_contracts()
        self.update_all_views()
        self.log_message("🔄 End of month summary complete.")

    def _handle_end_of_year(self):
        dialog = EndOfYearDialog(self.studio, self.calendar.year, self)
        dialog.exec()
        self.log_message(f"📊 End of Year {self.calendar.year} report generated.")

    # === Utilities ===
    def _get_turn_number(self):
        return (self.calendar.year - 2025) * 12 + self.calendar.month

    def log_message(self, msg, is_error=False):
        timestamp = self.calendar.display()
        prefix = "🔥" if is_error else f"[{timestamp}]"
        self.log_output.append(f"{prefix} {msg}")
        self.log_output.verticalScrollBar().setValue(self.log_output.verticalScrollBar().maximum())

    def _record_transaction(self, description, amount):
        balance = self.studio.balance
        self.ledger.append({
            "date": self.calendar.display(),
            "description": description,
            "amount": amount,
            "balance": balance
        })

    def update_all_views(self):
        self.dashboard_page.refresh_data()
        self.market_page.refresh_view()
        self.calendar_page.refresh_view()
        self.finance_page.refresh_view()
        self.released_page.refresh_view()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
