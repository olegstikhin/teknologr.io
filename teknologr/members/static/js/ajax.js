function loadSide(category) {
	//var category = $('input[type=radio][name=side]:checked').val();
	$("#side").load("/side/" + category);
};
