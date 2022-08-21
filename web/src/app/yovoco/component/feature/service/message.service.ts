import { Injectable } from '@angular/core';
import { MessageService } from 'primeng/api';
@Injectable({
	providedIn: 'root',
})
export class MessagesService {
	constructor(private messageService: MessageService) {}

	clear() {
		this.messageService.clear();
	}

	showSuccess(message) {
		this.messageService.add({ severity: 'success', summary: 'Success', detail: message, life: 3000 });
		setTimeout(() => {
			this.clear();
		}, 3000);
	}

	showError(message) {
		this.messageService.add({ severity: 'error', summary: 'Error', detail: message, life: 3000 });
		setTimeout(() => {
			this.clear();
		}, 3000);
	}

	showInfo(message) {
		this.messageService.add({ severity: 'info', summary: 'Info', detail: message, life: 3000 });
		setTimeout(() => {
			this.clear();
		}, 3000);
	}

	showWarning(message) {
		this.messageService.add({ severity: 'warning', summary: 'Warning', detail: message, life: 3000 });
		setTimeout(() => {
			this.clear();
		}, 3000);
	}
}
