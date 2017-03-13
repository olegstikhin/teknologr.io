$(document).ready(function() {

	//$('#{{form.degree_programme.id_for_label}}').editableSelect({ effects: 'slide' });

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

	$('[data-toggle="tooltip"]').tooltip({
		placement : 'top'
	});

	$('.removeMemberType').click(function(){
		if(confirm("Vill du radera denna medlemstyp?")) {
			var id = $(this).data('id');
			var request = $.ajax({
				url: "/api/memberTypes/" + id + "/",
				method: "DELETE",
			});

			request.done(function() {
				location.reload();
			});

			request.fail(function( jqHXR, textStatus ){
				alert( "Request failed: " + textStatus + ": " + jqHXR.responseText );
			})
			
		}
	});
});