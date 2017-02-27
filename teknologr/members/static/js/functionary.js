$(document).ready(function() {
	
	$("#functionaryTypeForm").submit(function(event){
		var id = $(this).data('id');	
		var request = $.ajax({
			url: "/api/functionaryTypes/" + id + "/",
			method: 'PUT',
			data: $(this).serialize()
		});

		request.done(function() {
			location.reload();
		});

		request.fail(function( jqHXR, textStatus ){
			alert( "Request failed: " + textStatus + ": " + jqHXR.responseText );
		});

		event.preventDefault();
	});


	$("#deleteFunctionaryType").click(function(){
		if(confirm("Vill du radera denna funktionärstyp?")) {
			var id = $(this).data('id');
			var request = $.ajax({
				url: "/api/functionaryTypes/" + id + "/",
				method: "DELETE",
			});
 
			request.done(function() { 
				window.location = "/functionaries/"; 
			});

			request.fail(function( jqHXR, textStatus ){
				alert( "Request failed: " + textStatus + ": " + jqHXR.responseText );
			});
		}
	});
});