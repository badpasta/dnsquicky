$(document).ready(function(){
	$.ajax({
		url: "http://127.0.0.1:8001/api/getuser", 
		type: "GET",    
		dataType:"json", 
		success: function (reponse){
				<!-- tables_line -->
				var jHTML = '<tr class="table-name-fonts">';
				var pageCount = 0;
				var pageSize = 10;
				$.each(reponse.tables_name, function(b, k){
					jHTML += '<th>' + k + '</th>';	
				});
				jHTML += '<th>options</th></tr>';

				<!-- context_line -->
				$.each(reponse.userlist, function(i,n){
					jContext =  '<div class="btn-group">' + 
                	            '<a class="btn btn-danger" data-uid="'+n.id+'" href="#"  data-toggle="modal" data-target="#userModal" role="button"><i class="fa  fa-pencil fa-sm"></i> Edit</a>' +
                	            '<a type="button" class="btn btn-danger dropdown-toggle" data-toggle="dropdown" href="#" aria-haspopup="true" aria-expanded="false">' +
                	            	'<span class="caret"></span>' +
                	            	'<span class="sr-only">Toggle Dropdown</span>' +
                	            '</a>' +
                	            '<ul class="dropdown-menu">' +
                	            	'<li><a href="#" id="delUserButton" data-id="'+ n.id +'" data-user="' + n.username + '" data-toggle="modal" role="button" ><i class="fa fa-fw fa-trash-o" ></i> Delete</a></li>' +
                	            '</ul></div>'

					jHTML += "<tr id='" + n.id +"' class='table-name-fonts-1'>" + 
							 "<td>" + n.id + "</td>" +
							 "<td>" + n.username + "</td>" + 
							 "<td>" + jContext + "</td>" + 
							 "</tr>";
					pageCount = i;
				});
				var pageNum = Math.ceil(pageCount / pageSize);
				$('#getuser').append(jHTML);
			}   
	});
});

$(document).on("click", "#delUserButton", function() { 
	var userId = $(this).data('id');
	var userName = $(this).data('user');
	var delContext = 'Please besure User:' + '<b style="color:red">' + userName + '</b>';
	var jData = '{"id": "' + userId +'"}';
	$('#delUserName').empty(); 
	$('#delUserName').append(delContext); 
	$('#delUserModal').modal('show');
	$('#delYes').click(function() {
		$.ajax({
			url: "http://127.0.0.1:8001/api/deluser",
			type: "POST",
			dataType: "json",
			data: jData,
			success: function(reponse){
				var jStatus = reponse.status;
				var uid = '#'+ userId;
				var notStatus = '';
				var notContext = '';
				$(uid).remove();
				if (jStatus)
					{notStatus = 'success';
					 notContext = 'User: ' + userName + ' was Delete!';}
				else
					{notStatus = 'error';
					 notContext = 'Delete Error!';}
				$.notify(notContext, notStatus);
			}
		});
		$('#delUserModal').modal('hide');
	});
});


