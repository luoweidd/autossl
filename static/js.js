var newscript = document.createElement('script');
newscript.setAttribute('type','text/javascript');
newscript.setAttribute('src','static/jquery-3.4.1.min.js');
var head = document.getElementsByTagName('head')[0];
head.appendChild(newscript);

function button() {
    var data=$('.input-xxlarge').val();
    $.ajax({
        url:"/applyssl",
        type:'POST',
        dataType:'text',
        data:data,
        success:function(result){
            $('.content').text(result)
        },
        messageerror:function (result) {
            $('.content').text(result)
        }
    });
}