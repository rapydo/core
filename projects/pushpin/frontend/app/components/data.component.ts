import { Component } from '@angular/core';

import { ApiService } from '@rapydo/services/api';
import { NotificationService } from '@rapydo/services/notification';
import { WebSocketsService } from '@rapydo/services/websockets'

@Component({
  templateUrl: './data.component.html'
})
export class DataComponent {

	constructor(
		private api: ApiService,
		private socket: WebSocketsService,
		private notify: NotificationService
		) {
	}

	private get_message_from_socket(message:string) {
        this.notify.showSuccess(message, "Notification received from the socket");
	}

	public start() {
		this.api.post("data").subscribe(
			response => {
				// Subscribing socket channel === task_id
				this.notify.showInfo("Task ID = " + response.data, "Request submitted");
				this.socket.subscribe(
					response.data,
					this.get_message_from_socket.bind(this)
				);
			}
		);
	}
}
