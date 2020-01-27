import { NgModule, ModuleWithProviders } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { SharedModule } from '@rapydo/shared.module';
import { AuthGuard } from '@rapydo/app.auth.guard';

// import {YourModule} from "your/module";

const routes: Routes = [
	{
		path: '',
		redirectTo: '/app/admin/users',
		pathMatch: 'full'
	},
	{
		path: 'app',
		redirectTo: '/app/admin/users',
		pathMatch: 'full'
	},
];

@NgModule({
	imports: [
		SharedModule,
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