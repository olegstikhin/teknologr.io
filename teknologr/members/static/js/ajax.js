function loadMember(id) {
	$("#main").load("member/"+id, function(response, status, xhr){
		if (status == "error") {
			$("#main").html('<h1 class="page-header">404 - Hittades inte</h1><h3>Denna medlem hittades inte i registret.</h3>');
		}
	});
};

function loadGroup(id) {
	$("#main").load("TODO");
};

function loadFunctionary(id) {
	$("#main").load("TODO");
};

function loadDecoration(id) {
	$("#main").load("TODO");
};

function loadMain(category, id) {
	$("#main").load(category + '/' + id)
}

function loadSide() {
	var category = $('input[type=radio][name=side]:checked').val();
	$("#side").load("side/" + category);
};
