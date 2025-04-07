//handel file input
const fileInput = document.getElementById("fileInput");
const uploadedImage = document.getElementById("uploadedImage");
const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const captureButton = document.getElementById("captureButton");
const captureLabel = document.getElementById("upload-by-clicking");
const retakeButton = document.getElementById("retake-reg");
const submitButton = document.getElementById("submit-reg");
let stream;
var site = window.location.href;

if(site.endsWith("second_register")){
    navigator.mediaDevices.getUserMedia({video:true}).then(stream=>{
        video.srcObject = stream;
    }).catch(err=>{
        console.log(err);
    })
};
if(retakeButton){
    retakeButton.addEventListener("click", ()=>{
        window.location.reload();
    })
}

async function submitRegImage(){
    const canvas = document.createElement("canvas");
    const ctx = canvas.getContext("2d");
    canvas.width = uploadedImage.width;
    canvas.height = uploadedImage.height;

    ctx.drawImage(uploadedImage, 0, 0, uploadedImage.width, uploadedImage.height);

    canvas.toBlob((blob)=>{
        const formData = new FormData();
        formData.append("image", blob, "image.jpg");
        fetch("/third_register_validation", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data =>{
            console.log("sucssesfully send", data);
            if(data.status == "success"){
                try{
                    const currInfo = JSON.parse(sessionStorage.getItem(sessionStorage.getItem("currEmail")));
                    currInfo.face_embbeding = data.encoding;
                    sessionStorage.setItem(sessionStorage.getItem("currEmail"), JSON.stringify(currInfo));
                    window.location.replace("/third_register/"+sessionStorage.getItem("currEmail"));
                }
                catch(error){
                    console.log("Error: ", error);
                    alert("Something went Wrong !");
                }
            }
            else{
                alert(data.description + ", Retake the image");
            }
        })
        .catch(error =>{
            console.log("Error: ", error);
        })
    }, "image/jpeg");
}

if(submitButton){
    submitButton.addEventListener("click", (event)=>{
        const emailInfo = sessionStorage.getItem("currEmail"); 
        const info = sessionStorage.getItem(emailInfo);
        console.log(info);
        console.log(emailInfo);
        submitRegImage();
    });
}

if(fileInput){
    fileInput.addEventListener('change', (event)=>{
        const file = event.target.files[0];
        if(file){
            const reader = new FileReader();
            reader.onload = function(e){
                uploadedImage.src = e.target.result;
                uploadedImage.style.display = "block";
                uploadedImage.style.width = "320px";
                uploadedImage.style.height = "240px";
                uploadedImage.style.alignSelf = "center";
                video.style.display = "none";
                captureButton.style.display = "none";
                captureLabel.style.display = "none";
                submitButton.style.display = "inline-block";
                retakeButton.style.display = "inline-block";
            };
            reader.readAsDataURL(file);
        }
    });
}



if(captureButton){
    captureButton.addEventListener('click', (event, stream)=>{
        const contex = canvas.getContext('2d');
        console.log('Clicked');
        contex.drawImage(video, 0, 0, canvas.width, canvas.height);
        const imagedata = canvas.toDataURL("image/png");
        uploadedImage.src = imagedata;
        uploadedImage.style.display = "block";
        if(stream){
            const tracks = stream.getTracks();
            tracks.forEach(track => {
                track.stop();
            });
        }
        video.srcObject = null;
        video.style.display = "none";
        captureButton.style.display = "none";
        captureLabel.style.display = "none";
        retakeButton.style.display = "inline-block";
        submitButton.style.display = "inline-block";
    });
}

