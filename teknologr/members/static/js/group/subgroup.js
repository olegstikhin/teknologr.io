$(document).ready(function() {

	$("#addgroupform").submit(function(event){

		var data = $(this).serialize();
	
		var request = $.ajax({
			url: "/api/groups/",
			method: "POST",
			data: data
		});

		request.done(function() {
			location.reload();
		});

		request.fail(function( jqHXR, textStatus ){
			alert( "Request failed: " + textStatus + ": " + jqHXR.responseText );
		});

		event.preventDefault();
	});

	$(".removeGroup").click(function(){
		var id = $(this).data('id');	

		var request = $.ajax({
			url: "/api/groups/" + id + "/",
			method: "DELETE"
		})

		request.done(function() {
			location.reload();
		});

		request.fail(function( jqHXR, textStatus ){
			alert( "Request failed: " + textStatus + ": " + jqHXR.responseText );
		});
	});

});
