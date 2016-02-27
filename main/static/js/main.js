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

    var active = $('.active');
    var hideDiv = '#' + active[0].id.substr(2);
    var showDiv = '#' + pageName.substr(2);
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
/** *************** **/

/***********validation********* */


function validation(emitName, obj, fn){  //send socket to validate any value of obj, fn - callback function
    var socket;
        socket = io.connect('http://' + document.domain + ':' + location.port + '/reg');

        socket.emit(emitName, obj);

        socket.on('flag', function (data) {
            console.log(data);
             fn(data['extra']);
        });
}



function checkValue(obj, val, i){ //check value of inputs, i - index of input
    if (val){
        switch (obj.id){
            case 'log-email':
                validation('validationEmail', {email:  val},
                    function(bool){
                        if(bool){
                            obj.check = true;
                            if (obj.cross){
                                document.getElementsByClassName('fa-times')[i].style.display = 'none';
                                obj.cross = false;
                            }
                            document.getElementsByClassName('fa-check')[i].style.display = 'inline-block';
                        }
                        else{
                            obj.cross = true;
                            if (obj.check){
                                document.getElementsByClassName('fa-check')[i].style.display = 'none';
                                obj.check = false;
                            }
                            document.getElementsByClassName('fa-times')[i].style.display = 'inline-block';
                        }
                    }
                );
                break;
            case 'log-pass2':
                    if (val == $('#log-pass1').val()){
                        obj.check = true;
                        if (obj.cross){
                            document.getElementsByClassName('fa-times')[i].style.display = 'none';
                            obj.cross = false;
                        }
                        document.getElementsByClassName('fa-check')[i].style.display = 'inline-block';
                    }
                    else {
                        obj.cross = true;
                        if (obj.check){
                            document.getElementsByClassName('fa-check')[i].style.display = 'none';
                            obj.check = false;
                        }
                        document.getElementsByClassName('fa-times')[i].style.display = 'inline-block';
                    }
                break;
            default:
                obj.check = true;
                if (obj.cross){
                    document.getElementsByClassName('fa-times')[i].style.display = 'none';
                    obj.cross = false;
                }
                document.getElementsByClassName('fa-check')[i].style.display = 'inline-block';
                break;
        }
    }
    else {
        obj.cross = true;
        if (obj.check){
            document.getElementsByClassName('fa-check')[i].style.display = 'none';
            obj.check = false;
        }
        document.getElementsByClassName('fa-times')[i].style.display = 'inline-block';
    }
}



