# -*- coding: utf-8 -*-
# copyright 2016-2022 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

"""cubicweb-slickgrid views/forms/actions/components for web ui"""

from cubicweb import tags
from cubicweb.dataimport import ucsvreader
from cubicweb.uilib import js
from cubicweb.web.formwidgets import FieldWidget


class EditableSlickGridWidget(FieldWidget):
    """
    Load a CSV file into a SlickGrid table.
    Loaded data can be edited with Excel copy-paste feature.
    This widgets comes with EditableSlickGridField which
    defines columns.
    """
    default_grid_options = {
        'editable': True,
        'enableAddRow': True,
        'enableCellNavigation': True,
        'asyncEditorLoading': False,
        'enableTextSelectionOnCells': True,
        'autoEdit': False
        }

    default_column_options = {'focusable': False}

    needs_css = (('SlickGrid/slick.grid.css',
                  'cubes.slickgrid.css',
                  'SlickGrid/css/smoothness/jquery-ui-1.8.16.custom.css',
                  'SlickGrid/slick-default-theme.css'))
    needs_js = (('jQuery/jquery.event.drag-2.2.js',
                 'SlickGrid/slick.core.js',
                 'SlickGrid/slick.grid.js',
                 'SlickGrid/slick.editors.js',
                 'SlickGrid/slick.formatters.js',
                 'SlickGrid/plugins/slick.autotooltips.js',
                 'SlickGrid/plugins/slick.cellrangedecorator.js',
                 'SlickGrid/plugins/slick.cellrangeselector.js',
                 'SlickGrid/plugins/slick.cellexternalcopymanager.js',
                 'SlickGrid/plugins/slick.cellselectionmodel.js',
                 'cubes.slickgrid.widgets.js'))
    columns = []

    def _render(self, form, field, renderer):
        columns = field.columns
        data = self.get_data(form, field, columns)
        divid = 'grid_{0}_{1}'.format(field.role_name(),
                                      form.edited_entity.eid)
        form._cw.add_onload(str(
            js.cw.slickgrid.editableGrid(
                '#%s' % divid, columns, data,
                self.default_grid_options)) + ';')
        width = sum(c.get('width', 0) for c in field.columns)
        return tags.div(id=divid, Class="cw-slickgrid",
                        style="width:%spx; height:400px;" % width,
                        **{'data-domid': field.dom_id(form)})

    def get_data(self, form, field, columns):
        grid_data = []
        columns = [h['field'] for h in columns]
        values = getattr(form.edited_entity, field.name)
        if values:
            encoding = field.encoding(form)
            for row in ucsvreader(values,
                                  delimiter=field.delimiter,
                                  encoding=encoding):
                grid_data.append(dict(zip(columns, row)))
            return grid_data
        return [dict(zip(columns, ('',) * len(columns)))]
