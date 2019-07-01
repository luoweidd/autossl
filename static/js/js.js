var newscript = document.createElement('script');
newscript.setAttribute('type','text/javascript');
newscript.setAttribute('src','static/js/jquery-3.4.1.min.js');
newscript.setAttribute('src','static/js/jquery.md5.js');
var head = document.getElementsByTagName('head')[0];
head.appendChild(newscript);

function loading_c() {
    var load = $("#loading");
    load[0].style.visibility="visible";
    $("#loading").html("<img src='static/images/loading.gif' />"); //在请求后台数据之前显示loading图标
}

function submit_apply() {
    var data=$('.input-xxlarge').val();
    $.ajax({
        url:"/applyssl",
        type:'POST',
        dataType:'text',
        data:data,
        beforeSend:function(){
            var load = $("#loading_1");
            load[0].style.visibility="visible";
            $("#loading_1").html("<img src='static/images/loading.gif' />"); //在请求后台数据之前显示loading图标
            $('.validationres').text("");
            var validation = $("#dns_validation");
            validation[0].style.visibility="visible";
            },
        success:function(result){
            var load = $("#loading_1");
            load[0].style.visibility="hidden";
            var res=JSON.parse(result);
            $('.content').html(res.msg[0]);
            var validation = $("#dns_validation");
            validation[0].style.visibility="visible";
            validation[0].title = res.msg[1];
            validation[0].alt = res.msg[2];
            validation[0].label = res.msg[3];
        },
        messageerror:function (result) {
            var load = $("#loading_1")
            load[0].style.visibility="hidden";
            var res=JSON.parse(result);
            $('.content').text(res.msg);
        }
    });
}

function new_site_dns_validation() {
        var domains = $('.input-xxlarge').val();
        var auth_link = $("#dns_validation");
        var auth = auth_link[0].title.toString();
        var challenge = auth_link[0].alt.toString();
        var txt = auth_link[0].label.toString();
        var data = JSON.stringify([domains,auth,challenge,txt])
    $.ajax({
        url:"/new_site_dns_validation",
        type:'POST',
        dataType:'text',
        data:data,
        beforeSend:function(){
            var load = $("#loading_1")
            load[0].style.visibility="visible"
            $("#loading_1").html("<img src='static/images/loading.gif' />"); //在请求后台数据之前显示loading图标
            },
        success:function(result){
            // var load = $("#loading_1")
            // load[0].style.visibility="hidden";
            var res=JSON.parse(result);
            var obj = res.msg;
            var txts = '';
            for (var i in obj){
                var txt = "<p>"+obj[i]+"</p>";
                txts += txt;
            }
            var load = $("#loading_1");
            load[0].style.visibility="hidden";
            $('.validationres').html(txts);
            var auth_buttom = $("#dns_validation");
            auth_buttom[0].style.visibility = "hidden";
        },
        messageerror:function (result) {
            var load = $("#loading_1");
            load[0].style.visibility="hidden";
            var res=JSON.parse(result);
            $('.validationres').text(res.msg);
        }
    });
}

function loader() {
    $.ajax({
        url:"/account_info_api",
        type:'GET',
        dataType:'text',
        beforeSend:function(){
            var load = $("#loading");
            load[0].style.visibility="visible";
            $("#loading").html("<img src='static/images/loading.gif' />"); //在请求后台数据之前显示loading图标
            },
        success:function(result){
            var load = $("#loading");
            load[0].style.visibility="hidden";
            var res=JSON.parse(result);
            $("#letf_form").contents().find("#letf_form_div").html(MsgAnalysis(res.msg));
        },
        messageerror:function (result) {
            var load = $("#loading");
            load[0].style.visibility="hidden";
            var res=JSON.parse(result);
            $("#letf_form").contents().find("#letf_form_div").html(MsgAnalysis(res.msg));
        }
    });
}

function MsgAnalysis(msg) {
    var li="<table class='account_info_tables'><H3>account infomation:</H3>"
    var liend="</table>"
    for (var i in msg){
        if (i == 'key' || i == 'nonce'){
            continue;
        //     for (var j in msg[i]){
        //         var text = "<tr><td>"+j+"</td><td style='word-break: break-all;'>"+msg[i][j]+"</td></tr>"
        //     }
        }
        // else
        text = "<tr><td>"+i+"</td><td style='word-break: break-all;'>"+msg[i]+"</td></tr>";
        var txt=li+=text;
    }
    var result=txt+liend;
    return result;
}

