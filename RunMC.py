from subprocess import Popen,PIPE,STDOUT
import glob,re,random,os
import logging,pickle,sys
import multiprocessing
import argparse

class MCRunner():

    def __init__(self,pArgs):
        self.workers = (multiprocessing.cpu_count() - 1 ) * 2
        self.l1path = pArgs.ifile
        self.l2MainPath = pArgs.opath
        self.silParFi = pArgs.prsil
        self.noiParFi = pArgs.prnoi
        self.itNum = pArgs.mcrns
        self.filesProcessed = 0
        self.l2SilFname = None
        self.l2NoiPath = None
        self.__GetL2FilePath()

    def ProcessFiles(self):
        '''manages MC file processing'''

        pass

    def _ProcessSilentFile(self):
        pass

    def _ProcessNoisyFile(self):
        pass

    def __GetL2FilePath(self):
        pattern = '(S[0-9]+).L1A'
        basename = re.findall(pattern,self.l1path)[0]
        l2path = os.path.join(self.l2MainPath,basename)
        self.l2SilFname = os.path.join(l2path,basename+'_silent.L2')
        self.l2NoiPath = os.path.join(l2path,'Noisy/')

def Main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--ifile',help='l1a input file',
                        type=str,required='True')
    parser.add_argument('-o','--opath',help='l2 output main path',
                        type=str,required='True')
    parser.add_argument('-s','--prsil',help='silent param. file',
                        type=str,required='True')
    parser.add_argument('-n','--prnoi',help='noisy param. file',
                        type=str,required='True')
    parser.add_argument('-m','--mcrns',help='number of MC iterations',
                        type=int,default=1000)
    parsedArgs = parser.parse_args(args)
    #Init MCRUnner Object, passing the args
    mcr = MCRunner(parsedArgs)
    # Process Silent file
    mcr.ProcessFiles()

if __name__ == '__main__':
    Main(sys.argv[1:])
