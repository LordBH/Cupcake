$(document).ready(function () {
    var cookie = document.cookie.split('=#')[1];
    console.log($('.active')[0].id.substr(0), cookie);
    OpenPage($('.active')[0].id.substr(0));
    sendSocket('unique_wire', {}, function () {}, '/chat');
});

var modalWindow = document.getElementById('modalWindow');
var usersID = {};
var chatRoom;

socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');

socket.on('send_Message', function (data) {
    console.log('send message: ');
    console.log(data);
    if (chatRoom == data['id']) {
        createMessage(data['msg'], data['id']);
    }
});

socket.on('status', function (data) {
    chatRoom = data['room'];
    console.log(chatRoom);
    $('.wall')[0].innerHTML = '';
    console.log('status socket: ');
    console.log(data);
    var history = data['history'];
    if (!$.isEmptyObject(history)) {
        console.log('history is not empty');
        for (var i = 0; i < history.length; i++) {
            for (var idKey in history[i]) {
                if (history[i][idKey] != null && idKey != 'time') {
                    createMessage(history[i][idKey], idKey, history[i]['time']);
                }
            }
        }
    }
    $('.typeMessage .sendMessage').click(function (e) {
        console.log('send message')
        socketMessage(data['room']);
    });
    $('#newMessage').keypress(function (e) {
        if (event.keyCode == 13) {
            socketMessage(data['room']);
            e.preventDefault();
        }
    })

});

function msgNr(name, msg, id){
    var block = $('.messageNotification').clone();
    console.log(block);
    block.css('display', 'flex');
    block[0].firstElementChild.lastElementChild.innerHTML =  new Date().getHours() +':'+ new Date().getMinutes();
    block[0].lastElementChild.firstElementChild.innerHTML = name;
    block[0].lastElementChild.lastElementChild.innerHTML = msg;
    block.click(function(e){
        block.remove();
        openChat(id);
    });
    $('body').append(block);
}

msgNr('Alex Bondarenko', 'hello how are you?', 1);

socket.on('msg', function(data){

});

socket.on('unique_wire', function (data) {
    console.log('unique_wire');
    console.log(data);
    sendSocket('joined', {'id': data['user']}, function () {
    }, '/chat')

});

function notifyMessage(index) {
    var button = $('.myfriends .sendMessage');
    button.get(index).innerHTML = '<i class="fa fa-envelope"></i> You got new message';
    button.get(index).classList.add('getNewMessage');
}


