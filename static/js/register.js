function bindCaptchaBtnClick(){
    //id均用#开头
    $("#captcha_btn").on("click",function (event){
        var $this = $(this);
        var email = $("input[name='email']").val();
        if (!email){
            alert('邮箱不能为空');
            return;
        }
        console.log(email);
        //通过js发送网络请求：ajax——Async JavaScript And XML(json)
        //url_for只能在jinja2中使用
        $.ajax({
            url:"/user/captcha",
            method:"POST",
            data:{
                "email":email
            },
            success:function (res){
                var code = res['code'];
                if (code == 200){
                    $this.off('click');
                    var countNum = 30;
                    var timer = setInterval(function (){
                        countNum -= 1;
                        if (countNum > 0){
                            $this.text(countNum+'秒后可重新发送');
                        }else {
                            $this.text('重新获取验证码');
                            bindCaptchaBtnClick();
                            //如果不需要倒计时，一定要清除！！！
                            clearInterval(timer);
                        }
                    },1000);
                    alert("验证码发送成功！请及时查收！");
                }else {
                    alert(res['message']);
                }
            }
        })
    });
}

//等网页文件全部加载完后在执行
$(function (){
    bindCaptchaBtnClick();
});