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
		this.render();
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
	render() {
		// Clear the parent
		this.parent.innerHTML = '';

		// Create the calendar
		let week, weekCounter;
		for (let i = 1; i <= this.days + this.firstDay; i++) {
			if (i % 7 == 1) {
				weekCounter = 0;
				week = document.createElement('tr');
				week.classList.add('calendar-week');
				this.parent.appendChild(week);
			}
			if (i <= this.firstDay) {
				const empty = document.createElement('td');
				empty.classList.add('calendar-empty');
				week.appendChild(empty);
				continue;
			}
			const day = document.createElement('td');
			day.classList.add('calendar-day');
			day.innerHTML = i - this.firstDay;
			if (i == this.today) {
				day.classList.add('calendar-today');
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

		// Update the month
		this.month_display.innerHTML = months[this.month];
		// Update the year
		this.year_display.innerHTML = this.year;
	}
}