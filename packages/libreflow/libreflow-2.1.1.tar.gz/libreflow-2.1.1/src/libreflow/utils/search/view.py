from kabaret.app import plugin
from kabaret.app.ui.gui.widgets.flow.flow_view import FlowView
from kabaret.app.ui.gui.widgets.widget_view import QtWidgets, QtGui, QtCore
from kabaret.app import resources


class SearchResult(QtWidgets.QTreeWidgetItem):

    def __init__(self, tree, result):
        super(SearchResult, self).__init__(tree)
        self.session = tree.session
        self.set_result(result)
    
    def set_result(self, result):
        self._result = result
        self._update()
    
    def _update(self):
        self.setText(0, self.label())
        self.setIcon(0, self.icon())
    
    def id(self):
        return self._result['id']
    
    def goto_oid(self):
        return self._result['goto_oid']
    
    def label(self):
        return self.session.cmds.Flow.get_source_display(
            self.goto_oid()
        )
    
    def icon(self):
        thumbnail_info = self.session.cmds.Flow.get_thumbnail_info(
            self.goto_oid()
        )
        if thumbnail_info.get('is_resource', False):
            return resources.get_icon(
                (thumbnail_info['folder'], thumbnail_info['name'])
            )
        else:
            return resources.get_icon(('icons.flow', 'object'))


class NoMatchingResultsItem(QtWidgets.QTreeWidgetItem):

    def __init__(self, tree):
        super(NoMatchingResultsItem, self).__init__(tree)
        self.setText(0, 'No matching results')


class ResultList(QtWidgets.QTreeWidget):

    def __init__(self, search_bar):
        super(ResultList, self).__init__()

        self.search_bar = search_bar
        self.session = search_bar.session
        self.header().hide()

        self.itemClicked.connect(self.on_result_clicked)

        self._active_result = None
    
    def refresh(self):
        self.clear()
        self.selectionModel().clearSelection()

        results = self.session.cmds.Search.query_project_index(
            self.search_bar.current_project(),
            self.search_bar.query_filter()
        )
        
        if results:
            for res in results:
                SearchResult(self, res)
            
            self._active_result = 0
            self.update_active_result(0)
        else:
            self._active_result = None
            NoMatchingResultsItem(self)
    
    def active_result(self):
        selected = self.selectedItems()
        
        if not selected or self._active_result is None:
            return None
        else:
            return selected[0]
    
    def update_active_result(self, index):
        self.clearSelection()
        self.setCurrentItem(self.topLevelItem(index), 0, QtCore.QItemSelectionModel.Select)
    
    def incr_active_result(self):
        if self._active_result is not None and self._active_result < self.topLevelItemCount() - 1:
            self._active_result += 1
            self.update_active_result(self._active_result)
    
    def decr_active_result(self):
        if self._active_result is not None and self._active_result > 0:
            self._active_result -= 1
            self.update_active_result(self._active_result)
    
    def on_result_clicked(self, item, column):
        self.search_bar.view.goto_request(item.goto_oid())
        self.search_bar.search_input.lineedit_input.clearFocus()
    
    def resizeEvent(self, event):
        # From https://stackoverflow.com/a/37724553
        height = 2 * self.frameWidth() # border around tree
        it = QtWidgets.QTreeWidgetItemIterator(self)

        while it.value() is not None:
            index = self.indexFromItem(it.value())
            height += self.rowHeight(index)
            it += 1

        self.parentWidget().parentWidget().resize(self.parentWidget().parentWidget().width(), height)
        super(ResultList, self).resizeEvent(event)


class ResultListWidget(QtWidgets.QWidget):
    
    def __init__(self, search_bar):
        super(ResultListWidget, self).__init__()

        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setMaximumHeight(200)

        self.result_list = ResultList(search_bar)
        lo = QtWidgets.QHBoxLayout()
        lo.addWidget(self.result_list)
        lo.setSpacing(0)
        lo.setContentsMargins(0, 0, 0, 0)
        self.setLayout(lo)

    def sizeHint(self):
        return QtCore.QSize(300, 200)


class ResultListDockWidget(QtWidgets.QDockWidget):

    def __init__(self, parent, search_bar):
        super(ResultListDockWidget, self).__init__(parent)

        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setFloating(True)
        # Make title bar invisible (https://doc.qt.io/qt-5/qdockwidget.html#appearance)
        self.setTitleBarWidget(QtWidgets.QWidget())

        self.result_list_widget = ResultListWidget(search_bar)
        self.setWidget(self.result_list_widget)

        self.hide()


