$(document).ready(function() {
	var userStatus = 1;
	var passStatus = 1;
	$('#addButton').click(function() {
		var userName = $('input#addName').val();
		var userPass = $('input#addPass').val();
		postUser(userName, userPass);
	});
	$('input#addName').keyup(function(){
		var userName = $(this).val();
		userStatus = checkStr(userName, 'UserName');
	});
	$('input#addPass').keyup(function(){
		var Password = $(this).val();
		passStatus = checkLength(Password, 'Password');
	});
	var iId = setInterval(function() {checkStatus(userStatus, passStatus);},200);	
});

function checkStatus (u, p) {
	if (u == 0 && p == 0)
		$('#addButton').removeClass('disabled');
	else
		$('#addButton').addClass('disabled');
}


function checkLength(context, type) {
	if (context.length < 8) 
		{$('#status').addClass('status-fonts');
		 $('#status').removeClass('status-fonts-success');
		 $('#status').html(type + ' length must greater than 8!');
		 return 1;}

	else
		{$('#status').removeClass('status-fonts');
		 $('#status').empty();
		 return 0;}
}

function checkStr(s, n) {
	var regu= /^([a-zA-Z0-9]|[._])+$/;
	if (!regu.exec(s)) 
 		{$('#status').addClass('status-fonts');
		 $('#status').removeClass('status-fonts-success');
		 $('#status').html(n + ' cloud not be empty and  only use letters and numbers.');
		 return 1;}
	else
		{$('#status').removeClass('status-fonts');
		 $('#status').empty();
		 return 0;}
}

function postUser(u, p) {
	var jData = '{ "username": "' + u + '", "password": "' + p +'"}';
	$.ajax({
		url: "http://127.0.0.1:8001/api/insertuser",
		type: "POST",
		dataType: "json",
		data: jData,
		success: function(reponse) {
			var jStatus = reponse.status;
			var notContext = '';
			var notClass = '';
			if (jStatus == 0)
				{notClass = 'status-fonts-success';
				 notContext = 'User: ' + u + ' bulid success!';}
			else if (jStatus == 1)
				{notClass = 'status-fonts';
				 notContext = 'User: ' + u + ' create failed.';}
			else if (jStatus == 2)
				{notClass = 'status-fonts';
				 notContext = 'User: ' + u + ' already exist!';}
			$('#status').addClass(notClass);
			$('#status').html(notContext);
			$('input#addName').val('');
			$('input#addPass').val('');
		}
	});	
}
