$(document).ready(function() {
	$("#newform").submit(function(event){
		var active = $(this).data('active');
		switch(active) {
			case 'members':
				var apipath = 'members'
				break;
			case 'groups':
				var apipath = 'groupTypes'
				break;
			case 'functionaries':
				var apipath = 'functionaryTypes'
				break;
			case 'decorations':
				var apipath = 'decorations'
				break;
		}


		var request = $.ajax({
			url: "/api/" + apipath + "/",
			method: 'POST',
			data: $(this).serialize()
		});

		request.done(function(msg) {
			window.location = "/"+ active +"/" + msg.id + "/";
		});

		request.fail(function( jqHXR, textStatus ){
			alert( "Request failed: " + textStatus + ": " + jqHXR.responseText );
		});

		event.preventDefault();
	});
});