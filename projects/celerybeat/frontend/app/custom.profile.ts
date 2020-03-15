import { Component, Input } from '@angular/core';

@Component({
  selector: '[my-profile-row]',
  providers: [],
  templateUrl: 'custom.profile.html'

})
export class CustomProfileComponent {

  @Input() row: any;

  constructor() { }

}