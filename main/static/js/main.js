$(document).ready(function () {
    OpenPage($('.active')[0].id.substr(0));
    sendSocket('chat_all', {}, function () {
    }, '/chat')


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

socket.on('chat_open', function (data) {
    console.log('chat_open');
    console.log(data);
    if (data['flag'] && (data['id'] == usersID['currentUser']['id'])) {
        console.log('sending to join this current_user : ' + data['id']);
        sendSocket('joined', {'id': data['user']}, function () {}, '/chat')
    }

});