/*

Create and render a calendar view

*/

class Calendar {
	constructor(parent, month_display, year_display) {
		this.parent = parent;
		this.month_display = month_display;
		this.year_display = year_display;
		this.getQueryParams = new URLSearchParams(window.location.search);
	}

	// Set up the calendar
	setup() {
		this.checkQueryParams();
		this.setMonthOfYear(parseInt(this.getQueryParams.get('year')), parseInt(this.getQueryParams.get('month')));
		this.getEvents();
	}

	nextMonth() {
		if (this.month == 11) {
			this.getQueryParams.set('year', parseInt(this.getQueryParams.get('year')) + 1);
			this.getQueryParams.set('month', 0);
		} else {
			this.getQueryParams.set('month', parseInt(this.getQueryParams.get('month')) + 1);
		}
		this.setup();
	}

	previousMonth() {
		if (this.month == 0) {
			this.getQueryParams.set('year', parseInt(this.getQueryParams.get('year')) - 1);
			this.getQueryParams.set('month', 11);
		} else {
			this.getQueryParams.set('month', parseInt(this.getQueryParams.get('month')) - 1);
		}
		this.setup();
	}

	// Check if the query parameters are set
	checkQueryParams() {
		if (!this.getQueryParams.has('year')) {
			const year = new Date().getFullYear();
			this.getQueryParams.set('year', year);
		}
		if (!this.getQueryParams.has('month')) {
			const month = new Date().getMonth();
			this.getQueryParams.set('month', month);
		}
		if (this.getQueryParams.get('year') < 1970) {
			this.getQueryParams.set('year', 1970);
		}
		if (this.getQueryParams.get('month') < 0) {
			this.getQueryParams.set('month', 0);
		}
		if (this.getQueryParams.get('month') > 11) {
			this.getQueryParams.set('month', 11);
		}
		history.replaceState(null, '', window.location.pathname + '?' + this.getQueryParams.toString());
	}


	// Set up the month to display
	setMonthOfYear(year, month) {
		this.year = year;
		this.month = month;

		this.days = this.getDaysInMonth();
		this.today = this.checkToday();
		this.firstDay = this.getWeekDay(1);
	}

	// Returns how many days are in a given month in a given year
	getDaysInMonth() {
		return new Date(this.year, this.month+1, 0).getDate();
	}

	// Returns the day of today if it's in the current month, 0 otherwise
	checkToday() {
		const today = new Date();
		if (this.year == today.getFullYear() && this.month == today.getMonth()) {
			return today.getDate();
		}
		return 0;
	}

	getWeekDay(day) {
		const date = new Date(this.year, this.month, day);
		let dayOfWeek = date.getDay();
		// Adjust so that Monday is 0 and Sunday is 6
		dayOfWeek = (dayOfWeek + 6) % 7;
		return dayOfWeek;
	}

	// Render the calendar
	render(events) {
		// Create buffer
		const fragment = document.createDocumentFragment();
		// Clear the parent
		this.parent.innerHTML = '';

		// Create the calendar
		let week, weekCounter;
		for (let i = 1; i <= this.days + this.firstDay; i++) {
			if (i % 7 == 1) {
				weekCounter = 0;
				week = document.createElement('tr');
				week.classList.add('calendar-week');
				fragment.appendChild(week);
			}
			if (i <= this.firstDay) {
				const empty = document.createElement('td');
				empty.classList.add('calendar-empty');
				week.appendChild(empty);
				continue;
			}
			const day = document.createElement('td');
			day.classList.add('calendar-day');
			day.id = 'day-' + (i - this.firstDay);
			day.innerHTML = i - this.firstDay;
			if (i - this.firstDay == this.today) {
				day.classList.add('calendar-today');
			}
			if (events[i - this.firstDay]) {
				day.insertAdjacentHTML('beforeend', this.getDayHTML(events[i - this.firstDay]));
			}
			week.appendChild(day);
			weekCounter++;
		}
		if (weekCounter < 7) {
			for (let i = weekCounter; i < 7; i++) {
				const empty = document.createElement('td');
				empty.classList.add('calendar-empty');
				week.appendChild(empty);
			}
		}

		// Render the calendar from the buffer
		this.parent.appendChild(fragment);
		// Update the month
		this.month_display.innerHTML = months[this.month];
		// Update the year
		this.year_display.innerHTML = this.year;
	}

	// Query the server for the events of the current month
	getEvents() {
		const url = '/events/' + this.year + '/' + (this.month + 1);
		fetch(url)
			.then(response => response.json())
			.then(data => {
				const events = new Array(31);
				for (let i = 0; i < data.events.length; i++) {
					const startDay = new Date(data.events[i].start).getDate();
					if (!events[startDay]) {
						events[startDay] = [];
					}
					events[startDay].push(data.events[i]);
				}
				this.render(events);
			});
	}

	getDayHTML(events) {
		if (!events instanceof Array) {
			events = [events];
		}

		let html = '', time;
		for (let i = 0; i < events.length; i++) {
			time = DateTime.fromHTTP(events[i].start).setLocale(locale);
			html +=
			`<div class="btn-public m-1 p-1 mx-auto calendar-event" data-id="${events[i].id}">
				<p class="m-0">${time.toLocaleString(DateTime.TIME_SIMPLE)}: ${events[i].title}</p>
			</div>`;
		}
		return html;
	}
}