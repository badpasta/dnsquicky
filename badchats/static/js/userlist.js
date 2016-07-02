<script type="text/javascript">
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
					jHTML += "<tr>" + 
							 "<td>" + n.id + "</td>" +
							 "<td>" + n.username + "</td>" + 
							 "<td>" + 'edit' + "</td>" + 
							 "</tr>";

					pageCount = i;
				});

				var pageNum = Math.ceil(pageCount / pageSize);
				$('#getuser').append(jHTML);

			}   
	});
});
</script>
