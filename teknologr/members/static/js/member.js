$(document).ready(function() {

	$("#deletemember").click(function(){
		if(confirm("Vill du radera denna medlem?")) {
			var id = $(this).data('id');
			var request = $.ajax({
				url: "/api/members/" + id + "/",
				method: "DELETE",
			});
 
			request.done(function() { 
				window.location = "/members/"; 
			});

			request.fail(function( jqHXR, textStatus ){
				alert( "Request failed: " + textStatus + ": " + jqHXR.responseText );
			});
		}
	});

});