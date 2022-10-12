$(function(){
//	登录校验
	$("#submit-login").click(function(){
		var username = $("#login_username").val();
		var password = $("#login_password").val();
		
		//字母开头，允许5-16字节，允许字母数字下划线：
		var unPattern = /^[a-zA-Z][a-zA-Z0-9_]{4,15}$/;
		//字母开头，长度在6~18之间，只能包含字母、数字和下划线：
		var pwPattern = /^[a-zA-Z]\w{5,17}$/;
		
		var flag1 = unPattern.test(username);
		var flag2 = pwPattern.test(password);
//		var flag = true;
//		if((username=null)||(password=null)){
//			$('#info').text('账号或密码不能为空');
//			$("#info").css("color","#aa0000");
//			flag=false;
//		}
		if(flag1&&flag2){
			$("#login-form").submit();
		}else{
			$("#info1").text('账号或密码格式不正确');
			$("#info1").css("color","#aa0000");
		}
	});
//	忘记密码
	$("#forget").click(function(){
		$('#info1').text('我也木得办法');
		$("#info1").css("color","#aa0000");
	});
//	注册校验
	$("#submit-register").click(function(){
		var username = $("#register_username").val();
		var email = $("#register_email").val();
		var password = $("#register_password").val();
		
		//字母开头，允许5-16字节，允许字母数字下划线：
		var unPattern = /^[a-zA-Z][a-zA-Z0-9_]{4,15}$/;
		//邮箱：^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$
		var emPattern = /^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/;
		//字母开头，长度在6~18之间，只能包含字母、数字和下划线：
		var pwPattern = /^[a-zA-Z]\w{5,17}$/;
		
		var flag1 = unPattern.test(username);
		var flag2 = emPattern.test(email);
		var flag3 = pwPattern.test(password);
		if(flag1&&flag2&&flag3){
			alert(username+password+email);
			$("#register-form").submit();
		}else{
			$("#info2").text('您输入的格式不正确');
			$("#info2").css("color","#aa0000");
		}
	});
	
});