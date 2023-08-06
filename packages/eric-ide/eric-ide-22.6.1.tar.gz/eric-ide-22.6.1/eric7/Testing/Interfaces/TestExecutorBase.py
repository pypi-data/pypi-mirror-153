# -*- coding: utf-8 -*-

# Copyright (c) 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the executor base class for the various testing frameworks
and supporting classes.
"""

import os
from dataclasses import dataclass
from enum import IntEnum

from PyQt6.QtCore import pyqtSignal, QObject, QProcess, QProcessEnvironment

import Preferences


class TestResultCategory(IntEnum):
    """
    Class defining the supported result categories.
    """
    RUNNING = 0
    FAIL = 1
    OK = 2
    SKIP = 3
    PENDING = 4


@dataclass
class TestResult:
    """
    Class containing the test result data.
    """
    category: TestResultCategory    # result category
    status: str                     # test status
    name: str                       # test name
    id: str                         # test id
    description: str = ""           # short description of test
    message: str = ""               # short result message
    extra: list = None              # additional information text
    duration: float = None          # test duration
    filename: str = None            # file name of a failed test
    lineno: int = None              # line number of a failed test
    subtestResult: bool = False     # flag indicating the result of a subtest


@dataclass
class TestConfig:
    """
    Class containing the test run configuration.
    """
    interpreter: str                # path of the Python interpreter
    discover: bool                  # auto discovery flag
    discoveryStart: str             # start directory for auto discovery
    testFilename: str               # name of the test script
    testName: str                   # name of the test function
    failFast: bool                  # stop on first fail
    failedOnly: bool                # run failed tests only
    collectCoverage: bool           # coverage collection flag
    eraseCoverage: bool             # erase coverage data first
    coverageFile: str               # name of the coverage data file


class TestExecutorBase(QObject):
    """
    Base class for test framework specific implementations.
    
    @signal collected(list of tuple of (str, str, str)) emitted after all tests
        have been collected. Tuple elements are the test id, the test name and
        a short description of the test.
    @signal collectError(list of tuple of (str, str)) emitted when errors
        are encountered during test collection. Tuple elements are the
        test name and the error message.
    @signal startTest(tuple of (str, str, str) emitted before tests are run.
        Tuple elements are test id, test name and short description.
    @signal testResult(TestResult) emitted when a test result is ready
    @signal testFinished(list, str) emitted when the test has finished.
        The elements are the list of test results and the captured output
        of the test worker (if any).
    @signal testRunAboutToBeStarted() emitted just before the test run will
        be started.
    @signal testRunFinished(int, float) emitted when the test run has finished.
        The elements are the number of tests run and the duration in seconds
    @signal stop() emitted when the test process is being stopped.
    @signal coverageDataSaved(str) emitted after the coverage data was saved.
        The element is the absolute path of the coverage data file.
    """
    collected = pyqtSignal(list)
    collectError = pyqtSignal(list)
    startTest = pyqtSignal(tuple)
    testResult = pyqtSignal(TestResult)
    testFinished = pyqtSignal(list, str)
    testRunAboutToBeStarted = pyqtSignal()
    testRunFinished = pyqtSignal(int, float)
    stop = pyqtSignal()
    coverageDataSaved = pyqtSignal(str)
    
    module = ""
    name = ""
    runner = ""
    
    def __init__(self, testWidget):
        """
        Constructor
        
        @param testWidget reference to the unit test widget
        @type TestingWidget
        """
        super().__init__(testWidget)
        
        self.__process = None
    
    @classmethod
    def isInstalled(cls, interpreter):
        """
        Class method to check whether a test framework is installed.
        
        The test is performed by checking, if a module loader can found.
        
        @param interpreter interpreter to be used for the test
        @type str
        @return flag indicating the test framework module is installed
        @rtype bool
        """
        if cls.runner:
            proc = QProcess()
            proc.start(interpreter, [cls.runner, "installed"])
            if proc.waitForFinished(3000):
                exitCode = proc.exitCode()
                return exitCode == 0
        
        return False
    
    def getVersions(self, interpreter):
        """
        Public method to get the test framework version and version information
        of its installed plugins.
        
        @param interpreter interpreter to be used for the test
        @type str
        @return dictionary containing the framework name and version and the
            list of available plugins with name and version each
        @rtype dict
        @exception NotImplementedError this method needs to be implemented by
            derived classes
        """
        raise NotImplementedError
        
        return {}
    
    def hasCoverage(self, interpreter):
        """
        Public method to get the test framework version and version information
        of its installed plugins.
        
        @param interpreter interpreter to be used for the test
        @type str
        @return flag indicating the availability of coverage functionality
        @rtype bool
        @exception NotImplementedError this method needs to be implemented by
            derived classes
        """
        raise NotImplementedError
        
        return False
    
    def createArguments(self, config):
        """
        Public method to create the arguments needed to start the test process.
        
        @param config configuration for the test execution
        @type TestConfig
        @return list of process arguments
        @rtype list of str
        @exception NotImplementedError this method needs to be implemented by
            derived classes
        """
        raise NotImplementedError
        
        return []
    
    def _prepareProcess(self, workDir, pythonpath):
        """
        Protected method to prepare a process object to be started.
        
        @param workDir working directory
        @type str
        @param pythonpath list of directories to be added to the Python path
        @type list of str
        @return prepared process object
        @rtype QProcess
        """
        process = QProcess(self)
        process.setProcessChannelMode(
            QProcess.ProcessChannelMode.MergedChannels)
        process.setWorkingDirectory(workDir)
        process.finished.connect(self.finished)
        if pythonpath:
            env = QProcessEnvironment.systemEnvironment()
            currentPythonPath = env.value('PYTHONPATH', None)
            newPythonPath = os.pathsep.join(pythonpath)
            if currentPythonPath:
                newPythonPath += os.pathsep + currentPythonPath
            env.insert('PYTHONPATH', newPythonPath)
            process.setProcessEnvironment(env)
        
        return process
    
    def start(self, config, pythonpath):
        """
        Public method to start the testing process.
        
        @param config configuration for the test execution
        @type TestConfig
        @param pythonpath list of directories to be added to the Python path
        @type list of str
        @exception RuntimeError raised if the the testing process did not start
        """
        workDir = (
            config.discoveryStart
            if config.discover else
            os.path.dirname(config.testFilename)
        )
        self.__process = self._prepareProcess(workDir, pythonpath)
        testArgs = self.createArguments(config)
        self.testRunAboutToBeStarted.emit()
        self.__process.start(config.interpreter, testArgs)
        running = self.__process.waitForStarted()
        if not running:
            raise RuntimeError
    
    def finished(self):
        """
        Public method handling the unit test process been finished.
        
        This method should read the results (if necessary) and emit the signal
        testFinished.
        
        @exception NotImplementedError this method needs to be implemented by
            derived classes
        """
        raise NotImplementedError
    
    def readAllOutput(self, process=None):
        """
        Public method to read all output of the test process.
        
        @param process reference to the process object
        @type QProcess
        @return test process output
        @rtype str
        """
        if process is None:
            process = self.__process
        output = (
            str(process.readAllStandardOutput(),
                Preferences.getSystem("IOEncoding"),
                'replace').strip()
            if process else
            ""
        )
        return output
    
    def stopIfRunning(self):
        """
        Public method to stop the testing process, if it is running.
        """
        if (
            self.__process and
            self.__process.state() == QProcess.ProcessState.Running
        ):
            self.__process.terminate()
            self.__process.waitForFinished(2000)
            self.__process.kill()
            self.__process.waitForFinished(3000)
            
            self.stop.emit()
