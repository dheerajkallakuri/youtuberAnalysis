import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QLineEdit, QFormLayout, QTextBrowser, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QByteArray, QBuffer
import re, requests
from youtuberData import get_youtube_data, get_channel_id
from quantllama import SummarizeYoutuber

class YouTubeInfoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('YouTuber Analysis')
        self.setGeometry(100, 100, 800, 800)

        # Create a central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Create a layout
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Create input field for YouTube link
        self.link_input = QLineEdit(self)
        self.link_input.setPlaceholderText('Enter YouTube Channel Link')
        self.layout.addWidget(self.link_input)

        # Create a button to fetch channel info
        self.fetch_button = QPushButton('Fetch Channel Info', self)
        self.fetch_button.clicked.connect(self.fetch_channel_info)
        self.layout.addWidget(self.fetch_button)

        # Create widgets to display channel info
        self.logo_label = QLabel(self)
        self.layout.addWidget(self.logo_label)

        self.channel_name_label = QLabel(self)
        self.layout.addWidget(self.channel_name_label)

        self.channel_id_label = QLabel(self)
        self.layout.addWidget(self.channel_id_label)

        self.subscribers_label = QLabel(self)
        self.layout.addWidget(self.subscribers_label)

        self.videos_label = QLabel(self)
        self.layout.addWidget(self.videos_label)

        self.views_label = QLabel(self)
        self.layout.addWidget(self.views_label)

        self.location_label = QLabel(self)
        self.layout.addWidget(self.location_label)

        self.summary_text = QTextBrowser(self)
        self.summary_text.setFixedHeight(200)
        self.layout.addWidget(self.summary_text)

        self.top_videos_text = QTextBrowser(self)
        self.layout.addWidget(self.top_videos_text)
    
    def validate_youtube_url(self, url):
        if "@" in url:
            pattern=re.compile(r'https://www\.youtube\.com/@[a-zA-Z0-9_-]+')
        else:
            pattern = re.compile(r'^https://www\.youtube\.com/channel/UC[a-zA-Z0-9_-]+$')
        return pattern.match(url) is not None

    def extract_channel_id(self, url):
        if "@" in url:
            handle = url.split('@')[1]
            match = get_channel_id(handle)
            return match
        else:
            match = re.search(r'/channel/UC[a-zA-Z0-9_-]+', url)
            return match.group(0).replace('/channel/', '') if match else None

    def show_message(self, title, message):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()
    
    def display_image_from_url(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                image_data = QByteArray(response.content)
                image = QPixmap()
                image.loadFromData(image_data)
                image = image.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.logo_label.setPixmap(image)
            else:
                self.logo_label.setText('Failed to load image')
        except Exception as e:
            self.logo_label.setText(f'Error: {str(e)}')

    def update_summary_text(self, summary):
        self.summary_text.setHtml(f"<h3>Summary:</h3><p>{summary}</p>")

    def fetch_channel_info(self):
        channel_url = self.link_input.text().strip()
        
        if not self.validate_youtube_url(channel_url):
            # self.channel_id_label.setText('Invalid YouTube URL')
            self.show_message("Error", "Invalid YouTube URL")
            return

        channel_id = self.extract_channel_id(channel_url)

        data = get_youtube_data(channel_id)

        # Update the GUI with fetched data
        self.display_image_from_url(data['logo_url'])
        self.channel_name_label.setText(f"Channel Name: {data['name']}")
        self.channel_id_label.setText(f"Channel ID: {data['id']}")
        self.subscribers_label.setText(f"Total Subscribers: {data['subscribers']}")
        self.videos_label.setText(f"Total Videos: {data['videos']}")
        self.views_label.setText(f"Total Views: {data['views']}")
        self.location_label.setText(f"Location: {data['location']}")

        top_videos_html = """<h3>Top 5 Videos:</h3>
                            <p>&nbsp;&nbsp;&nbsp;</p>
                                <table border="1" cellspacing="0" cellpadding="5">
                                    <tr>
                                        <td width="50px">Links</td>
                                        <td width="100px">Views</td>
                                    </tr>
                        """
        for video in data['top_videos']:
            top_videos_html += f'''<tr>
                                        <td width="50px">
                                            <a href="{video["link"]}">{video["title"]}</a>
                                        </td>
                                        <td width="100px">
                                            {video["views"]}
                                        </td>
                                    </tr>'''
        top_videos_html += "</table>"
        self.top_videos_text.setHtml(top_videos_html)

        print("got youtube data")

        summary = SummarizeYoutuber(data['name'])
        self.summary_text.setHtml(f"<h3>Summary:</h3><p>{summary}</p>")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = YouTubeInfoApp()
    main_window.show()
    sys.exit(app.exec_())
