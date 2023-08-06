# -*- coding: utf-8 -*-

# Copyright (c) 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a widget to orchestrate unit test execution.
"""

import contextlib
import enum
import locale
import os

from PyQt6.QtCore import pyqtSignal, pyqtSlot, Qt, QEvent, QCoreApplication
from PyQt6.QtWidgets import (
    QAbstractButton, QComboBox, QDialogButtonBox, QWidget
)

from EricWidgets import EricMessageBox
from EricWidgets.EricApplication import ericApp
from EricWidgets.EricMainWindow import EricMainWindow
from EricWidgets.EricPathPicker import EricPathPickerModes

from .Ui_TestingWidget import Ui_TestingWidget

from .TestResultsTree import TestResultsModel, TestResultsTreeView
from .Interfaces import Frameworks
from .Interfaces.TestExecutorBase import (
    TestConfig, TestResult, TestResultCategory
)
from .Interfaces.TestFrameworkRegistry import TestFrameworkRegistry

import Preferences
import UI.PixmapCache

from Globals import (
    recentNameTestDiscoverHistory, recentNameTestFileHistory,
    recentNameTestNameHistory, recentNameTestFramework,
    recentNameTestEnvironment
)


class TestingWidgetModes(enum.Enum):
    """
    Class defining the various modes of the testing widget.
    """
    IDLE = 0            # idle, no test were run yet
    RUNNING = 1         # test run being performed
    STOPPED = 2         # test run finished


class TestingWidget(QWidget, Ui_TestingWidget):
    """
    Class implementing a widget to orchestrate unit test execution.
    
    @signal testFile(str, int, bool) emitted to show the source of a
       test file
    @signal testRunStopped() emitted after a test run has finished
    """
    testFile = pyqtSignal(str, int, bool)
    testRunStopped = pyqtSignal()
    
    def __init__(self, testfile=None, parent=None):
        """
        Constructor
        
        @param testfile file name of the test to load
        @type str
        @param parent reference to the parent widget (defaults to None)
        @type QWidget (optional)
        """
        super().__init__(parent)
        self.setupUi(self)
        
        self.__resultsModel = TestResultsModel(self)
        self.__resultsModel.summary.connect(self.__setStatusLabel)
        self.__resultsTree = TestResultsTreeView(self)
        self.__resultsTree.setModel(self.__resultsModel)
        self.__resultsTree.goto.connect(self.__showSource)
        self.resultsGroupBox.layout().addWidget(self.__resultsTree)
        
        self.versionsButton.setIcon(
            UI.PixmapCache.getIcon("info"))
        self.clearHistoriesButton.setIcon(
            UI.PixmapCache.getIcon("clearPrivateData"))
        
        self.testsuitePicker.setMode(EricPathPickerModes.OPEN_FILE_MODE)
        self.testsuitePicker.setInsertPolicy(
            QComboBox.InsertPolicy.InsertAtTop)
        self.testsuitePicker.setSizeAdjustPolicy(
            QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon)
        
        self.discoveryPicker.setMode(EricPathPickerModes.DIRECTORY_MODE)
        self.discoveryPicker.setInsertPolicy(
            QComboBox.InsertPolicy.InsertAtTop)
        self.discoveryPicker.setSizeAdjustPolicy(
            QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon)
        
        self.testComboBox.lineEdit().setClearButtonEnabled(True)
        
        # create some more dialog buttons for orchestration
        self.__showLogButton = self.buttonBox.addButton(
            self.tr("Show Output..."),
            QDialogButtonBox.ButtonRole.ActionRole)
        self.__showLogButton.setToolTip(
            self.tr("Show the output of the test runner process"))
        self.__showLogButton.setWhatsThis(self.tr(
            """<b>Show Output...</b"""
            """<p>This button opens a dialog containing the output of the"""
            """ test runner process of the most recent run.</p>"""))
        
        self.__showCoverageButton = self.buttonBox.addButton(
            self.tr("Show Coverage..."),
            QDialogButtonBox.ButtonRole.ActionRole)
        self.__showCoverageButton.setToolTip(
            self.tr("Show code coverage in a new dialog"))
        self.__showCoverageButton.setWhatsThis(self.tr(
            """<b>Show Coverage...</b>"""
            """<p>This button opens a dialog containing the collected code"""
            """ coverage data.</p>"""))
        
        self.__startButton = self.buttonBox.addButton(
            self.tr("Start"), QDialogButtonBox.ButtonRole.ActionRole)
        
        self.__startButton.setToolTip(self.tr(
            "Start the selected testsuite"))
        self.__startButton.setWhatsThis(self.tr(
            """<b>Start Test</b>"""
            """<p>This button starts the test run.</p>"""))
        
        self.__startFailedButton = self.buttonBox.addButton(
            self.tr("Rerun Failed"), QDialogButtonBox.ButtonRole.ActionRole)
        self.__startFailedButton.setToolTip(
            self.tr("Reruns failed tests of the selected testsuite"))
        self.__startFailedButton.setWhatsThis(self.tr(
            """<b>Rerun Failed</b>"""
            """<p>This button reruns all failed tests of the most recent"""
            """ test run.</p>"""))
        
        self.__stopButton = self.buttonBox.addButton(
            self.tr("Stop"), QDialogButtonBox.ButtonRole.ActionRole)
        self.__stopButton.setToolTip(self.tr("Stop the running test"))
        self.__stopButton.setWhatsThis(self.tr(
            """<b>Stop Test</b>"""
            """<p>This button stops a running test.</p>"""))
        
        self.setWindowFlags(
            self.windowFlags() |
            Qt.WindowType.WindowContextHelpButtonHint
        )
        self.setWindowIcon(UI.PixmapCache.getIcon("eric"))
        self.setWindowTitle(self.tr("Testing"))
        
        try:
            # we are called from within the eric IDE
            self.__venvManager = ericApp().getObject("VirtualEnvManager")
            self.__project = ericApp().getObject("Project")
            self.__project.projectOpened.connect(self.__projectOpened)
            self.__project.projectClosed.connect(self.__projectClosed)
        except KeyError:
            # we were called as a standalone application
            from VirtualEnv.VirtualenvManager import VirtualenvManager
            self.__venvManager = VirtualenvManager(self)
            self.__venvManager.virtualEnvironmentAdded.connect(
                self.__populateVenvComboBox)
            self.__venvManager.virtualEnvironmentRemoved.connect(
                self.__populateVenvComboBox)
            self.__venvManager.virtualEnvironmentChanged.connect(
                self.__populateVenvComboBox)
            ericApp().registerObject("VirtualEnvManager", self.__venvManager)
            
            self.__project = None
        
        self.__discoverHistory = []
        self.__fileHistory = []
        self.__testNameHistory = []
        self.__recentFramework = ""
        self.__recentEnvironment = ""
        self.__failedTests = []
        
        self.__coverageFile = ""
        self.__coverageDialog = None
        
        self.__editors = []
        self.__testExecutor = None
        self.__recentLog = ""
        
        # connect some signals
        self.discoveryPicker.editTextChanged.connect(
            self.__resetResults)
        self.testsuitePicker.editTextChanged.connect(
            self.__resetResults)
        self.testComboBox.editTextChanged.connect(
            self.__resetResults)
        
        self.__frameworkRegistry = TestFrameworkRegistry()
        for framework in Frameworks:
            self.__frameworkRegistry.register(framework)
        
        self.__setIdleMode()
        
        self.__loadRecent()
        self.__populateVenvComboBox()
        
        if self.__project and self.__project.isOpen():
            self.venvComboBox.setCurrentText(self.__project.getProjectVenv())
            self.frameworkComboBox.setCurrentText(
                self.__project.getProjectTestingFramework())
            self.__insertDiscovery(self.__project.getProjectPath())
        else:
            self.__insertDiscovery("")
        
        self.__insertTestFile(testfile)
        self.__insertTestName("")
        
        self.clearHistoriesButton.clicked.connect(self.clearRecent)
        
        self.tabWidget.setCurrentIndex(0)
    
    def __populateVenvComboBox(self):
        """
        Private method to (re-)populate the virtual environments selector.
        """
        currentText = self.venvComboBox.currentText()
        if not currentText:
            currentText = self.__recentEnvironment
        
        self.venvComboBox.clear()
        self.venvComboBox.addItem("")
        self.venvComboBox.addItems(
            sorted(self.__venvManager.getVirtualenvNames()))
        self.venvComboBox.setCurrentText(currentText)
    
    def __populateTestFrameworkComboBox(self):
        """
        Private method to (re-)populate the test framework selector.
        """
        currentText = self.frameworkComboBox.currentText()
        if not currentText:
            currentText = self.__recentFramework
        
        self.frameworkComboBox.clear()
        
        if bool(self.venvComboBox.currentText()):
            interpreter = self.__venvManager.getVirtualenvInterpreter(
                self.venvComboBox.currentText())
            self.frameworkComboBox.addItem("")
            for index, (name, executor) in enumerate(
                sorted(self.__frameworkRegistry.getFrameworks().items()),
                start=1
            ):
                isInstalled = executor.isInstalled(interpreter)
                entry = (
                    name
                    if isInstalled else
                    self.tr("{0} (not available)").format(name)
                )
                self.frameworkComboBox.addItem(entry)
                self.frameworkComboBox.model().item(index).setEnabled(
                    isInstalled)
            
            self.frameworkComboBox.setCurrentText(self.__recentFramework)
    
    def getResultsModel(self):
        """
        Public method to get a reference to the model containing the test
        result data.
        
        @return reference to the test results model
        @rtype TestResultsModel
        """
        return self.__resultsModel
    
    def hasFailedTests(self):
        """
        Public method to check for failed tests.
        
        @return flag indicating the existence of failed tests
        @rtype bool
        """
        return bool(self.__resultsModel.getFailedTests())
        
    def getFailedTests(self):
        """
        Public method to get the list of failed tests (if any).
        
        @return list of IDs of failed tests
        @rtype list of str
        """
        return self.__failedTests[:]
    
    @pyqtSlot(str)
    def __insertHistory(self, widget, history, item):
        """
        Private slot to insert an item into a history object.
        
        @param widget reference to the widget
        @type QComboBox or EricComboPathPicker
        @param history array containing the history
        @type list of str
        @param item item to be inserted
        @type str
        """
        # prepend the given directory to the discovery picker
        if item is None:
            item = ""
        if item in history:
            history.remove(item)
        history.insert(0, item)
        widget.clear()
        widget.addItems(history)
        widget.setEditText(item)
    
    @pyqtSlot(str)
    def __insertDiscovery(self, start):
        """
        Private slot to insert the discovery start directory into the
        discoveryPicker object.
        
        @param start start directory name to be inserted
        @type str
        """
        self.__insertHistory(self.discoveryPicker, self.__discoverHistory,
                             start)
    
    @pyqtSlot(str)
    def setTestFile(self, testFile, forProject=False):
        """
        Public slot to set the given test file as the current one.
        
        @param testFile path of the test file
        @type str
        @param forProject flag indicating that this call is for a project
            (defaults to False)
        @type bool (optional)
        """
        if testFile:
            self.__insertTestFile(testFile)
        
        self.discoverCheckBox.setChecked(forProject or not bool(testFile))
        
        if forProject:
            self.__projectOpened()
        
        self.tabWidget.setCurrentIndex(0)
    
    @pyqtSlot(str)
    def __insertTestFile(self, prog):
        """
        Private slot to insert a test file name into the testsuitePicker
        object.
        
        @param prog test file name to be inserted
        @type str
        """
        self.__insertHistory(self.testsuitePicker, self.__fileHistory,
                             prog)
    
    @pyqtSlot(str)
    def __insertTestName(self, testName):
        """
        Private slot to insert a test name into the testComboBox object.
        
        @param testName name of the test to be inserted
        @type str
        """
        self.__insertHistory(self.testComboBox, self.__testNameHistory,
                             testName)
    
    def __loadRecent(self):
        """
        Private method to load the most recently used lists.
        """
        Preferences.Prefs.rsettings.sync()
        
        # 1. recently selected test framework and virtual environment
        self.__recentEnvironment = Preferences.Prefs.rsettings.value(
            recentNameTestEnvironment, "")
        self.__recentFramework = Preferences.Prefs.rsettings.value(
            recentNameTestFramework, "")
        
        # 2. discovery history
        self.__discoverHistory = []
        rs = Preferences.Prefs.rsettings.value(
            recentNameTestDiscoverHistory)
        if rs is not None:
            recent = [f for f in Preferences.toList(rs) if os.path.exists(f)]
            self.__discoverHistory = recent[
                :Preferences.getDebugger("RecentNumber")]
        
        # 3. test file history
        self.__fileHistory = []
        rs = Preferences.Prefs.rsettings.value(
            recentNameTestFileHistory)
        if rs is not None:
            recent = [f for f in Preferences.toList(rs) if os.path.exists(f)]
            self.__fileHistory = recent[
                :Preferences.getDebugger("RecentNumber")]
        
        # 4. test name history
        self.__testNameHistory = []
        rs = Preferences.Prefs.rsettings.value(
            recentNameTestNameHistory)
        if rs is not None:
            recent = [n for n in Preferences.toList(rs) if n]
            self.__testNameHistory = recent[
                :Preferences.getDebugger("RecentNumber")]
    
    def __saveRecent(self):
        """
        Private method to save the most recently used lists.
        """
        Preferences.Prefs.rsettings.setValue(
            recentNameTestEnvironment, self.__recentEnvironment)
        Preferences.Prefs.rsettings.setValue(
            recentNameTestFramework, self.__recentFramework)
        Preferences.Prefs.rsettings.setValue(
            recentNameTestDiscoverHistory, self.__discoverHistory)
        Preferences.Prefs.rsettings.setValue(
            recentNameTestFileHistory, self.__fileHistory)
        Preferences.Prefs.rsettings.setValue(
            recentNameTestNameHistory, self.__testNameHistory)
        
        Preferences.Prefs.rsettings.sync()
    
    @pyqtSlot()
    def clearRecent(self):
        """
        Public slot to clear the recently used lists.
        """
        # clear histories
        self.__discoverHistory = []
        self.__fileHistory = []
        self.__testNameHistory = []
        
        # clear widgets with histories
        self.discoveryPicker.clear()
        self.testsuitePicker.clear()
        self.testComboBox.clear()
        
        # sync histories
        self.__saveRecent()
    
    @pyqtSlot()
    def __resetResults(self):
        """
        Private slot to reset the test results tab and data.
        """
        self.__totalCount = 0
        self.__runCount = 0
        
        self.progressCounterRunCount.setText("0")
        self.progressCounterRemCount.setText("0")
        self.progressProgressBar.setMaximum(100)
        self.progressProgressBar.setValue(0)
        
        self.statusLabel.clear()
        
        self.__resultsModel.clear()
        self.__updateButtonBoxButtons()
    
    @pyqtSlot()
    def __updateButtonBoxButtons(self):
        """
        Private slot to update the state of the buttons of the button box.
        """
        failedAvailable = bool(self.__resultsModel.getFailedTests())
        
        # Start button
        if self.__mode in (
            TestingWidgetModes.IDLE, TestingWidgetModes.STOPPED
        ):
            self.__startButton.setEnabled(
                bool(self.venvComboBox.currentText()) and
                bool(self.frameworkComboBox.currentText()) and
                (
                    (self.discoverCheckBox.isChecked() and
                     bool(self.discoveryPicker.currentText())) or
                    bool(self.testsuitePicker.currentText())
                )
            )
            self.__startButton.setDefault(
                self.__mode == TestingWidgetModes.IDLE or
                not failedAvailable
            )
        else:
            self.__startButton.setEnabled(False)
            self.__startButton.setDefault(False)
        
        # Start Failed button
        self.__startFailedButton.setEnabled(
            self.__mode == TestingWidgetModes.STOPPED and
            failedAvailable
        )
        self.__startFailedButton.setDefault(
            self.__mode == TestingWidgetModes.STOPPED and
            failedAvailable
        )
        
        # Stop button
        self.__stopButton.setEnabled(
            self.__mode == TestingWidgetModes.RUNNING)
        self.__stopButton.setDefault(
            self.__mode == TestingWidgetModes.RUNNING)
        
        # Code coverage button
        self.__showCoverageButton.setEnabled(
            self.__mode == TestingWidgetModes.STOPPED and
            bool(self.__coverageFile) and
            (
                (self.discoverCheckBox.isChecked() and
                 bool(self.discoveryPicker.currentText())) or
                bool(self.testsuitePicker.currentText())
            )
        )
        
        # Log output button
        self.__showLogButton.setEnabled(bool(self.__recentLog))
        
        # Close button
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Close
        ).setEnabled(self.__mode in (
            TestingWidgetModes.IDLE, TestingWidgetModes.STOPPED
        ))
    
    @pyqtSlot()
    def __updateProgress(self):
        """
        Private slot update the progress indicators.
        """
        self.progressCounterRunCount.setText(
            str(self.__runCount))
        self.progressCounterRemCount.setText(
            str(self.__totalCount - self.__runCount))
        self.progressProgressBar.setMaximum(self.__totalCount)
        self.progressProgressBar.setValue(self.__runCount)
    
    @pyqtSlot()
    def __setIdleMode(self):
        """
        Private slot to switch the widget to idle mode.
        """
        self.__mode = TestingWidgetModes.IDLE
        self.__updateButtonBoxButtons()
        self.progressGroupBox.hide()
        self.tabWidget.setCurrentIndex(0)
    
    @pyqtSlot()
    def __setRunningMode(self):
        """
        Private slot to switch the widget to running mode.
        """
        self.__mode = TestingWidgetModes.RUNNING
        
        self.__totalCount = 0
        self.__runCount = 0
        
        self.__coverageFile = ""
        
        self.sbLabel.setText(self.tr("Running"))
        self.tabWidget.setCurrentIndex(1)
        self.__updateButtonBoxButtons()
        self.__updateProgress()
        
        self.progressGroupBox.show()
    
    @pyqtSlot()
    def __setStoppedMode(self):
        """
        Private slot to switch the widget to stopped mode.
        """
        self.__mode = TestingWidgetModes.STOPPED
        if self.__totalCount == 0:
            self.progressProgressBar.setMaximum(100)
        
        self.progressGroupBox.hide()
        
        self.__updateButtonBoxButtons()
        
        self.testRunStopped.emit()
        
        self.raise_()
        self.activateWindow()
    
    @pyqtSlot(bool)
    def on_discoverCheckBox_toggled(self, checked):
        """
        Private slot handling state changes of the 'discover' checkbox.
        
        @param checked state of the checkbox
        @type bool
        """
        if not bool(self.discoveryPicker.currentText()):
            if self.__project and self.__project.isOpen():
                self.__insertDiscovery(self.__project.getProjectPath())
            else:
                self.__insertDiscovery(
                    Preferences.getMultiProject("Workspace"))
        
        self.__resetResults()
    
    @pyqtSlot()
    def on_testsuitePicker_aboutToShowPathPickerDialog(self):
        """
        Private slot called before the test file selection dialog is shown.
        """
        if self.__project:
            # we were called from within eric
            py3Extensions = ' '.join([
                "*{0}".format(ext)
                for ext in
                ericApp().getObject("DebugServer").getExtensions('Python3')
            ])
            fileFilter = self.tr(
                "Python3 Files ({0});;All Files (*)"
            ).format(py3Extensions)
        else:
            # standalone application
            fileFilter = self.tr("Python Files (*.py);;All Files (*)")
        self.testsuitePicker.setFilters(fileFilter)
        
        defaultDirectory = (
            self.__project.getProjectPath()
            if self.__project and self.__project.isOpen() else
            Preferences.getMultiProject("Workspace")
        )
        if not defaultDirectory:
            defaultDirectory = os.path.expanduser("~")
        self.testsuitePicker.setDefaultDirectory(defaultDirectory)
    
    @pyqtSlot(QAbstractButton)
    def on_buttonBox_clicked(self, button):
        """
        Private slot called by a button of the button box clicked.
        
        @param button button that was clicked
        @type QAbstractButton
        """
        if button == self.__startButton:
            self.startTests()
            self.__saveRecent()
        elif button == self.__stopButton:
            self.__stopTests()
        elif button == self.__startFailedButton:
            self.startTests(failedOnly=True)
        elif button == self.__showCoverageButton:
            self.__showCoverageDialog()
        elif button == self.__showLogButton:
            self.__showLogOutput()
    
    @pyqtSlot(int)
    def on_venvComboBox_currentIndexChanged(self, index):
        """
        Private slot handling the selection of a virtual environment.
        
        @param index index of the selected environment
        @type int
        """
        self.__populateTestFrameworkComboBox()
        self.__updateButtonBoxButtons()
        
        self.versionsButton.setEnabled(bool(self.venvComboBox.currentText()))
        
        self.__updateCoverage()
    
    @pyqtSlot(int)
    def on_frameworkComboBox_currentIndexChanged(self, index):
        """
        Private slot handling the selection of a test framework.
        
        @param index index of the selected framework
        @type int
        """
        self.__resetResults()
        self.__updateCoverage()
    
    @pyqtSlot()
    def __updateCoverage(self):
        """
        Private slot to update the state of the coverage checkbox depending on
        the selected framework's capabilities.
        """
        hasCoverage = False
        
        venvName = self.venvComboBox.currentText()
        if venvName:
            framework = self.frameworkComboBox.currentText()
            if framework:
                interpreter = self.__venvManager.getVirtualenvInterpreter(
                    venvName)
                executor = self.__frameworkRegistry.createExecutor(
                    framework, self)
                hasCoverage = executor.hasCoverage(interpreter)
        
        self.coverageCheckBox.setEnabled(hasCoverage)
        if not hasCoverage:
            self.coverageCheckBox.setChecked(False)
    
    @pyqtSlot()
    def on_versionsButton_clicked(self):
        """
        Private slot to show the versions of available plugins.
        """
        venvName = self.venvComboBox.currentText()
        if venvName:
            headerText = self.tr("<h3>Versions of Frameworks and their"
                                 " Plugins</h3>")
            versionsText = ""
            interpreter = self.__venvManager.getVirtualenvInterpreter(venvName)
            for framework in sorted(
                self.__frameworkRegistry.getFrameworks().keys()
            ):
                executor = self.__frameworkRegistry.createExecutor(
                    framework, self)
                versions = executor.getVersions(interpreter)
                if versions:
                    txt = "<p><strong>{0} {1}</strong>".format(
                        versions["name"], versions["version"])
                    
                    if versions["plugins"]:
                        txt += "<table>"
                        for pluginVersion in versions["plugins"]:
                            txt += self.tr(
                                "<tr><td>{0}</td><td>{1}</td></tr>"
                            ).format(
                                pluginVersion["name"], pluginVersion["version"]
                            )
                        txt += "</table>"
                    txt += "</p>"
                    
                    versionsText += txt
            
            if not versionsText:
                versionsText = self.tr("No version information available.")
            
            EricMessageBox.information(
                self,
                self.tr("Versions"),
                headerText + versionsText
            )
    
    @pyqtSlot()
    def startTests(self, failedOnly=False):
        """
        Public slot to start the test run.
        
        @param failedOnly flag indicating to run only failed tests
        @type bool
        """
        if self.__mode == TestingWidgetModes.RUNNING:
            return
        
        self.__recentLog = ""
        
        self.__recentEnvironment = self.venvComboBox.currentText()
        self.__recentFramework = self.frameworkComboBox.currentText()
        
        self.__failedTests = (
            self.__resultsModel.getFailedTests()
            if failedOnly else
            []
        )
        discover = self.discoverCheckBox.isChecked()
        if discover:
            discoveryStart = self.discoveryPicker.currentText()
            testFileName = ""
            testName = ""
            
            if discoveryStart:
                self.__insertDiscovery(discoveryStart)
        else:
            discoveryStart = ""
            testFileName = self.testsuitePicker.currentText()
            if testFileName:
                self.__insertTestFile(testFileName)
            testName = self.testComboBox.currentText()
            if testName:
                self.__insertTestName(testName)
        
        self.sbLabel.setText(self.tr("Preparing Testsuite"))
        QCoreApplication.processEvents()
        
        if self.__project:
            mainScript = self.__project.getMainScript(True)
            coverageFile = (
                os.path.splitext(mainScript)[0] + ".coverage"
                if mainScript else
                ""
            )
        else:
            coverageFile = ""
        interpreter = self.__venvManager.getVirtualenvInterpreter(
            self.__recentEnvironment)
        config = TestConfig(
            interpreter=interpreter,
            discover=discover,
            discoveryStart=discoveryStart,
            testFilename=testFileName,
            testName=testName,
            failFast=self.failfastCheckBox.isChecked(),
            failedOnly=failedOnly,
            collectCoverage=self.coverageCheckBox.isChecked(),
            eraseCoverage=self.coverageEraseCheckBox.isChecked(),
            coverageFile=coverageFile,
        )
        
        self.__testExecutor = self.__frameworkRegistry.createExecutor(
            self.__recentFramework, self)
        self.__testExecutor.collected.connect(self.__testsCollected)
        self.__testExecutor.collectError.connect(self.__testsCollectError)
        self.__testExecutor.startTest.connect(self.__testStarted)
        self.__testExecutor.testResult.connect(self.__processTestResult)
        self.__testExecutor.testFinished.connect(self.__testProcessFinished)
        self.__testExecutor.testRunFinished.connect(self.__testRunFinished)
        self.__testExecutor.stop.connect(self.__testsStopped)
        self.__testExecutor.coverageDataSaved.connect(self.__coverageData)
        self.__testExecutor.testRunAboutToBeStarted.connect(
            self.__testRunAboutToBeStarted)
        
        self.__setRunningMode()
        self.__testExecutor.start(config, [])
    
    @pyqtSlot()
    def __stopTests(self):
        """
        Private slot to stop the current test run.
        """
        self.__testExecutor.stopIfRunning()
    
    @pyqtSlot(list)
    def __testsCollected(self, testNames):
        """
        Private slot handling the 'collected' signal of the executor.
        
        @param testNames list of tuples containing the test id, the test name
            and a description of collected tests
        @type list of tuple of (str, str, str)
        """
        testResults = [
            TestResult(
                category=TestResultCategory.PENDING,
                status=self.tr("pending"),
                name=name,
                id=id,
                message=desc,
            ) for id, name, desc in testNames
        ]
        self.__resultsModel.addTestResults(testResults)
        
        self.__totalCount += len(testResults)
        self.__updateProgress()
    
    @pyqtSlot(list)
    def __testsCollectError(self, errors):
        """
        Private slot handling the 'collectError' signal of the executor.
        
        @param errors list of tuples containing the test name and a description
            of the error
        @type list of tuple of (str, str)
        """
        testResults = []
        
        for testFile, error in errors:
            if testFile:
                testResults.append(TestResult(
                    category=TestResultCategory.FAIL,
                    status=self.tr("Failure"),
                    name=testFile,
                    id=testFile,
                    message=self.tr("Collection Error"),
                    extra=error.splitlines()
                ))
            else:
                EricMessageBox.critical(
                    self,
                    self.tr("Collection Error"),
                    self.tr(
                        "<p>There was an error while collecting tests."
                        "</p><p>{0}</p>"
                    ).format("<br/>".join(error.splitlines()))
                )
        
        if testResults:
            self.__resultsModel.addTestResults(testResults)
    
    @pyqtSlot(tuple)
    def __testStarted(self, test):
        """
        Private slot handling the 'startTest' signal of the executor.
        
        @param test tuple containing the id, name and short description of the
            tests about to be run
        @type tuple of (str, str, str)
        """
        self.__resultsModel.updateTestResults([
            TestResult(
                category=TestResultCategory.RUNNING,
                status=self.tr("running"),
                id=test[0],
                name=test[1],
                message="" if test[2] is None else test[2],
            )
        ])
    
    @pyqtSlot(TestResult)
    def __processTestResult(self, result):
        """
        Private slot to handle the receipt of a test result object.
        
        @param result test result object
        @type TestResult
        """
        if not result.subtestResult:
            self.__runCount += 1
        self.__updateProgress()
        
        self.__resultsModel.updateTestResults([result])
    
    @pyqtSlot(list, str)
    def __testProcessFinished(self, results, output):
        """
        Private slot to handle the 'testFinished' signal of the executor.
        
        @param results list of test result objects (if not sent via the
            'testResult' signal
        @type list of TestResult
        @param output string containing the test process output (if any)
        @type str
        """
        self.__recentLog = output
        
        self.__setStoppedMode()
        self.__testExecutor = None
        
        self.__adjustPendingState()
    
    @pyqtSlot(int, float)
    def __testRunFinished(self, noTests, duration):
        """
        Private slot to handle the 'testRunFinished' signal of the executor.
        
        @param noTests number of tests run by the executor
        @type int
        @param duration time needed in seconds to run the tests
        @type float
        """
        self.sbLabel.setText(
            self.tr("Ran %n test(s) in {0}s", "", noTests).format(
                locale.format_string("%.3f", duration, grouping=True)
            )
        )
        
        self.__setStoppedMode()
    
    @pyqtSlot()
    def __testsStopped(self):
        """
        Private slot to handle the 'stop' signal of the executor.
        """
        self.sbLabel.setText(self.tr("Ran %n test(s)", "", self.__runCount))
        
        self.__setStoppedMode()
    
    @pyqtSlot()
    def __testRunAboutToBeStarted(self):
        """
        Private slot to handle the 'testRunAboutToBeStarted' signal of the
        executor.
        """
        self.__resultsModel.clear()
    
    def __adjustPendingState(self):
        """
        Private method to change the status indicator of all still pending
        tests to "not run".
        """
        newResults = []
        for result in self.__resultsModel.getTestResults():
            if result.category == TestResultCategory.PENDING:
                result.category = TestResultCategory.SKIP
                result.status = self.tr("not run")
                newResults.append(result)
        
        if newResults:
            self.__resultsModel.updateTestResults(newResults)
    
    @pyqtSlot(str)
    def __coverageData(self, coverageFile):
        """
        Private slot to handle the 'coverageData' signal of the executor.
        
        @param coverageFile file containing the coverage data
        @type str
        """
        self.__coverageFile = coverageFile
    
    @pyqtSlot()
    def __showCoverageDialog(self):
        """
        Private slot to show a code coverage dialog for the most recent test
        run.
        """
        if self.__coverageDialog is None:
            from DataViews.PyCoverageDialog import PyCoverageDialog
            self.__coverageDialog = PyCoverageDialog(self)
            self.__coverageDialog.openFile.connect(self.__openEditor)
        
        testDir = (
            self.discoveryPicker.currentText()
            if self.discoverCheckBox.isChecked() else
            os.path.dirname(self.testsuitePicker.currentText())
        )
        if testDir:
            self.__coverageDialog.show()
            self.__coverageDialog.start(self.__coverageFile, testDir)
    
    @pyqtSlot()
    def __showLogOutput(self):
        """
        Private slot to show the output of the most recent test run.
        """
        from EricWidgets.EricPlainTextDialog import EricPlainTextDialog
        dlg = EricPlainTextDialog(
            title=self.tr("Test Run Output"),
            text=self.__recentLog
        )
        dlg.exec()
    
    @pyqtSlot(str)
    def __setStatusLabel(self, statusText):
        """
        Private slot to set the status label to the text sent by the model.
        
        @param statusText text to be shown
        @type str
        """
        self.statusLabel.setText(f"<b>{statusText}</b>")
    
    @pyqtSlot()
    def __projectOpened(self):
        """
        Private slot to handle a project being opened.
        """
        self.venvComboBox.setCurrentText(self.__project.getProjectVenv())
        self.frameworkComboBox.setCurrentText(
            self.__project.getProjectTestingFramework())
        self.__insertDiscovery(self.__project.getProjectPath())
    
    @pyqtSlot()
    def __projectClosed(self):
        """
        Private slot to handle a project being closed.
        """
        self.venvComboBox.setCurrentText("")
        self.frameworkComboBox.setCurrentText("")
        self.__insertDiscovery("")
    
    @pyqtSlot(str, int)
    def __showSource(self, filename, lineno):
        """
        Private slot to show the source of a traceback in an editor.
        
        @param filename file name of the file to be shown
        @type str
        @param lineno line number to go to in the file
        @type int
        """
        if self.__project:
            # running as part of eric IDE
            self.testFile.emit(filename, lineno, True)
        else:
            self.__openEditor(filename, lineno)
    
    def __openEditor(self, filename, linenumber=1):
        """
        Private method to open an editor window for the given file.
        
        Note: This method opens an editor window when the testing dialog
        is called as a standalone application.
        
        @param filename path of the file to be opened
        @type str
        @param linenumber line number to place the cursor at (defaults to 1)
        @type int (optional)
        """
        from QScintilla.MiniEditor import MiniEditor
        editor = MiniEditor(filename, "Python3", self)
        editor.gotoLine(linenumber)
        editor.show()
        
        self.__editors.append(editor)
    
    def closeEvent(self, event):
        """
        Protected method to handle the close event.
        
        @param event close event
        @type QCloseEvent
        """
        event.accept()
        
        for editor in self.__editors:
            with contextlib.suppress(Exception):
                editor.close()


class TestingWindow(EricMainWindow):
    """
    Main window class for the standalone dialog.
    """
    def __init__(self, testfile=None, parent=None):
        """
        Constructor
        
        @param testfile file name of the test script to open
        @type str
        @param parent reference to the parent widget
        @type QWidget
        """
        super().__init__(parent)
        self.__cw = TestingWidget(testfile=testfile, parent=self)
        self.__cw.installEventFilter(self)
        size = self.__cw.size()
        self.setCentralWidget(self.__cw)
        self.resize(size)
        
        self.setStyle(Preferences.getUI("Style"),
                      Preferences.getUI("StyleSheet"))
        
        self.__cw.buttonBox.accepted.connect(self.close)
        self.__cw.buttonBox.rejected.connect(self.close)
    
    def eventFilter(self, obj, event):
        """
        Public method to filter events.
        
        @param obj reference to the object the event is meant for (QObject)
        @param event reference to the event object (QEvent)
        @return flag indicating, whether the event was handled (boolean)
        """
        if event.type() == QEvent.Type.Close:
            QCoreApplication.exit(0)
            return True
        
        return False


def clearSavedHistories(self):
    """
    Function to clear the saved history lists.
    """
    Preferences.Prefs.rsettings.setValue(
        recentNameTestDiscoverHistory, [])
    Preferences.Prefs.rsettings.setValue(
        recentNameTestFileHistory, [])
    Preferences.Prefs.rsettings.setValue(
        recentNameTestNameHistory, [])
    
    Preferences.Prefs.rsettings.sync()
