import { NgModule, ModuleWithProviders } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { SharedModule } from '@rapydo/shared.module';
import { AuthGuard } from '@rapydo/app.auth.guard';

import { DataComponent } from "@app/components/data.component";

const routes: Routes = [
	{
		path: '',
		redirectTo: '/app/data',
		pathMatch: 'full'
	},
	{
		path: 'app',
		redirectTo: '/app/data',
		pathMatch: 'full'
	},
	{
		path: 'app/data',
		component: DataComponent,
		canActivate: [AuthGuard],
		runGuardsAndResolvers: 'always',
		data: { roles: ['normal_user'] }
	},
];

@NgModule({
	imports: [
		SharedModule,
	    RouterModule.forChild(routes),
	],
	declarations: [
		DataComponent
	],

	providers: [
	],

	exports: [
		RouterModule
  	]

})
export class CustomModule {
} 