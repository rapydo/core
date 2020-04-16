import { Component, ViewChild, TemplateRef, Injector } from '@angular/core';

import { BasePaginationComponent } from '@rapydo/components/base.pagination.component'

export interface Data {

}

@Component({
  selector: 'data',
  templateUrl: './data.component.html'
})
export class DataComponent extends BasePaginationComponent<Data> {

	@ViewChild('controlsCell', { static: false }) public controlsCell: TemplateRef<any>;
	@ViewChild('emptyHeader', { static: false }) public emptyHeader: TemplateRef<any>;
	@ViewChild('formModal', { static: false }) public formModal: TemplateRef<any>;

	protected endpoint = 'data'

	constructor(protected injector: Injector) {

	    super(injector);
	    this.init("entry");

	    this.list();
	    this.initPaging(20);
	}

	public ngAfterViewInit(): void {

	    this.columns = [];
	    this.columns.push({name: 'Name', prop: "name", flexGrow: 1.0});
	    this.columns.push({name: 'Age', prop: "age", flexGrow: 1.0});
	    this.columns.push({name: 'Date', prop: "date", flexGrow: 1.0});
	    this.columns.push({name: 'Healthy', prop: "healthy", flexGrow: 1.0});
	    this.columns.push({name: 'HGB', prop: "hgb", flexGrow: 1.0});
	    this.columns.push({name: 'controls', prop: 'controls', cellTemplate: this.controlsCell, headerTemplate: this.emptyHeader, flexGrow: 0.2});
	}

	list() {
		return this.get(this.endpoint)
	}

	remove(uuid) {
		return this.delete(this.endpoint, uuid);
	}


	create() {
		let data = {'get_schema': true, 'autocomplete': false}


		return this.post(this.endpoint, data, this.formModal, false);
	}

	update(row, element) {

		let data = {'get_schema': true, 'autocomplete': false}

		return this.put(row, this.endpoint, data, this.formModal, false);
	}
	submit() {
		this.send(this.endpoint);
	}

	filter(data_filter) {
		return this.unfiltered_data.filter(function(d) {
			// if (d.name.toLowerCase().indexOf(data_filter) !== -1) {
			// 	return true;
			// }

		return false;
		});
	}

}
