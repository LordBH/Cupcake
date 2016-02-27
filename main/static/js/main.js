$(document).ready(function () {
    OpenPage($('.active')[0].id.substr(0));
});

var modalWindow = document.getElementById('modalWindow');


function editImgs() {  //add func for modal window to all imgs
    var imgs = document.getElementsByTagName('img');
    for (var i = 0; i < imgs.length; i++) {
        imgs[i].setAttribute('onclick', 'openModal(this)');
    }
}


// =================================================

function openModal(img) {   //open modal window
    console.log('edit');
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
    $('body').removeClass('body-log');
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

var flag = false;

function openChat() {
    $('#Messages').hide();
    flag = true;
    $('#ChatWindow').show();

}


function OpenPage(pageName) {
    editImgs();
    var active = $('.active');
    var hideDiv = '#' + active[0].id.substr(2);
    var showDiv = '#' + pageName.substr(2);
    sendSocket('page', {id : pageName}, function(){},'/main');
    pageName = '#' + pageName;

    active.removeClass('active');
    $(pageName).addClass('active');

    if (flag){
        $('#ChatWindow').hide();
        flag = false;
    }

    $(hideDiv).hide();
    $(showDiv).show();
}


function putData(page, obj){

}

/** *************** **/

/***********validation********* */

function sendSocket(emitName, obj, fn, namespace){  //send socket to validate any value of obj, fn - callback function
    var socket;
        socket = io.connect('http://' + document.domain + ':' + location.port + namespace);

        socket.emit(emitName, obj);

        socket.on('flag', function (data) {
             fn(data['extra'], 2);
        });

        socket.on('userData', function(data){
            if (data['flag']){
                console.log('lalka');
            }
            else{
                $('#wrapper').innerHTML = '404';
            }
        });
}

function checks(flag, i) {
    if (flag) {
        document.getElementsByClassName('fa-times')[i].style.display = 'none';
        document.getElementsByClassName('fa-check')[i].style.display = 'inline-block';
    }
    else {
        document.getElementsByClassName('fa-check')[i].style.display = 'none';
        document.getElementsByClassName('fa-times')[i].style.display = 'inline-block';
    }
}



function checkValue(obj, val, i){ //check value of inputs, i - index of input
    if (val){
        switch (obj.id){
            case 'log-email':
                sendSocket('validationEmail', {email:  val}, checks, '/reg');
                break;
            case 'log-pass2':
                checkPass2(val, i);
                break;
            case 'log-pass1':
                checks(obj, i);
                if ($('#log-pass2').val()){
                    checkPass2($('#log-pass2').val(), 4);
                }
                break;
            default:
                checks(true, i);
                break;
        }
    }
    else {
        if (obj.id = 'log-pass1'){
            if ($('#log-pass2').val()){
                checkPass2($('#log-pass2').val(), 4);
            }
        }
        checks(false, i);
    }
}

function checkPass2(val, i){
    if (val == $('#log-pass1').val()){
        checks(true, i);
    }
    else {
        checks(false, i);
    }
}


