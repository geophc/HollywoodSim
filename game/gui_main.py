# gui_main.py
import sys
from PySide6 import QtWidgets, QtCore, QtGui
import os

# Import your game logic classes and functions
from dashboard_view import DashboardView
from studio import Studio
from calendar import GameCalendar
from market import init_market, refresh_market, adjust_market_prices
from market_view import MarketView
from personnel import CastingPool
from contracts import create_contract
from calendar_view import CalendarView
from post_production_dialog import PostProductionDialog
from post_production import MARKETING_PLANS
from scripts import generate_script, finalize_script, rewrite_script
from rivals import RivalStudio  # Import RivalStudio
import events  # Import the events module

# Main Window Class
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Movie Studio Tycoon")
        self.setGeometry(100, 100, 1400, 900)

        # Initialize models
        self.studio = Studio()
        self.calendar = GameCalendar()
        self.market_pool = init_market()
        self.casting_pool = CastingPool()

        # NEW: Initialize rival studios
        self.rival_studios = [
            RivalStudio("Silver Screen Studios", balance=150, prestige=10),
            RivalStudio("Golden Gate Films", balance=120, prestige=8),
            RivalStudio("Sunset Pictures", balance=100, prestige=5),
        ]

        # UI
        self._apply_stylesheet()
        self._load_font()
        self._setup_ui()
        
        # Initial state
        self.log_message("Welcome to Movie Studio Tycoon!")
        self.log_message(f"Competing against: {', '.join(r.name for r in self.rival_studios)}")
        self.update_all_views()


    def _load_font(self):
        font_path = os.path.join("assets", "fonts", "PressStart2P.ttf")
        id = QtGui.QFontDatabase.addApplicationFont(font_path)
        if id >= 0:
            family = QtGui.QFontDatabase.applicationFontFamilies(id)[0]
            QtWidgets.QApplication.setFont(QtGui.QFont(family, 10))
        else:
            print("⚠️ Pixel font failed to load.")


    def _apply_stylesheet(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #000000;   /* Retro black */
                color: #e0e0e0;              /* Soft gray/white text */
                font-size: 12px;
            }
            QPushButton {
                background-color: #111111;
                border: 2px solid #888888;   /* Gray outline */
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
        main_widget = QtWidgets.QWidget()
        main_layout = QtWidgets.QGridLayout(main_widget)
        self.setCentralWidget(main_widget)

        # --- Main content area (Stacked Widget) ---
        self.main_content_area = QtWidgets.QStackedWidget()

        # --- Create Views ---
        self.dashboard_page = DashboardView(self.studio, self.calendar)
        self.market_page = MarketView(self.market_pool, self.studio)
        self.calendar_page = CalendarView(self.calendar)

        # Add them to stacked widget
        self.main_content_area.addWidget(self.dashboard_page)  # index 0
        self.main_content_area.addWidget(self.market_page)     # index 1
        self.main_content_area.addWidget(self.calendar_page)   # index 2

        # --- Side navigation ---
        nav_widget = QtWidgets.QWidget()
        nav_layout = QtWidgets.QVBoxLayout(nav_widget)
        nav_widget.setFixedWidth(150)

        nav_buttons = {"Dashboard": 0, "Market": 1, "Calendar": 2}
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

        # Dashboard signals
        self.dashboard_page.new_script_requested.connect(self.handle_new_script)
        self.dashboard_page.rewrite_script_requested.connect(self.handle_rewrite_script)
        self.dashboard_page.finalize_script_requested.connect(self.handle_finalize_script)
        self.dashboard_page.start_production_requested.connect(self.handle_start_production)
        self.dashboard_page.open_post_production_requested.connect(self.handle_open_post_production)

        # Market signals
        self.market_page.buy_script_signal.connect(self.handle_buy_script)
        self.market_page.sign_talent_signal.connect(self.handle_sign_talent)

    def _get_turn_number(self):
        """Calculates the total number of months elapsed since the game started."""
        return (self.calendar.year - 2025) * 12 + self.calendar.month

    def log_message(self, msg):
        timestamp = self.calendar.display()
        self.log_output.append(f"[{timestamp}] {msg}")
        self.log_output.verticalScrollBar().setValue(self.log_output.verticalScrollBar().maximum())

    def update_all_views(self):
        """Refreshes the data in all UI views."""
        self.dashboard_page.refresh_data()
        self.market_page.refresh_view()
        # No separate log message here to avoid clutter

    def run_monthly_turn(self):
        # --- 1. Bankruptcy Check ---
        if self.studio.is_bankrupt():
            QtWidgets.QMessageBox.information(self, "Game Over", "💀 Your studio is bankrupt! You can no longer continue.")
            self.advance_month_btn.setEnabled(False)
            self.advance_month_btn.setText("Game Over")
            return

        # --- 2. Advance Time ---
        self.calendar.advance()
        self.log_message(f"📅 A new month begins: {self.calendar.display()}")
        
        # --- 3. Refresh Market ---
        refresh_market(self.market_pool, self.casting_pool, self.calendar, self.studio)
        self.log_message("🛒 Market refreshed with new scripts and talent.")
        
        # --- 4. Rivals Act (NEW) ---
        self.log_message("🏢 Rival studios are making their moves...")
        for rival in self.rival_studios:
            actions = rival.act_month(self.market_pool, self.calendar)
            for action in actions:
                self.log_message(f"   - {action}")

        # --- 5. Market Prices Adjust (NEW) ---
        adjust_market_prices(self.market_pool, self.calendar)
        self.log_message("📉 Market prices adjusted based on supply & demand.")

        # --- 6. Update Movie Statuses ---
        for movie in self.studio.scheduled_movies:
            if movie.get("status") == "in_production":
                if self._get_turn_number() >= movie.get("production_end_turn", 0):
                    movie["status"] = "post_production"
                    self.log_message(f"'{movie['title']}' has finished photography and is in post-production.")

        # --- 7. Handle Releases ---
        released_this_month = self.studio.check_for_releases(self.calendar)
        for movie in released_this_month:
            score, review = self.studio.generate_review(movie)
            self.log_message(f"🎉 '{movie['title']}' released! Critics score: {score}/100. {review}")
        
        # --- 8. Update Finances ---
        self.studio.update_revenue()
        total_salaries = sum(c.get("salary", 1.0) for contracts in self.studio.contracts.values() for c in contracts)
        if total_salaries > 0:
            self.studio.balance -= total_salaries
            self.log_message(f"💰 Paid salaries: ${total_salaries:.2f}M.")
        
        # --- 9. Random Events & News (NEW) ---
        initial_news_count = len(self.studio.newsfeed)
        events.run_random_events(self.studio, self.calendar)
        if len(self.studio.newsfeed) > initial_news_count:
            self.log_message("📰 Hollywood News:")
            for story in self.studio.newsfeed[initial_news_count:]:
                self.log_message(f"• {story}")

        # --- 10. Final Updates ---
        self.studio.renew_contracts()
        self.update_all_views()
        self.log_message("🔄 End of month summary complete.")

    # --- Handler Methods for Game Logic ---
    def handle_buy_script(self, script):
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
        self.log_message(f"'{script['title']}' has been finalized and is ready for production.")
        self.update_all_views()

    def handle_rewrite_script(self, script):
        writer_contracts = self.studio.contracts.get("writers", [])
        if not writer_contracts:
            self.log_message("Cannot rewrite: No writers under contract.")
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
        """Assigns talent and moves a script into the production pipeline."""
        actors = self.studio.list_signed_talent("actors")
        directors = self.studio.list_signed_talent("directors")

        if not actors or not directors:
            QtWidgets.QMessageBox.warning(
                self, "Missing Talent",
                "You need at least one actor and one director under contract."
            )
            return

        # Pick actor
        actor_names = [c["person"]["name"] for c in actors]
        actor_name, ok = QtWidgets.QInputDialog.getItem(
            self, "Select Actor", "Choose lead actor:", actor_names, 0, False
        )
        if not ok: return
        actor_contract = next(c for c in actors if c["person"]["name"] == actor_name)
        actor = actor_contract["person"]

        # Pick director
        director_names = [c["person"]["name"] for c in directors]
        director_name, ok = QtWidgets.QInputDialog.getItem(
            self, "Select Director", "Choose director:", director_names, 0, False
        )
        if not ok: return
        director_contract = next(c for c in directors if c["person"]["name"] == director_name)
        director = director_contract["person"]

        # Create the movie
        movie = self.studio.produce_movie(script, actor, director, self.calendar, months_ahead=6)
        if movie:
            movie["status"] = "in_production"
            movie["production_end_turn"] = self._get_turn_number() + 3
            self.studio.scripts.remove(script)
            self.log_message(f"🎬 Production started for '{movie['title']}' starring {actor['name']}.")
            self.update_all_views()

    def handle_open_post_production(self, movie):
        """Opens the dialog to set marketing and release strategy."""
        dialog = PostProductionDialog(movie, self.studio.balance, self)
        if dialog.exec():
            choices = dialog.get_choices()
            
            plan_name = choices['marketing_plan']
            plan_data = MARKETING_PLANS[plan_name]
            cost = plan_data['cost']
            
            self.studio.balance -= cost
            movie["buzz"] = movie.get("buzz", 0) + plan_data['buzz']
            movie["marketing_spend"] = cost
            movie["marketing_plan"] = plan_name
            movie["release_strategy"] = choices['release_strategy']
            movie["status"] = "scheduled"
            
            self.log_message(f"'{movie['title']}' marketing plan set to '{plan_name}'. Release strategy: '{choices['release_strategy']}'.")
            self.update_all_views()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())