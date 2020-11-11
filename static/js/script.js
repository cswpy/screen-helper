
$(document).ready(function() {

            var socket = io.connect('http://' + document.domain + ':' + location.port);

           socket.on( 'connect', function() {
                 socket.emit( 'my event', {
                 data: 'User Connected'
             });
         });

            socket.on('attention lost', function(){
                alert("Attention lost!");
            });

            socket.on('class mode notification', function(){
                alert("Take a break!");
            });

            socket.on('study mode notification', function(){
                alert("You are distracted, get back to the class!");
            });


            var random_num = Math.ceil(Math.random() * 7);
            var string = "url('/static/images/relaxing_" + random_num + ".jpg')";

            $( "body" ).css("background-image", string);

            $("#show-image").on("click", function(){
                $("#video-feed").toggleClass("d-none");
                 var text = $('#show-image').text();
                $(this).text(
                text == "Show me the magic!" ? "Hide the magic!" : "Show me the magic!");
            });
});