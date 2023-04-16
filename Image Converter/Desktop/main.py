from PIL import Image
import toml
from UI import*
from languages import LANGUAGES
from cairosvg import svg2png,svg2pdf
from PyPDF2 import PdfMerger
from pathlib import Path

EXTENSIONS = (".jpg" ,".jpeg" ,".apng" ,".png" ,".bmp" ,".tiff" ,".tif" ,".webp" ,".jfif" ,".ico" ,".cur" ,".gif" ,".svg" ,".afiv")
DO_NOT_SUPPORT_RGBA = ("jpg", "jpeg", "jfif")
Selected_images = []
Selected_image = None
def Change_language(language:str):
    global Language
    Language = language
    for index,button in enumerate(buttons_list):
        button.setText(LANGUAGES[Language]["Buttons"][index])
    Main_window.image_name.setText(LANGUAGES[Language]["Info"][0]+Main_window.image_name.text().split(":")[1])
    Main_window.folder_name.setText(LANGUAGES[Language]["Info"][1]+Main_window.folder_name.text().split(":")[1])
    if not Main_window.image.pixmap():
        Main_window.image.setText(LANGUAGES[Language]["Info"][2])
    Messages.log_copied.setText(LANGUAGES[Language]["Errors"]["text"][0])
    Messages.open_explorer_error.setText(LANGUAGES[Language]["Errors"]["text"][1])
    Messages.folder_empty.setText(LANGUAGES[Language]["Errors"]["text"][4])
    with open(find_file("active language.toml"),"w",encoding="utf-8") as file:
        toml.dump({"Language":Language},file)


def Copy_log():
    if Main_window.log_list.item(0):
        result = ""
        for log in range(0,Main_window.log_list.count()):
            result = result +f"\n {log}: {Main_window.log_list.item(log).text()}"
        app.clipboard().setText(result)
        Messages.log_copied.exec()


def Select_image():
    global Selected_image,Selected_images
    try:
        image,_ = QFileDialog.getOpenFileName(filter="Images (*.jpg *.jpeg *.apng *.png *.bmp *.tiff *.tif *.webp *.jfif *.ico *.cur *.gif *.svg *.afiv)")
    except:
        Messages.open_explorer_error.exec()
    else:
        if image:
            Main_window.image.resize(Main_window.window.width()*0.7,Main_window.window.height()*0.7)
            Main_window.image.setPixmap(QPixmap(image).scaled(Main_window.image.width(),Main_window.image.height(),Qt.KeepAspectRatio,Qt.SmoothTransformation))
            Main_window.image_name.setText(LANGUAGES[Language]["Info"][0] +" "+ Path(image).name)
            Main_window.folder_name.setText(LANGUAGES[Language]["Info"][1] +" "+ Path(image).parent.name)
            Main_window.log_list.addItem(LANGUAGES[Language]["result_log"][3].replace("name",Path(image).name))
            Selected_image = image
            Selected_images = []


def Select_folder():
    global Selected_images,Selected_image
    try:
        folder = QFileDialog.getExistingDirectory()
    except:
        Messages.open_explorer_error.exec()
    else:
        Selected_image = None
        Selected_images = []
        for file in os.listdir(folder):
            if Path(file).suffix in EXTENSIONS:
                Selected_images.append(f"{folder}/{file}")
        if len(Selected_images) == 0:
            Messages.folder_empty.exec()
            return
        Main_window.image.resize(Main_window.window.width()*0.7,Main_window.window.height()*0.7)
        Main_window.image.setPixmap(QPixmap(Selected_images[0]).scaled(Main_window.image.width(),Main_window.image.height(),Qt.KeepAspectRatio,Qt.SmoothTransformation))
        Main_window.image_name.setText(LANGUAGES[Language]["Info"][0] +" "+ Path(Selected_images[0]).name)
        Main_window.folder_name.setText(LANGUAGES[Language]["Info"][1] +" "+ Selected_images[0].split("/")[-2])
        Main_window.log_list.addItem(LANGUAGES[Language]["result_log"][2].replace("name",Path(folder).name))


