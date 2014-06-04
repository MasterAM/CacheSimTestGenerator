CacheSimTestGenerator
=====================

This utility is used for running the tests and gathering the data for the 3rd section of the exercise.

Installation
=

Clone the repository by using the following command:

    $ git clone https://github.com/MasterAM/CacheSimTestGenerator.git

A subdirectory with the relevant files will be created. CD into it

    $ cd CacheSimTestGenerator


On t2, switch to the appropriate branch:

    $ git checkout t2

See the Usage section for more details.

If there is an update to this script, you can get it by using:

    $ git pull origin master
    
or, on t2

    $ git pull origin t2

Requirements:
=


 - Python (tested on 2.7.x)
 - Matplotlib (v1.3.1 or newer) - a python plotting library (and more).

On t2 it creates the CSV file, which should allow easier comparison of results and easy generation of the graphs using a spreadsheet program.


Status
=
  
Currently, it generates 6 graphs with normalized values (relative to the highest result for integer data, such as the number of compulsory misses, while fractional data remains unchanged).  

The graphs are saved to a PDF file (vector form) and PNG files (raster).

Usage
=
    $ python Generator.py --graphs <prog> <inFile>
Generates the data for section 3. Give it the full paths, including file names. The CSV file will be created in the working directory.

Example usage:

    $ python Generator.py --graphs ../cachesim/cacheSim ../lbm.din

On t2, this will run the simulator with all of the configurations specified in section 3 and create a csv file called `results.csv` in the current directory.

On a system with Matplotlib 1.3.1+ installed, this will also generate various graphs that are much more elaborate than required.

Bugs
=
Since it is barely tested, I guess that bugs will be detected.  
Feel free to let me know on FB or email, or (if it means anything to you) send a pull request.
