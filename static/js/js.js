// var newscript = document.createElement('script');
// newscript.setAttribute('type','text/javascript');
// newscript.setAttribute('src','static/js/jquery-3.4.1.min.js');
// var head = document.getElementsByTagName('head')[0];
// head.appendChild(newscript);

function button() {
    var data=$('.input-xxlarge').val();
    $.ajax({
        url:"/applyssl",
        type:'POST',
        dataType:'text',
        data:data,
        success:function(result){
            var res=JSON.parse(result)
            $('.content').text(res.msg)
        },
        messageerror:function (result) {
            var res=JSON.parse(result)
            $('.content').text(res.msg)
        }
    });
}

function loader() {
    var div=$('<div class="letr_div"></div>')
    $.ajax({
        url:"/account_info_api",
        type:'GET',
        dataType:'text',
        success:function(result){
            var res=JSON.parse(result)
            $('.letr_div').contents().find("body").append(div).text(res.msg)
        },
        messageerror:function (result) {
            var res=JSON.parse(result)
            $('.letr_div').contents().find("body").append(div).text(res.msg)
        }
    });
}