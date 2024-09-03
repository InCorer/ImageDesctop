from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
                             QVBoxLayout, QListWidget, QHBoxLayout, QFileDialog)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PIL import Image, ImageFilter
import os

def choose_folder():
    global work_dir
    work_dir = QFileDialog.getExistingDirectory()
    if work_dir != '':
        files = os.listdir(work_dir)
        files = filter(files)
        image_list.clear()
        image_list.addItems(files)
    else:
        image_list.clear()



def filter(files):
    extensions = ['.png', '.webp', '.jpg', '.jpeg']
    result = []
    for file in files:
        for extension in extensions:
            if file.endswith(extension):
                result.append(file)
                break
    return result


def show_selected_picture():
    image_name = image_list.selectedItems()[0].text()
    image_processor.load_image(image_name, work_dir)
    image_processor.show_image(os.path.join(work_dir, image_processor.file_name))
class ImageProcessor:
    def __init__(self):
        self.image = None
        self.file_name = None
        self.dir = None

    def load_image(self, file_name, dir):
        self.file_name = file_name
        self.dir = dir
        self.image = Image.open(os.path.join(dir, file_name))

    def show_image(self, image_path):
        picture_label.hide()
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaled(picture_label.width(), picture_label.height(),
                               Qt.AspectRatioMode.KeepAspectRatio)
        picture_label.setPixmap(pixmap)
        picture_label.show()

    def do_b_w(self):
        try:
            self.image = self.image.convert('L')
            self.save_image()
            image_path = os.path.join(self.dir, 'edited', self.file_name)
            self.show_image(image_path)
        except AttributeError:
            pass

    def do_sharpness(self):
        try:
            self.image = self.image.filter(ImageFilter.SHARPEN)
            self.save_image()
            image_path = os.path.join(self.dir, 'edited', self.file_name)
            self.show_image(image_path)
        except AttributeError:
            pass

    def do_mirror(self):
        try:
            self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
            self.save_image()
            image_path = os.path.join(self.dir, 'edited', self.file_name)
            self.show_image(image_path)
        except AttributeError:
            pass

    def do_left(self):
        try:
            self.image = self.image.transpose(Image.ROTATE_90)
            self.save_image()
            image_path = os.path.join(self.dir, 'edited', self.file_name)
            self.show_image(image_path)
        except AttributeError:
            pass

    def do_right(self):
        try:
            self.image = self.image.transpose(Image.ROTATE_270)
            self.save_image()
            image_path = os.path.join(self.dir, 'edited', self.file_name)
            self.show_image(image_path)
        except AttributeError:
            pass

    def save_image(self):
        path = os.path.join(work_dir, 'edited')
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        full_name = os.path.join(path, self.file_name)
        self.image.save(full_name)
app = QApplication([])
window = QWidget()
window.resize(1000, 600)
window.show()


main_layout = QHBoxLayout()
left_vertical_layout = QVBoxLayout()
right_vertical_layout = QVBoxLayout()
buttons_layout = QHBoxLayout()


window.setLayout(main_layout)
main_layout.addLayout(left_vertical_layout)
main_layout.addLayout(right_vertical_layout)


image_processor = ImageProcessor()
folder = QPushButton('Папка')
image_list = QListWidget()
picture_label = QLabel('Картинка')
left = QPushButton('Лево')
right = QPushButton('Право')
mirror = QPushButton('Зеркало')
sharpness = QPushButton('Резкость')
b_w = QPushButton('Ч/Б')

folder.clicked.connect(choose_folder)
image_list.itemClicked.connect(show_selected_picture)
b_w.clicked.connect(image_processor.do_b_w)
sharpness.clicked.connect(image_processor.do_sharpness)
mirror.clicked.connect(image_processor.do_mirror)
left.clicked.connect(image_processor.do_left)
right.clicked.connect(image_processor.do_right)
image_list.setFixedWidth(300)

right_vertical_layout.addWidget(picture_label)
right_vertical_layout.addLayout(buttons_layout)
left_vertical_layout.addWidget(folder)
left_vertical_layout.addWidget(image_list)
buttons_layout.addWidget(left)
buttons_layout.addWidget(right)
buttons_layout.addWidget(mirror)
buttons_layout.addWidget(sharpness)
buttons_layout.addWidget(b_w)





app.exec()