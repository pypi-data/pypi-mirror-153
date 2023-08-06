# -*- coding: utf-8 -*-
# copyright 2014-2022 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
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


from cubicweb.web.views import tableview
from cubicweb.uilib import js
from cubicweb.utils import UStringIO, JSString


class RsetGridColRenderer(tableview.RsetTableColRenderer):
    '''Same as cubicweb.web.views.tableview.RsetTableColRenderer
    but render data that Slick.Grid accepts as header definitions.
    '''

    def render_header(self):
        stream = UStringIO()
        super(RsetGridColRenderer, self).render_header(stream.write)
        return stream.getvalue()

    def render_cell(self, rownum):
        stream = UStringIO()
        super(RsetGridColRenderer, self).render_cell(stream.write, rownum)
        return stream.getvalue()


class GridLayout(tableview.TableLayout):
    '''Same as cubicweb.web.views.tableview.TableLayout but
    render data that Slick.Grid accepts.
    '''
    __regid__ = 'slickgrid_layout'

    enable_column_picker = True

    def _setup_tablesorter(self, divid):
        # should do the corresponding things
        pass

    def render_table(self, w, *args, **kwargs):
        cnx = self._cw
        _ = self._cw._
        divid = self.view.domid
        self.render_assets()

        w(u'<div id="%s">' % divid)
        w(_(u'loading data grid ...'))
        w(u'</div>')

        # Store js to be added onload, by cell renderers, into a
        # temporary list. This is required because these js may need
        # the dom to be populated. But the dom is populated once the
        # slickgrid rendering is performed. A solution is to
        # synchronously execute these js after the slickgrid
        # rendering.
        onloads = []

        # monkeypatch add_onload to control onloaded js
        orig_onload = cnx.html_headers.add_onload
        cnx.html_headers.add_onload = lambda x: onloads.append(x)

        # render cells that may add js to onload
        onload_call = self.get_js(divid)

        # bring back the original behaviour
        cnx.html_headers.add_onload = orig_onload

        # synchronously add slickgrid rendering then every other js
        # from cells renderers
        onloads.insert(0, str(onload_call))
        cnx.add_onload('\n'.join(onloads))

    def get_js(self, divid):
        view = self.view
        colrenderers = view.build_column_renderers()
        headers = self.render_table_headers(colrenderers)
        data = self.render_table_body(colrenderers)
        return str(
            js.cw.slickgrid.displayGrid(
                '#%s' % divid, headers, data,
                view.default_grid_options,
                self.enable_sorting,
                self.enable_column_picker)) + ';'

    def render_table_headers(self, colrenderers):
        return [self.render_header(cr) for cr in colrenderers]

    def render_header(self, colrenderer):
        colid = colrenderer.colid
        header = {'id': colid, 'field': colid,
                  'name': colrenderer.render_header()}
        if self.enable_sorting:
            header['sortable'] = True
        header.update(self.view.get_column_options(colrenderer.colid))
        return header

    def render_table_body(self, colrenderers):
        return [self.render_row(rownum, colrenderers)
                for rownum in range(self.cw_rset.rowcount)]

    def render_row(self, rownum, renderers):
        row = {'id': rownum}
        row.update((str(cr.colid), self.render_cell(rownum, cr))
                   for cr in renderers)
        return row

    def render_cell(self, rownum, renderer):
        return renderer.render_cell(rownum)

    def render_assets(self):
        cnx = self._cw
        cnx.add_css(('SlickGrid/slick.grid.css',
                     'SlickGrid/slick-default-theme.css'))
        cnx.add_js(('jQuery/jquery.event.drag-2.2.js',
                    'SlickGrid/slick.core.js',
                    'SlickGrid/slick.dataview.js',
                    'SlickGrid/slick.grid.js'))
        if self.enable_column_picker:
            cnx.add_css('SlickGrid/controls/slick.columnpicker.css')
            cnx.add_js('SlickGrid/controls/slick.columnpicker.js')
        cnx.add_css('cubes.slickgrid.css')
        cnx.add_js('cubes.slickgrid.js')


class RsetGridView(tableview.RsetTableView):
    """This Grid view uses the slickgrid
    https://github.com/mleibman/SlickGrid javascript librairy to render
    a rset.

    This view accepts any non-empty rset. It uses intropection on the
    result set to compute column names and the proper way to display
    the cells.

    It is highly configurable and accepts the same wealth of option than
    :class:`cubicweb.web.view.tableview.RsetTableView` plus the following:

    * `default_grid_options`: a dictionary containing slickgrid grid
      options, see https://github.com/mleibman/SlickGrid/wiki/Grid-Options

    * `default_column_options`: slickgrid options applied to every
      column by default, see
      https://github.com/mleibman/SlickGrid/wiki/Column-Options

    * `columns_options`: a dictionary referencing a column index to a
      dict of slickgrid # column options. This completely overrides the
      default column options set in `default_column_options`.

    """
    __regid__ = 'slickgrid'
    layout_id = 'slickgrid_layout'
    default_column_renderer_class = RsetGridColRenderer
    handle_pagination = False  # pagination does not works well for now

    default_grid_options = {
        'forceFitColumns': True,
        'defaultFormatter': JSString('function (r,c,v,cc,d){return v;}'),
        'fullWidthRows': True,
        'autoHeight': True,
        'syncColumnCellResize': True,
    }
    default_column_options = {'focusable': False}
    columns_options = None

    def get_column_options(self, colid):
        '''Return a dictionary containing'''
        if self.columns_options is None:
            return self.default_column_options
        column_options = self.columns_options.get(colid, None)
        if column_options is None:
            return self.default_column_options
        return column_options
