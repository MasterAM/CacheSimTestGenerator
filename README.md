CacheSimTestGenerator
=====================
This utility is intended for 2 tasks:

The trivial one is fixing the format of the lbm.idn file (remove a redundant symbol from each line).
The less trivial one is running the tests and generating graphs for the 3rd section of the exercise.

Requirements:
=

 - Python (tested on 2.7.x)
 - Matplotlib (v1.3.1 or newer) - a python plotting library (and more).
 
Currently tested with Ububntu Linux, not with Windows (I recall Matplotlib installation was not that easy on Windows).
 
Not tested on T2. Let me know how it goes.


Status
=
 
Currently, it generates 2 graphs with normalized values (relative to the highest result for integer data and to 100% for fractional data).  
The graphs are saved to a PDF file (vector form) and 2 PNG files (raster).

Usage
=
    $ Generator.py --fix path to lbm.idn without the file name itself>
Removes the third element from each line of `lbm.idn`

    $ Generator.py --graphs <prog> <inFile>
Generates the graphs for section 3. Give it the full paths, including file names. Data will be generated in working directory.

Bugs
=
Since it is barely tested, I guess that bugs will be detected.  
Feel free to let me know on FB or email, or (if it means anything to you) send a pull request.
