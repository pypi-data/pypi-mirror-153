######################################################
## si@medatechuk.com
## 30/10/21
## https://github.com/MedatechUK/Medatech.APY
## 
## Logging class
## https://docs.python.org/3/howto/logging.html
##
## Usage: Start the Logger: !!USE ONCE!! in entry file
## from MedatechUK.mLog import mLog
##
##      # Creates a log reference to the running file
##        log = mLog()
##      # Start the Logger: !!USE ONCE!! in entry file
##        log.start( os.path.dirname(__file__), "DEBUG" )
##
## Usage: 
## from MedatechUK.mLog import mLog
##
##      # Creates a log reference to the running file
##        log = mLog()
##      # Write to the log
##        log.logger.info("Hello test!")

import logging
import inspect
from datetime import datetime
import os
from os.path import exists
import shutil

class mLog():

    ## Ctor
    def __init__(self):  
        
        ## Build stack trace of caller frame             
        tree = [] 
        previous_frame = inspect.currentframe().f_back
        (filename) = inspect.getframeinfo(previous_frame)        
        tree.append(os.path.basename(filename.filename))

        previous_frame = previous_frame.f_back        
        while previous_frame and os.path.basename(filename.filename)!='runpy.py':
            (filename) = inspect.getframeinfo(previous_frame)        
            if os.path.basename(filename.filename) != tree[-1] and os.path.basename(filename.filename)!='runpy.py':
                tree.append(os.path.basename(filename.filename))
            previous_frame = previous_frame.f_back
        
        t = tree[-1]
        for i in range(len(tree)-2, -1 , -1):
            t = "{} > {}".format(t , tree[i] )

        ## Start the logger with stack trace %(name)s
        self.logger = logging.getLogger(t)

    def start(self, path , level):        
        ## Set the Log location
        now = datetime.now() # current date and time
        fn = '{}\log\{}-{}\{}.log'.format(
                path , 
                now.strftime("%Y") , 
                now.strftime("%m"), 
                now.strftime("%y%m%d")
            )
        try:
            os.makedirs(os.path.dirname(fn),exist_ok=True)
        except OSError as e:
            raise
            
        ## Set the configuration for the log
        logging.basicConfig(
            filename= fn, 
            encoding='utf-8', 
            format='%(asctime)s %(levelname)s %(name)s %(message)s', datefmt='%H:%M:%S',
            level=getattr(logging, level.upper())
        )        

    def logFile(self , f):
        if not exists(f):
            self.logger.critical("Failed to log file: {}".format(f))

        else:
            now = datetime.now() # current date and time
            try:
                fn = '{}\\{}\\'.format(
                    os.path.dirname(logging.root.handlers[0].baseFilename).rstrip("\\") ,  
                    now.strftime("%d")
                )            
                os.makedirs(os.path.dirname(fn),exist_ok=True)

                fi = f.split("\\")[-1].split(".")[0]
                ex = f.split("\\")[-1].split(".")[1]
                newf = "{}.{}".format(fi , ex)

                if exists("{}\\{}".format(fn , newf)):
                    i = 1
                    while exists("{}\\{}-{}.{}".format(fn , fi , i , ex)):
                        i += 1
                
                    newf = "{}-{}.{}".format(fi , i , ex)

                self.logger.info("Moving file from {} to {}".format(f , "{}\\".format(fn)))
                shutil.move(f, "{}\\{}".format(os.path.dirname(f).rstrip("\\"), newf))
                shutil.move("{}\\{}".format(os.path.dirname(f).rstrip("\\") , newf), "{}\\".format(fn) )

            except OSError as e:
                self.logger.critical("Error logging file: {}".format(str(e)))                
