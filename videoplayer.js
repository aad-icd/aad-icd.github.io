var videoList = [
    "videos/AAD Groupwork VEOM.mp4",
    "videos/AAD-CityDraft.mp4",
    "videos/shevillon_aad22_1.mp4",
    ]
    var curVideo = 0;
    var videoPlayer = document.getElementById('vid');

    console.log(videoPlayer)

    videoPlayer.onended = function(){
    curVideo++;  

    if(curVideo < videoList.length){            
    videoPlayer.src = videoList[curVideo];  
     
    }  
    if (curVideo == videoList.length){
    curVideo=0;
    videoPlayer.src = videoList[curVideo];       
    }
    }
