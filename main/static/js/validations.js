/***********validation********* */

function sendSocket(emitName, obj, fn, namespace) {  //send socket to validate any value of obj, fn - callback function
    var socket;
    socket = io.connect('http://' + document.domain + ':' + location.port + namespace);

    socket.emit(emitName, obj);

    socket.on('flag', function (data) {
        console.log('flag');
        fn(data['extra'], 2);
    });

    socket.on('chat_open', function (data) {
        console.log('chat_open');
        if (data['flag'] && (data['id'] == usersID['currentUser']['id'])){
            console.log('sending to join this current_user' + data['id']);
            sendSocket('joined', {}, function(){}, '/chat')
        }
    });

    socket.on('userData', function (data) {
        console.log('userData');
        if (data['flag']) {
            fn(data);
        }
        else {
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


function checkValue(obj, val, i) { //check value of inputs, i - index of input
    if (val) {
        switch (obj.id) {
            case 'log-email':
                sendSocket('validationEmail', {email: val}, checks, '/reg');
                break;
            case 'log-pass2':
                checkPass2(val, i);
                break;
            case 'log-pass1':
                checks(obj, i);
                if ($('#log-pass2').val()) {
                    checkPass2($('#log-pass2').val(), 4);
                }
                break;
            default:
                checks(true, i);
                break;
        }
    }
    else {
        if (obj.id = 'log-pass1') {
            if ($('#log-pass2').val()) {
                checkPass2($('#log-pass2').val(), 4);
            }
        }
        checks(false, i);
    }
}

function checkPass2(val, i) {
    if (val == $('#log-pass1').val()) {
        checks(true, i);
    }
    else {
        checks(false, i);
    }
}

