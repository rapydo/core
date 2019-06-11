import { NgModule, ModuleWithProviders } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { RapydoModule } from '/rapydo/src/app/rapydo.module';
import { AuthGuard } from '/rapydo/src/app/app.auth.guard';

// import {YourModule} from "your/module";

const routes: Routes = [

];

@NgModule({
	imports: [
		RapydoModule,
	    RouterModule.forChild(routes),
	],
	declarations: [
	],

	providers: [
	],

	exports: [
		RouterModule
  	]

})
export class CustomModule {
} 