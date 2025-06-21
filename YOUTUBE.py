import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import yt_dlp
import requests
from io import BytesIO
import os

class YouTubeThumbnailDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('YouTube 썸네일 다운로더')
        self.setGeometry(100, 100, 400, 400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText('YouTube URL을 입력하세요')
        layout.addWidget(self.url_input)

        self.download_btn = QPushButton('썸네일 가져오기', self)
        self.download_btn.clicked.connect(self.download_thumbnail)
        layout.addWidget(self.download_btn)

        self.video_download_btn = QPushButton('영상 다운로드', self)
        self.video_download_btn.clicked.connect(self.download_video)
        layout.addWidget(self.video_download_btn)

        self.thumbnail_label = QLabel(self)
        self.thumbnail_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.thumbnail_label)

        self.setLayout(layout)

    def download_thumbnail(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, '경고', 'URL을 입력하세요!')
            return
        try:
            ydl_opts = {'quiet': True, 'skip_download': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                thumbnail_url = info.get('thumbnail')
                if not thumbnail_url:
                    QMessageBox.warning(self, '오류', '썸네일을 찾을 수 없습니다.')
                    return
                response = requests.get(thumbnail_url)
                pixmap = QPixmap()
                pixmap.loadFromData(BytesIO(response.content).read())
                self.thumbnail_label.setPixmap(pixmap.scaled(320, 180, Qt.KeepAspectRatio))
        except Exception as e:
            QMessageBox.critical(self, '오류', f'문제가 발생했습니다: {e}')

    def download_video(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, '경고', 'URL을 입력하세요!')
            return
        try:
            # 사용자 Download 폴더 경로 구하기
            download_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
            ydl_opts = {
                'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
                'ffmpeg_location': r'C:/Users/USER/ffmpeg-7.1.1-full_build/bin',
                'format': 'bestvideo+bestaudio/best',
                'merge_output_format': 'mp4',
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            QMessageBox.information(self, '완료', f'영상이 다운로드 폴더에 저장되었습니다!\n{download_dir}')
        except Exception as e:
            QMessageBox.critical(self, '오류', f'다운로드 중 문제가 발생했습니다: {e}')

def main():
    app = QApplication(sys.argv)
    window = YouTubeThumbnailDownloader()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
