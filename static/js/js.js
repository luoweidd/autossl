document.write("<script src='static/js/jquery-3.4.1.min.js' type='text/javascript'></script>")
document.write("<script src='static/js/jquery.md5.js' type='text/javascript'></script>")

function loading_c() {
    var load = $("#loading");
    load[0].style.visibility="visible";
    $("#loading").html("<img src='static/images/loading.gif' />"); //在请求后台数据之前显示loading图标
}

function submit_apply() {
    var data=$('.input-xxlarge').val();
    if(data != null && data != undefined && data != ""){
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
    else {
        alert('请填写正确的域名！')
    }
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
    var user= $("#user")[0].value;
    var passwd=$("#passwd")[0].value;
    var data = JSON.stringify({"user":user,"passwd":$.md5(passwd)});
    $.ajax({
        url:"/login",
        type:'POST',
        data:data,
        dataType:'json',
        success:function(result){
            var validation = $("#validationres");
            validation[0].style.visibility ="visible";
            validation.html('<p style="color: red; background-color: white; width: 400px; height: auto; margin: auto; opacity: 0.9; margin-top: 26%">'+result.msg.result+'</p>');
            var close_window = $('#close_window');
            close_window[0].style.visibility='visible';
            if (result.msg.redirectUrl !=undefined && result.msg.redirectUrl != null){
                window.location.href = result.msg.redirectUrl;
            }
            else {
                validation.html('<p style="color: red; background-color: white; width: 400px; height: auto; margin: auto; opacity: 0.9; margin-top: 26%">系统错误，请联系管理员！</p>')
            }

        },
        error:function (result) {
            var validation = $("#validationres");
            validation[0].style.visibility ="visible";
            validation.html('<p style="color: red; background-color: white; width: 400px; height: auto; margin: auto; opacity: 0.9; margin-top: 26%">'+result.msg+'</p>');
            var close_window = $('#close_window');
            close_window[0].style.visibility='visible';
        }
    });
}

function update_domain(obj){
    var objs = obj.parentNode;
    var id =  objs.parentNode.children[0].innerHTML;
    var itemVal = objs.parentNode.children[2].children[0].value;
    var old_itemVal = objs.parentNode.children[2].children[0].alt;
    var data = JSON.stringify({"id":id,"old_itemVal":old_itemVal,"itemVal":itemVal});
    $.ajax({
        url:"/update_name_server",
        type:'POST',
        data:data,
        dataType:'json',
        beforeSend:function(){
            var load = $("#loading");
            load[0].style.visibility="visible";
            $("#loading").html("<img style='margin-top: 26%' src='static/images/loading.gif' />"); //在请求后台数据之前显示loading图标
            },
        success:function(result){
            // var res=JSON.parse(result);
            console.log(result)
            var load = $("#loading");
            load[0].style.visibility="hidden";
            var validation = $("#validationres");
            validation[0].style.visibility ="visible";
            validation.html('<p style="color: red; background-color: white; width: 400px; height: auto; margin: auto; opacity: 0.9; margin-top: 25%">'+result.msg[0]+'</p>');
            var close_window = $('#close_window');
            close_window[0].style.visibility='visible';
            if (result.code <= 0){
                var validations = $("#dns_validation");
                validations[0].style.visibility='visible';
                validations[0].title = result.msg[1];
                validations[0].alt = result.msg[2];
                validations[0].label = result.msg[3];
                validations[0].txt =result.msg[5];
                console.log(validations[0].txt);
            };

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
    var auth_link = $("#dns_validation");
    var auth = auth_link[0].title.toString();
    var challenge = auth_link[0].alt.toString();
    var txt = auth_link[0].label.toString();
    var db_ = auth_link[0].txt;
    var domains = db_["itemVal"];
    var data = JSON.stringify([domains,auth,challenge,txt,db_]);
    $.ajax({
        url:"/update_name_server_validation",
        type:'POST',
        dataType:'json',
        data:data,
        // beforeSend:function(){
        //     var load = $("#loading")
        //     load[0].style.visibility="visible"
        //     $("#loading").html("<img style='margin-top: 25%;' src='static/images/loading.gif' />"); //在请求后台数据之前显示loading图标
        //     },
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
    var obj = $('#validationres');
    obj[0].style.visibility='hidden';
    var auth_buttom = $("#dns_validation");
    auth_buttom[0].style.visibility = "hidden";
}
function forget_password(){
     window.location.href = '/forget_password'
}

function login_close_windows() {
    var meobj = $('#close_window');
    meobj[0].style.visibility='hidden';
    var obj = $('#validationres');
    obj[0].style.visibility='hidden';
    var auth_buttom = $("#dns_validation");
}

function winform_new() {
    var rigth_from = parent.$('#right_form');
    rigth_from[0].src = '/apply_ssl_form';
}

function winform_update() {
    var rigth_from = parent.$('#right_form');
    rigth_from[0].src = '/name_list';
}

function logout(obj) {

}
function get_user(obj) {

}