//-*- coding: utf-8 -*-
//copyright 2016 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
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

    editorsMap: {
        'Text':  Slick.Editors.Text,
        'Integer': Slick.Editors.Integer,
        'Date': Slick.Editors.Date
    },

    editableGrid: function(nodeSelector, columns, data, options) {
        // object containing the grid options
        // https://github.com/mleibman/SlickGrid/wiki/Grid-Options
        // NOTE :
        // 1. we can not use Slick.Data.DataView model
        //    as cellexternalcopymanager do not use it
        // 2. we set the right editor from editorsMap mapping
        for (var idx in columns){
            if (columns.hasOwnProperty(idx)) {
               var column = columns[idx]
               if ('editor' in column) {
                   column.editor = this.editorsMap[column['editor']];
               }
            }
        };
        var grid = new Slick.Grid(nodeSelector, data, columns, options);
        // add form input
        var domid = $(nodeSelector).data('domid'),
            $input = $('<input type="hidden" name="'+domid+'" id="'+domid+'"/>')
            .val(JSON.stringify(grid.getData()));
        $(nodeSelector).data('cw-slickgrid-grid', grid).append($input);

        grid.setSelectionModel(new Slick.CellSelectionModel());
        grid.registerPlugin(new Slick.AutoTooltips({enableForHeaderCells: true}));
        // set keyboard focus on the grid
        grid.getCanvasNode().focus();

        var pluginOptions = {
            includeHeaderWhenCopying : false
        };

        var copyManager = new Slick.CellExternalCopyManager(pluginOptions);
        grid.registerPlugin(copyManager);

        // subscribe to events
        copyManager.onPasteCells.subscribe(function (e, args) {
            $input.val(JSON.stringify((grid.getData())));
        });

        grid.onCellChange.subscribe(function (e, args) {
            $input.val(JSON.stringify((grid.getData())));
        });

        grid.onAddNewRow.subscribe(function (e, args) {
            grid.invalidateRow(data.length);
            data.push(args.item);
            grid.updateRowCount();
            grid.render();
            $input.val(JSON.stringify((grid.getData())));
       });
    }
});
