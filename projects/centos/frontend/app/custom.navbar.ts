import { Component, Input } from '@angular/core';

@Component({
  selector: 'customlinks',
  providers: [],
  templateUrl: './custom.navbar.links.html',
})
export class CustomNavbarComponent {

  @Input() user: any;

  constructor() { }

}


@Component({
  selector: 'custombrand',
  providers: [],
  templateUrl: './custom.navbar.brand.html',
})
export class CustomBrandComponent {

  public myproject: string

  constructor() {
    var t = process.env.projectTitle;
    t = t.replace(/^'/, "");
    t = t.replace(/'$/, "");
    this.myproject = t; 
  }

}
