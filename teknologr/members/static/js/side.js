$(".side-member").click(function(e) {
	e.preventDefault();
	loadMember($(this).attr('data-id'));
});


