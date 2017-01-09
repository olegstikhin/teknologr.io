$(".side-object").click(function(e) {
	e.preventDefault();
	loadMember($(this).attr('data-id'));
});


