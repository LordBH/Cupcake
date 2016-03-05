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

function createMessage() {
    var mess = document.getElementById('newMessage').value;
    if (mess != '' && mess != undefined && mess[0] != '\n') {
        var miniMessage = document.createElement('div');
        var photoDate = document.createElement('div');
        var friendPhoto = document.createElement('div');
        var img = document.createElement('img');
        var date = document.createElement('span');
        var minMessage = document.createElement('span');

        miniMessage.classList.add('miniMessage');
        photoDate.classList.add('photoDate');
        friendPhoto.classList.add('friendPhoto');
        img.src = 'img/hulk.jpg';
        date.classList.add('date');
        date.innerHTML = (new Date()).getHours() + ':' + (new Date()).getMinutes();
        minMessage.classList.add('minMessage');
        minMessage.innerHTML = mess;

        friendPhoto.appendChild(img);
        photoDate.appendChild(friendPhoto);
        photoDate.appendChild(date);
        miniMessage.appendChild(photoDate);
        miniMessage.appendChild(minMessage);
        document.getElementsByClassName('wall')[0].appendChild(miniMessage);
        document.getElementById('newMessage').value = '';
        document.getElementById('newMessage').focus();

        sendSocket('message', {'room': '7|2', 'msg': minMessage.innerHTML}, {}, '/chat');
        return false;
    }
}

