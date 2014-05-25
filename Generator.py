from numpy.distutils.system_info import blas_src_info

__author__ = 'alon'

from sys import argv
import subprocess
import re
import csv

try:
    print 'Trying to load charting library...'
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.cm as cm
    from matplotlib.backends.backend_pdf import PdfPages
    pltAvailable = True
    print 'loaded.'
except ImportError:
    pltAvailable = False
    print 'not available. Will only export CSV. Install matplotlib to generate graphs.'

KB = 1024
MB = KB * KB
WORD = 4

class Generator:
    # prog = ''
    assoc = [1, 2, 4, 8, 16]
    bsizes = [8, 16, 32, 64]
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
    doPlot = True
    doCsv = True
    def __init__(self, prog, inputFile):
        self.prog = prog
        self.inFile = inputFile
    @staticmethod
    def convertLbm(path):
        with open(path+'/'+'lbm.din', "r") as infile, open(path+'/'+'lbm_fixed.din', "w") as outfile:
            for line in infile:
                outdata = line.split(' ')
                outfile.write(outdata[0] + ' ' + outdata[1]+'\n')

    @staticmethod
    def num(s):
        try:
            return int(s)
        except ValueError:
            return float(s)

    def generateGraphs(self):
        self.cssData = []
        self.graphData = []
        size = 64 * KB

        bsize = 16 * WORD
        for assoc in self.assoc:
            for unified in [False, True]:
                self.appendStats(unified, size, bsize, assoc)
        d1 = self.graphData
        self.graphData = []
        assoc = 4
        for bsize in [x * WORD for x in self.bsizes]:
            for unified in [False, True]:
                self.appendStats(unified, size, bsize, assoc)
        d2 = self.graphData

        if self.doPlot:
            fig1 = self.drawConfigurationGraphs(d1, 'assoc')
            fig2 = self.drawConfigurationGraphs(d2, 'bsize')
            try:
                with PdfPages('output.pdf') as pdf:
                    pdf.savefig(figure=fig1)
                    pdf.savefig(figure=fig2)
                    # pdf.savefig()
            except AttributeError:
                print 'Make sure that you have matplotlib 1.3.1 or newer'

            plt.savefig('assoc.png', figure=fig1)
            plt.savefig('bsize.png', figure=fig2)

        if self.doCsv:
            self.writeCSV()

    def writeCSV(self, filename='results.csv'):
        fields = self.graphData[0]
        fields = fields[0].keys() + fields[1].keys()
        with open(filename, 'wb') as csvfile:
            dataWriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            # dataWriter.writeheader()
            dataWriter.writerow(fields)
            for row in self.cssData:
                dataWriter.writerow(row)

    def appendStats(self, unified, size, bsize, assoc):
        results = self.runTest(unified, size, bsize, assoc)
        v = {'unified': unified, 'size': size, 'bsize': bsize, 'assoc': assoc}
        self.graphData.append((v, results))
        self.cssData.append(v.values() + results.values())


    def runTest(self, unified, size, bsize, assoc):
        progArgs = [self.prog, self.inFile]
        if unified:
            progArgs.append('--unified')
        progArgs.extend(['--size', '{0}'.format(size)])
        progArgs.extend(['--bsize', '{0}'.format(bsize)])
        progArgs.extend(['--assoc', '{0}'.format(assoc)])

        cmd = ' '.join(progArgs)
        print 'running: {0}'.format(cmd)

        output = subprocess.Popen(progArgs,
                                  stdout=subprocess.PIPE,
                                  stdin=subprocess.PIPE, #windows issue fix
                                  stderr=subprocess.PIPE).communicate()[0]
        print output
        data = re.match(self.rx, output)
        if data is None:
            print 'data does not match the expected format'
            return
        results = {k: Generator.num(v) for k,v in data.groupdict().iteritems()}
        return results
    def drawConfigurationGraphs(self, graphData, variable):
        data = [v[1] for v in graphData]
        dataConfigs = [v[0] for v in graphData]
        maxVals = self.getMaxVals(data)
        #is the data a float (percent) or int (absolute value)
        types = {k: isinstance(v, int) for k,v in data[0].items()}
        keys = data[0].keys()
        legends = ['{0}: {1}, unified: {2}'.format(variable, item[variable], item['unified']) for item in dataConfigs]
        relativeVals = [{k: v*100/maxVals[k] if types[k] else v for k,v in item.items()} for item in data]
        N = len(keys)
        Ndata = len(data)
        Fdata = float(Ndata)
        ind = np.arange(N)
        width = 0.35
        fig, ax = plt.subplots()
        colors = [cm.hot(i/Fdata,1) for i in np.arange(len(data))]
        rects = []
        legends = ['{0}: {1}, unified: {2}'.format(variable, item[variable], item['unified']) for item in dataConfigs]
        i = 0
        for item in relativeVals:
            rects.append(ax.bar([idx*(Ndata+1)*width + i*width for idx in ind], item.values(), width, color=colors[i]))
            i = i+1
        ax.set_xticks([idx*width*(Ndata+1) + Ndata*width/2 for idx in ind])
        ax.set_xticklabels(keys, rotation=30)
        plt.ylabel('Relative Values')
        plt.title('Performance by {0}'.format('bwidth'))
        plt.legend( (rects[i][0] for i in np.arange(Ndata)), legends, loc='upper center',
                    bbox_to_anchor=(0.5, 1.05), ncol=3, fancybox=True, shadow=True)
        return fig


    def getMaxVals(self, data):
        maxVals = {}
        for k in data[0].keys():
            maxVals[k] = max([v[k] for v in data])
        return maxVals

if __name__ == '__main__':
    if len(argv) == 3 and argv[1] == '--fix':
        Generator.convertLbm(argv[2])
    elif len(argv) == 4 and argv[1] == '--graphs':
        gen = Generator(argv[2], argv[3])
        #for test only
        gen.assoc = [2]
        gen.bsizes = [8]

        #end test
        gen.doPlot = pltAvailable
        # gen.generateGraphs()
        gen.generateGraphs()
    else:
        print '{0}: Saves you some precious time and frustration by running some tests and generating some graphs.'.format(argv[0])
        print 'usage:'
        print '{0} --fix <path to lbm.idn without the file name itself>: removes the third argument from each line'.format(argv[0])
        print '{0} --graphs <prog> <inFile>: generates the graphs for q3'.format(argv[0])
        # for bsize in [8, 16]*WORD:
