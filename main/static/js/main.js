$(document).ready(function () {
    OpenPage($('.active')[0].id.substr(0));
    sendSocket('unique_wire', {}, function () {}, '/chat');
});

var modalWindow = document.getElementById('modalWindow');
var usersID = {};
var myPicture;
var myFriend;
var people;
var friendPageFlag = true; //friendPAgeFlag = false - function myFriends() doesn't put all data again

socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');

socket.on('send_Message', function (data) {
    removeAnimation();
    if ($('.wall').get(0).room == undefined || !flag){
        msgNr(data['name'], data['msg'], data['id']);
    }else{
        var roomId = $('.wall').get(0).room.split('|');
        if(data['id'] == +roomId[0] || data['id'] == +roomId[1]){
            createMessage(data['msg'], data['id'], undefined, true, myPicture, myFriend);
        }
        else{
            msgNr(data['name'], data['msg'], data['id']);
        }
    }
});

function searchById(id){
    for (var key in people){
        for (var newKey in people[key]){
            if (newKey == 'id' && people[key][newKey] == id){
                console.log(newKey, people[key][newKey], key);
                 return key;
            }
        }
    }
}

socket.on('status', function (data) {
    removeAnimation();
    $('.wall').get(0).room = data['room'];
    myPicture = usersID['currentUser']['picture'];
    myFriend =  people[searchById(data['id'])]['picture'];

    document.getElementsByClassName('wall')[0].innerHTML = '';
    var history = data['history'];
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

    function pressed(e){
        if (event.keyCode == 13) {
            console.log('send message: '+ data['room']);
            socketMessage(data['room']);
            e.preventDefault();
        }
    }

    function clicks(){
        socketMessage(data['room']);
    }

});

function msgNr(name, msg, id){
    var block = $('.messageNotification').clone();
    block.css('display', 'flex');
    block[0].firstElementChild.lastElementChild.innerHTML =  new Date().getHours() +':'+ new Date().getMinutes();
    block[0].lastElementChild.firstElementChild.innerHTML = name;
    block[0].lastElementChild.lastElementChild.innerHTML = msg;
    var picture = people[searchById(id)]['picture'];
    console.log(picture);
    block[0].firstElementChild.firstElementChild.firstElementChild.setAttribute('src', picture);
    block.click(function(e){
        block.remove();
        openChat(id);
    });
    $('body').append(block);
}


socket.on('unique_wire', function (data) {
    removeAnimation();
    //console.log('unique_wire');
    //console.log(data);
    sendSocket('joined', {'id': data['user']}, function () {
    }, '/chat')

});

function notifyMessage(index) {
    var button = $('.myfriends .sendMessage');
    button.get(index).innerHTML = '<i class="fa fa-envelope"></i> You got new message';
    button.get(index).classList.add('getNewMessage');
}


