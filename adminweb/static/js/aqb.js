$(document).ready(function() {
	initTables();
	var wsServer = 'ws://127.0.0.1:8001/api/aqb.check';
	mySocket = new WebSocket(wsServer); 
	mySocket.onopen = function (openEvent) {   
	     //
	};
	mySocket.onmessage = function (messageEvent) {   
		var table = document.getElementById('aqb_message');
		var data = event.data
		$(table).append(data + '<br>');
		if ( data.indexOf("状态") >= 0 && (data.indexOf('200') < 0 && data.indexOf('405') < 0)) {
			getNotify(data, 'danger');
		}
	};
	mySocket.onerror = function (errorEvent) {   
	      //
	};
	mySocket.onclose = function (closeEvent) {
	     //
	}
});

function sendSocket(data) {
	mySocket.send(data);
}


function sleep(n) { 
	var start = new Date().getTime();
	//alert('1') ;
	while(true)  if(new Date().getTime()-start > n) break; 
}

/*
$(document).ready(function() {
	sleep(10);
	var dataSrc = {"param": "bulabula"};
	sendSocket(JSON.stringify(dataSrc));
})
*/

$(document).on("click", "#aqbTable button[name=status]", function() {
	var data = $('#aqbTable').DataTable().row($(this).parents('tr')).data();
	var st = $(this).parents('tr').children();
	var cloud_dom = $(st[4]).children()[0];
	var power_i = $(this).children('i');
	//alert(data.rid + " " + data.zid);
	data.status = !data.status;
	//var s = recordStatus('update', data);
	dataSrc = {"param":"aqb", "rid":data.rid, "status":data.status, "sub_domain": data.sub_domain, "zone_name": data.zone_name};
	$('#aqb_message').empty();
	sendSocket(JSON.stringify(dataSrc));
	var s = true;
	if (s == true) {
		if (data.status == true) {
			$(cloud_dom).css('color', '#4DB3B3');
			$(power_i).removeClass('fa-power-off').addClass('fa-ban').css('color','#DC143C');
		} else {
			$(cloud_dom).css('color', '#808080');
			$(power_i).removeClass('fa-ban').addClass('fa-power-off').css('color', 'green');
		}
	}
});

$(document).on("click", "#aqb_add", function() {
	var theParent = $(this).parents('tr');
	var data = $('#aqbTable').DataTable().row().data();
	var dataSrc = new Object();
	$.each(data, function(i, n) {
		dataSrc[i] = n;
	})
	$('#aqbAddModal').modal('show');
	$('#aqb_alert').fadeOut(3000);
	$('input#sub_domain').val('');
	$('input#aqb_record_value').val('');
	$('input#aqb_record_urlpath').val('');
	initRecordTables('');
});

$(document).on("change", "#select_domain", function() {
	var val = $('#select_domain').val();
	//alert(val);
	dataSrc = {"zone_name": val}
	initRecordTables(dataSrc);
});

$(document).on("keyup", "input#sub_domain", function() {
	var val = $('input#sub_domain').val();
	$('#aqbSelectTable').DataTable().search(val).draw();
});


$(document).on("click", "#aqbSelectTable tr", function() {
	var data = $('#aqbSelectTable').DataTable().row($(this)).data();
	$(this).toggleClass('table-selected');
	$('input#sub_domain').val(data.sub_domain);
	$('#aqbSelectTable').DataTable().search(data.sub_domain).draw();
});


$(document).on("click", "button#aqb_insert", function() {
	var zone_name = $('select#select_domain option:selected').text();
	var sub_domain = $('input#sub_domain').val();
	var value = $('input#aqb_record_value').val();
	var ttl = $('input#aqb_record_ttl').val();
	var url_path = $('input#aqb_record_urlpath').val();
	var data = $('#aqbSelectTable').DataTable().rows('.table-selected').data();
	var record_rids = [];
	$.each(data, function(i, n) {
		record_rids.push(n.rid);
	});
	var diff_data = {
		"zone_name": zone_name,
		"sub_domain": sub_domain,
		"value": value,
		"record_type": "CNAME" 
		}
	var rep_status = false;
	$.ajax({
		url: '/api/getrid',
		type: "POST",
		dataType: 'json',
		async: false,
		data: JSON.stringify(diff_data),
		success: function(reponse) {
			if (reponse.status == true) {
				alert('record already exist!');
			} else {
				rep_status = true;
			}
		}
	});
	//var diff_status = pubPostAjax('/api/getrid', diff_data);
	dataSrc = {
		"zone_name": zone_name,
		"sub_domain": sub_domain,
		"value": value,
		"ttl": ttl,
		"url_path": url_path,
		"rids": record_rids
		}
	if (rep_status == true) {
		var insert_record_status = pubPostAjax("/api/aqb", dataSrc);
		$('#aqbTable').DataTable().ajax.reload();
		$('#aqbAddModal').modal('hide');
	}
	//alert(zone_name + ' ' + sub_domain + " "+  value + ' ' + ttl + '  ' + url_path + ' ' + record_rids);
});


$(document).on("click", "#aqbTable button[name=url]", function() {
	var data = $('#aqbTable').DataTable().row($(this).parents('tr')).data();
	var st = $(this).parents('tr').children();
	var cloud_dom = $(st[4]).children()[0];
	var power_i = $(this).children('i');
	data.status = !data.status;
	var record = 'http://' + data.sub_domain + '.' + data.zone_name
	$('#aqbUrlModal').modal('show');
	$('span#domain_form').html(record);
	$('input#url_form').val(data.url);
	$('a#domain_show').html(record);
	$('a#url_show').html(data.url);
	$('h5#rid').html(data.rid);
});

