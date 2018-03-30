import { Component, Input } from '@angular/core';

@Component({
  selector: 'customlinks',
  providers: [],
  templateUrl: './app.custom.navbar.html',
})
export class CustomNavbarComponent {

	@Input() user: any;

	constructor() { console.log("custom");}

}
