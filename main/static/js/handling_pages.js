/**manual functions**/


function myPage() {
    $('body').removeClass('body-log');
    OpenPage('myPage');
}

var friendPageFlag = true;

function myFriends() {
    OpenPage('myFriends');
    if (usersID && friendPageFlag) {
        friendPageFlag = false;
        var people = usersID['currentUser']['people'];
        for (var i = 0; i < people.length - 1; i++) {
            $('.friends').append($('.myfriends:first').clone());
            $('.myfriends').get(i).style.display = 'block';
        }
        for (i = 0; i < people.length; i++) {
            for (var key in people[i]) {
                if ($('.myfriends .' + key).attr('class') != undefined) {
                    if (key == 'online') {
                        if (people[i][key]) {
                            $('.state').get(i).classList.add('online');
                        }
                    }
                    else {
                        $('.myfriends .' + key).get(i).innerHTML = people[i][key];
                    }
                }
                else {
                    if (key == 'first_name') {
                        $('.myfriends .friendName').get(i).innerHTML = people[i]['first_name'] + ' ' + people[i]['last_name'];
                    }
                    else if (key == 'status') {
                        $('.myfriends .user-status').get(i).innerHTML = people[i][key];
                    }
                }

            }
        }
    }
}

function myMessages() {
    OpenPage('myMessages');

}

function myConfiguration() {
    OpenPage('myConfiguration');
    if (usersID) {
        var currentUser = usersID['currentUser'];
        for (var key in currentUser) {
            if (key == $('#' + key).attr('id') && currentUser[key]) {
                $('.inputs #' + key).val(currentUser[key]);
            }
        }
    }
}


var flag = false;


function openChat(friendFlag) {
    sendSocket();
    if (friendFlag) {
        $('#Friends').hide();
    }
    $('#Messages').hide();
    flag = true;
    $('#ChatWindow').show();
    sendSocket('joined', {'id': usersID}, function(){}, '/chat')
}

var socketFlag = 0;

function OpenPage(pageName) {
    var active = $('.active');
    var hideDiv = '#' + active[0].id.substr(2);
    var showDiv = '#' + pageName.substr(2);
    //var load = '#' + 'Load';
    if (socketFlag == 0) {
        //$(load).show();
        sendSocket('page', {}, putData, '/main');

        //setTimeout(function () {
        //    $(load).hide();
        //}, 2000);

        socketFlag++;
    }
    editImgs();
    pageName = '#' + pageName;

    active.removeClass('active');
    $(pageName).addClass('active');

    if (flag) {
        $('#ChatWindow').hide();
        flag = false;
    }
    $(hideDiv).hide();
    $(showDiv).show();

}


function putData(data) {
    console.log(data);
    $('#name').html(data['first_name'] + ' ' + data['last_name']);
    $('#city').html(data['city']);
    $('#mail').html(data['email']);
    $('#mail').attr('href', 'malito:' + data['email']);
    $('#tel').html(data['phone']);
    $('#tel').attr('href', 'tel:' + data['phone']);
    if (data['birthday'] != 'None') {
        $('#birthday').html(data['birthday']);
    }
    if (data['online']) {
        $('.state').addClass('online');
    }
    $('.user-status').html(data['status']);
    usersID['currentUser'] = data;
}

/** *************** **/