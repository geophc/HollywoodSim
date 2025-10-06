# HollywoodSim/game/auction_dialog.py
from PySide6 import QtWidgets, QtCore

class AuctionDialog(QtWidgets.QDialog):
    def __init__(self, script, studio, rivals, parent=None):
        super().__init__(parent)
        self.script = script
        self.studio = studio
        self.rivals = rivals
        self.current_bid = script.get("value", 1.0)
        self.highest_bidder = "Rival"
        self.setWindowTitle(f"Auction: {script['title']}")
        self._setup_ui()
        
    def _setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(QtWidgets.QLabel(
            f"<b>{self.script['title']}</b> ({self.script['genre']})<br>"
            f"Potential: {self.script.get('potential_quality', 0)}<br>"
            f"Starting Price: ${self.current_bid}M"
        ))

        self.status_label = QtWidgets.QLabel(f"Current Bid: ${self.current_bid}M by {self.highest_bidder}")
        layout.addWidget(self.status_label)

        self.bid_input = QtWidgets.QDoubleSpinBox()
        self.bid_input.setPrefix("$")
        self.bid_input.setRange(self.current_bid + 0.1, self.studio.balance)
        self.bid_input.setSingleStep(0.1)
        layout.addWidget(self.bid_input)

        btn_bid = QtWidgets.QPushButton("Place Bid")
        btn_pass = QtWidgets.QPushButton("Pass")
        btn_bid.clicked.connect(self._place_bid)
        btn_pass.clicked.connect(self.reject)
        layout.addWidget(btn_bid)
        layout.addWidget(btn_pass)

    def _simulate_rival_bids(self):
        from random import uniform
        # Each rival may decide to bid up to 140% of base value
        for rival in self.rivals:
            if rival.balance > self.current_bid * 1.1:
                rival_bid = round(uniform(self.current_bid, self.current_bid * 1.3), 2)
                if rival_bid > self.current_bid:
                    self.current_bid = rival_bid
                    self.highest_bidder = rival.name
        self.status_label.setText(f"Current Bid: ${self.current_bid}M by {self.highest_bidder}")

    def _place_bid(self):
        player_bid = round(self.bid_input.value(), 2)
        if player_bid <= self.current_bid:
            QtWidgets.QMessageBox.warning(self, "Low Bid", "Your bid must exceed the current bid.")
            return
        if player_bid > self.studio.balance:
            QtWidgets.QMessageBox.warning(self, "Insufficient Funds", "You can't afford that bid.")
            return
        self.current_bid = player_bid
        self.highest_bidder = self.studio.name
        self._simulate_rival_bids()

        # Check if rivals outbid; continue until no higher bids
        if self.highest_bidder == self.studio.name:
            QtWidgets.QMessageBox.information(self, "Auction Won", f"You won '{self.script['title']}' for ${self.current_bid}M!")
            self.accept()
        else:
            QtWidgets.QMessageBox.information(self, "Outbid", f"Rivals outbid you at ${self.current_bid}M.")
            self.reject()

    def get_result(self):
        return self.highest_bidder, self.current_bid
