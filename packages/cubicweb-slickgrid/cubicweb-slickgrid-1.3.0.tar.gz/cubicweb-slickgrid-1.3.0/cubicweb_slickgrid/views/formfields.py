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

import json

from cubicweb import Binary
from cubicweb.web import ProcessFormError
from cubicweb.web import formfields as ff

from cubicweb_slickgrid.views.formwidgets import EditableSlickGridWidget


class EditableSlickGridField(ff.Field):
    """This field replaces FileField to handle edition of Binary data
       with SlickGrid Widget.
       Each field must define proper columns. For ex ::

         columns = [{'width': 200, 'editor': 'Text',
                    'id': 'col1', 'name': 'one', 'field': 'col1'},
                    {'width': 200, 'editor': 'Text',
                    'id': 'col2', 'name': 'two', 'field': 'col2'}]
    """
    widget = EditableSlickGridWidget
    delimiter = ','

    @property
    def columns(self):
        raise NotImplementedError

    def _ensure_correctly_typed(self, form, value, line):
        pass

    def _process_form_value(self, form):
        widget = self.get_widget(form)
        values = widget.process_field_data(form, self)
        res = []
        encoding = self.encoding(form)
        cols = [e['field'] for e in self.columns]
        for line, data in enumerate(json.loads(values), 1):
            _values = [e[1] for e in sorted(data.items(),
                                            key=lambda e: cols.index(e[0]))]
            self._ensure_correctly_typed(form, _values, line)
            res.append(self.delimiter.join(_values).encode(encoding))
        return Binary(str('\n'.join(res)))


class FloatEditableSlickGridField(EditableSlickGridField):

    def _ensure_correctly_typed(self, form, values, line):
        res = []
        # remove empty lines
        if not any(values):
            return res
        for value in values:
            if isinstance(value, str):
                value = value.strip()
                if not value:
                    res.append('')
                try:
                    res.append(float(value))
                except ValueError:
                    msg = form._cw._('float values are '
                                     'expected on line %s') % line
                    raise ProcessFormError(msg)
        return res
