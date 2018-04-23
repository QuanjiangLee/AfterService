function dialogAlert(title, content) {
    $(".Dialog").remove()
    var html = ''
    html += '<div class="Dialog"><div class="modal-backdrop fade in" style="z-index: 1040;"></div>';
    html += '<div class="modal bootstrap-dialog type-warning fade size-normal in" role="dialog" aria-hidden="true" tabindex="-1" style="z-index: 1050;display: block;text-align: center;">';
    html += '<div class="modal-dialog"><div class="modal-content">';
    html += '<div class="modal-header"><div class="bootstrap-dialog-header">';
    html += '<button type="button" class="close" data-dismiss="modal" aria-hidden="true" onclick="closeDialog(this)">&times;</button>'
    html += '<div class="bootstrap-dialog-title" style="text-align: center;">' + title + '</div></div></div><div class="modal-body"><div class="bootstrap-dialog-body">';
    html += '<div class="bootstrap-dialog-message">';
    html += content;
    html += '</div></div></div></div></div></div></div>';
    $("body").append(html);
}

function userLogin() {
    var html = ''
    html += '用户名:<input style="height: 35px;margin: 10px;box-shadow: none;border: 1px solid #e5e5e5;border-radius: 2px;padding: 6px 10px;" type="text" placeholder="用户名" name="username"><br>'
    html += '密&emsp;码:<input style="height: 35px;margin: 10px;box-shadow: none;border: 1px solid #e5e5e5;border-radius: 2px;padding: 6px 10px;" type="password" placeholder="密码" name="password"><br>'
    html += '<input style="margin: 10px;" type="button" onclick="checkLogin()" class="sign-in-button btn btn-info" name="submit" value="登录"><input style="margin: 10px;" type="button" onclick="userRegister()" class="sign-in-button btn btn-info" name="regsiter" value="注册">'
    html += '<div class="rightTips"><a href="javascript:void(0);">忘记密码？</a></div></div>'
    title = '登录';
    dialogAlert(title, html);
}

function userRegister() {
    var html = ''
    html += '&emsp;用户名:<input style="height: 35px;margin: 10px;box-shadow: none;border: 1px solid #e5e5e5;border-radius: 2px;padding: 6px 10px;" type="text" placeholder="用户名" name="username"><br>'
    html += '&emsp;&emsp;密码:<input style="height: 35px;margin: 10px;box-shadow: none;border: 1px solid #e5e5e5;border-radius: 2px;padding: 6px 10px;" type="password" box-shadow: none;border - radius: 2px;padding: 6px 10px;" placeholder="密码" name="password"><br>'
    html += '重复密码:<input style="height: 35px;margin: 10px;box-shadow: none;border: 1px solid #e5e5e5;border-radius: 2px;padding: 6px 10px;" type="password" box-shadow: none;border - radius: 2px;padding: 6px 10px;" placeholder="重复密码" name="repassword"><br>'
    html += '<input style="margin: 10px;" type="button" onclick="registerUser(this)" class="sign-in-button btn btn-info" name="submit" value="注册">'
    html += '<div class="rightTips" onclick="userLogin()"><a href="javascript:void(0);">返回登录？</a></div></div>'
    title = '注册';
    dialogAlert(title, html);
}

function closeDialog(elem) {
    $(elem).parents(".Dialog").remove();
}

function checkData_form() {  //检查form表单数据的合法性
    var index = true;
    var username = $("input[name='username']").val();
    var password = $("input[name='password']").val();
    var repassword = $("input[name='repassword']");
    $("input").css("border-color", "#ddd");
    if (username == "") {
        index = false;
        $("input[name='username']").css("border-color", "#f33");
    }
    if (password == "") {
        index = false;
        $("input[name='password']").css("border-color", "#f33");
    }
    if (repassword.length != 0) {
        if (repassword.val() == "") {
            index = false
            $("input[name='repassword']").css("border-color", "#f33");
        }
    }
    return index
}
function checkLogin() {
    var verifyInput = checkData_form();
    if (verifyInput == true) {
        var username = $("input[name='username']").val();
        var password = $("input[name='password']").val();
        data = { 'userNo': username, 'passwd': password }
        postRequest("/verifyLogin/", data, true, verifyResult);
    } else {
        alert("要登录的用户名或密码不能为空!")
    }
}
function verifyResult(ret) {
    if (ret['result'] == true) {
        if (ret['user_grant'] == 0) {
            window.location.href = "/userIndex/home";
        } else {
            window.location.href = "/adminIndex/";
        }
    } else {
        alert(ret['error']);
    }

}

function registerUser(elem) {
    var verifyInput = checkData_form();
    if (verifyInput == true) {
        var username = $("input[name='username']").val();
        var password = $("input[name='password']").val();
        var repassword = $("input[name='repassword']").val();
        if (password != repassword) {
            alert("两次输入的密码不一样，请重新输入!")
        } else {
            data = { 'userNo': username, 'passwd': password }
            postRequest("/registerUser/", data, true, registerResult);
        }
    } else {
        alert("要注册的用户名或密码不能为空!")
    }
}

function registerResult(ret) {
    if (ret['ret'] == true) {
        alert("恭喜注册新用户成功！")
        userLogin();
    } else {
        alert("opps!注册新用户失败！")
    }
}