$(function () {
    $("#password_confirm").change(function () {

        var password = $("#password").val();
        var password_confirm = $(this).val();
        if (password == password_confirm){
            $("#password_confirm_info").html("两次一致").css("color","green");
        }else{
            $("#password_confirm_info").html("两次输入不一致").css("color","red");
        }
    })
})


