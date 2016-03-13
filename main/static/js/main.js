$(document).ready(function () {
    OpenPage($('.active')[0].id.substr(0));
    sendSocket('unique_wire', {}, function () {
    }, '/chat');
});

var modalWindow = document.getElementById('modalWindow');
var usersID = {};
var chatRooms = [];

socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');

socket.on('send_Message', function (data) {
    console.log(data);
    createMessage(data['msg'], data['id']);
});

socket.on('status', function (data) {
    console.log('status socket');
    for (var i = 0; i < chatRooms.length; i++){
        if (data['room'] == chatRooms[i]['room']){
            var currentRoom = chatRooms[i];
        }
    }
    var history = currentRoom.history = data['history'];
    console.log(history);
    if (!$.isEmptyObject(history)) {
        console.log('history is not empty');
        //for (var key in history){
        //    for (var idKey in history[key]){
        //        console.log(history[key][idKey]);
        //        if (history[key][idKey] != null && idKey != 'time'){
        //            createMessage(history[key][idKey], idKey, history[key]['time']);
        //        }
        //    }
        //}
    }
    $('.typeMessage .sendMessage').click(function (e) {
        socketMessage(data['room']);
    });
    $('#newMessage').keypress(function (e) {
        if (event.keyCode == 13) {
            socketMessage(data['room']);
            e.preventDefault();
        }
    })

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


