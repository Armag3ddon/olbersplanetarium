/* Show warning messages for malformed input */

function initWarnings() {
	// Start date is in the past or later than the end date
	$('#start').on('change', (data) => {
		const date = DateTime.fromISO(data.target.value);
		if (date < DateTime.now()) {
			showWarning(warn_BeginInPast);
		}
		const end = DateTime.fromISO($('#end').val());
		if (end < date) {
			showWarning(warn_EndBeforeStart);
		}
	});
	// End date is before start date
	$('#end').on('change', (data) => {
		const start = DateTime.fromISO($('#start').val());
		const end = DateTime.fromISO(data.target.value);
		if (end < start) {
			showWarning(warn_EndBeforeStart);
		}
	});
	// Event title gets too long
	$('#title').on('input', (data) => {
		if (data.target.value.length >= 256) {
			showWarning(warn_TitleTooLong);
		}
	});
	// Event description gets too long
	$('#description').on('input', (data) => {
		if (data.target.value.length >= 256) {
			showWarning(warn_DescriptionTooLong);
		}
	});
}

// Create a div element and show in the flash message area
function showWarning(message) {
	const alert = $('<div class="alert alert-warning alert-dismissible mt-2 fade show" role="alert">' + message + '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>');
	$('#flash-message').append(alert);
}