## A simple polygon forex aggregate library using Max Christ’s code

# this is only meant for a class project. 

This library is capable of collecting currency exchange rate from polygon every second and then aggregate every six minutes of data
into a single table entry. The condensed data then can be used to do data processing on top of it.

The main loop will continuously collect data for 24 Hours with 10 preset currency exchanges.

To use this, simply
```commandline
pip install polygon_forex_aggregate
```

and in your main code, do
``` python
from polygon_forex_aggregate import *
```

I know this is not the best way to import a package, however, this is the limitation of the code where you need to import everything.

This project uses sqlite as the database since it doesn't require a server. 
sqlalchemy is used to interface with the sqlite files.
