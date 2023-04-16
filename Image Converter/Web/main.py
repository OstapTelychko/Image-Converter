from flask import Flask,render_template,request,Response,send_file,send_from_directory
from werkzeug.utils import secure_filename
import base64
from io import BytesIO
from zipfile import ZipFile
from PIL import Image
from PyPDF2 import PdfMerger,PdfFileReader,PageObject
from sys import getsizeof
from pdf2image import convert_from_bytes
from cairosvg import svg2pdf,svg2png


app = Flask(__name__)

ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg","jfif","gif", "ico","webp","tiff","pdf","svg","bmp","afiv"]
CONVERSION_EXTENSIONS = ["png", "jpg", "jpeg","jfif", "gif", "ico","webp", "tiff","pdf","bmp"]
DO_NOT_SUPPORT_RGBA = ("jpg", "jpeg", "jfif","pdf")

@app.route("/")
def home():
    return render_template("home.html")


def convert_file(buffer:BytesIO,file_data:BytesIO,extension:str,file_current_extension:str):
    """Converts a file current extension to `extension` and save to `buffer`

       Args:
            `buffer` (BytesIO): Buffer to save file
            `extension` (str): target extension
            `file_data` (BytesIO): data of file
            `file_current_extension` (str): current file extension 
        Returns:
            buffer (BytesIO):  Buffer with converted file
    """
    if file_current_extension == "svg":
        if extension != "pdf":
            buffer.write(svg2png(file_obj=file_data))
            if extension != "png":
                image = Image.open(buffer)
                if extension in DO_NOT_SUPPORT_RGBA:
                    image=image.convert("RGB")
                image.save(buffer,format=extension.upper())
            buffer.seek(0)
        else:
            buffer.write(svg2pdf(file_obj=file_data))
            buffer.seek(0)
    else:
        if extension != "pdf":
            with ZipFile(buffer,"w") as zip_file:
                file_data.seek(0)
                for iteration,image in enumerate(convert_from_bytes(file_data.read())):
                    file = BytesIO()
                    image.save(file,format=extension.upper())
                    file.seek(0)
                    zip_file.writestr(f"{iteration}.{extension}",file.read())
            buffer.seek(0)
        else:
            image = Image.open(file_data)
            image = image.convert("RGB")
            image.save(buffer,format="PDF")
            buffer.seek(0)
        

def process_file_data(data,mode:str="single"):
    "Parse file `data` and return `file_name`,`file_current_extension`,`extension` and `file_data`"
    data_base64 = data["file_data"].split(",")[1]
    file_data = BytesIO(base64.b64decode(data_base64))
    file_name = data["file_name"]
    file_current_extension = file_name.split(".")[1]
    if mode == "single":
        extension = data["extension"]
        return file_name,file_current_extension,extension,file_data
    return file_name,file_current_extension,file_data


@app.route("/single_conversion",methods=["POST"])
def single_conversion():
    print("Converting...")
    Result = BytesIO() # I will save result in RAM
    if getsizeof(request.form) < 52_428_800: # 50MB
        file_name,file_current_extension,extension,file_data = process_file_data(request.form)
        if file_current_extension in ALLOWED_EXTENSIONS and extension in CONVERSION_EXTENSIONS:
            new_file_name = secure_filename(file_name).replace(file_current_extension,extension)
            convert_file(Result,file_data,extension,file_current_extension)
            if file_current_extension != "pdf":
                return send_file(Result,as_attachment=True,download_name=new_file_name)
            else:
                return send_file(Result,as_attachment=True,download_name=file_name.replace(file_current_extension,"zip"))
            

@app.route("/multiple_conversion",methods=["POST"])  
def multiple_conversion():
    print("Converting...")
    request_data = request.get_json()
    folder_data = request_data["folder_data"] # Here i gets data about images
    Result = BytesIO() # I will save zip file in RAM 
    extension = request_data["extension"]
    folder_name = request_data["folder_name"]

    if getsizeof(folder_data) < 52_428_800: #50 MB
        if extension in ALLOWED_EXTENSIONS and extension in CONVERSION_EXTENSIONS:
            if extension != "pdf":
                with ZipFile(Result,"w") as zip_file:
                    for file in folder_data:
                        file_name,file_current_extension,file_data = process_file_data(folder_data[file],mode="multiple")
                        new_file_name = secure_filename(file_name.replace(file_current_extension,extension))
                        file_buffer = BytesIO()
                        convert_file(file_buffer,file_data,extension,file_current_extension)
                        zip_file.writestr(new_file_name,file_buffer.read())
                Result.seek(0)

                return send_file(Result,as_attachment=True,download_name=folder_name+".zip")
            else:
                merger = PdfMerger()
                for file in folder_data:
                    file_name,file_current_extension,file_data = process_file_data(folder_data[file],mode="multiple")
                    file_buffer = BytesIO()
                    convert_file(file_buffer,file_data,extension,file_current_extension)
                    merger.append(file_buffer)
                new_file_name = secure_filename(folder_name+".pdf")
                merger.write(Result)
                merger.close()
                Result.seek(0)
                return send_file(Result,as_attachment=True,download_name=folder_name+".pdf")


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)