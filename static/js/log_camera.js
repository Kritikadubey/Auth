//handel file input
const retakeButtonLog = document.getElementById("retake-log");
const submitButtonLog = document.getElementById("submit-log");
const captureButtonLog = document.getElementById("captureButtonLog");
const uploadedImageLog = document.getElementById("uploadedImageLog");
const uploadLabel = document.getElementById("upload-log");
const videoLog = document.getElementById("video-log");
const canvasLog = document.getElementById("canvas-log");
let frames;
let currPage = window.location.href;

if(currPage.endsWith("third")){
    navigator.mediaDevices.getUserMedia({video:true}).then(frames=>{
        videoLog.srcObject = frames;
    }).catch(err=>{
        console.log(err);
    })
};

if(retakeButtonLog){
    retakeButtonLog.addEventListener("click", ()=>{
        window.location.reload();
    })    
}


async function submitLogImg(){
    const canvas = document.createElement("canvas");
    const ctx = canvas.getContext("2d");
    canvas.width = uploadedImageLog.width;
    canvas.height = uploadedImageLog.height;
    
    ctx.drawImage(uploadedImageLog, 0, 0, uploadedImageLog.width, uploadedImageLog.height);

    canvas.toBlob((blob)=>{
        const formData = new FormData();
        formData.append("image", blob, "image.jpg");
        formData.append("email", sessionStorage.getItem("currEmail"));
        fetch("/last_login", {
            method: "POST",
            body : formData
        })
        .then(response => response.json())
        .then(data=>{
            if(data.status == "success"){
                window.location.replace("/profile/" + sessionStorage.getItem("currEmail"));
            }
            else{
                alert("Not matched Please retake the photo !");
            }
        })
        .catch(error=>{
            console.log("Error: ", error);
        })
    })
}
if(submitButtonLog){
    submitButtonLog.addEventListener("click", (event)=>{
        submitLogImg();
    })
}

if(captureButtonLog){
    captureButtonLog.addEventListener('click', (event, frames)=>{
        const contex = canvasLog.getContext('2d');
        console.log('Clicked');
        contex.drawImage(videoLog, 0, 0, canvasLog.width, canvasLog.height);
        const imagedata = canvasLog.toDataURL("image/png");
        uploadedImageLog.src = imagedata;
        uploadedImageLog.style.display = "block";
        if(frames){
            const tracks = frames.getTracks();
            tracks.forEach(track => {
                track.stop();
            });
        }
        videoLog.srcObject = null;
        videoLog.style.display = "none";
        captureButtonLog.style.display = "none";
        uploadLabel.style.display = "none";
        retakeButtonLog.style.display = "inline-block";
        submitButtonLog.style.display = "inline-block";
    });
}

