var modalWindow = document.getElementById('modalWindow');
var usersID = {};
var myPicture;
var myFriend;
var people;
var friendPageFlag = false; //friendPAgeFlag = false - function myFriends() doesn't put all data again
var flag = false;
var socketFlag = true;

$(document).ready(function () {
    if (socketFlag) {
        sendSocket('page', {}, putData, '/main');
        sendSocket('friends', {}, {}, '/main');
        socketFlag = false;
    }

    sendSocket('unique_wire', {}, '', '/chat');
});

setInterval(function () {
    console.log('Send');
    sendSocket('friends', {}, {}, '/main');
}, 15000);

socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');

socket.on('send_Message', function (data) {
    console.log(data);
    if ($('.wall').get(0).room == undefined) {
        msgNr(data['name'], data['msg'], data['id']);
    } else {
        var roomId = $('.wall').get(0).room.split('|');
        if ((data['id'] == +roomId[0] || data['id'] == +roomId[1]) && flag) {
            createMessage(data['msg'], data['id'], undefined, true, myPicture, myFriend, data['name']);
        }
        else {
            msgNr(data['name'], data['msg'], data['id']);
        }
    }
});

function searchById(id) {
    for (var key in people) {
        for (var newKey in people[key]) {
            if (newKey == 'id' && people[key][newKey] == id) {
                return key;
            }
        }
    }
}

socket.on('status', function (data) {
    $('.wall').get(0).room = data['room'];
    myPicture = usersID['currentUser']['picture'];
    myFriend = people[searchById(data['id'])]['picture'];

    document.getElementsByClassName('wall')[0].innerHTML = '';
    var history = data['history'];
    console.log(history);
    if (!$.isEmptyObject(history)) {
        for (var key in  history) {
            for (var idKey in history[key]) {
                if (history[key][idKey] != null && idKey != 'time') {
                    createMessage(history[key][idKey], idKey, history[key]['time'], false, myPicture, myFriend);
                }
            }
        }
    }

    $('#myPhoto').attr('src', myPicture);
    $('#friendPhoto').attr('src', myFriend);

    document.getElementById('newMessage').onkeypress = pressed;
    document.getElementById('buttonMessage').onclick = clicks;

    function pressed(e) {
        if (event.keyCode == 13) {
            socketMessage(data['room']);
            e.preventDefault();
        }
    }

    function clicks() {
        socketMessage(data['room']);
    }

});

function msgNr(name, msg, id) {
    var block = $('.messageNotification:first').clone();

        $('.lastNotification').remove();

    block[0].style.display = 'flex';
    block[0].firstElementChild.lastElementChild.innerHTML = new Date().getHours() + ':' + new Date().getMinutes();
    block[0].lastElementChild.firstElementChild.innerHTML = name;
    block[0].lastElementChild.childNodes['4'].innerHTML = msg;
    var picture = people[searchById(id)]['picture'];
    block[0].firstElementChild.firstElementChild.firstElementChild.setAttribute('src', picture);
    block.click(function (e) {
        block.remove();
        openChat(id);
    });
    block[0].lastElementChild.lastElementChild.addEventListener('click', function (e) {
        block.remove();
    });
    block[0].classList.add('lastNotification');
    $('body').append(block);
    var audio = new Audio('main/media/hangouts_message.mp3');
    audio.play();

    setTimeout(function () {
        block.remove();
    }, 5000);
}


socket.on('unique_wire', function (data) {
    sendSocket('joined', {'id': data['user']}, '', '/chat');
});


