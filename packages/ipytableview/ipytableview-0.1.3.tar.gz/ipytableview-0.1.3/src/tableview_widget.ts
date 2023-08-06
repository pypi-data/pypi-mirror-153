// Copyright (c) {{ cookiecutter.author_name }}
// Distributed under the terms of the Modified BSD License.

import $ from 'jquery';

import {
  DOMWidgetModel,
  DOMWidgetView,
  ISerializers,
} from '@jupyter-widgets/base';

import { MODULE_NAME, MODULE_VERSION } from './version';

// Import the CSS
import '../css/widget.css';

export class TableModel extends DOMWidgetModel {
  defaults() {
    return {
      ...super.defaults(),
      _model_name: TableModel.model_name,
      _model_module: TableModel.model_module,
      _model_module_version: TableModel.model_module_version,
      _view_name: TableModel.view_name,
      _view_module: TableModel.view_module,
      _view_module_version: TableModel.view_module_version,
      table_body: [],
      headers: [],
      selected: -1,
    };
  }

  static serializers: ISerializers = {
    ...DOMWidgetModel.serializers,
    // Add any extra serializers here
  };

  static model_name = 'TableModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'TableView'; // Set to null if no view
  static view_module = MODULE_NAME; // Set to null if no view
  static view_module_version = MODULE_VERSION;
}

export class TableView extends DOMWidgetView {
  table_body: JQuery<HTMLElement>;

  render() {
    this.el.classList.add('tableview-widget');

    this.makeTable(this.model.get('headers'));

    this.model.on('change:table_body', this.table_body_changed, this);
    this.model.on('change:selected', this.set_selected_row, this);
  }

  table_body_changed() {
    const table_body_list = this.model.get('table_body');
    this.table_body.empty();
    for (const i in table_body_list) {
      const row = $('<tr/>');
      this.table_body.append(row);
      for (const j in table_body_list[i]) {
        const col = $('<td/>').text(table_body_list[i][j]);
        row.append(col);
      }
    }

    this.auto_size_columns();
    this.set_onclick_handler();
  }

  set_selected_row() {
    const index = this.model.get('selected');
    if (index === -1) {
      $('table')
        .find('tbody tr')
        .each((_i, tr) => {
          $(tr).removeClass('selected');
        });
    } else {
      const tr = $('table').find('tbody tr')[index];
      $(tr).addClass('selected').siblings().removeClass('selected');
    }
  }

  set_onclick_handler() {
    const model = this.model;
    $('table')
      .find('tbody tr')
      .each((idx, tr) => {
        tr.onclick = function () {
          model.set('selected', idx);
          model.save_changes();
          $(tr).addClass('selected').siblings().removeClass('selected');
        };
      });
  }

  auto_size_columns() {
    const $table = $('table');
    const $headCells = $table.find('thead tr').children();
    const $bodyCells = $table.find('tbody tr:first').children();

    // Get the thead columns width array
    const headColWidth = $headCells
      .map(function () {
        return $(this).width();
      })
      .get();

    // Get the tbody columns width array
    const bodyColWidth = $bodyCells
      .map(function () {
        return $(this).width();
      })
      .get();

    // Get max between thead and tbody widths
    const colWidth: number[] = [];
    for (const index in headColWidth) {
      colWidth[index] = Math.max(headColWidth[index], bodyColWidth[index]);
    }

    // Set the width of thead columns
    $table
      .find('tbody tr')
      .children()
      .each((i, v) => {
        $(v).width(colWidth[i]);
      });
    $table
      .find('thead tr')
      .children()
      .each((i, v) => {
        $(v).width(colWidth[i]);
      });
  }

  makeTable(headers: string[]) {
    const table = $('<table/>').addClass('tb');
    const header = $('<thead/>');
    table.append(header);
    const row = $('<tr/>');
    header.append(row);

    for (const index in headers) {
      const col = $('<th/>').text(headers[index]);
      row.append(col);
    }

    this.table_body = $('<tbody/>');
    table.append(this.table_body);

    return this._setElement(table[0]);
  }
}
