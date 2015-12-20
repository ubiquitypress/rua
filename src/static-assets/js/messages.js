var frm = $('#message_form');
frm.submit(function () {
    $.ajax({
        type: frm.attr('method'),
        url: frm.attr('action'),
        data: frm.serialize(),
        success: function (data) {
            data = $.parseJSON(data);
            $( "#message-list" ).prepend( '<li class="left clearfix"><span class="chat-img pull-left"><img src="http://placehold.it/50/55C1E7/fff&amp;text=' + $('#initials').val() + '" alt="User Avatar" class="img-circle" /></span><div class="chat-body clearfix"><div class="header"><strong class="primary-font">' + data.sender + '</strong> <small class="pull-right text-muted"><span class="glyphicon glyphicon-time"></span><small>' + data.date_sent + '</small></small></div>' + data.message + '</div></li><input class="last_message" type="hidden" value="' + data.message_id + '">' );
            $('#id_message').val("");
        },
        error: function(data) {
           $("#MESSAGE-DIV").html("Something went wrong!");
           console.log(data)
        }
    });
    return false;
});

var book_id = document.getElementById("book_id").value;

window.setInterval(function(){
    var last_message = $(".last_message:first").val();
    $.get('/book/'+ book_id +'/messages/', {last_message: last_message}, function(data){
        data = $.parseJSON(data);
        for (i = 0; i < data.messages.length; i++) { 

            $( "#message-list" ).prepend( '<li class="left clearfix"><span class="chat-img pull-left"><img src="http://placehold.it/50/FA6F57/fff&amp;text=' + data.messages[i].initials + '" alt="User Avatar" class="img-circle" /></span><div class="chat-body clearfix"><div class="header"><strong class="primary-font">' + data.messages[i].sender + '</strong> <small class="pull-right text-muted"><span class="glyphicon glyphicon-time"></span><small>' + data.messages[i].date_sent + '</small></small></div>' + data.messages[i].message + '</div></li><input class="last_message" type="hidden" value="' + data.messages[i].message_id + '">' );
            $('#id_message').val("");
            $('.message-new').fadeOut(1000);
            $('.message-new').fadeIn(1000);
        }
        data.messages = new Array();
    });

    $('.message-new').hover(function() {
        $(this).removeClass('message-new');
    });
  
}, 5000);

