from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QListWidget, QFileDialog
import os 
from PyQt5.QtGui import QPixmap
from PIL import Image
from PIL import ImageFilter

workdir = ''
def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def filter(files, extensions):
    result = []
    for filename in files:
        for extension in extensions:
            if filename.endswith(extension):
                result.append(filename)
    return result

def showFilenamesList():
    chooseWorkdir()
    extensions = ['.jpg','.jpeg','.png','.bmp','.gif']
    files = os.listdir(workdir)
    save = filter(files,extensions)
    listt.clear()
    listt.addItems(save)

class ImageProcessor():
    def __init__(self):
        self.filename = None
        self.image = None
        self.savedir = 'modified/'
    def loadImage(self, filename):
        self.filename = filename
        image_path = os.path.join(workdir, filename)
        self.image = Image.open(image_path)
    def showImage(self, path):
        text.hide()
        pixmapimage = QPixmap(path)
        w, h = text.width(), text.height()
        pixmapimage = pixmapimage.scaled(w , h, Qt.KeepAspectRatio)
        text.setPixmap(pixmapimage)
        text.show() 
    def do_bw(self):
        self.image = self.image.convert('L')
        self.saveImage()
        image_path = os.path.join(workdir, self.savedir, self.filename)
        self.showImage(image_path)
    def saveImage(self):
        path = os.path.join(workdir, self.savedir)
        if not(os.path.exists(path)or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)
    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.savedir, self.filename)
        self.showImage(image_path)
    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.savedir, self.filename)
        self.showImage(image_path)
    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.savedir, self.filename)
        self.showImage(image_path)
    def do_sharp(self):
        self.image = self.image.filter(ImageFilter.SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir, self.savedir, self.filename)
        self.showImage(image_path)
    

workimage = ImageProcessor()




def showChosenImage():
    if listt.currentRow() >= 0:
        filename = listt.currentItem().text()
        workimage.loadImage(filename)
        image_path = os.path.join(workdir,filename)
        workimage.showImage(image_path)








app = QApplication([])
main_win = QWidget()
main_win.setWindowTitle('Easy Editor')
main_win.resize(700,400)
folder = QPushButton('Папка')
left = QPushButton('Лево')
right = QPushButton('Право')
mirror = QPushButton('Зеркало')
sharpness = QPushButton('Резкость')
cb = QPushButton('Ч/Б')
text = QLabel('Картинка')
listt = QListWidget()

h_buttons = QHBoxLayout() 
v_list_layout = QVBoxLayout()
v_layout = QVBoxLayout()
main_layout = QHBoxLayout()

h_buttons.addWidget(left)
h_buttons.addWidget(right)
h_buttons.addWidget(mirror)
h_buttons.addWidget(sharpness)
h_buttons.addWidget(cb)
v_list_layout.addWidget(folder)
v_list_layout.addWidget(listt)
v_layout.addWidget(text)
v_layout.addLayout(h_buttons)
main_layout.addLayout(v_list_layout,20)
main_layout.addLayout(v_layout, 80)
main_win.setLayout(main_layout)


folder.clicked.connect(showFilenamesList)
listt.currentRowChanged.connect(showChosenImage)
cb.clicked.connect(workimage.do_bw)
mirror.clicked.connect(workimage.do_flip)
right.clicked.connect(workimage.do_right)
left.clicked.connect(workimage.do_left)
sharpness.clicked.connect(workimage.do_sharp)

main_win.show()
app.exec_()






