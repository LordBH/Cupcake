$(document).ready(function () {
    OpenPage($('.active')[0].id.substr(0));
    sendSocket('unique_wire', {}, function () {
    }, '/chat')


    var audio = new Audio('main/media/hangouts_message.mp3');
    audio.play();


});

var modalWindow = document.getElementById('modalWindow');
var usersID = {};

socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');

socket.on('send_Message', function (data) {
    console.log('send_Message');
    console.log(data);
});

socket.on('status', function (data) {
    console.log('status');
    console.log(data);
});

socket.on('unique_wire', function (data) {
    console.log('unique_wire');
    console.log(data);
    sendSocket('joined', {'id': data['user']}, function () {}, '/chat')

});


