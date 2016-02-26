$(document).ready(function () {
    editImgs();
});


function editImgs() {  //add func for modal window to all imgs
    var imgs = document.getElementsByTagName('img');
    for (var i = 0; i < imgs.length; i++) {
        imgs[i].setAttribute('onclick', 'openModal(this)');
    }
}


// =================================================

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

// ====================================================

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

// ===========================================================

function createMessage() {
    var mess = document.getElementById('newMessage').value;
    if (mess != '' && mess != undefined && mess[0] != '\n') {
        var miniMessage = document.createElement('div');
        miniMessage.classList.add('miniMessage');
        var photoDate = document.createElement('div');
        photoDate.classList.add('photoDate');
        var friendPhoto = document.createElement('div');
        friendPhoto.classList.add('friendPhoto');
        var img = document.createElement('img');
        img.src = 'img/hulk.jpg';
        var date = document.createElement('span');
        date.classList.add('date');
        date.innerHTML = (new Date()).getHours() + ':' + (new Date()).getMinutes();
        var minMessage = document.createElement('span');
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
        return false;
    }

}

/**manual functions**/


function myPage() {
    OpenPage('myPage');
}

function myFriends() {
    OpenPage('myFriends');

}

function myMessages() {
    OpenPage('myMessages');

}

function myConfiguration() {
    OpenPage('myConfiguration');

}

var flag = false; //flag for hiding chat

function openChat() {
    $('#Messages').hide();
    flag = true;
    $('#ChatWindow').show();

}


function OpenPage(pageName) {
    var active = $('.active');
    var hideDiv = '#' + active[0].id.substr(2);
    var showDiv = '#' + pageName.substr(2);
    pageName = '#' + pageName;

    active.removeClass('active');
    $(pageName).addClass('active');

    if (flag){
        $('#ChatWindow').hide();
    }
    $(hideDiv).hide();
    $(showDiv).show();
}
/** *************** **/