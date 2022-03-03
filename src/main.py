import sys
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QWidget, QPlainTextEdit, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from capture import imageToTexts
from train import languageDict, predict, majority


class ImageLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setAlignment(Qt.AlignCenter)
        self.setText('\n\n Drop Image Here \n\n')
        self.setStyleSheet('''
            QLabel{
                border: 4px dashed #aaa
            }
        ''')

    def setPixmap(self, image):
        super().setPixmap(image)

class ImageWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 400, 400, 400)
        self.setAcceptDrops(True)
        self.photoViewer = ImageLabel()

        imageLayout = QVBoxLayout()
        imageLayout.addWidget(self.photoViewer)
        self.setLayout(imageLayout)

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)
            self.filepath = event.mimeData().urls()[0].toLocalFile()
            self.setImage(self.filepath)

            texts = self.setText(self.filepath)
            result = self.prediction(texts)
            main_window.setText(languageDict[result], texts[result])

            event.accept()
        else:
            event.ignore()

    def setImage(self, filepath):
        self.photoViewer.setPixmap(QPixmap(filepath))

    def setText(self, filepath):
        return imageToTexts(filepath)

    def prediction(self, texts):
        result = predict(texts)
        return majority(result)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('LanguageCapture')
        self.setGeometry(200, 50, 500, 500)

        self.resultText = QPlainTextEdit(self)
        self.resultText.setPlaceholderText('Result Text')
        self.resultText.setGeometry(50, 150, 400, 300)

        self.resultLang = QLineEdit(self)
        self.resultLang.setPlaceholderText('Result Language')
        self.resultLang.setGeometry(50, 50, 400, 30)

    def setText(self, lang, text):
        self.resultLang.setText(lang)
        self.resultText.setPlainText(text)
        main_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    image_window = ImageWindow()
    image_window.show()
    sys.exit(app.exec_())
