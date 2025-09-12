# calendar_view.py
from PySide6 import QtWidgets, QtCore

class CalendarView(QtWidgets.QWidget):
    """
    A GUI panel showing the current month, events, forecasts, and upcoming industry shifts.
    Works with GameCalendar.
    """

    def __init__(self, calendar_model, parent=None):
        super().__init__(parent)
        self.calendar = calendar_model

        layout = QtWidgets.QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # --- Title ---
        title = QtWidgets.QLabel("🗓️ Industry Calendar")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #FFD700;")
        layout.addWidget(title)

        # --- Current Month / Event ---
        self.current_event_card = QtWidgets.QLabel()
        self.current_event_card.setAlignment(QtCore.Qt.AlignCenter)
        self.current_event_card.setMinimumHeight(100)
        self.current_event_card.setStyleSheet("""
            QLabel {
                background-color: #1c1c1c; border: 2px solid #00BFFF;
                border-radius: 10px; padding: 10px; color: #f5f5f5;
                font-size: 16px;
            }
        """)
        layout.addWidget(self.current_event_card)

        # --- Trending Genres ---
        self.trending_label = QtWidgets.QLabel()
        self.trending_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.trending_label)

        # --- Forecast Genres ---
        self.forecast_label = QtWidgets.QLabel()
        self.forecast_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.forecast_label)

        # --- Upcoming Events Table ---
        layout.addWidget(QtWidgets.QLabel("📅 Upcoming Events (next 3 months):"))
        self.events_table = QtWidgets.QTableWidget()
        self.events_table.setColumnCount(3)
        self.events_table.setHorizontalHeaderLabels(["Month", "Year", "Event"])
        self.events_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.events_table)

        layout.addStretch()
        self.refresh_view()

    def refresh_view(self):
        """Update the calendar info from the model."""
        # Current Event
        # calendar_view.py - inside refresh_view
        current_event = self.calendar.get_current_event()
        if current_event:
            self.current_event_card.setText(
                f"<b>{self.calendar.month_name()} {self.calendar.year}</b><br>"
                f"🎭 <i>{current_event}</i>"
            )
        else:
            self.current_event_card.setText(
                f"<b>{self.calendar.month_name()} {self.calendar.year}</b><br>No major industry events this month."
            )

        # Upcoming Events
        upcoming = [(self.calendar.year, m, e) for m, e in self.calendar.events.items() if m >= self.calendar.month][:3]
        self.events_table.setRowCount(len(upcoming))
        for row, (year, month, event) in enumerate(upcoming):
            self.events_table.setItem(row, 0, QtWidgets.QTableWidgetItem(self.calendar.month_name()))
            self.events_table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(year)))
            self.events_table.setItem(row, 2, QtWidgets.QTableWidgetItem(event))
