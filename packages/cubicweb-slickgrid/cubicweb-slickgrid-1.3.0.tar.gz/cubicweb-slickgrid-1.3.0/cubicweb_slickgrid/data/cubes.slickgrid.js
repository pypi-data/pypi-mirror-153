//-*- coding: utf-8 -*-
//copyright 2014 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
//ontact http://www.logilab.fr -- mailto:contact@logilab.fr
//This program is free software: you can redistribute it and/or modify it under
//the terms of the GNU Lesser General Public License as published by the Free
//Software Foundation, either version 2.1 of the License, or (at your option)
//any later version.
//
//This program is distributed in the hope that it will be useful, but WITHOUT
//ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
//FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
//details.
//
//You should have received a copy of the GNU Lesser General Public License along
//with this program. If not, see <http://www.gnu.org/licenses/>.

cw.slickgrid = new Namespace('cw.slickgrid');

jQuery.extend(cw.slickgrid, {

    // Display the grid on the DOM.
    // * `nodeSelector`: an JQuery node selector, ex: "#mynode", see
    // * `columns`: an object containing columns definitions/options, see
    //              https://github.com/mleibman/SlickGrid/wiki/Column-Options
    // * `data`: an object container the data
    // * `enable_sorting`: if `true` the column will be sortable by clicking 
    //                     on the header
    // * ``enable_column_picker`: if `true` a right click menu is added on 
    //                            headers allowing to choose displayed columns
    displayGrid: function (nodeSelector, columns, data, options, 
                           enable_sorting, enable_column_picker) {
    // object containing the grid options
    // https://github.com/mleibman/SlickGrid/wiki/Grid-Options
    var dataView = new Slick.Data.DataView();
    var grid = new Slick.Grid(nodeSelector, dataView, columns, options);
    $(nodeSelector).data('cw-slickgrid-grid', grid);

    // enable column picker
    if (enable_column_picker) {
        new Slick.Controls.ColumnPicker(columns, grid, options);
    }

    // set sorting algorithm that consideres lower cases of cells content
    // XXX maybe we can extract text part from HTML.
    if (enable_sorting){
        grid.onSort.subscribe(function fraiseGridOnSort(e, args) {
        sortcol = args.sortCol.field;
        function comparer(a, b) {
            var x = a[sortcol].toLowerCase(), y = b[sortcol].toLowerCase();
            return (x == y ? 0 : (x > y ? 1 : -1));
        }
        dataView.sort(comparer, args.sortAsc);
        });
    }

    // update grid when data changes (a.k.a. on sorting)
    dataView.onRowsChanged.subscribe(function fraiseGridOnRowChanged(e, args) {
            grid.invalidateRows(args.rows);
            grid.render();
    });

    // setup data to dataView
    dataView.setItems(data);
    grid.invalidate();
    grid.render();
    }
});
