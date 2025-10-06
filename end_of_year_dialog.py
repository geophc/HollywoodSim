# HollywoodSim/game/end_of_year_dialog.py

from PySide6 import QtWidgets, QtCore

class EndOfYearDialog(QtWidgets.QDialog):
    def __init__(self, studio, year, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"📊 End of Year Report: {year}")
        self.setMinimumSize(600, 500)

        layout = QtWidgets.QVBoxLayout(self)

        # --- Title ---
        title = QtWidgets.QLabel(f"<h2>Studio Report for {year}</h2>")
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)

        # --- Released Movies Table ---
        movies_label = QtWidgets.QLabel("<b>Movies Released:</b>")
        layout.addWidget(movies_label)

        self.movies_table = QtWidgets.QTableWidget(0, 5)
        self.movies_table.setHorizontalHeaderLabels(["Title", "Genre", "Budget", "Quality", "Box Office ($M)"])
        self.movies_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.movies_table)

        # Fill from permanent history
        movies = studio.get_movies_by_year(year)
        self.movies_table.setRowCount(len(movies))
        for row, movie in enumerate(movies):
            self.movies_table.setItem(row, 0, QtWidgets.QTableWidgetItem(movie.get("title", "Untitled")))
            self.movies_table.setItem(row, 1, QtWidgets.QTableWidgetItem(movie.get("genre", "")))
            self.movies_table.setItem(row, 2, QtWidgets.QTableWidgetItem(movie.get("budget_class", "")))
            self.movies_table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(movie.get("quality", ""))))
            self.movies_table.setItem(row, 4, QtWidgets.QTableWidgetItem(f"{movie.get('box_office', 0):.2f}"))

        # --- Summary Stats ---
        summary_label = QtWidgets.QLabel("<b>Summary:</b>")
        layout.addWidget(summary_label)

        total_movies = len(movies)
        total_box = sum(m.get("box_office", 0) for m in movies)
        avg_quality = sum(m.get("quality", 0) for m in movies) / total_movies if total_movies else 0

        summary = QtWidgets.QTextEdit()
        summary.setReadOnly(True)
        summary.setPlainText(
            f"Movies Released: {total_movies}\n"
            f"Total Box Office: ${total_box:.2f}M\n"
            f"Average Quality: {avg_quality:.1f}\n"
            f"Prestige: {studio.prestige}\n"
            f"Reputation: {studio.reputation}\n"
            f"Balance: ${studio.balance:.2f}M\n"
        )
        layout.addWidget(summary)

        # --- Close Button ---
        close_btn = QtWidgets.QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

    def populate_report(self, studio, year=None):
        text = []

        # Use permanent history instead of temporary released_movies
        movies = studio.get_movies_by_year(year) if year else studio.movie_history

        # Awards
        awards = studio.evaluate_awards()
        if awards:
            text.append("🏆 End of Year Awards\n")
            text.append(f"Best Picture: {awards['Best Picture']['title']} "
                        f"(Quality {awards['Best Picture']['quality']})")
            text.append(f"Star of the Year: {awards['Star of the Year']['name']} "
                        f"(Fame {awards['Star of the Year']['fame']})")
            if "Best Director" in awards:
                d = awards["Best Director"]
                text.append(f"Best Director: {d['name']} (Fame {d['fame']})")
        else:
            text.append("No awards this year. Better luck next time!")

        # Summary
        text.append("\n📊 Studio Summary")
        text.append(f"Films Released: {len(movies)}")
        text.append(f"Total Earnings: ${studio.total_earnings:.2f}M")
        text.append(f"Total Expenses: ${studio.total_expenses:.2f}M")
        text.append(f"Prestige: {studio.prestige}")
        text.append(f"Final Balance: ${studio.balance:.2f}M")
        if studio.highest_grossing:
            hg = studio.highest_grossing
            text.append(f"Top Earner: {hg['title']} (${hg['box_office']}M, Quality {hg['quality']})")

        # Filmography
        text.append("\n🎞️ Filmography")
        for m in movies:
            y, mo = m.get("release_date", (0, 0))
            text.append(f"{m['title']} ({m['genre']}, {m['budget_class']}) "
                        f"Released {mo}/{y} "
                        f"Quality {m['quality']} | Box Office ${m['box_office']}M")

        self.report_view.setText("\n".join(text))
