# HollywoodSim/game/calendar_view.py

from PySide6 import QtWidgets, QtCore, QtGui


class CalendarView(QtWidgets.QWidget):
    """
    A rich, interactive GUI panel showing the current in-game industry calendar.
    Includes events, trending genres, forecasts, market reports, and upcoming shifts.
    """

    def __init__(self, calendar_model, parent=None):
        super().__init__(parent)
        self.calendar = calendar_model

        layout = QtWidgets.QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # --- Title ---
        title = QtWidgets.QLabel("🗓️ Industry Calendar Dashboard")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 26px; font-weight: bold;
            color: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 #FFD700, stop:1 #FF6347
            );
            padding: 10px;
        """)
        layout.addWidget(title)

        # --- Current Month Highlight ---
        self.current_event_card = QtWidgets.QLabel()
        self.current_event_card.setAlignment(QtCore.Qt.AlignCenter)
        self.current_event_card.setMinimumHeight(120)
        self.current_event_card.setWordWrap(True)
        self.current_event_card.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        self.current_event_card.setOpenExternalLinks(True)
        self.current_event_card.setStyleSheet("""
            QLabel {
                background-color: #222;
                border: 2px solid #FFD700;
                border-radius: 12px;
                padding: 15px;
                color: #f5f5f5;
                font-size: 16px;
            }
            QLabel:hover {
                background-color: #2e2e2e;
                border-color: #FF6347;
            }
        """)
        layout.addWidget(self.current_event_card)

        # --- Market Report ---
        self.market_label = QtWidgets.QLabel()
        self.market_label.setAlignment(QtCore.Qt.AlignCenter)
        self.market_label.setStyleSheet("font-size: 14px; color: #90EE90;")
        layout.addWidget(self.market_label)

        # --- Trending Genres ---
        self.trending_label = QtWidgets.QLabel()
        self.trending_label.setAlignment(QtCore.Qt.AlignCenter)
        self.trending_label.setStyleSheet("color: #FFA500; font-size: 14px;")
        layout.addWidget(self.trending_label)

        # --- Forecast with Hype Bar ---
        forecast_container = QtWidgets.QVBoxLayout()
        self.forecast_label = QtWidgets.QLabel()
        self.forecast_label.setAlignment(QtCore.Qt.AlignCenter)
        self.forecast_label.setStyleSheet("color: #87CEFA; font-size: 14px;")
        forecast_container.addWidget(self.forecast_label)

        self.forecast_bar = QtWidgets.QProgressBar()
        self.forecast_bar.setRange(0, 100)
        self.forecast_bar.setTextVisible(True)
        self.forecast_bar.setFormat("Market Hype: %p%")
        self.forecast_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #555;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #00BFFF;
            }
        """)
        forecast_container.addWidget(self.forecast_bar)
        layout.addLayout(forecast_container)

        # --- Upcoming Events Table ---
        upcoming_label = QtWidgets.QLabel("📅 Upcoming Events (Next 3 Months):")
        upcoming_label.setStyleSheet("font-size: 15px; font-weight: bold; color: #FFD700;")
        layout.addWidget(upcoming_label)

        self.events_table = QtWidgets.QTableWidget()
        self.events_table.setColumnCount(3)
        self.events_table.setHorizontalHeaderLabels(["Month", "Year", "Event"])
        self.events_table.horizontalHeader().setStretchLastSection(True)
        self.events_table.setAlternatingRowColors(True)
        self.events_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #444;
                background-color: #1c1c1c;
                alternate-background-color: #2a2a2a;
                color: #f0f0f0;
            }
            QHeaderView::section {
                background-color: #333;
                font-weight: bold;
                color: #FFD700;
                padding: 5px;
            }
        """)
        layout.addWidget(self.events_table)

        layout.addStretch()
        self.refresh_view()

    def refresh_view(self):
        """Update the calendar info from the model with more dynamic formatting."""

        # Current Event Display
        current_event = self.calendar.get_current_event()
        if current_event:
            # Importance is now expected in the event dict from GameCalendar
            importance_color = "#FF4500" if current_event.get("importance", "normal") == "high" else "#00BFFF"
            self.current_event_card.setText(
                f"<b style='font-size:18px; color:{importance_color};'>"
                f"{self.calendar.month_name()} {self.calendar.year}</b><br>"
                f"🎭 <i>{current_event['name']}</i><br>"
                f"🎬 Bonus Genres: {', '.join(current_event['bonus_genres'])}"
            )
            # Description is now expected in the event dict
            self.current_event_card.setToolTip(f"Special industry event: {current_event.get('description', 'Annual event.')}")
        else:
            self.current_event_card.setText(
                f"<b>{self.calendar.month_name()} {self.calendar.year}</b><br>"
                f"No major industry events this month."
            )

        # Trending and Forecast
        self.trending_label.setText(
            f"🔥 <b>Trending Genres:</b> {', '.join(self.calendar.trending_genres)}"
        )
        self.forecast_label.setText(
            f"🔮 <b>Forecast:</b> {', '.join(self.calendar.forecast_genres)}"
        )

        # Forecast Hype Gauge - Uses the new get_hype_index() method
        hype = self.calendar.get_hype_index() # e.g., integer 0–100
        self.forecast_bar.setValue(hype)

        # Market Info
        report = self.calendar.get_market_report()
        if report:
            self.market_label.setText(
                f"💹 <b>Market Index:</b> {report['market_index']} ({report['trend']})<br>"
                f"📈 Sentiment: {report['sentiment']} — 💰 Economy: {report['economy']}"
            )

        # Upcoming Events
        # Filter annual events for the rest of the year
        upcoming = [
            (self.calendar.year, m, e)
            for m, e in self.calendar.events.items()
            if m >= self.calendar.month
        ][:3]

        self.events_table.setRowCount(len(upcoming))
        for row, (year, month, event) in enumerate(upcoming):
            self.events_table.setItem(row, 0, QtWidgets.QTableWidgetItem(self.calendar.month_name_from_num(month)))
            self.events_table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(year)))

            event_item = QtWidgets.QTableWidgetItem(event["name"])
            # Importance check based on the new event data structure
            if event.get("importance") == "high":
                event_item.setForeground(QtGui.QBrush(QtGui.QColor("#FF4500")))
                event_item.setFont(QtGui.QFont("Arial", 10, QtGui.QFont.Bold))
                event_item.setToolTip(event.get("description", "Major industry shift"))
            self.events_table.setItem(row, 2, event_item)