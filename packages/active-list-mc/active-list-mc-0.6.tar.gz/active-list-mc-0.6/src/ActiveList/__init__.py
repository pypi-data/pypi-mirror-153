import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk


class TVColumn(gtk.TreeViewColumn):

    def __init__(self, ID, object_type, title="", width=0, background_column=None, renderer_type=None, alignment=0.0):
        self.ID = ID
        self.object_type = object_type
        self.title = title
        self.width = width
        self.background_column = background_column
        self.renderer_type = renderer_type
        self.alignment = alignment


class ActiveList(object):
    _columns = None

    def __init__(self, tree_view, **kwargs):

        column_type_list = []  # for creating the model
        totalWidth = 0

        # Loop through the columns and initialize the TreeView
        for column in self._columns:

            # Save the type for gtk.TreeStore creation
            column_type_list.append(column.object_type)
            # Is it visible?
            if column.renderer_type:
                # Renderer type is specified, i.e. it's a visible column
                # Create an instance of renderer_type
                _renderer = column.renderer_type()

                # Create the Column and set up suitable attributes
                col = gtk.TreeViewColumn(
                    column.title
                    , _renderer
                )
                col.set_sizing(gtk.TreeViewColumnSizing.FIXED)
                col.set_fixed_width(column.width)

                if isinstance(_renderer, gtk.CellRendererText):
                    col.add_attribute(_renderer, "text", column.ID)
                    # Set right-justified if requested, default is left
                    _renderer.set_property('xalign', column.alignment)
                elif isinstance(_renderer, gtk.CellRendererToggle):
                    self.toggle_renderer = _renderer  # so outer routine can connect to "toggled" signal
                    # GTK automatically sets the PROPERTIES activatable to True and active to False
                    # The ATTRIBUTES with the same names determine which column of the model (if any)
                    # is used to set the properties. Thus we don't need
                    #       col.add_attribute(_renderer, "activatable", column.ID)
                    # because we want to leave the property "activatable" set to True. However we do want ...
                    col.add_attribute(_renderer, "active", column.ID)
                    # ... because we want the property "active" to be set from the value in the column.
                    print(f"Column {column.ID}; Activatable is ", _renderer.get_activatable())
                    print(f"Column {column.ID}; Active is ", _renderer.get_active())

                col.add_attribute(_renderer, "cell-background", column.background_column)
                tree_view.append_column(col)
                totalWidth += col.get_fixed_width()

        # Create the gtk.TreeStore model to use with the TreeView
        self.model = gtk.ListStore(*column_type_list)
        tree_view.set_size_request(totalWidth, -1)
        self.treeselection = tree_view.get_selection()
        self.treeselection.set_mode(gtk.SelectionMode.SINGLE)

    @staticmethod
    def whence():   # ActiveList will be imported from package active-list-mc
        return 'active-list-mc'

