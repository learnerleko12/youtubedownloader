import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import requests
from yt_dlp import YoutubeDL
from io import BytesIO

class YouTubeThumbnailApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('YouTube 썸네일 추출기')
        self.setGeometry(100, 100, 400, 400)
        self.layout = QVBoxLayout()

        self.label = QLabel('YouTube URL을 입력하세요:')
        self.layout.addWidget(self.label)

        self.url_input = QLineEdit()
        self.layout.addWidget(self.url_input)

        self.button = QPushButton('썸네일 가져오기')
        self.button.clicked.connect(self.get_thumbnail)
        self.layout.addWidget(self.button)

        self.download_button = QPushButton('영상 다운로드')
        self.download_button.clicked.connect(self.download_video)
        self.layout.addWidget(self.download_button)

        self.thumbnail_label = QLabel()
        self.thumbnail_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.thumbnail_label)

        self.setLayout(self.layout)

    def get_thumbnail(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, '오류', 'URL을 입력하세요.')
            return
        try:
            ydl_opts = {'quiet': True, 'skip_download': True}
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                thumbnail_url = info.get('thumbnail')
                if not thumbnail_url:
                    raise Exception('썸네일을 찾을 수 없습니다.')
                response = requests.get(thumbnail_url)
                pixmap = QPixmap()
                pixmap.loadFromData(response.content)
                self.thumbnail_label.setPixmap(pixmap.scaled(320, 180, Qt.KeepAspectRatio))
        except Exception as e:
            QMessageBox.critical(self, '에러', f'썸네일을 가져오는 중 오류 발생: {e}')

    def download_video(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, '오류', 'URL을 입력하세요.')
            return
        try:
            ydl_opts_info = {'quiet': True, 'skip_download': True}
            with YoutubeDL(ydl_opts_info) as ydl:
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'youtube_video')
            default_path = f'C:/'+title+'.mp4'
            save_path, _ = QFileDialog.getSaveFileName(self, '저장 위치 선택', default_path, 'MP4 Files (*.mp4);;All Files (*)')
            if not save_path:
                return
            ydl_opts = {
                'outtmpl': save_path,
                'format': 'bestvideo+bestaudio/best',
                'merge_output_format': 'mp4',
                'quiet': True
            }
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            QMessageBox.information(self, '완료', '영상이 성공적으로 저장되었습니다!')
        except Exception as e:
            QMessageBox.critical(self, '에러', f'영상 다운로드 중 오류 발생: {e}')

def main():
    app = QApplication(sys.argv)
    window = YouTubeThumbnailApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
