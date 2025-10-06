# HollywoodSim/game/released_movies_view.py

from PySide6 import QtWidgets, QtGui

class ReleasedMoviesView(QtWidgets.QWidget):
    def __init__(self, studio):
        super().__init__()
        self.studio = studio
        self._setup_ui()

    def _setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        # --- Filters ---
        filter_layout = QtWidgets.QHBoxLayout()
        self.year_filter = QtWidgets.QComboBox()
        self.year_filter.addItem("All Years")
        self.year_filter.currentIndexChanged.connect(self.refresh_view)

        self.genre_filter = QtWidgets.QComboBox()
        self.genre_filter.addItem("All Genres")
        self.genre_filter.currentIndexChanged.connect(self.refresh_view)

        filter_layout.addWidget(QtWidgets.QLabel("Filter:"))
        filter_layout.addWidget(self.year_filter)
        filter_layout.addWidget(self.genre_filter)
        filter_layout.addStretch()
        layout.addLayout(filter_layout)

        # --- Table ---
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels([
            "Title", "Year", "Genre", "Budget", "Quality",
            "Buzz", "Box Office", "Director", "Marketing", "Release"
        ])
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setSortingEnabled(True)
        self.table.itemSelectionChanged.connect(self._show_movie_details)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        layout.addWidget(self.table, 2)

        # --- Detail Panel ---
        self.detail_panel = QtWidgets.QTextEdit()
        self.detail_panel.setReadOnly(True)
        self.detail_panel.setStyleSheet("background: #111; color: #0f0; font-family: monospace;")
        layout.addWidget(self.detail_panel, 1)

        # Initial refresh
        self.refresh_view()

    def refresh_view(self):
        """Refresh table with studio's released movies (movie_history)."""
        movies = self.studio.movie_history if hasattr(self.studio, "movie_history") else []

        # Apply filters
        year_sel = self.year_filter.currentText()
        genre_sel = self.genre_filter.currentText()
        if year_sel != "All Years":
            movies = [m for m in movies if str(m.get("year")) == year_sel]
        if genre_sel != "All Genres":
            movies = [m for m in movies if m.get("genre") == genre_sel]

        # Populate table
        self.table.setRowCount(len(movies))
        for row, m in enumerate(movies):
            values = [
                m.get("title", "N/A"),
                str(m.get("year", "?")),
                m.get("genre", "N/A"),
                m.get("budget_class", "N/A"),
                str(m.get("quality", 0)),
                str(m.get("buzz", 0)),
                f"${m.get('box_office', 0):.2f}M",
                m.get("director", {}).get("name") if isinstance(m.get("director"), dict) else m.get("director", "N/A"),
                m.get("marketing_plan", "None"),
                m.get("release_strategy", "N/A"),
            ]
            for col, v in enumerate(values):
                item = QtWidgets.QTableWidgetItem(str(v))
                self.table.setItem(row, col, item)

        # Refresh filter dropdowns
        years = sorted(set(str(m.get("year")) for m in self.studio.movie_history))
        self.year_filter.blockSignals(True)
        self.year_filter.clear()
        self.year_filter.addItem("All Years")
        self.year_filter.addItems(years)
        self.year_filter.blockSignals(False)

        genres = sorted(set(m.get("genre") for m in self.studio.movie_history if m.get("genre")))
        self.genre_filter.blockSignals(True)
        self.genre_filter.clear()
        self.genre_filter.addItem("All Genres")
        self.genre_filter.addItems(genres)
        self.genre_filter.blockSignals(False)

    def _show_movie_details(self):
        """Display extended details about the selected movie."""
        row = self.table.currentRow()
        if row < 0 or row >= len(self.studio.movie_history):
            return

        movie = self.studio.movie_history[row]

        cast = []
        if isinstance(movie.get("cast"), list):
            cast = [a.get("name", "?") for a in movie.get("cast")]
        elif isinstance(movie.get("cast"), dict):
            cast = [movie["cast"].get("name", "?")]

        details = [
            f"🎬 {movie.get('title', 'Untitled')} ({movie.get('year', '?')})",
            f"Genre: {movie.get('genre', 'N/A')} | Quality: {movie.get('quality', 0)} | Buzz: {movie.get('buzz', 0)}",
            f"Director: {movie.get('director', {}).get('name') if isinstance(movie.get('director'), dict) else movie.get('director', 'N/A')}",
            f"Writer: {movie.get('writer', {}).get('name') if isinstance(movie.get('writer'), dict) else movie.get('writer', 'N/A')}",
            f"Cast: {', '.join(cast) if cast else 'N/A'}",
            f"Box Office: ${movie.get('box_office', 0):.2f}M",
            f"Marketing Plan: {movie.get('marketing_plan', 'None')}",
            f"Release Strategy: {movie.get('release_strategy', 'N/A')}",
            f"Awards: {movie.get('awards', 'None')}",            
        ]

        self.detail_panel.setText("\n".join(details))
