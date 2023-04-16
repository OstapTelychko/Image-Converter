document.addEventListener("DOMContentLoaded", function(){
    let Selected_image = document.querySelector("#basic-conversion-image")
    let Selected_images = document.querySelector("#basic-conversion-folder")
    let Confirm_question = document.querySelector("#question")
    let Selected_extension = document.querySelector("#selected-extension")
    let Conversion_mode = 0

    const Image_selection_button = document.querySelector("#select-image")
    const Folder_selection_button = document.querySelector("#select-folder")
    const Convert_button = document.querySelector("#convert")
    const Allowed_extensions = ["png", "jpg", "jpeg","jfif", "gif", "ico","webp", "tiff","pdf","svg","bmp", "afiv"]
    const Conversion_extensions = ["png", "jpg", "jpeg","jfif", "gif", "ico","webp","pdf","bmp"]

    Toggle_menu_visibility("hide")

    Image_selection_button.onclick = function(){Selected_image.click()}
    Folder_selection_button.onclick = function(){Selected_images.click()}
    document.querySelector("#cancel").onclick = function(){Cancel_conversion()}


    function Toggle_menu_visibility(mode=String) {
        // Hide or show the menu of basic conversion
        if (mode == "hide"){
            for(element of document.querySelector("#convert-file").children){
                element.style.display = "none"
            }
            document.querySelector("#selected-extension").style.display = "none"
            document.querySelector(".clue").style.display = "none"
            document.querySelector("#preview").style.display = "none"
            Image_selection_button.style.display = "flex"
            Folder_selection_button.style.display = "flex"
        }else if(mode=="show"){
            for(element of document.querySelector("#convert-file").children){
                element.style.display = "block"
            }
            document.querySelector("#selected-extension").style.display = "block"
            document.querySelector(".clue").style.display = "block"
            document.querySelector("#preview").style.display = "block"
            Image_selection_button.style.display = "none"
            Folder_selection_button.style.display = "none"
        }
    }


    function Cancel_conversion(){
        Toggle_menu_visibility("hide")
        url = null
        Selected_image.value = ""
        Selected_images.value = ""
        Conversion_mode = 0
        Selected_extension.value = ""
        file_link = null
        window.scrollTo(0,0)       
    }


    function Single_conversion(image,image_name,extension){
        let image_extension = image_name.split(".")[1]
        if (Allowed_extensions.includes(image_extension)){
            if (Conversion_extensions.includes(extension)){
                $.ajax({type: "POST",url: "/single_conversion",data:{file_data:image,file_name:image_name,extension:extension},
                    xhrFields:{
                        responseType: "blob"
                    },
                    success: function(data){
                        url = URL.createObjectURL(data)
                        let file_link = document.createElement("a")
                        if (image_extension != "pdf"){image_name = image_name.replace(image_name.split(".")[1],extension)}
                        else{image_name = image_name.replace(image_name.split(".")[1],"zip")}
                        file_link.setAttribute("download",image_name)
                        file_link.setAttribute("href",url)
                        file_link.click()
                        URL.revokeObjectURL(url)
                        Cancel_conversion()
                    }
                })
            }else{alert(`We can't convert this image to ${extension}. Plese check entered extension`)}
        }else{alert(`We don't support ${image_extension} extension`)}
    }


    function Multiple_conversion(folder,folder_name,extension){
        let Cancel = false
        for(let file in folder){
            let file_name = folder[file]["file_name"]
            let file_exstension = file_name.split(".")[1]
            if (!Allowed_extensions.includes(file_exstension)){
                alert(`We don't support ${file_exstension} extension`)
                Cancel = true    
                break
            }
            if (!Conversion_extensions.includes(extension)){
                alert(`We can't convert this image to ${extension}. Plese check entered extension`)
                Cancel = true
                break
            }
        }
        if (Cancel==false){
            console.log(folder)
            $.ajax({
                type: "POST",
                contentType : "application/json",
                // dataType:"json",
                // async:false,
                url: "/multiple_conversion",
                data:JSON.stringify({folder_data:folder,folder_name:folder_name,extension:extension}),
                xhrFields:{responseType:"blob"},
                success: function(data){   
                    url = URL.createObjectURL(data)
                    let file_link = document.createElement("a")
                    if (extension != "pdf"){file_link.setAttribute("download",folder_name+".zip")}
                    else{file_link.setAttribute("download",folder_name+".pdf")}
                    file_link.setAttribute("href",url)
                    file_link.click()
                    URL.revokeObjectURL(url)
                    Cancel_conversion()
                }
            })
        }
    }

    
    Selected_image.onchange = function(){
        Toggle_menu_visibility("show")
        let url = URL.createObjectURL(Selected_image.files[0])
        document.querySelector("#preview").src = url
        Confirm_question.textContent = Confirm_question.textContent.replace("$filename",Selected_image.files[0].name)
        Conversion_mode = 1
    }


    Selected_images.onchange = function(){
        Toggle_menu_visibility("show")
        let url = URL.createObjectURL(Selected_images.files[0])
        document.querySelector("#preview").src = url
        let path = Selected_images.files[0].webkitRelativePath
        let folder_name = path.split("/")[path.split("/").length-2]
        // console.log(folder_name)
        Confirm_question.textContent = Confirm_question.textContent.replace("$filename",folder_name)
        Conversion_mode = 2
    }


    Convert_button.onclick =  async function(){
        if (Conversion_mode == 1){
            const reader = new FileReader()
            reader.readAsDataURL(Selected_image.files[0])
            reader.onloadend = function(){Single_conversion(reader.result,Selected_image.files[0].name,Selected_extension.value,false)}
        } else if (Conversion_mode == 2){
            const reader = new FileReader()
            let folder = {}
            let path = Selected_images.files[0].webkitRelativePath
            let folder_name = path.split("/")[path.split("/").length-2]
            const timer = ms => new Promise(res => setTimeout(res, ms))

            async function Save_images(){
                let iteration = 0
                for (let file of Selected_images.files){
                    folder[iteration]={}
                    console.log(iteration)
                    console.log(folder[iteration])
                    folder[iteration]["file_name"]=Selected_images.files[iteration].name
                    reader.readAsDataURL(file)
                    reader.onloadend =  async function(){
                        folder[iteration]["file_data"]=reader.result
                        await timer(100)
                    }
                    await timer(900)
                    iteration+=1
                }
                // console.log(folder)
                // for (let file in folder){
                //     console.log(folder[file])
                // }
            }
            await Save_images()
            console.log(folder)
            Multiple_conversion(folder,folder_name,Selected_extension.value,true)
        }
    }
})
