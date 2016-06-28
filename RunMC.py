from subprocess import Popen,STDOUT,DEVNULL
import glob,re,random,os
import logging,pickle,sys
import multiprocessing as mp
import argparse
from itertools import islice

class MCRunner():

    def __init__(self,pArgs):
        maxProcs = mp.cpu_count() - 1 ) * 2
        if pArgs.workers > maxProcs
            self.workers = maxProcs
        else:
            self.workers = pArgs.workers
        self.l1path = pArgs.ifile
        self.l2MainPath = pArgs.opath
        self.silParFi = pArgs.prsil
        self.noiParFi = pArgs.prnoi
        self.itNum = pArgs.mcrns
        self.filesProcessed = 0
        self.l2SilFname = None
        self.l2NoiPath = None
        self.basename
        self.__GetL2FilePath()

    def __GetL2FilePath(self):
        pattern = '(S[0-9]+).L1A'
        basename = re.findall(pattern,self.l1path)[0]
        l2path = os.path.join(self.l2MainPath,basename)
        if not os.path.exists(l2path):
            os.makedirs(l2path)
        self.l2SilFname = os.path.join(l2path,basename+'_silent.L2')
        self.l2NoiPath = os.path.join(l2path,'Noisy/')
        if not os.path.exists(self.l2NoiPath):
            os.makedirs(self.l2NoiPath)
        self.basename = basename

    def GetCmdList(self):
        '''Generates cmdList for subprocess calls'''
        cmdList = []
        cmdBase = 'l2gen ifile=%s ofile=' % self.l1path
        if not os.path.exists(l2fs):
            # silent L2 does not exist, add it to the tasklist
            cmd = cmdBase + '%s par=%s' %(self.l2SilFname, self.silParFi)
            cmdList.append(cmd)
        for it in range self.itNum:
            l2f = '%s_noisy_%d.L2' %(self.basename, it+1)
            ofile = os.path.join(self.l2NoiPath, l2f)
            if os.path.exists(ofile):
                continue
            cmd = cmdBase + '%s par=%s' %(ofile, self.noiParFi)
            cmdList.append(cmd)
        return cmdList

    def Runner(self,cmdList,verbose=false):
        '''
        Creates a generator for processes then slices by the number of
        concurrent processes allowed.
        cmdList is a list containing the l2gen command line for each process.
        '''
        processes = (Popen(cmd,shell=True) for cmd in cmdList)
        runningProcs = list(islice(processes,self.workers)) # start new processes
        if verbose: # get ready to record log
            j = 0
        while runningProcs:
            for i,process in enumerate(runningProcs):
                if process.poll() is not None: # process has finished
                    if verbose: # add entry to log
                        with open('MCLog.dat','a') as f:
                            print('%s -- completed ' % cmdList[j],file=f,flush=True)
                            j += 1
                    runningProcs[i] = next(processes,None) # start new process
                    if runningProcs[i] is None: # no new processes
                    del runningProcs[i]
                    break

class Namespace():
    '''
    Class to replace command line argument parser for IPython calls.
    Usage: args=Namespace(ifile='',opath='',prsil='',prnoi='')
    '''

    def __init__(self,**kwargs):
        self.__dict__.update(kwargs)

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
    parser.add_argument('-w','--workers',help='process # to allocate',
                        type=int,default=1)
    parsedArgs = parser.parse_args(args)
    #Init MCRUnner Object, passing the args
    mcr = MCRunner(parsedArgs)
    # Process Silent file
    taskList = mcr.GetCmdList()
    mcr.Runner

if __name__ == '__main__':
    Main(sys.argv[1:])
