$(document).ready(function () {
    OpenPage($('.active')[0].id.substr(0));
    sendSocket('unique_wire', {}, function () {}, '/chat');
});

var modalWindow = document.getElementById('modalWindow');
var usersID = {};
var myPicture;
var myFriend;

socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');

socket.on('send_Message', function (data) {
    //console.log('send message: ');
    console.log(data);
    if (data['id'] != usersID['currentUser']['id'] && !flag){
        //console.log(data['id']);
        //console.log(searchById(data['id']));
        //console.log(people[searchById(data['id'])]['picture']);
        //console.log();
        //
        //var pic =  people[searchById(data['id'])]['picture'];
        msgNr(data['name'], data['msg'], data['id']);
    }else{
        createMessage(data['msg'], data['id'], undefined, true, myPicture, myFriend);
    }
});

function searchById(id){
    console.log(id);
    for (var key in people){
        for (var newKey in people[key]){
            if (newKey == 'id' && people[key][newKey] == id){
                console.log(newKey, people[key][newKey], key);
                 return key
            }
        }
    }
}

socket.on('status', function (data) {
    console.log(data);
    myPicture = usersID['currentUser']['picture'];
    console.log(people[searchById(data['id'])]['picture']);

    myFriend =  people[searchById(data['id'])]['picture'];


    document.getElementsByClassName('wall')[0].innerHTML = '';
    console.log(document.getElementsByClassName('wall')[0]);
    var history = data['history'];
    if (!$.isEmptyObject(history)) {
        //console.log('history is not empty');
        //console.log(history);
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

    //$('.typeMessage .sendMessage').click(function (e) {
    //    console.log('send message: '+ data['room']);
    //    socketMessage(data['room']);
    //});
    //$('#newMessage').keypress(function (e) {
    //    if (event.keyCode == 13) {
    //        console.log('send message: '+ data['room']);
    //        socketMessage(data['room']);
    //        e.preventDefault();
    //    }
    //})

});

function msgNr(name, msg, id, picture){
    var block = $('.messageNotification').clone();
    block.css('display', 'flex');
    block[0].firstElementChild.lastElementChild.innerHTML =  new Date().getHours() +':'+ new Date().getMinutes();
    block[0].lastElementChild.firstElementChild.innerHTML = name;
    block[0].lastElementChild.lastElementChild.innerHTML = msg;
    $('.notifPhoto').attr('src', picture);
    block.click(function(e){
        block.remove();
        openChat(id);
    });
    $('body').append(block);
}


socket.on('msg', function(data){

});

socket.on('unique_wire', function (data) {
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


