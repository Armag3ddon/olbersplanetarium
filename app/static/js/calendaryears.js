/*

Handling of holiday/vacation creation en mass

*/

// Calendar class
class CalendarYear {
	constructor(parent, year_element) {
		this.parent = parent;
		this.year_element = year_element;
		this.row = 0;
	}

	queryYear() {
		const url = '/calendaryeardata/' + this.year_element.value;
		fetch(url)
			.then(response => response.json())
			.then(data => {
				console.log(data);
				this.parent.innerHTML = '';
				this.row = 0;
				for (const event of data.events) {
					this.createRow(event.title, event.begin, event.end);
				}
				this.JSONify();
			})
			.catch(error => console.error('Error fetching calendar year data:', error));
	}

	createRow(title, begin, end) {
		this.row += 1;
		const html =
			`<div class="row g-2 align-items-center mb-1" id="row_${this.row}">
				<div class="col-auto form-floating">
					<input type="text" class="form-control" id="title_${this.row}" name="title_${this.row}" value="${title}" placeholder="${title_text}">
					<label for="title_${this.row}" class="form-label">${title_text}</label>
				</div>
				<div class="col-auto">
					<label for="startdate_${this.row}" class="form-label">${startdate_text}</label>
				</div>
				<div class="col-auto">
					<input type="date" class="form-control" id="startdate_${this.row}" name="startdate_${this.row}" value="${begin}">
				</div>
				<div class="col-auto">
					<label for="enddate_${this.row}" class="form-label">${enddate_text}</label>
				</div>
				<div class="col-auto">
					<input type="date" class="form-control" id="enddate_${this.row}" name="enddate_${this.row}" value="${end}">
				</div>
				<div class="col-auto">
					<button class="btn btn-danger" id="delete_${this.row}">X</button>
				</div>
			</div>`;
		this.parent.insertAdjacentHTML('beforeend', html);
		const currentRow = this.row;
		document.getElementById('delete_' + this.row).addEventListener('click', () => {
			this.deleteRow(currentRow);
		});
		$(`#startdate_${this.row}`).change(() => {
			this.JSONify();
		});
		$(`#enddate_${this.row}`).change(() => {
			this.JSONify();
		});
		$(`#title_${this.row}`).change(() => {
			this.JSONify();
		});
	}

	clearRows() {
		this.parent.innerHTML = '';
		this.row = 0;
	}

	deleteRow(rowId) {
		console.log(rowId);
		const row = document.getElementById('row_' + rowId);
		if (row) row.remove();
	}

	JSONify() {
		const json = {};
		for (let i = 1; i <= this.row; i++) {
			if (!document.getElementById('row_' + i))
				continue;
			const title = document.getElementById('title_' + i);
			const startdate = document.getElementById('startdate_' + i);
			const enddate = document.getElementById('enddate_' + i);
			json[i] = {
				title: title.value,
				start: startdate.value,
				end: enddate.value
			};
		}
		$('#days').val(JSON.stringify(json));
	}

	changeYear() {
		this.clearRows();
		this.queryYear();
		current_year = this.year_element.value;
	}

	revertChangeYear() {
		this.year_element.value = current_year;
	}
}