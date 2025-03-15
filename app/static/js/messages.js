/*

Receive and render messages on the start page
Additional functions for the creation form

*/

class Messages {
	constructor(parent) {
		this.parent = parent;
		this.getQueryParams = new URLSearchParams(window.location.search);
	}

	setup() {
		this.checkQueryParams();
		this.page = this.getQueryParams.get('page');
		this.singlePost = this.getQueryParams.get('post');
		this.getMessages();
	}

	// Check if the query parameter (page) is set
	checkQueryParams() {
		if (!this.getQueryParams.has('page')) {
			this.getQueryParams.set('page', 1);
		}
		if (this.getQueryParams.get('page') < 1) {
			this.getQueryParams.set('page', 1);
		}
	}

	getMessages() {
		let url = '/posts/' + this.page;
		if (this.singlePost) {
			url = '/posts/' + this.singlePost + '?post=1';
		}
		fetch(url)
			.then(response => response.json())
			.then(data => {
				if (data.posts.length != 0) {
					this.render(data);
				}
			});
	}

	render(messages) {
		// Create buffer
		const fragment = document.createDocumentFragment();
		// Clear parent
		this.parent.innerHTML = '';

		if (this.singlePost) {
			const back = $('<a>',{ class: 'btn btn-primarycontrast btn-sm ms-4', href: '/' });
			back.html(backToPosts);
			fragment.appendChild(back.get(0));
		}

		// Loop through top level messages
		for (let i = 0; i < messages.posts.length; i++) {
			let message = "";
			if (this.singlePost) {
				message = this.renderMessage(messages.posts[i]);
			} else {
				message = this.renderMessage(messages.posts[i], false, true);
			}
			fragment.appendChild(message);

			let counter = 0;
			for (let j = 0; j < messages.answers.length; j++) {
				if (messages.answers[j].answer_to == messages.posts[i].id) {
					counter++;
					if (this.singlePost || counter == 1) {
						const answer = this.renderMessage(messages.answers[j], true);
						fragment.appendChild(answer);
					} else {
						if (counter == 2) {
							const loadmore = $('<a>',{ class: 'btn btn-primarycontrast btn-sm ms-4', href: '/?post=' + messages.posts[i].id });
							loadmore.html(loadMoreAnswers);
							fragment.appendChild(loadmore.get(0));
						}
					}
				}
			}
		}
		this.parent.appendChild(fragment);

		// Add event listener to the post creation form to clear the form if it is hidden
		$('#postcreation').on('hidden.bs.collapse', function () {
			$('#newpost_header').show();
			$('#answer_header').hide();
			$('#answer_to').val(null);
		});
	}

	renderMessage(message, with_indent = false, answerable = false) {
		const messageContainer = $('<div>', { class: 'container p-1' });
		const time = DateTime.fromHTTP(message.timestamp).setLocale(locale);
		let title = escapeHtml(message.title);
		if (title) {
			title = `<h6 class="card-title">${title}</h6>`;
		}
		const content = parser.render(escapeHtml(message.content));
		let avatar = default_avatar;
		if (message.author_avatar) {
			avatar = avatar_url + message.author_avatar;
		}
		let indent = "";
		let answer_button = "";;
		if (with_indent) {
			indent =
				`<div class="d-flex ms-auto" style="height: 50px;">
					<div class="vr"></div>
				</div>
				<hr style="width: 20px;">`;
			answer_button = "";
		}
		if (answerable) {
			answer_button =
			`<button type="button" class="btn btn-primarycontrast float-end" onclick="createAnswer(${message.id})">
				<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-return-left" viewBox="0 0 16 16">
					<path fill-rule="evenodd" d="M14.5 1.5a.5.5 0 0 1 .5.5v4.8a2.5 2.5 0 0 1-2.5 2.5H2.707l3.347 3.346a.5.5 0 0 1-.708.708l-4.2-4.2a.5.5 0 0 1 0-.708l4-4a.5.5 0 1 1 .708.708L2.707 8.3H12.5A1.5 1.5 0 0 0 14 6.8V2a.5.5 0 0 1 .5-.5"></path>
				</svg>
			</button>`;
		}
		messageContainer.html(`
			<div class="hstack justify-content-md-center bg-complementary mb-1">
				${indent}
				<div class="card" style="width: 100%;">
					<div class="card-body py-0 lh-sm">
						<img src="${avatar}" class="img-fluid border rounded-circle border-3 border-light float-end" style="max-width:50px" alt="${message.author}">
						${title}
						${content}
					</div>
					<div class="card-footer fs-6">
						<p class="card-text text-muted fs-6 float-start">${message.author} - ${time.toLocaleString(DateTime.DATETIME_MED)}</p>
						${answer_button}
					</div>
				</div>
			</div>
		`);
		return messageContainer.get(0);
	}
}

function createAnswer(id) {
	$('#postcreation').collapse('show');
	$('#postcreation').get(0).scrollIntoView({ behavior: 'smooth' });
	$('#answer_to').val(id);
	$('#newpost_header').hide();
	$('#answer_header').show();
}