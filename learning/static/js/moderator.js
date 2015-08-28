function likes() {
	var $this = $(this),
		topicId = $this.data('topic'),
		action = $this.data('action'),
		url = '/vote/' + topicId + '/' + action;
	$.ajax(url, {
		method: 'POST',
		success: function (data) { console.log('vote success', data) },
		error: function (error) { console.error('vote failed', error) }
	});
}

$(document).ready(function () {
	$('.vote').on('click', likes);
});