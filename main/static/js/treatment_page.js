function openModal(img) {   //open modal window
    var imgContainer = document.getElementById('imgContainer');
    imgContainer.innerHTML = '';
    modalWindow.style.display = 'block';
    var localImg = img.cloneNode(true);
    imgContainer.appendChild(localImg);
}

function closeModal() {
    modalWindow.style.display = 'none';
}


function editImgs() {  //add func for modal window to all imgs
    var imgs = document.getElementsByTagName('img');
    for (var i = 0; i < imgs.length; i++) {
        imgs[i].setAttribute('onclick', 'openModal(this)');
    }
}

/* ******************************   ******************************  */

function changeTextArea(val) {
    var span = document.getElementById("commentChg");
    if (val.length > 20) {
        val = val.split(' ');
        val.push('\n');
        val = val.join(' ');
        span.innerHTML = val;
    }
    else {
        span.innerHTML = val;
    }
}

function showPhoto() {
    document.getElementById('mainPhComm').style.display = 'block';
}

function checkArea(val) {
    if (!val) {
        document.getElementById('mainPhComm').style.display = 'none';
    }
}

/* ******************************   ******************************  */

function socketMessage(room) {
    if (room) {
        var mess = document.getElementById('newMessage').value;
        sendSocket('message', {'room': room, 'msg': mess}, function () {}, '/chat');
    }
}

function createMessage(mess, id, time, audio, myimg, myfriend) {
    if (mess != '' && mess != undefined && mess[0] != '\n') {
        var picture;
        if (id != usersID['currentUser']['id'] && id != undefined && audio) {
            var audio = new Audio('main/media/hangouts_message.mp3');
            audio.play();
        }

        if (id != usersID['currentUser']['id']){
            picture = myfriend;
        }
        else{
            picture = myimg;
        }
        var miniMessage = document.createElement('div');
        var photoDate = document.createElement('div');
        var friendPhoto = document.createElement('div');
        var img = document.createElement('img');
        var date = document.createElement('span');
        //var name = document.createElement('span');
        var minMessage = document.createElement('span');

        miniMessage.classList.add('miniMessage');
        photoDate.classList.add('photoDate');
        friendPhoto.classList.add('friendPhoto');
        img.src = picture;
        date.classList.add('date');
        if (time == undefined){
            date.innerHTML = (new Date()).getHours() + ':' + (new Date()).getMinutes();
        }
        else {
            date.innerHTML = (new Date(time)).getHours() + ':' + (new Date(time)).getMinutes();
        }
        minMessage.classList.add('minMessage');
        minMessage.innerHTML = mess;
        //name.classList.add('MessageName');
        //name.innerHTML =

        friendPhoto.appendChild(img);
        photoDate.appendChild(friendPhoto);
        photoDate.appendChild(date);
        miniMessage.appendChild(photoDate);
        miniMessage.appendChild(minMessage);
        document.getElementsByClassName('wall')[0].appendChild(miniMessage);
        document.getElementById('newMessage').value = '';
        document.getElementById('newMessage').focus();
        var scrollDiv = document.getElementById("scroll_div");
        scrollDiv.scrollTop = scrollDiv.scrollHeight;
    }
}

