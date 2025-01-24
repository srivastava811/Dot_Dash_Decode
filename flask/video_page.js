let v = document.querySelector("#videoElement");

if (navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(function (stream) {
            v.srcObject = stream;
        })
        .catch(function (error) {
            console.log("Something went wrong:", error);
        });
} else {
    console.log("getUserMedia not supported!");
}
