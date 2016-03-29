socket = io.connect('http://' + document.domain + ':' + location.port + '/main');

socket.on('people', function (data) {
    people = data['people'];
    if (friendPageFlag){
        putMyfriendsData();
        removeAnimation();
        $('.left-side').get(0).style.display = 'block';
        friendPageFlag = false;
    }
});

function myPage() {
    $('body').removeClass('body-log');
    OpenPage('myPage');
}

function myFriends() {
    friendPageFlag = true;
    OpenPage('myFriends');
}

function putMyfriendsData() {
    if (usersID) {
        $('.myfriends:not(.original)').remove();
        for (var i = 0; i < people.length - 1; i++) {
            var block = $('.original:first').clone();
            block[0].classList.remove('original');
            $('.friends').append(block[0]);
        }
        for (i = 0; i < people.length; i++) {
            $('.myfriends').css('display', 'block');
            for (var key in people[i]) {
                if ($('.myfriends .' + key).attr('class') != undefined) {
                    if (key == 'birthday') {
                        if (people[i][key] != 'None') {
                            var date = new Date(Date.parse(people[i][key]));
                            $('.myfriends .' + key).get(i).innerHTML = date.getDay() + '-' + date.getDate() + '-' + date.getFullYear();
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
                    else if (key == 'online') {
                        if (people[i][key]) {
                            $('.myfriends .state').get(i).classList.add('online-state');
                        }
                    }
                    else if (key == 'id') {
                        $('.sendMessage').get(i).setAttribute('onclick', 'openChat(' + people[i][key] + ')');
                    }
                    else if (key == 'picture') {
                        $('.myfriends .userImg').get(i).setAttribute('src', people[i][key]);
                    }
                }
            }
        }
    }
}


function myConfiguration() {
    OpenPage('myConfiguration');
    if (usersID) {
        var currentUser = usersID['currentUser'];
        for (var key in currentUser) {
            if (key == $('#' + key).attr('id') && currentUser[key]) {
                $('.inputs #' + key).val(currentUser[key]);
            }
            if (key == 'birthday') {
                var now = new Date(Date.parse(currentUser[key]));
                var day = ("0" + now.getDate()).slice(-2);
                var month = ("0" + (now.getMonth() + 1)).slice(-2);
                var today = now.getFullYear() + "-" + (month) + "-" + (day);
                $('.inputs #' + key).val(today);
            }
        }
    }
}


function openChat(id) {
    sendSocket('joined', {'id': id}, '', '/chat');
    $('#Friends').hide();
    $('#Page').hide();
    flag = true;
    $('#ChatWindow').show();
    var scrollDiv = document.getElementById("scroll_div");
    scrollDiv.scrollTop = scrollDiv.scrollHeight;
}



function OpenPage(pageName) {
    if (pageName == 'myFriends'){
        sendSocket('friends', {}, function () {
        }, '/main');
    }
    var active = $('.active');
    var hideDiv = '#' + active[0].id.substr(2);
    var showDiv = '#' + pageName.substr(2);

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
    $('#name').html(data['first_name'] + ' ' + data['last_name']);
    $('#city').html(data['city']);
    $('#mail').html(data['email']);
    $('#mail').attr('href', 'malito:' + data['email']);
    $('#tel').html(data['phone']);
    $('#tel').attr('href', 'tel:' + data['phone']);
    $('.mainPhoto .userImg').attr('src', data['picture']);
    $('.user-status').html(data['status']);

    if (data['birthday'] != 'None') {
        var date = new Date(Date.parse(data['birthday']));
        $('#birthday').html(date.getDay() + '-' + date.getDate() + '-' + date.getFullYear());
    }
    if (data['online']) {
        $('#Page .state').addClass('online-state');
    }
    if (data['rooms']) {
        sendSocket('join_all_rooms', {'rooms': data['rooms']}, '', '/chat');
    }
    usersID['currentUser'] = data;
}
