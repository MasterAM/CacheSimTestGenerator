CacheSimTestGenerator
=====================
This utility is intended for 2 tasks:

The trivial one is fixing the format of the lbm.idn file (remove a redundant symbol from each line).
The less trivial one is running the tests and generating graphs for the 3rd section of the exercise.

Installation
=

Clone the repository by using the following command:

    $ git clone https://github.com/MasterAM/CacheSimTestGenerator.git

A subdirectory with the relevant files will be created.

On t2, switch to the appropriate branch:

    $ git checkout t2

Requirements:
=

 - Python (tested on 2.7.x)
 - Matplotlib (v1.3.1 or newer) - a python plotting library (and more).
 
Currently tested with Ububntu Linux, not with Windows (I recall Matplotlib installation was not that easy on Windows).

On t2 it creates the CSV files only, which should allow easier comparison of results and easy generation of the graphs using a spreadsheet program.


Status
=
 
Currently, it generates 2 graphs with normalized values (relative to the highest result for integer data and to 100% for fractional data).  
The graphs are saved to a PDF file (vector form) and 2 PNG files (raster).

Usage
=
    $ python Generator.py --fix path to lbm.idn without the file name itself>
Removes the third element from each line of `lbm.idn`. No longer relevant, as the course staff published a fixed version.

    $ python Generator.py --graphs <prog> <inFile>
Generates the graphs for section 3. Give it the full paths, including file names. Data will be generated in working directory.

Example usage:

    $ python Generator.py --graphs ../cachesim/cacheSim ../lbm.din

On t2, this will run the simulator with all of the required configuration create a csv file called `results.csv` in the current directory.
On a system with Matplotlib 1.3.1+ installed, this will also generate graphs that are much more elaborate than required.

Bugs
=
Since it is barely tested, I guess that bugs will be detected.  
Feel free to let me know on FB or email, or (if it means anything to you) send a pull request.
