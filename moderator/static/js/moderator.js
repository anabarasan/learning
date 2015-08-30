function likes() {
	var $this = $(this);
	$this.parent().submit();
}

$(document).ready(function () {
	$('.vote').on('click', likes);
});