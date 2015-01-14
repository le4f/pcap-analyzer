var content = [
	{ title: 'http' },
	{ title: 'dns' },
	{ title: 'icmp' },
	{ title: 'smb || nbns || dcerpc || nbss || dns' },
	{ title: 'ip.src==' },
	{ title: 'ip.dst==' },
	{ title: 'ip.src==192.168.0.0/16 and ip.dst==192.168.0.0/16' },
	{ title: '!(ip.src == 10.43.54.65 or ip.dst == 10.43.54.65)'},
	{ title: 'udp contains 81:60:03' },
	{ title: 'eth.addr[0:3]==00:06:5B' },
	{ title: 'http.request.uri matches "login$"' },
	{ title: 'tcp.port eq 25' },
	// etc
];

$(document).ready(function() {
	$('#analyzer-nav').addClass('active');

    $('.ui.checkbox').checkbox();

	$('.ui.accordion').accordion();

	$('.menu .item').tab();

	$("#pcaptable").FixedHead({ tableLayout: "floated" });

	$('.ui.search').search({
    	source: content
	});
	
	$('input#filter').keyup(function(e){
	   		event.preventDefault();
	   		if (e.keyCode == 13) {
	   			$('.ui.small.que.modal')
				  		.modal({
						   	closable  : true,
						   	onDeny    : function(){
						      return true;
						    },
						    onApprove : function() {
						      window.location.href= window.location.pathname + '?filter=' + $('input#filter').val();
						    }
						  }).modal('show');	   			
	   		}
	 });
	
	$('.pktdetail tr').on('click', function(e){
			$("#loadbartable").addClass('active');
			$("#loadbar").modal({closable  : true,}).modal('show');
	   		e.preventDefault();
	   		var packetPane = $('.packetPane')
	   		packetPane.html('');
	   		$('.spinner').removeClass('hide');
	   		var packetDetail = $.ajax({
	   			type : "GET",
	   			url : "/packetdetail/" + $("input[name='analyzeid']").val() + '/' + $(this).children().first().text(),
	   			contentType: 'application/text;charset=UTF-8',
	   			success: function(text){
			   		$('.spinner').addClass('hide');
			   		packetPane.html(text);
			   			$('.ui.packetPane.modal')
				  		.modal({
						   	closable  : true,
						  }).modal('show');
			   	}
	   		});
		});
});