class SearchInputLineEdit(QtWidgets.QLineEdit):

    def __init__(self, search_input):
        super(SearchInputLineEdit, self).__init__()
        self.search_input = search_input
        self.setPlaceholderText('Search...')

        # Install callbacks
        self.textChanged.connect(self.search_input.refresh_result_list)
        self.returnPressed.connect(self.search_input.goto_active_result)

    def resizeEvent(self, event):
        self.search_input.update_result_list_width(self.width())
    
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.search_input.result_list.setVisible(False)
            self.clearFocus()
        elif event.key() == QtCore.Qt.Key_Up:
            self.search_input.decr_active_result()
        elif event.key() == QtCore.Qt.Key_Down:
            self.search_input.incr_active_result()
        else:
            super(SearchInputLineEdit, self).keyPressEvent(event)
    
    def focusInEvent(self, event):
        self.search_input.result_list.setVisible(True)
        g = self.search_input.result_list.geometry()
        g.setTopLeft(self.mapToGlobal(self.geometry().bottomLeft()))
        self.search_input.result_list.setGeometry(g)
        self.search_input.update_result_list_width(self.width())
        super(SearchInputLineEdit, self).focusInEvent(event)
    
    def focusOutEvent(self, event):
        self.search_input.result_list.setVisible(False)
        super(SearchInputLineEdit, self).focusOutEvent(event)


class SearchInputWidget(QtWidgets.QWidget):

    def __init__(self, search_bar):
        super(SearchInputWidget, self).__init__()
        self.search_bar = search_bar

        self.lineedit_input = SearchInputLineEdit(self)
        self.result_list = ResultListDockWidget(self, search_bar)

        vlo = QtWidgets.QVBoxLayout()
        vlo.addWidget(self.lineedit_input)
        vlo.setSpacing(0)
        vlo.setContentsMargins(0, 0, 0, 0)
        self.setLayout(vlo)
    
    def update_result_list_width(self, w):
        self.result_list.resize(w, self.result_list.height())
    
    def refresh_result_list(self):
        self.result_list.result_list_widget.result_list.refresh()
    
    def goto_active_result(self):
        active = self.result_list.result_list_widget.result_list.active_result()
        
        if active is not None:
            self.search_bar.view.goto_request(active.goto_oid())
            self.lineedit_input.clearFocus()
    
    def incr_active_result(self):
        self.result_list.result_list_widget.result_list.incr_active_result()
    
    def decr_active_result(self):
        self.result_list.result_list_widget.result_list.decr_active_result()


class SearchBar(QtWidgets.QWidget):

    def __init__(self, parent, view, session):
        super(SearchBar, self).__init__(parent)
        self.view = view
        self.session = session
        
        self.combobox_projects = QtWidgets.QComboBox()
        self.search_input = SearchInputWidget(self)

        hlo = QtWidgets.QHBoxLayout()
        hlo.addWidget(self.combobox_projects)
        hlo.addWidget(self.search_input)
        hlo.setSpacing(2)
        hlo.setContentsMargins(2, 0, 2, 0)
        self.setLayout(hlo)

        self.refresh()
    
    def refresh(self):
        self.combobox_projects.insertItems(0, self.project_names())
    
    def current_project(self):
        return self.combobox_projects.currentText() or None
    
    def query_filter(self):
        return self.search_input.lineedit_input.text() or None
    
    def project_names(self):
        return self.session.cmds.Search.list_project_names()


class SearchFlowView(FlowView):

    def __init__(self, session, view_id=None, hidden=False, area=None, oid=None, root_oid=None):
        self.search_bar = None
        super(SearchFlowView, self).__init__(session, view_id=view_id, hidden=hidden, area=area, oid=oid, root_oid=root_oid)

    def build_top(self, top_parent, top_layout, header_parent, header_layout):
        super(SearchFlowView, self).build_top(top_parent, top_layout, header_parent, header_layout)
        self.search_bar = SearchBar(top_parent, self, self.session)
        top_layout.addWidget(self.search_bar)


class SearchFlowViewPlugin:
    """
    Custom Flow view.

    Will only be installed if no other view
    is registered under the "Flow" view type name.
    """

    @plugin(trylast=True)
    def install_views(session):
        if not session.is_gui():
            return

        type_name = SearchFlowView.view_type_name()
        if not session.has_view_type(type_name):
            session.register_view_type(SearchFlowView)
            session.add_view(type_name)
