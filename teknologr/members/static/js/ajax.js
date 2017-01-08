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

function loadSideMembers() {
	$("#side").load("side_members");
};

function loadSideGroups() {
	$("#side").load("TODO");
};

function loadSideFunctionaries() {
	$("#side").load("TODO");
};

function loadSideDecorations() {
	$("#side").load("TODO");
};