$(document).on("keyup", "input#url_form", function() {
	var val = $('input#url_form').val();
	$('a#url_show').html(val);
});

$(document).on('click', "button#url_save", function() {
	var val = $('input#url_form').val();
	var rid = $('h5#rid').text();
	var data = {"rid": rid, "url": val};
	var dataSrc = JSON.stringify(data)
	alert(dataSrc);
	$.ajax({
		url: "http://127.0.0.1:8001/api/aqb.url",
		type: "POST",
		data: dataSrc,
		dataType: 'json',
		success: function(reponse) {
			var rep_status = reponse.status;
			var message = reponse.message;
			if (rep_status == true) {
				getNotify(message, 'success');
				$('#aqbTable').DataTable().ajax.reload();
			} else {
				getNotify(message, 'danger');
			}
			$('#aqbUrlModal').modal('hide');
		}
	});
});


function recordStatus(choose, src) {
	var dataSrc =  JSON.stringify(pickDataSrc(choose, src));
	var result_status = false;
	//use time
	//var mydate = new Date();
	//alert(mydate.toLocaleString());
	$.ajax({
		url: '/api/record',	
		type: "POST",
		dataType: 'json',
		async: false,
		data: dataSrc,
		success: function(reponse) {
			var rep = reponse[0];
			if (rep.status == true) {
				getNotify(rep.message, 'success');
				result_status = true;
			} else {
				getNotify(rep.message, 'danger');
			}
		}
	});
	//user time
	//var thedata = new Date();
	//alert(thedata.toLocaleString());
	return result_status
}


function pubGetAjax(url, dataSrc) {
	var rep_status = false;
	alert(url+dataSrc);
	$.ajax({
		url: url + dataSrc,
		type: "GET",
		async: false,
		success: function(reponse) {
			if (reponse.status == true) {
				getNotify(reponse.message, 'success');
				rep_status = true;
			} else {
				getNotify(reponse.message, 'danger');
			}
		}
	});
	return rep_status
}

function pubPostAjax(url, dataSrc) {
	var rep_status = false;
	$.ajax({
		url: url,
		type: "POST",
		dataType: 'json',
		async: false,
		data: JSON.stringify(dataSrc),
		success: function(reponse) {
			if (reponse.status == true) {
				getNotify(reponse.message, 'success');
				rep_status = true;
			} else {
				getNotify(reponse.message, 'danger');
			}
		}
	});
	return rep_status
}


function initRecordTables(data){
	$('#aqbSelectTable').DataTable({
		destroy: true,
		dom: '<"top">rt<"bottom"<"col-sm-12"p>><"clear">',
		pageLength: 3,
		ajax: {
			url: "/api/record",
			dataSrc: function(reponse) {
				rep = reponse.records;
				var records = [];
				$.each(rep, function(i,n) {
					if (rep[i].record_type == 'A') {
						records.push(rep[i]);
					}
				});
				return  records
			},
			data: data
		},
		columns: [
			{data: 'rid',  visible: false},
			{data: 'sub_domain', orderable: false},
			{data: 'record_type', width: '70', orderable: false},
			{data: 'value', orderable: false},
		]
	});
}




function initTables(){
	$('#aqbTable').DataTable({
		destroy: true,
		bPaginate: false,
		dom: '<"top"<"col-sm-7"<"toolbar">><"col-sm-5"f>>rt<"bottom"<"col-sm-5"i><"col-sm-7"p>><"clear">',
		ajax: {
			url: "/api/aqb",
			dataSrc: function(reponse) {
				records = reponse.records;
				$.each(records, function(i,n) {
					records[i]['operation'] = '';
					records[i]['r_status'] = '';
					if (records[i].status == true) {
						records[i].r_status  = iconHtml('cloud', '#4DB3B3');
						records[i].operation += buttonHtmlbyDefault('status', 'ban', '#DC143C');
					} else {
						records[i].r_status  = iconHtml('cloud', '#808080');
						records[i].operation += buttonHtmlbyDefault('status','power-off', 'green');
					}
					records[i].operation += buttonHtmlbyDefault('url', 'magnet', '#C78017')
				});
				return  records
			},
		},
		columns: [
			{data: 'rid',  visible: false},
			{data: 'sub_domain'},
			{data: 'record_type', width: '70'},
			{data: 'value', orderable: false},
			{data: 'url', orderable: false, visible: false},
			{data: 'zone_name'},
			{data: 'status', visible: false},
			{data: 'r_status', width: '50'},
			{data: 'operation', orderable: false}
		]
	});
	var toolAdd = $('div.toolbar').html('<button id="aqb_add" name="add"></button>');
	var addStr = $('<i></i>').addClass('fa fa-lock fa-lg');
	$(toolAdd).children('button').addClass('btn btn-default').html(addStr).append('加入安全宝');
}

function getNotify(message, type) {
	$.notify(
		{
			message: message,
		},
		{
			type: type
		});
}

function iconHtml(icon_name, icon_color) {
	return '<i name="'+icon_name+'" class="fa fa-'+icon_name+' fa-lg" style="color:'+icon_color+';"></i>'
}

function buttonHtmlbyDefault(name, icon_name, icon_color) {
	return  '<button name="'+name+'" class="btn btn-default">'+iconHtml(icon_name, icon_color)+'</button>';
}

