import sys
from MedatechUK.mLog import mLog
import os
from os import listdir
from os.path import exists, isfile, join
import sys
import subprocess

#region Command Line Arguments            
class clArg():

    def __init__(self, **kwargs):
        log = mLog()
        self._kw = {}
        self._a = []
        last = None
        if kwargs.__contains__("args"):
            sys.argv = kwargs["args"]            
        for arg in sys.argv[:0:-1] :
            if arg[0] in {'-', '/'} :                
                while arg[0] in {'-', '/'} :
                    arg = arg[1:]
                self._kw[arg] = last
                last = None
            else:
                if last != None:
                    self._a.append(last)
                last = arg
        if last != None:
            self._a.append(last)

        for k in self._kw:
            log.logger.debug("Key: [{}] = {}".format(k , self._kw[k]))
        for a in self._a:
            log.logger.debug("Arg [{}]".format( a ) )

    def kwargs(self):        
        return self._kw
    
    def args(self):
        return self._a[::-1]
    
    def byName(self, key):
        for k in self._kw:
            for i in key:
                if k.upper() == i.upper():
                    return self._kw[k]
        return None

#endregion

#region folder watcher
class folderWatch():
    
    def __init__(self , **kwargs):
        
        self.log = mLog()
        
        #region cl validation
        if not kwargs.__contains__("folder"):
            self.log.logger.critical("Folder not specified.")
            raise NameError("Folder not specified.")
        if not kwargs.__contains__("handler"):
            self.log.logger.critical("Handler not specified.")
            raise NameError("Handler not specified.")            
        if not kwargs.__contains__("env"):
            self.log.logger.critical("Environment not specified.")
            raise NameError("Environment not specified.")                        
        if not exists(kwargs['folder']):
            self.log.logger.critical("Folder {} not found.".format(kwargs['folder']))
            raise NameError("Folder {} not found.".format(kwargs['folder']))
        if not exists(kwargs['handler']):
            self.log.logger.critical("handler [{}] not found.".format(kwargs['handler']))
            raise NameError("handler [{}] not found.".format(kwargs['handler']))

        #endregion

        #region Set local properties from commandline
        self._folder = kwargs['folder'].rstrip('\\') + "\\"
        self._handler = kwargs['handler']
        self._env = kwargs['env']        
        
        if not kwargs.__contains__('ext'):
            self._ext = None
            self.log.logger.info("fWatch folder {} with handler {} in env {}.".format(self._folder  , self._handler , self._env ))
        else :            
            self._ext = kwargs['ext']        
            self.log.logger.info("fWatch folder {} for {} with handler {} in env {}.".format(self._folder  ,self._ext, self._handler , self._env ))

        #endregion

    def EnvStr(self):
        return "-e {}".format(self._env)

    def filePath(self,f):
        return "{}{}".format(self._folder , f)

    def CMD(self, cwd, f):
        return ( 
            "{} {} {} {}".format (
                self._handler ,
                self.EnvStr() ,
                "-cwd {}".format(cwd) ,
                self.filePath(f)        
            )
        )

    def isFileLocked(self, filePath):
        '''
        Checks to see if a file is locked. Performs three checks
            1. Checks if the file even exists
            2. Attempts to open the file for reading. This will determine if the file has a write lock.
                Write locks occur when the file is being edited or copied to, e.g. a file copy destination
            3. Attempts to rename the file. If this fails the file is open by some other process for reading. The 
                file can be read, but not written to or deleted.
        @param filePath:
        '''
        if not (os.path.exists(filePath)):
            return False
        try:
            f = open(filePath, 'r')
            f.close()
        except IOError:
            return True

        lockFile = filePath + ".lckchk"
        if (os.path.exists(lockFile)):
            os.remove(lockFile)
        try:
            os.rename(filePath, lockFile)
            # sleep(1)
            os.rename(lockFile, filePath)
            return False
        except WindowsError:
            return True

    def files(self):
        onlyfiles = [f for f in listdir(self._folder) if isfile(join(self._folder, f))
            and not self.isFileLocked(self._folder + '\\' + f)]
        if self._ext == None :
            return onlyfiles
        else :
            return [f for f in onlyfiles 
                if os.path.splitext(f)[1].lstrip('.').upper()==self._ext.lstrip('.').upper()
                    and not self.isFileLocked(self._folder + '\\' + f)]
    
    def check(self, cwd):
        for f in self.files():  
            self.log.logger.info("Found file {}.".format(self.filePath(f))) 
            self.log.logger.info(               
                "shell: {}".format(self.CMD(cwd , f))
            )         
            subprocess.call(
                self.CMD(cwd , f)
                , shell=False
            )
            self.log.logFile(self.filePath(f))

#endregion

#region Examples
if __name__ == '__main__' :

    l = mLog()
    l.start( "C:\pyedi", "DEBUG" )
    l.logger.debug("Starting {}".format(__file__)) 

    ## Get command line arguments
    arg = clArg()
    #print(arg.kwargs())
    #print(arg.args()[0])
    #print(arg.byName(['arg1']))

    ## Watch a folder
    fs = folderWatch(
        folder="M:\\python\\apy\\SolidWorks\\" , 
        handler="M:\\python\\apy\\solidworks.exe" , 
        env="wlnd" , 
        ext="xml"
    )
    fs.check("C:\\pyedi")

#endregion    