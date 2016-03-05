$(document).ready(function () {
    OpenPage($('.active')[0].id.substr(0));
    sendSocket('chat_all', {}, function(){}, '/chat')


});

var modalWindow = document.getElementById('modalWindow');
var usersID = {};


function editImgs() {  //add func for modal window to all imgs
    var imgs = document.getElementsByTagName('img');
    for (var i = 0; i < imgs.length; i++) {
        imgs[i].setAttribute('onclick', 'openModal(this)');
    }
}

