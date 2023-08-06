#!/usr/bin/python
#-*-coding:utf-8-*-
import logging.handlers
import os
import time
LOGGER_STANDARD = None
LOGGER_DMESG = None


class Logger(object):
    """Class provides methods to perform logging."""
    m_logger = None
    log_path = None

    def __init__(self, opts, logfile, myname):
        """Set the default logging path."""
        self.opts = opts
        self.myname = myname
        self.console = None
        self.filelog = None
        self.filename = os.path.join('.', logfile)
        self.logfilename = os.path.normpath(os.path.expanduser(self.filename))
        Logger.log_path = self.logfilename

    @staticmethod
    def get_log_path():
        return Logger.log_path

    def loginit(self):
        """Calls function LoggerInit to start initialising the logging system."""
        self.logger_init(self.myname)

    def logger_init(self, loggername):
        """Initialise the logging system.
        This includes logging to console and a file. By default, console prints
        messages of level WARN and above and file prints level INFO and above.
        In DEBUG mode (-D command line option) prints messages of level DEBUG
        and above to both console and file.
        Args:
         loggername: String - Name of the application printed along with the log
         message.
        """
#         fileformat =
        # '%(asctime)s <%(filename)s %(funcName)s: %(lineno)d> %(levelname)-5s %(message)s'
        if loggername == "dmesg":
            fileformat = '%(asctime)s %(message)s'
        else:
            fileformat = '%(asctime)s <%(filename)10s: %(lineno)3d> %(levelname)-5s %(message)s'
        Logger.m_logger = logging.getLogger(loggername)
        Logger.m_logger.propagate = 0
        Logger.m_logger.setLevel(logging.INFO)
        self.console = logging.StreamHandler()
        self.console.setLevel(logging.CRITICAL)
        consformat = logging.Formatter(fileformat, datefmt="%H:%M:%S")
        self.console.setFormatter(consformat)
        self.filelog = logging.handlers.RotatingFileHandler(filename=self.logfilename,\
                                                             maxBytes=20*1024*1024, backupCount=5)
        self.filelog.setLevel(logging.INFO)
        self.filelog.setFormatter(consformat)
        Logger.m_logger.addHandler(self.filelog)
        if loggername != "dmesg":
            Logger.m_logger.addHandler(self.console)
        if self.opts['debug']:
            if 'LOGLEVEL' in os.environ:
                log_lever = os.environ['LOGLEVEL']
            else:
                log_lever = 'DEBUG'
            self.console.setLevel(log_lever)
            self.filelog.setLevel('DEBUG')
            Logger.m_logger.setLevel(log_lever)
        if not self.opts['nofork']:
            self.console.setLevel(logging.WARN)

    @staticmethod
    def log_stop():
        """Shutdown logging process."""
        logging.shutdown()


def default_log(log_tag):
    """define default log"""
    #debug mode & not in daemon
    opts = {'debug': True, 'nofork': True}
    iso_time_format = "%Y%m%d%H%M%S"
    log_dir = os.path.join(os.path.dirname(__file__),  "..", "log")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_name = "%s_%s.log"%(log_tag, time.strftime(iso_time_format, time.localtime(time.time())))
    log_file = os.path.join(log_dir, log_name)
    log = Logger(opts, log_file, log_tag)
    log.loginit()
    return log, log.m_logger


Log, LOGGER_ = default_log("log")
# LOGGER_DMESG = default_log("dmesg")
DEBUG = LOGGER_.debug
INFO = LOGGER_.info
WARN = LOGGER_.warn
ERR = LOGGER_.error
