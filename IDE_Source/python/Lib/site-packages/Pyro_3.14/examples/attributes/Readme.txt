This test shows the possibility of direct attribute access.

Notice that the client no longer uses getter and setter methods,
it directly accesses the object's attributes by using normal
Python syntax.


Note that the nested attributes from the person object can only
work because the Person.py module (that contains the Person class)
is available to the client !!!  If the Person.py wasn't in this directory
(and hence, not available to the client) the client will crash
with an error such as "No module named Person")

