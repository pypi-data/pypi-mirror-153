Summary
=======

Table view rendered using the SlickGrid_ library.

SlickGrid is an advanced JavaScript grid/spreadsheet component.

This view accepts any non-empty rset. It uses introspection on the
result set to compute column names and the proper way to display the
cells.

It is highly configuration and accepts the same wealth of option than
cubicweb.web.view.tableview.RsetTableView.

.. _SlickGrid: https://github.com/mleibman/SlickGrid

Example
=======

To try it at the speed of light
--------------------------------

Once your instance is running you can go to::

  http://localhost:8080/view?rql=Any L, X WHERE X is CWUser, X login L&vid=slickgrid

That's all. The rendered table uses the 'slickgrid' view.

Calling the slidgrid from your views
------------------------------------

The simplest way is to call:

.. sourcecode:: python

  self._cw.wview('slickgrid', rset, 'null')

Options can be specified by class attributes:

* `displaycols`, if not `None`, should be a list of rset's columns to be
  displayed.

* `headers`, if not `None`, should be a list of headers for the table's
  columns.  `None` values in the list will be replaced by computed column
  names.

* `cellvids`, if not `None`, should be a dictionary with table column index
  as key and a view identifier as value, telling the view that should be
  used in the given column.

As well as SlickGrid_ specific option:

* `columns_options`: a dictionary of SlickGrid column options

One can use:

.. sourcecode:: python

  class MyRsetGridView(RsetGridView):
      __regid__ = 'myslickgrid'
      headers = (_('first'), _('second'), _('third'))
      cellvids = {0: 'text', 1: 'inline', 2:'outofcontext'}
      columns_options = {0: {'sortable': False}}

  self._cw.wview('myslickgrid', rset, 'null')

Note that the pagination is not working yet.
