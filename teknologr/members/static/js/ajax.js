function loadMain(category, id) {
	$("#main").load(category + '/' + id, function(response, status, xhr){
		if (status == "error") {
			$("#main").html('<h1 class="page-header">Ett fel uppstod</h1>');
		}
	});
};

function loadSide() {
	var category = $('input[type=radio][name=side]:checked').val();
	$("#side").load("side/" + category);
};
