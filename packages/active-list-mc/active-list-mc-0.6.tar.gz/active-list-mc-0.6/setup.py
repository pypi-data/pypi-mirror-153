# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ActiveList']

package_data = \
{'': ['*']}

install_requires = \
['PyGObject>=3.42.0,<4.0.0', 'tomlkit<1.0.0']

setup_kwargs = {
    'name': 'active-list-mc',
    'version': '0.6',
    'description': 'Facade to simplify usage of Gtk.TreeView',
    'long_description': 'This module is a Facade to simplify usage of the\nGtk.TreeView with Gtk.ListStore model.\n\nThe module creates a list of Gtk.TreeViewColumn\'s and initialises it\nwith the required column specifications and cell renderers.\n\nThe information as to the required columns and cell renderers\nis specified as a list of tuples in the calling module.\n\n\nThe following excerpts from my book "Programming Python with Gtk and SQLite" will illustrate.\n# 4.21.2  The example data\n\nLet\'s imagine we want to display some data selected from the Chinook example database (which will be discussed in Part 3). We want it to look as below.\n\n![](./_images/Screenshot_Employee_List.png)\nThe data will be presented in a separate file, *employees.csv*, to avoid any questions of database access at this stage. (Note: csv stands for "Comma Separated Variables".) \n\nYou will notice there are more data items in the file than are shown above. This is deliberate; the columns Address,City,State,Country etc. from the example database are present in the .csv file but are ignored for simplicity and to show that we aren\'t forced to display all the data.\n\nAlso note the fourth column "ReportsTo" is a numeric reference to the record for the named person\'s supervisor. This will come in handy to illustrate the TreeStore model later.\n\n# 4.21.5  The ActiveList module\n\nMy ActiveList module was written to encapsulate the setting up of the tree model and treeview to avoid having to re-write this code for every new application, and repeat very similar code for each treeview column. \n\nThe ActiveList module (*ActiveList.py*) is provided under the MIT license.\n\nIf you import this module, you need only write a specification of the required columns, like this.\n```py\nfrom ActiveList import TVColumn, ActiveList\n```\n```py\n# TreeModel column ID\'s\nCOL_SEQ = 0\nCOL_LAST = 1        # LastName\nCOL_FIRST = 2       # FirstName\nCOL_TITLE = 3       # Title\nCOL_BOSS = 4        # ReportsTo\nCOL_BORN = 5        # Birth Date\nCOL_HIRED = 6       # Hire Date\nCOL_SORT = 7        # Sort Key - not used\nCOL_KEY = 8         # Database Key - not used\n\n\n#...or (easier to modify correctly)\nCOL_SEQ,\\\nCOL_LAST,\\\nCOL_FIRST,\\\nCOL_TITLE,\\\nCOL_BOSS,\\\nCOL_BORN,\\\nCOL_HIRED,\\\nCOL_SORT,\\\nCOL_KEY = range(9)\n\nclass TV(ActiveList):\n    # The ActiveList defines the columns for the treeview\n    _columns = [\n        # We\'ll use column 0 of each row to specify a background colour for\n        # the row. This is not compulsory but I found it a useful convention.\n        # This column is not displayed.\n        TVColumn(COL_SEQ, str)\n\n        # The following columns are obtained from the data source\n        # and displayed in the treeview.\n\n        # column 1 (LastName)\n        , TVColumn(COL_LAST, str, "LastName", 75, COL_SEQ, gtk.CellRendererText)\n        # column 2 (FirstName)\n        , TVColumn(COL_FIRST, str, "FirstName", 75, COL_SEQ, gtk.CellRendererText)\n        # column 3 (Title)\n        , TVColumn(COL_TITLE, str, "Title", 93, COL_SEQ, gtk.CellRendererText)\n        # column 4 (Reports To)\n        , TVColumn(COL_BOSS, str, "ReportsTo", 75, COL_SEQ, gtk.CellRendererText)\n        # column 5 (BirthDate)\n        , TVColumn(COL_BORN, str, "Born", 70, COL_SEQ, gtk.CellRendererText)\n        # column 6 (HireDate)\n        , TVColumn(COL_HIRED, str, "Hired", 70, COL_SEQ, gtk.CellRendererText)\n\n        # The following column is used but not displayed\n        # KEY - e.g. database key to identify a record for UPDATE etc\n        , TVColumn(COL_KEY, int)\n    ]\n```\nThe parameters to TVColumn are\n* tree model column ID\n* column data type\n* column heading\n* column width (pixels)\n* model column to specify this column\'s background colour\n* cell renderer type\n* column justification (0 = left (default), 0.5 = centre, 1 = right)\n\nActiveList sets up the treeview which you supply with the columns and cell renderers you specify and returns the resulting "column_type_list" which can be used to create the treeview\'s model.\n```py\nmy_TV = TV(self.treeview)   # an instance of our descendant of ActiveList\n                            # which defines the columns of the treeview\nmy_TV.model = gtk.ListStore(*my_TV.column_type_list)\nself.treeview.set_model(my_TV.model)\n```\nIf the column should be present in the model but not displayed in the view, only the first two parameters should be given. This is useful for example to keep a database key for every record in the model so we could update or delete the record if required.\n\nYou can specify any number of columns which can be used and/or displayed as you wish. You can use this for "future-proofing" e.g. specify columns for which the display code is not written yet.\n\nThe parameter "model column to specify this column\'s background colour" may need further explanation. The intention is to allow rows to have alternating background colours to help with reading the data, as in the section on "The example data". This could have been implemented within ActiveList, but I have just provided the framework for doing it yourself, to give users the choice.\n\nI understand that some users will want this feature, but prefer it to be provided by their desktop theme. I might have gone that route but couldn\'t find a theme which worked.',
    'author': 'Chris Brown',
    'author_email': 'chris@marcrisoft.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
