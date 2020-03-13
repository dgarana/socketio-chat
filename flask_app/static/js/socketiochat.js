var sio;

$(document).ready(function(){
  sio = io();

  sio.on('connect', function() {
    console.log('Connected!');
    $('#chat_status > #status').html('<b>Connected</b>');
  });

  sio.on('disconnect', function(){
    console.log('Disonnected!')
    $('#chat_status > #status').html('<b>Disconnected</b>');
    $('#chat_status > #username').html('<b>Not connected</b>');
  });

  sio.on('set_name', function(data){
    $('#chat_status > #username').html('<b>'+ data.name +'</b>');
  });

  sio.on('user_connected', function(data){
    console.log(data);
  });

  sio.on('user_disconnected', function(data){
    console.log(data);
  });

  sio.on('new_message', function(data){
    add_message(data)
  });

  $("#chat_text").submit(function (event) {
    event.preventDefault();
    event.stopPropagation();
    console.log('Emitting event');
    sio.emit('send_message', {'message': $(this).find("input[id='chat_message']").val()}, function(){
      $("#chat_text")[0].reset();
    });
    console.log('Finished emitting');
  });

  add_message = function(data){
    $('#chat_wrapper').append('<span>' + data['user'] + ' // ' + data['message'] + '</span><br>');
  }
});