This module is a Facade to simplify usage of the
Gtk.TreeView with Gtk.ListStore model.

The module creates a list of Gtk.TreeViewColumn's and initialises it
with the required column specifications and cell renderers.

The information as to the required columns and cell renderers
is specified as a list of tuples in the calling module.


The following excerpts from my book "Programming Python with Gtk and SQLite" will illustrate.
# 4.21.2  The example data

Let's imagine we want to display some data selected from the Chinook example database (which will be discussed in Part 3). We want it to look as below.

![](./_images/Screenshot_Employee_List.png)
The data will be presented in a separate file, *employees.csv*, to avoid any questions of database access at this stage. (Note: csv stands for "Comma Separated Variables".) 

You will notice there are more data items in the file than are shown above. This is deliberate; the columns Address,City,State,Country etc. from the example database are present in the .csv file but are ignored for simplicity and to show that we aren't forced to display all the data.

Also note the fourth column "ReportsTo" is a numeric reference to the record for the named person's supervisor. This will come in handy to illustrate the TreeStore model later.

# 4.21.5  The ActiveList module

My ActiveList module was written to encapsulate the setting up of the tree model and treeview to avoid having to re-write this code for every new application, and repeat very similar code for each treeview column. 

The ActiveList module (*ActiveList.py*) is provided under the MIT license.

If you import this module, you need only write a specification of the required columns, like this.
```py
from ActiveList import TVColumn, ActiveList
```
```py
# TreeModel column ID's
COL_SEQ = 0
COL_LAST = 1        # LastName
COL_FIRST = 2       # FirstName
COL_TITLE = 3       # Title
COL_BOSS = 4        # ReportsTo
COL_BORN = 5        # Birth Date
COL_HIRED = 6       # Hire Date
COL_SORT = 7        # Sort Key - not used
COL_KEY = 8         # Database Key - not used


#...or (easier to modify correctly)
COL_SEQ,\
COL_LAST,\
COL_FIRST,\
COL_TITLE,\
COL_BOSS,\
COL_BORN,\
COL_HIRED,\
COL_SORT,\
COL_KEY = range(9)

class TV(ActiveList):
    # The ActiveList defines the columns for the treeview
    _columns = [
        # We'll use column 0 of each row to specify a background colour for
        # the row. This is not compulsory but I found it a useful convention.
        # This column is not displayed.
        TVColumn(COL_SEQ, str)

        # The following columns are obtained from the data source
        # and displayed in the treeview.

        # column 1 (LastName)
        , TVColumn(COL_LAST, str, "LastName", 75, COL_SEQ, gtk.CellRendererText)
        # column 2 (FirstName)
        , TVColumn(COL_FIRST, str, "FirstName", 75, COL_SEQ, gtk.CellRendererText)
        # column 3 (Title)
        , TVColumn(COL_TITLE, str, "Title", 93, COL_SEQ, gtk.CellRendererText)
        # column 4 (Reports To)
        , TVColumn(COL_BOSS, str, "ReportsTo", 75, COL_SEQ, gtk.CellRendererText)
        # column 5 (BirthDate)
        , TVColumn(COL_BORN, str, "Born", 70, COL_SEQ, gtk.CellRendererText)
        # column 6 (HireDate)
        , TVColumn(COL_HIRED, str, "Hired", 70, COL_SEQ, gtk.CellRendererText)

        # The following column is used but not displayed
        # KEY - e.g. database key to identify a record for UPDATE etc
        , TVColumn(COL_KEY, int)
    ]
```
The parameters to TVColumn are
* tree model column ID
* column data type
* column heading
* column width (pixels)
* model column to specify this column's background colour
* cell renderer type
* column justification (0 = left (default), 0.5 = centre, 1 = right)

ActiveList sets up the treeview which you supply with the columns and cell renderers you specify and returns the resulting "column_type_list" which can be used to create the treeview's model.
```py
my_TV = TV(self.treeview)   # an instance of our descendant of ActiveList
                            # which defines the columns of the treeview
my_TV.model = gtk.ListStore(*my_TV.column_type_list)
self.treeview.set_model(my_TV.model)
```
If the column should be present in the model but not displayed in the view, only the first two parameters should be given. This is useful for example to keep a database key for every record in the model so we could update or delete the record if required.

You can specify any number of columns which can be used and/or displayed as you wish. You can use this for "future-proofing" e.g. specify columns for which the display code is not written yet.

The parameter "model column to specify this column's background colour" may need further explanation. The intention is to allow rows to have alternating background colours to help with reading the data, as in the section on "The example data". This could have been implemented within ActiveList, but I have just provided the framework for doing it yourself, to give users the choice.

I understand that some users will want this feature, but prefer it to be provided by their desktop theme. I might have gone that route but couldn't find a theme which worked.