from PySide6.QtWidgets import QWidget,QApplication,QHBoxLayout,QVBoxLayout,QLabel,QPushButton,QComboBox,QListWidget,QMessageBox,QFileDialog
from PySide6.QtGui import QPixmap,QIcon,QFont
from PySide6.QtCore import Qt,QSize
import os,inspect
from sys import exit
from style import style
from pathlib import Path

app = QApplication([])
app.setStyleSheet(style)

errors_list = []
buttons_list = []
def create_message(text:str,type_confirm:bool,icon:QMessageBox.Icon) -> QMessageBox:
    error = QMessageBox()
    error.setText(text)
    error.addButton(QMessageBox.StandardButton.Ok)
    error.setWindowTitle("Image Converter")
    if type_confirm:
        error.addButton(QMessageBox.StandardButton.Cancel)  
    error.setIcon(icon)
    errors_list.append(error)
    return error

def create_button(button_text:str,size:tuple[int])->QPushButton:
    button = QPushButton(text=button_text)
    button.setFont(QFont("Calibri",pointSize=10))
    button.setMinimumSize(*size)
    button.setMaximumSize(*size)
    buttons_list.append(button)
    return button

def find_file(file:str)->Path:
    "Return path to file"
    # Path = os.path.join(os.environ.get("_MEIPASS2",os.path.abspath(".")),"Images/"+file).replace("\\","/")
    path = __file__.replace(Path(__file__).name,file)
    if os.path.exists(path):
        return path 
    else:
        error_info = inspect.getframeinfo(inspect.stack()[1][0])
        line = error_info[1]
        File = error_info[0].split("\\")[-1]
        Messages.file_not_found.setText(f"[ERROR] File {path} doesn't exist | Line: {line} | File: {File} [ERROR]")
        Messages.file_not_found.exec()
        exit()

class Messages():
    log_copied = create_message("Log has been copied",False,QMessageBox.Icon.Information)
    open_explorer_error = create_message("Failed to open explorer",False,QMessageBox.Icon.Critical)
    file_not_found = create_message("",False,QMessageBox.Icon.Critical)
    image_exists = create_message("image already exists",True,QMessageBox.Icon.Question)
    folder_exists = create_message("Folder already exists",True,QMessageBox.Icon.Question)
    folder_empty = create_message("There are no images supported by me in the selected folder.",False,QMessageBox.Icon.Critical)
class Main_window():
    window = QWidget()
    window.resize(900,600)
    icon = QIcon(find_file("Images/icon.png"))

    #LOG LIST
    log_list = QListWidget()
    log_list.setFont(QFont("Calibri",10))
    log_list.setMaximumWidth(240)
    log_list.setMinimumWidth(240)
    log_list.setWordWrap(True)
    copy_log = create_button("Copy",(110,30))
    log_layout = QVBoxLayout()
    log_layout.addWidget(log_list,alignment=Qt.AlignmentFlag.AlignHCenter)
    log_layout.addWidget(copy_log,alignment=Qt.AlignmentFlag.AlignHCenter)

    #IMAGE AND TOOL BAR
    image = QLabel("Your image will be here :)")
    select_file = create_button(" Select image",(150,30))
    select_file.setIcon(icon)
    select_folder = create_button("Select folder",(140,30))
    select_folder.setIcon(QIcon(find_file("Images/folder icon.png")))
    select_format = QComboBox()
    select_format.addItems((".png",".jpg",".jpeg",".jfif",".gif",".ico",".bmp",".tiff",".bmp",".pdf"))
    select_format.setIconSize(QSize(30,30))
    select_format.setFont(QFont("Calibri",15))
    select_format.setMinimumSize(120,30)
    select_format.setMaximumSize(370,30)
    convert = create_button("Convert",(140,30))
    tool_bar_layout = QHBoxLayout()
    tool_bar_layout.setSpacing(60)
    tool_bar_layout.addStretch(1)
    tool_bar_layout.addWidget(select_file,alignment=Qt.AlignmentFlag.AlignRight)
    tool_bar_layout.addWidget(select_folder,alignment=Qt.AlignmentFlag.AlignHCenter)
    tool_bar_layout.addWidget(select_format,alignment=Qt.AlignmentFlag.AlignHCenter)
    tool_bar_layout.addWidget(convert,alignment=Qt.AlignmentFlag.AlignLeft)
    tool_bar_layout.addStretch(1)
    #Info
    image_name = QLabel("Image: - ")
    folder_name = QLabel("Folder: - ")
    languages = QComboBox()
    languages.setMaximumSize(110,25)
    languages.addItems(("English","Українська"))
    languages.setItemIcon(0,QIcon(find_file("Images/English.png")))
    languages.setItemIcon(1,QIcon(find_file("Images/Ukrainian.png")))
    info_layout = QHBoxLayout()
    info_layout.addWidget(image_name)
    info_layout.addWidget(folder_name)
    info_layout.addWidget(languages)

    image_and_tool_bar_layout = QVBoxLayout()
    image_and_tool_bar_layout.addLayout(info_layout)
    image_and_tool_bar_layout.addWidget(image,alignment=Qt.AlignmentFlag.AlignHCenter)  
    image_and_tool_bar_layout.addLayout(tool_bar_layout)
    
    main_layout = QHBoxLayout()
    main_layout.addLayout(log_layout,stretch=20)
    main_layout.insertSpacing(1,30)
    main_layout.addLayout(image_and_tool_bar_layout,stretch=80)

    window.setLayout(main_layout)
    window.setWindowIcon(icon)
    window.setWindowTitle("Image Converter")
