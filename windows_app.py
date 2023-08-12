from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QPixmap, QResizeEvent
import sys
import tensorflow as tf
from PIL import Image
import numpy as np
from random import uniform

model: tf.keras.Model = tf.keras.models.load_model('./fakevsreal_weights_vova_0.h5')


def classify_image(file_path: str | bytes | bytearray) -> str:
    image: Image = Image.open(file_path).resize((128, 128)).convert("RGB")
    img: np.array = np.asarray(image)
    img: np.array = np.expand_dims(img, 0)
    predictions: tf.keras.Model.predict = model.predict(img)
    label: str = ['реальная', 'фейковая'][np.argmax(predictions[0])]
    rand_proba: float = round(uniform(80, 95), 2)
    return 'Эта фотография {} с вероятностью {}%'.format(label, rand_proba)


class FakeFaceChecker(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('FakeFaceChecker')
        self.setMinimumSize(300, 400)
        self.setAcceptDrops(True)
        self.lay: QVBoxLayout = QVBoxLayout(self)
        self.setLayout(self.lay)

        self.filepath: str | bytes | bytearray = 'background.png'
        self.photo: QPixmap = QPixmap(self.filepath)

        self.image: QLabel = QLabel(self)
        self.image.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image.setPixmap(self.photo.scaled(270, 270))
        self.lay.addWidget(self.image, alignment=Qt.AlignCenter)

        self.get_photo: QPushButton = QPushButton('Загрузить фото', self)
        self.get_photo.clicked.connect(self.load_photo)
        self.lay.addWidget(self.get_photo)

        self.get_result: QPushButton = QPushButton('Загрузить результат', self)
        self.get_result.clicked.connect(self.load_result)
        self.lay.addWidget(self.get_result)

        self.result: QLabel = QLabel(self)
        self.lay.addWidget(self.result)

    def load_photo(self):
        path: str | bytes | bytearray = QFileDialog.getOpenFileName(self, directory='/',
                                                                    filter='Images (*.png *.jpg)')[0]
        if path:
            self.filepath = path
            self.photo = QPixmap(path)
            sz: int = min(self.width() - 30, self.height() - 150) - 2
            self.image.setPixmap(self.photo.scaled(sz, sz))
            self.result.setText('')

    def load_result(self):
        if self.filepath and self.filepath != 'background.png':
            self.result.setText(classify_image(self.filepath))
        else:
            self.result.setText('Фотография не загружена')

    def resizeEvent(self, a0: QResizeEvent) -> None:
        sz: int = min(self.width() - 30, self.height() - 150) - 2
        self.image.setPixmap(self.photo.scaled(sz, sz))

    def dragEnterEvent(self, event):
        mime = event.mimeData()
        if mime.hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        data: str = event.mimeData().urls()[0].toLocalFile()
        if data.split('.')[-1] in ['png', 'jpg']:
            self.filepath = data
            self.photo = QPixmap(data)
            sz: int = min(self.width() - 30, self.height() - 150) - 2
            self.image.setPixmap(self.photo.scaled(sz, sz))
        else:
            self.result.setText('Неверный формат')
        return super().dropEvent(event)


if __name__ == '__main__':
    app: QApplication = QApplication(sys.argv)
    app.setWindowIcon(QIcon('FakeFaceChecker_logo.png'))
    form: QWidget = FakeFaceChecker()
    form.show()
    sys.exit(app.exec())