import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QSlider
from PyQt6.QtGui import QPixmap, QImage, QColor
from PyQt6.QtCore import Qt
from PIL import Image


class MainViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.original_image = Image.open('1.jpg').convert('RGBA')
        self.resize(300, 700)
        self.image = self.original_image.copy()
        self.current_color_channel = None
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.label = QLabel()
        self.update_image()
        layout.addWidget(self.label)

        self.transparency_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.transparency_slider.setRange(0, 100)
        self.transparency_slider.setValue(100)
        self.transparency_slider.valueChanged.connect(self.update_transparency)
        layout.addWidget(self.transparency_slider)


        self.rotate_left_button = QPushButton('Rotate Left (90°)', self)
        self.rotate_left_button.clicked.connect(self.rotate_left)
        layout.addWidget(self.rotate_left_button)

        self.rotate_right_button = QPushButton('Rotate Right (90°)', self)
        self.rotate_right_button.clicked.connect(self.rotate_right)
        layout.addWidget(self.rotate_right_button)


        for label, channel in [("Все каналы", None), ("Синий", "red"), ("Зеленый", "green"), ("Красный", "blue")]:
            button = QPushButton(label, self)
            button.clicked.connect(lambda checked, ch=channel: self.set_color_channel(ch))
            layout.addWidget(button)

        self.cls_btn = QPushButton("Выйти")
        self.cls_btn.clicked.connect(self.close)
        layout.addWidget(self.cls_btn)

        self.setLayout(layout)
        self.setWindowTitle('Image Viewer')
        self.show()

    def update_image(self):
        data = self.image.tobytes("raw", "RGBA")
        q_image = QImage(data, self.image.width, self.image.height, QImage.Format.Format_ARGB32)
        pixmap = QPixmap.fromImage(q_image)

        self.label.setPixmap(pixmap)

    def update_transparency(self):
        transparency = self.transparency_slider.value()
        alpha = int(255 * (transparency / 100))
        self.image = self.original_image.copy()
        self.image.putalpha(alpha)
        self.apply_color_channel()

    def rotate_left(self):
        self.image = self.image.rotate(90, expand=True)
        self.apply_color_channel()
        self.update_image()

    def rotate_right(self):
        self.image = self.image.rotate(-90, expand=True)
        self.apply_color_channel()
        self.update_image()

    def apply_color_channel(self):
        if self.current_color_channel is not None:
            new_image = Image.new('RGBA', self.image.size)

            for x in range(self.image.width):
                for y in range(self.image.height):
                    pixel = self.image.getpixel((x, y))
                    if self.current_color_channel == "red":
                        new_image.putpixel((x, y), (pixel[0], 0, 0, pixel[3]))
                    elif self.current_color_channel == "green":
                        new_image.putpixel((x, y), (0, pixel[1], 0, pixel[3]))
                    elif self.current_color_channel == "blue":
                        new_image.putpixel((x, y), (0, 0, pixel[2], pixel[3]))

            self.image = new_image
        self.update_image()

    def set_color_channel(self, channel):
        self.current_color_channel = channel
        self.apply_color_channel()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = MainViewer()
    sys.exit(app.exec())
