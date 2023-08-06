from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget

from ... import __version__

about_text = f"""
<p>Vigilant Crypto Snatch</p>

<p>Version {__version__}</p>

<p><a href="https://martin-ueding.github.io/vigilant-crypto-snatch/">Online Documentation</a></p>
"""


class AboutTab(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)
        label = QLabel(about_text.strip())
        label.setTextFormat(Qt.TextFormat.RichText)
        label.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
        label.setOpenExternalLinks(True)
        layout.addWidget(label)