function login() {
    var user= $("#user").text.toString();
    var passwd=$("#passwd").text.toString();
    var date = {"user":user,"passwd":$.md5(passwd)};
    $.ajax({
        url:"/login",
        type:'POST',
        date:date,
        dataType:'json',
        beforeSend:function(){

            },
        success:function(result){
            var load = $("#loading")
            load[0].style.visibility="hidden";
            var res=JSON.parse(result);
            $("#letf_form").contents().find("#letf_form_div").html(MsgAnalysis(res.msg));
        },
        messageerror:function (result) {
            var load = $("#loading");
            load[0].style.visibility="hidden";
            var res=JSON.parse(result);
            $("#letf_form").contents().find("#letf_form_div").html(MsgAnalysis(res.msg));
        }
    });
}

function forget_password() {
    var user= $("#user").text.toString();
    var passwd=$("#passwd").text.toString()
    $.ajax({
        url:"/forget_password",
        type:'POST',
        dataType:'json',
        beforeSend:function(){
            var load = $("#loading")
            load[0].style.visibility="visible"
            $("#loading").html("<img src='static/images/loading.gif' />"); //在请求后台数据之前显示loading图标
            },
        success:function(result){
            var load = $("#loading");
            load[0].style.visibility="hidden";
            var res=JSON.parse(result);
            $("#letf_form").contents().find("#letf_form_div").html(MsgAnalysis(res.msg));
        },
        messageerror:function (result) {
            var load = $("#loading");
            load[0].style.visibility="hidden";
            var res=JSON.parse(result);
            $("#letf_form").contents().find("#letf_form_div").html(MsgAnalysis(res.msg));
        }
    });
}

function update_domain(obj){
    var objs = obj.parentNode;
    var id =  objs.parentNode.children[0].innerHTML;
    var itemVal = objs.parentNode.children[2].children[0].value;
    var data = {"id":id,"itemVal":itemVal};
    $.ajax({
        url:"/update_name_server",
        type:'POST',
        data:data,
        dataType:'json',
        beforeSend:function(){
            var load = $("#loading");
            load[0].style.visibility="visible";
            $("#loading").html("<img src='static/images/loading.gif' />"); //在请求后台数据之前显示loading图标
            },
        success:function(result){
            //var res=JSON.parse(result);
            var load = $("#loading");
            load[0].style.visibility="hidden";
            //var res=JSON.parse(result);
            var validation = $("#validation");
            validation[0].style.visibility ="visible";
            validation.html('<p style="color: red; background-color: white; width: 400px; height: auto; margin: auto; opacity: 0.9; margin-top: 25%">'+result.msg+'</p>');
            var validations = $("#dns_validation");
            validations[0].style.visibility='visible'
            validation[0].title = res.msg[1];
            validation[0].alt = res.msg[2];
            validation[0].label = res.msg[3];
            var close_window = $('#close_window');
            close_window[0].style.visibility='visible';

        },
        messageerror:function (result) {
            var load = $("#loading");
            load[0].style.visibility="visible";
            var res=JSON.parse(result);
            $("#validationres").html(result.msg);
        }
    });
}

function old_site_dns_validation() {
    var domains = $('.input-xxlarge').val();
    var auth_link = $("#dns_validation");
    var auth = auth_link[0].title.toString();
    var challenge = auth_link[0].alt.toString();
    var txt = auth_link[0].label.toString();
    var data = JSON.stringify([domains,auth,challenge,txt])
    $.ajax({
        url:"/update_name_server_validation",
        type:'POST',
        dataType:'text',
        data:data,
        beforeSend:function(){
            var load = $("#loading")
            load[0].style.visibility="visible"
            $("#loading").html("<img src='static/images/loading.gif' />"); //在请求后台数据之前显示loading图标
            },
        success:function(result){
            // var load = $("#loading_1")
            // load[0].style.visibility="hidden";
            var res=JSON.parse(result);
            var obj = res.msg;
            var txts = '';
            for (var i in obj){
                var txt = "<p>"+obj[i]+"</p>";
                txts += txt;
            }
            var load = $("#loading");
            load[0].style.visibility="hidden";
            $('.validationres').html(txts);
            var auth_buttom = $("#dns_validation");
            auth_buttom[0].style.visibility = "hidden";
        },
        messageerror:function (result) {
            var load = $("#loading");
            load[0].style.visibility="hidden";
            var res=JSON.parse(result);
            $('.validationres').text(res.msg);
        }
    });
}

function close_windows(){
    var meobj = $('#close_window');
    meobj[0].style.visibility='hidden';
    var obj = $('#validation');
    obj[0].style.visibility='hidden';
}