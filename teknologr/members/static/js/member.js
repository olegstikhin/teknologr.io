$(document).ready(function() {

	$("#addmembertypeform").submit(function(event){
		var data = $(this).serialize();
		var request = $.ajax({
			url: "/api/memberTypes/",
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
			});	
		}
	});

	$('.editMemberType').click(function(){
		var id = $(this).data('id');
		$("#editMemberType .modal-body").load("/membertype/" + id + "/edit/", function() {
			
		});
	});

});