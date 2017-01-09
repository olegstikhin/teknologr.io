function loadMain(category, id) {
	$("#main").load(category + '/' + id, function(response, status, xhr){
		if (status == "error") {
			$("#main").html('<h1 class="page-header">404 - Hittades inte</h1><h3>Det begärda objektet hittades inte</h3>');
		}
	});
};

function loadSide() {
	var category = $('input[type=radio][name=side]:checked').val();
	$("#side").load("side/" + category);
};
