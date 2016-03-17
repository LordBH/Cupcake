/**manual functions**/
var people, friendPageFlag = true; //friendPAgeFlag = false - function myFriends() doesn't put all data again

function myPage() {
    $('body').removeClass('body-log');
    OpenPage('myPage');
}

function myFriends() {
    OpenPage('myFriends');
    if (usersID && friendPageFlag) {
        friendPageFlag = false;
        people = usersID['currentUser']['people'];
        //console.log(people);
        for (var i = 0; i < people.length - 1; i++) {
            $('.friends').append($('.myfriends:first').clone());
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
                        //console.log(key);
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
                        //console.log(people[i]['id']+' '+people[i][key]);
                        if (people[i][key]) {
                            $('.myfriends .state').get(i).classList.add('online-state');
                        }
                    }
                    else if (key == 'id') {
                        //chatRooms.unshift({room : usersID['currentUser']['id'] +'|'+ people[i][key]});
                        $('.sendMessage').get(i).setAttribute('onclick', 'openChat(' + people[i][key] + ')');
                    }
                    else if (key == 'picture'){
                        $('.myfriends .userImg').get(i).setAttribute('src', people[i][key]);
                    }
                }
            }
        }
       // notifyMessage(1);
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


var flag = false;

function openChat(id) {
    sendSocket('joined', {'id': id}, function () {}, '/chat');

    $('#Friends').hide();
    $('#Page').hide();
    flag = true;
    $('#ChatWindow').show();
    var scrollDiv = document.getElementById("scroll_div");
    scrollDiv.scrollTop = scrollDiv.scrollHeight;
}

var socketFlag = 0;

function OpenPage(pageName) {
    var load = '#' + 'Load';
    if (socketFlag == 0) {
        var link  = document.createElement('link');
        link.rel  = 'stylesheet';
        link.type = 'text/css';
        link.id = 'animation';
        link.href = '/main/css/loading.css';

        $('head').append(link);
        $(load).show();

        sendSocket('page', {}, putData, '/main');
        socketFlag++;
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
    document.cookie = 'page=' + pageName;
}


function putData(data) {
    console.log(data);
    $('#name').html(data['first_name'] + ' ' + data['last_name']);
    $('#city').html(data['city']);
    $('#mail').html(data['email']);
    $('#mail').attr('href', 'malito:' + data['email']);
    $('#tel').html(data['phone']);
    $('#tel').attr('href', 'tel:' + data['phone']);
    $('.mainPhoto .userImg').attr('src', data['picture']);
    if (data['birthday'] != 'None') {
        var date = new Date(Date.parse(data['birthday']));
        $('#birthday').html(date.getDay() + '-' + date.getDate() + '-' + date.getFullYear());
    }
    if (data['online']) {
        $('#Page .state').addClass('online-state');
    }
    //if (!data['activated']){
    //    $('#ConfirmEmail').show();
    //    $('#ConfirmEmail span').html(data['email']);
    //}
    if (data['rooms']) {
        sendSocket('join_all_rooms', {'rooms': data['rooms']}, function () {
        }, '/chat');
    }
    $('.user-status').html(data['status']);
    usersID['currentUser'] = data;

}

function removeAnimation(){
    setTimeout(function(){
        $('#animation').remove();
        $('#Load').hide();
    }, 2000);
}

/** *************** **/