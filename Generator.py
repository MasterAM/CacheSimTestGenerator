__author__ = 'alon'

from sys import argv
import subprocess
import re

KB = 1024
MB = KB * KB
WORD = 4

class Generator:
    # prog = ''
    rx = "Global Hit Rate: (?P<GlobalHR>\d+\.\d+)\n" \
         "Instruction Hit Rate: (?P<InstructionHR>\d+\.\d+)\n" \
         "Load Hit Rate: (?P<LoadHR>\d+\.\d+)\n" \
         "Store Hit Rate: (?P<StoreHR>\d+\.\d+)\n" \
         "Number of memory accesses: (?P<nAccess>\d+)\n" \
         "Number of misses: (?P<nMisses>\d+)\n" \
         "Number of loads: (?P<nLoads>\d+)\n" \
         "Number of stores: (?P<nStores>\d+)\n" \
         "Number of instruction read: (?P<nInstructionReads>\d+)\n" \
         "Compulsory misses: (?P<Compulsory>[-+]?\d+)\n" \
         "Capacity misses: (?P<Capacity>\d+)\n" \
         "Conflict misses: (?P<Conflict>\d+)\n" \
         "Compulsory miss percentage: (?P<CompulsoryR>\d+\.\d+)\n" \
         "Capacity miss percentage: (?P<CapacityR>\d+\.\d+)\n" \
         "Conflict miss percentage: (?P<ConflictR>\d+\.\d+)"
    cmd = 'cacheSim'
    def __init__(self, prog, inputFile):
        self.prog = prog
        self.inFile = inputFile
    @staticmethod
    def convertLbm(path):
        with open(path+'/'+'lbm.din', "r") as infile, open(path+'/'+'lbm_fixed.din', "w") as outfile:
            for line in infile:
                outdata = line.split(' ')
                outfile.write(outdata[0] + ' ' + outdata[1]+'\n')

    def generateGraphs(self):
        size = 64 * KB
        for unified in [False, True]:
            bsize = 16 * WORD
            for assoc in [1, 2, 4, 8, 16]:
                self.runTest(unified, size, bsize, assoc)
            for bsize in [8, 16, 32, 64]*WORD:
                self.runTest(unified, size, bsize, assoc)


    def runTest(self, unified, size, bsize, assoc):
        progArgs = [self.prog, self.inFile]
        if unified:
            progArgs.append('--unified')
        progArgs.extend(['--size', '{0}'.format(size)])
        progArgs.extend(['--bsize', '{0}'.format(bsize)])
        progArgs.extend(['--assoc', '{0}'.format(assoc)])

        cmd = ' '.join(progArgs)
        print 'running: {0}'.format(cmd)

        output = subprocess.Popen(progArgs, stdout=subprocess.PIPE).communicate()[0]
        print output
        data = re.match(self.rx, output)
        if data is None:
            print 'data does not match the expected format'
            return
        print data.groupdict()


if __name__ == '__main__':
    if len(argv) == 3 and argv[1] == '--fix':
        Generator.convertLbm(argv[2])
    elif len(argv) == 4 and argv[1] == '--graphs':
        gen = Generator(argv[2], argv[3])
        # gen.generateGraphs()
        gen.runTest(False, 512, 16, 4)
    else:
        print '{0}: Saves you some precious time and frustration by running some tests and generating some graphs.'.format(argv[0])
        print 'usage:'
        print '{0} --fix <path to lbm.idn without the file name itself>: removes the third argument from each line'.format(argv[0])
        print '{0} --graphs <prog> <inFile>: generates the graphs for q3'.format(argv[0])