def convert_image(final_path:str|list[str], format:str,many_images:bool=False):
    global Selected_images,Selected_image
    if many_images:
        if format != "pdf":
            #Create new folder for converted images
            destination_folder = os.path.dirname(final_path[0]) + LANGUAGES[Language]["Info"][3]
            if not os.path.exists(destination_folder):
                os.mkdir(destination_folder)
            else:
                Messages.folder_exists.setText(destination_folder+LANGUAGES[Language]["Errors"]["text"][3])
                if Messages.folder_exists.exec() == QMessageBox.StandardButton.Cancel:
                    return
            #Adding images to folder
            for path in final_path:
                image_name = Path(path).name
                new_path = destination_folder+"/"+image_name.replace(Path(image_name).suffix,format)
                if Path(image_name).suffix == "svg":
                    svg2png(url=path,write_to=new_path)
                else:
                    image = Image.open(path)
                    if format in DO_NOT_SUPPORT_RGBA:
                        image = image.convert("RGB",colors=1000)
                    image.save(new_path)
            Main_window.log_list.addItem(destination_folder+LANGUAGES[Language]["result_log"][0])
        else:
            temp_files = []
            #Add temporary pdfs to the temp folder
            for path in final_path:
                new_path = f"Temp/temp_{final_path.index(path)}.pdf"
                if Path(path).suffix == ".svg":
                    svg2pdf(url=path,write_to=new_path)
                else:
                    image = Image.open(path)
                    image = image.convert("RGB",colors=1000)
                    image.save(new_path)
                temp_files.append(new_path)
            pdf_merger = PdfMerger()
            #Merge the temp pdfs into one file
            for path in temp_files:
                pdf_merger.append(path)
            new_path = os.path.dirname(final_path[0])+"/"+Path(final_path[0]).parent.name + LANGUAGES[Language]["Info"][3]+".pdf"
            #Check if the pdf file already exists
            if os.path.exists(new_path):
                Messages.image_exists.setText(new_path+LANGUAGES[Language]["Errors"]["text"][2])
                if Messages.image_exists.exec() == QMessageBox.StandardButton.Cancel:
                    return
            pdf_merger.write(new_path)
            pdf_merger.close()
            #Remove the temp files
            for path in temp_files:
                os.remove(path)
            Main_window.log_list.addItem(os.path.dirname(final_path[0])+LANGUAGES[Language]["result_log"][0])
        destination_folder = Path(new_path).parent
    else:
        #Check if the image already exists
        if os.path.exists(final_path):
            Messages.image_exists.setText(final_path+LANGUAGES[Language]["Errors"]["text"][2])
            if Messages.image_exists.exec() == QMessageBox.StandardButton.Cancel:
                return
        image = Image.open(Selected_image)
        if format in DO_NOT_SUPPORT_RGBA:
            image = image.convert("RGB",colors=1000)
        image.save(final_path)
        destination_folder = os.path.dirname(final_path)
        Main_window.log_list.addItem(Selected_image+LANGUAGES[Language]["result_log"][0])
    #Reset to default
    Main_window.image.setText(LANGUAGES[Language]["Info"][2])
    Main_window.image_name.setText(LANGUAGES[Language]["Info"][0])
    Main_window.folder_name.setText(LANGUAGES[Language]["Info"][1])
    Selected_image = []
    Selected_image = None
    os.startfile(destination_folder)


def Start_converting():
    format = Main_window.select_format.currentText()
    if Selected_image:
        final_path = Selected_image.replace(Path(Selected_image).suffix,format)
        convert_image(final_path, format)
    elif Selected_images:
        convert_image(Selected_images,format,True)

if __name__ == "__main__":
    Language = str(toml.load(find_file("active language.toml"))["Language"])
    Change_language(Language)
    if Language == "Українська":
        Main_window.languages.setCurrentIndex(1)
    else:
        Main_window.languages.setCurrentIndex(0)
    Main_window.languages.currentTextChanged.connect(Change_language)
    Main_window.copy_log.clicked.connect(Copy_log)
    Main_window.select_file.clicked.connect(Select_image)
    Main_window.select_folder.clicked.connect(Select_folder)
    Main_window.convert.clicked.connect(Start_converting)
    Main_window.window.show()
    app.exec()
