$(document).ready(function () {
    OpenPage($('.active')[0].id.substr(0));
    sendSocket('unique_wire', {}, function () {}, '/chat');
});

var modalWindow = document.getElementById('modalWindow');
var usersID = {};

socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');

socket.on('send_Message', function (data) {
    console.log('send message' + data);
    createMessage(data['msg']);
});

socket.on('status', function (data) {
    console.log('send joined');
    $('.typeMessage .sendMessage').click(function(e){
       socketMessage(data['room']);
    });
    $('#newMessage').keypress(function(e){
        if (event.keyCode == 13){
            socketMessage(data['room']);
            e.preventDefault();
        }
    })

});

socket.on('unique_wire', function (data) {
    console.log('unique_wire');
    console.log(data);
    sendSocket('joined', {'id': data['user']}, function () {}, '/chat')

});


