# -*- coding: utf-8 -*-

# Copyright (c) 2015 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Package implementing the pip GUI logic.
"""

import os
import sys
import json
import contextlib

from PyQt6.QtCore import (
    pyqtSlot, QObject, QProcess, QUrl, QCoreApplication, QThread
)
from PyQt6.QtWidgets import QDialog, QInputDialog, QLineEdit
from PyQt6.QtNetwork import (
    QNetworkAccessManager, QNetworkRequest, QNetworkReply
)

from EricWidgets import EricMessageBox
from EricWidgets.EricApplication import ericApp

from EricNetwork.EricNetworkProxyFactory import proxyAuthenticationRequired
try:
    from EricNetwork.EricSslErrorHandler import EricSslErrorHandler
    SSL_AVAILABLE = True
except ImportError:
    SSL_AVAILABLE = False

from .PipDialog import PipDialog
from .PipVulnerabilityChecker import PipVulnerabilityChecker

import Preferences
import Globals


class Pip(QObject):
    """
    Class implementing the pip GUI logic.
    """
    DefaultPyPiUrl = "https://pypi.org"
    DefaultIndexUrlPypi = DefaultPyPiUrl + "/pypi"
    DefaultIndexUrlSimple = DefaultPyPiUrl + "/simple"
    DefaultIndexUrlSearch = DefaultPyPiUrl + "/search/"
    
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the user interface object
        @type QObject
        """
        super().__init__(parent)
        
        self.__ui = parent
        
        # attributes for the network objects
        self.__networkManager = QNetworkAccessManager(self)
        self.__networkManager.proxyAuthenticationRequired.connect(
            proxyAuthenticationRequired)
        if SSL_AVAILABLE:
            self.__sslErrorHandler = EricSslErrorHandler(self)
            self.__networkManager.sslErrors.connect(
                self.__sslErrorHandler.sslErrorsReply)
        self.__replies = []
        
        self.__vulnerabilityChecker = PipVulnerabilityChecker(self, self)
    
    def getNetworkAccessManager(self):
        """
        Public method to get a reference to the network access manager object.
        
        @return reference to the network access manager object
        @rtype QNetworkAccessManager
        """
        return self.__networkManager
    
    def getVulnerabilityChecker(self):
        """
        Public method to get a reference to the vulnerability checker object.
        
        @return reference to the vulnerability checker object
        @rtype PipVulnerabilityChecker
        """
        return self.__vulnerabilityChecker
    
    ##########################################################################
    ## Methods below implement some utility functions
    ##########################################################################
    
    def runProcess(self, args, interpreter):
        """
        Public method to execute the current pip with the given arguments.
        
        The selected pip executable is called with the given arguments and
        waited for its end.
        
        @param args list of command line arguments
        @type list of str
        @param interpreter path of the Python interpreter to be used
        @type str
        @return tuple containing a flag indicating success and the output
            of the process
        @rtype tuple of (bool, str)
        """
        ioEncoding = Preferences.getSystem("IOEncoding")
        
        process = QProcess()
        process.start(interpreter, args)
        procStarted = process.waitForStarted()
        if procStarted:
            finished = process.waitForFinished(30000)
            if finished:
                if process.exitCode() == 0:
                    output = str(process.readAllStandardOutput(), ioEncoding,
                                 'replace')
                    return True, output
                else:
                    return (False,
                            self.tr("python exited with an error ({0}).")
                            .format(process.exitCode()))
            else:
                process.terminate()
                process.waitForFinished(2000)
                process.kill()
                process.waitForFinished(3000)
                return False, self.tr("python did not finish within"
                                      " 30 seconds.")
        
        return False, self.tr("python could not be started.")
    
    def getUserConfig(self):
        """
        Public method to get the name of the user configuration file.
        
        @return path of the user configuration file
        @rtype str
        """
        # Unix:     ~/.config/pip/pip.conf
        # OS X:     ~/Library/Application Support/pip/pip.conf
        # Windows:  %APPDATA%\pip\pip.ini
        # Environment: $PIP_CONFIG_FILE
        
        with contextlib.suppress(KeyError):
            return os.environ["PIP_CONFIG_FILE"]
        
        if Globals.isWindowsPlatform():
            config = os.path.join(os.environ["APPDATA"], "pip", "pip.ini")
        elif Globals.isMacPlatform():
            config = os.path.expanduser(
                "~/Library/Application Support/pip/pip.conf")
        else:
            config = os.path.expanduser("~/.config/pip/pip.conf")
        
        return config
    
    def getVirtualenvConfig(self, venvName):
        """
        Public method to get the name of the virtualenv configuration file.
        
        @param venvName name of the environment to get config file path for
        @type str
        @return path of the virtualenv configuration file
        @rtype str
        """
        # Unix, OS X:   $VIRTUAL_ENV/pip.conf
        # Windows:      %VIRTUAL_ENV%\pip.ini
        
        pip = "pip.ini" if Globals.isWindowsPlatform() else "pip.conf"
        
        venvManager = ericApp().getObject("VirtualEnvManager")
        venvDirectory = (
            os.path.dirname(self.getUserConfig())
            if venvManager.isGlobalEnvironment(venvName) else
            venvManager.getVirtualenvDirectory(venvName)
        )
        
        config = os.path.join(venvDirectory, pip) if venvDirectory else ""
        
        return config
    
    def getProjectEnvironmentString(self):
        """
        Public method to get the string for the project environment.
        
        @return string for the project environment
        @rtype str
        """
        if ericApp().getObject("Project").isOpen():
            return self.tr("<project>")
        else:
            return ""
    
    def getVirtualenvInterpreter(self, venvName):
        """
        Public method to get the interpreter for a virtual environment.
        
        @param venvName logical name for the virtual environment
        @type str
        @return interpreter path
        @rtype str
        """
        interpreter = (
            ericApp().getObject("Project").getProjectInterpreter()
            if venvName == self.getProjectEnvironmentString() else
            ericApp().getObject("VirtualEnvManager")
            .getVirtualenvInterpreter(venvName)
        )
        if not interpreter:
            EricMessageBox.critical(
                None,
                self.tr("Interpreter for Virtual Environment"),
                self.tr("""No interpreter configured for the selected"""
                        """ virtual environment."""))
        
        return interpreter
    
    def getVirtualenvNames(self, noRemote=False, noConda=False):
        """
        Public method to get a sorted list of virtual environment names.
        
        @param noRemote flag indicating to exclude environments for remote
            debugging
        @type bool
        @param noConda flag indicating to exclude Conda environments
        @type bool
        @return sorted list of virtual environment names
        @rtype list of str
        """
        return sorted(
            ericApp().getObject("VirtualEnvManager").getVirtualenvNames(
                noRemote=noRemote, noConda=noConda))
    
    def installPip(self, venvName, userSite=False):
        """
        Public method to install pip.
        
        @param venvName name of the environment to install pip into
        @type str
        @param userSite flag indicating an install to the user install
            directory
        @type bool
        """
        interpreter = self.getVirtualenvInterpreter(venvName)
        if not interpreter:
            return
        
        dia = PipDialog(self.tr('Install PIP'))
        commands = (
            [(interpreter, ["-m", "ensurepip", "--user"])]
            if userSite else
            [(interpreter, ["-m", "ensurepip"])]
        )
        if Preferences.getPip("PipSearchIndex"):
            indexUrl = Preferences.getPip("PipSearchIndex") + "/simple"
            args = ["-m", "pip", "install", "--index-url", indexUrl,
                    "--upgrade"]
        else:
            args = ["-m", "pip", "install", "--upgrade"]
        if userSite:
            args.append("--user")
        args.append("pip")
        commands.append((interpreter, args[:]))
    
        res = dia.startProcesses(commands)
        if res:
            dia.exec()
    
    @pyqtSlot()
    def repairPip(self, venvName):
        """
        Public method to repair the pip installation.
        
        @param venvName name of the environment to install pip into
        @type str
        """
        interpreter = self.getVirtualenvInterpreter(venvName)
        if not interpreter:
            return
        
        # python -m pip install --ignore-installed pip
        if Preferences.getPip("PipSearchIndex"):
            indexUrl = Preferences.getPip("PipSearchIndex") + "/simple"
            args = ["-m", "pip", "install", "--index-url", indexUrl,
                    "--ignore-installed"]
        else:
            args = ["-m", "pip", "install", "--ignore-installed"]
        args.append("pip")
        
        dia = PipDialog(self.tr('Repair PIP'))
        res = dia.startProcess(interpreter, args)
        if res:
            dia.exec()
    
    def __checkUpgradePyQt(self, packages):
        """
        Private method to check, if an upgrade of PyQt packages is attempted.
        
        @param packages list of packages to upgrade
        @type list of str
        @return flag indicating a PyQt upgrade
        @rtype bool
        """
        pyqtPackages = [
            p for p in packages if p.lower() in [
                "pyqt6", "pyqt6-sip", "pyqt6-webengine", "pyqt6-charts",
                "pyqt6-qscintilla", "pyqt6-qt6", "pyqt6-webengine-qt6",
                "pyqt6-charts-qt6"
            ]
        ]
        return bool(pyqtPackages)
    
    def __checkUpgradeEric(self, packages):
        """
        Private method to check, if an upgrade of the eric-ide package is
        attempted.
        
        @param packages list of packages to upgrade
        @type list of str
        @return flag indicating an eric-ide upgrade
        @rtype bool
        """
        ericPackages = [
            p for p in packages if p.lower() == "eric-ide"
        ]
        return bool(ericPackages)
    
    def upgradePackages(self, packages, venvName, userSite=False):
        """
        Public method to upgrade the given list of packages.
        
        @param packages list of packages to upgrade
        @type list of str
        @param venvName name of the virtual environment to be used
        @type str
        @param userSite flag indicating an install to the user install
            directory
        @type bool
        @return flag indicating a successful execution
        @rtype bool
        """
        if not venvName:
            return False
        
        if self.getVirtualenvInterpreter(venvName) in (
            sys.executable, Globals.getPythonExecutable()
        ):
            upgradePyQt = self.__checkUpgradePyQt(packages)
            upgradeEric = self.__checkUpgradeEric(packages)
            if upgradeEric or upgradePyQt:
                try:
                    if upgradeEric and upgradePyQt:
                        self.__ui.upgradeEricPyQt()
                    elif upgradeEric:
                        self.__ui.upgradeEric()
                    elif upgradePyQt:
                        self.__ui.upgradePyQt()
                    return None     # should not be reached; play it safe
                except AttributeError:
                    return False
        
        interpreter = self.getVirtualenvInterpreter(venvName)
        if not interpreter:
            return False
        
        if Preferences.getPip("PipSearchIndex"):
            indexUrl = Preferences.getPip("PipSearchIndex") + "/simple"
            args = ["-m", "pip", "install", "--index-url", indexUrl,
                    "--upgrade"]
        else:
            args = ["-m", "pip", "install", "--upgrade"]
        if userSite:
            args.append("--user")
        args += packages
        dia = PipDialog(self.tr('Upgrade Packages'))
        res = dia.startProcess(interpreter, args)
        if res:
            dia.exec()
        return res
    
    def installPackages(self, packages, venvName="", userSite=False,
                        interpreter="", forceReinstall=False):
        """
        Public method to install the given list of packages.
        
        @param packages list of packages to install
        @type list of str
        @param venvName name of the virtual environment to be used
        @type str
        @param userSite flag indicating an install to the user install
            directory
        @type bool
        @param interpreter interpreter to be used for execution
        @type str
        @param forceReinstall flag indicating to force a reinstall of
            the packages
        @type bool
        """
        if venvName:
            interpreter = self.getVirtualenvInterpreter(venvName)
            if not interpreter:
                return
        
        if interpreter:
            if Preferences.getPip("PipSearchIndex"):
                indexUrl = Preferences.getPip("PipSearchIndex") + "/simple"
                args = ["-m", "pip", "install", "--index-url", indexUrl]
            else:
                args = ["-m", "pip", "install"]
            if userSite:
                args.append("--user")
            if forceReinstall:
                args.append("--force-reinstall")
            args += packages
            dia = PipDialog(self.tr('Install Packages'))
            res = dia.startProcess(interpreter, args)
            if res:
                dia.exec()
    
    def installRequirements(self, venvName):
        """
        Public method to install packages as given in a requirements file.
        
        @param venvName name of the virtual environment to be used
        @type str
        """
        from .PipFileSelectionDialog import PipFileSelectionDialog
        dlg = PipFileSelectionDialog(self, "requirements")
        if dlg.exec() == QDialog.DialogCode.Accepted:
            requirements, user = dlg.getData()
            if requirements and os.path.exists(requirements):
                interpreter = self.getVirtualenvInterpreter(venvName)
                if not interpreter:
                    return
                
                if Preferences.getPip("PipSearchIndex"):
                    indexUrl = Preferences.getPip("PipSearchIndex") + "/simple"
                    args = ["-m", "pip", "install", "--index-url", indexUrl]
                else:
                    args = ["-m", "pip", "install"]
                if user:
                    args.append("--user")
                args += ["--requirement", requirements]
                dia = PipDialog(self.tr('Install Packages from Requirements'))
                res = dia.startProcess(interpreter, args)
                if res:
                    dia.exec()
    
    def uninstallPackages(self, packages, venvName):
        """
        Public method to uninstall the given list of packages.
        
        @param packages list of packages to uninstall
        @type list of str
        @param venvName name of the virtual environment to be used
        @type str
        @return flag indicating a successful execution
        @rtype bool
        """
        res = False
        if packages and venvName:
            from UI.DeleteFilesConfirmationDialog import (
                DeleteFilesConfirmationDialog
            )
            dlg = DeleteFilesConfirmationDialog(
                self.parent(),
                self.tr("Uninstall Packages"),
                self.tr(
                    "Do you really want to uninstall these packages?"),
                packages)
            if dlg.exec() == QDialog.DialogCode.Accepted:
                interpreter = self.getVirtualenvInterpreter(venvName)
                if not interpreter:
                    return False
                args = ["-m", "pip", "uninstall", "--yes"] + packages
                dia = PipDialog(self.tr('Uninstall Packages'))
                res = dia.startProcess(interpreter, args)
                if res:
                    dia.exec()
        return res
    
    def uninstallRequirements(self, venvName):
        """
        Public method to uninstall packages as given in a requirements file.
        
        @param venvName name of the virtual environment to be used
        @type str
        """
        if venvName:
            from .PipFileSelectionDialog import PipFileSelectionDialog
            dlg = PipFileSelectionDialog(self, "requirements",
                                         install=False)
            if dlg.exec() == QDialog.DialogCode.Accepted:
                requirements, _user = dlg.getData()
                if requirements and os.path.exists(requirements):
                    try:
                        with open(requirements, "r") as f:
                            reqs = f.read().splitlines()
                    except OSError:
                        return
                    
                    from UI.DeleteFilesConfirmationDialog import (
                        DeleteFilesConfirmationDialog
                    )
                    dlg = DeleteFilesConfirmationDialog(
                        self.parent(),
                        self.tr("Uninstall Packages"),
                        self.tr(
                            "Do you really want to uninstall these packages?"),
                        reqs)
                    if dlg.exec() == QDialog.DialogCode.Accepted:
                        interpreter = self.getVirtualenvInterpreter(venvName)
                        if not interpreter:
                            return
                        
                        args = ["-m", "pip", "uninstall", "--requirement",
                                requirements]
                        dia = PipDialog(
                            self.tr('Uninstall Packages from Requirements'))
                        res = dia.startProcess(interpreter, args)
                        if res:
                            dia.exec()
    
    def getIndexUrl(self):
        """
        Public method to get the index URL for PyPI.
        
        @return index URL for PyPI
        @rtype str
        """
        indexUrl = (
            Preferences.getPip("PipSearchIndex") + "/simple"
            if Preferences.getPip("PipSearchIndex") else
            Pip.DefaultIndexUrlSimple
        )
        
        return indexUrl
    
    def getIndexUrlPypi(self):
        """
        Public method to get the index URL for PyPI API calls.
        
        @return index URL for XML RPC calls
        @rtype str
        """
        indexUrl = (
            Preferences.getPip("PipSearchIndex") + "/pypi"
            if Preferences.getPip("PipSearchIndex") else
            Pip.DefaultIndexUrlPypi
        )
        
        return indexUrl
    
    def getIndexUrlSearch(self):
        """
        Public method to get the index URL for PyPI API calls.
        
        @return index URL for XML RPC calls
        @rtype str
        """
        indexUrl = (
            Preferences.getPip("PipSearchIndex") + "/search/"
            if Preferences.getPip("PipSearchIndex") else
            Pip.DefaultIndexUrlSearch
        )
        
        return indexUrl
    
    def getInstalledPackages(self, envName, localPackages=True,
                             notRequired=False, usersite=False):
        """
        Public method to get the list of installed packages.
        
        @param envName name of the environment to get the packages for
        @type str
        @param localPackages flag indicating to get local packages only
        @type bool
        @param notRequired flag indicating to list packages that are not
            dependencies of installed packages as well
        @type bool
        @param usersite flag indicating to only list packages installed
            in user-site
        @type bool
        @return list of tuples containing the package name and version
        @rtype list of tuple of (str, str)
        """
        packages = []
        
        if envName:
            interpreter = self.getVirtualenvInterpreter(envName)
            if interpreter:
                args = [
                    "-m", "pip",
                    "list",
                    "--format=json",
                ]
                if localPackages:
                    args.append("--local")
                if notRequired:
                    args.append("--not-required")
                if usersite:
                    args.append("--user")
                
                if Preferences.getPip("PipSearchIndex"):
                    indexUrl = Preferences.getPip("PipSearchIndex") + "/simple"
                    args += ["--index-url", indexUrl]
                
                proc = QProcess()
                proc.start(interpreter, args)
                if proc.waitForStarted(15000) and proc.waitForFinished(30000):
                    output = str(proc.readAllStandardOutput(),
                                 Preferences.getSystem("IOEncoding"),
                                 'replace').strip()
                    try:
                        jsonList = json.loads(output)
                    except Exception:
                        jsonList = []
                    
                    for package in jsonList:
                        if isinstance(package, dict):
                            packages.append((
                                package["name"],
                                package["version"],
                            ))
           
        return packages
    
    def getOutdatedPackages(self, envName, localPackages=True,
                            notRequired=False, usersite=False):
        """
        Public method to get the list of outdated packages.
        
        @param envName name of the environment to get the packages for
        @type str
        @param localPackages flag indicating to get local packages only
        @type bool
        @param notRequired flag indicating to list packages that are not
            dependencies of installed packages as well
        @type bool
        @param usersite flag indicating to only list packages installed
            in user-site
        @type bool
        @return list of tuples containing the package name, installed version
            and available version
        @rtype list of tuple of (str, str, str)
        """
        packages = []
        
        if envName:
            interpreter = self.getVirtualenvInterpreter(envName)
            if interpreter:
                args = [
                    "-m", "pip",
                    "list",
                    "--outdated",
                    "--format=json",
                ]
                if localPackages:
                    args.append("--local")
                if notRequired:
                    args.append("--not-required")
                if usersite:
                    args.append("--user")
                
                if Preferences.getPip("PipSearchIndex"):
                    indexUrl = Preferences.getPip("PipSearchIndex") + "/simple"
                    args += ["--index-url", indexUrl]
                
                proc = QProcess()
                proc.start(interpreter, args)
                if proc.waitForStarted(15000) and proc.waitForFinished(30000):
                    output = str(proc.readAllStandardOutput(),
                                 Preferences.getSystem("IOEncoding"),
                                 'replace').strip()
                    try:
                        jsonList = json.loads(output)
                    except Exception:
                        jsonList = []
                    
                    for package in jsonList:
                        if isinstance(package, dict):
                            packages.append((
                                package["name"],
                                package["version"],
                                package["latest_version"],
                            ))
           
        return packages
    
    def checkPackageOutdated(self, packageStart, envName):
        """
        Public method to check, if a group of packages is outdated.
        
        @param packageStart start string for package names to be checked
            (case insensitive)
        @type str
        @param envName name of the environment to get the packages for
        @type str
        @return tuple containing a flag indicating outdated packages and the
            list of tuples containing the package name, installed version
            and available version
        @rtype tuple of (bool, (str, str, str))
        """
        filteredPackages = []
        
        if bool(envName) and bool(packageStart):
            packages = self.getOutdatedPackages(envName)
            filterStr = packageStart.lower()
            filteredPackages = [
                p for p in packages
                if p[0].lower().startswith(filterStr)]
        
        return bool(filteredPackages), filteredPackages
    
    def getPackageDetails(self, name, version):
        """
        Public method to get package details using the PyPI JSON interface.
        
        @param name package name
        @type str
        @param version package version
        @type str
        @return dictionary containing PyPI package data
        @rtype dict
        """
        result = {}
        
        if name and version:
            url = "{0}/{1}/{2}/json".format(
                self.getIndexUrlPypi(), name, version)
            request = QNetworkRequest(QUrl(url))
            reply = self.__networkManager.get(request)
            while not reply.isFinished():
                QCoreApplication.processEvents()
                QThread.msleep(100)
            
            reply.deleteLater()
            if reply.error() == QNetworkReply.NetworkError.NoError:
                data = str(reply.readAll(),
                           Preferences.getSystem("IOEncoding"),
                           'replace')
                with contextlib.suppress(Exception):
                    result = json.loads(data)
        
        return result
    
    def getPackageVersions(self, name):
        """
        Public method to get a list of versions available for the given
        package.
        
        @param name package name
        @type str
        @return list of available versions
        @rtype list of str
        """
        result = []
        
        if name:
            url = "{0}/{1}/json".format(self.getIndexUrlPypi(), name)
            request = QNetworkRequest(QUrl(url))
            reply = self.__networkManager.get(request)
            while not reply.isFinished():
                QCoreApplication.processEvents()
                QThread.msleep(100)
            
            reply.deleteLater()
            if reply.error() == QNetworkReply.NetworkError.NoError:
                dataStr = str(reply.readAll(),
                              Preferences.getSystem("IOEncoding"),
                              'replace')
                with contextlib.suppress(Exception):
                    data = json.loads(dataStr)
                    result = list(data["releases"].keys())
        
        return result
    
    def getFrozenPackages(self, envName, localPackages=True, usersite=False,
                          requirement=None):
        """
        Public method to get the list of package specifiers to freeze them.
        
        @param envName name of the environment to get the package specifiers
            for
        @type str
        @param localPackages flag indicating to get package specifiers for
            local packages only
        @type bool
        @param usersite flag indicating to get package specifiers for packages
            installed in user-site only
        @type bool
        @param requirement name of a requirements file
        @type str
        @return list of package specifiers
        @rtype list of str
        """
        specifiers = []
        
        if envName:
            interpreter = self.getVirtualenvInterpreter(envName)
            if interpreter:
                args = [
                    "-m", "pip",
                    "freeze",
                ]
                if localPackages:
                    args.append("--local")
                if usersite:
                    args.append("--user")
                if requirement and os.path.exists(requirement):
                    args.append("--requirement")
                    args.append(requirement)
                
                success, output = self.runProcess(args, interpreter)
                if success and output:
                    specifiers = [spec.strip() for spec in output.splitlines()
                                  if spec.strip()]
        
        return specifiers
    
    #######################################################################
    ## Cache handling methods below
    #######################################################################
    
    def showCacheInfo(self, venvName):
        """
        Public method to show some information about the pip cache.
        
        @param venvName name of the virtual environment to be used
        @type str
        """
        if venvName:
            interpreter = self.getVirtualenvInterpreter(venvName)
            if interpreter:
                args = ["-m", "pip", "cache", "info"]
                dia = PipDialog(self.tr("Cache Info"))
                res = dia.startProcess(interpreter, args, showArgs=False)
                if res:
                    dia.exec()
    
    def cacheList(self, venvName):
        """
        Public method to list files contained in the pip cache.
        
        @param venvName name of the virtual environment to be used
        @type str
        """
        if venvName:
            interpreter = self.getVirtualenvInterpreter(venvName)
            if interpreter:
                pattern, ok = QInputDialog.getText(
                    None,
                    self.tr("List Cached Files"),
                    self.tr("Enter a file pattern (empty for all):"),
                    QLineEdit.EchoMode.Normal)
                
                if ok:
                    args = ["-m", "pip", "cache", "list"]
                    if pattern.strip():
                        args.append(pattern.strip())
                    dia = PipDialog(self.tr("List Cached Files"))
                    res = dia.startProcess(interpreter, args,
                                           showArgs=False)
                    if res:
                        dia.exec()
    
    def cacheRemove(self, venvName):
        """
        Public method to remove files from the pip cache.
        
        @param venvName name of the virtual environment to be used
        @type str
        """
        if venvName:
            interpreter = self.getVirtualenvInterpreter(venvName)
            if interpreter:
                pattern, ok = QInputDialog.getText(
                    None,
                    self.tr("Remove Cached Files"),
                    self.tr("Enter a file pattern:"),
                    QLineEdit.EchoMode.Normal)
                
                if ok and pattern.strip():
                    args = ["-m", "pip", "cache", "remove", pattern.strip()]
                    dia = PipDialog(self.tr("Remove Cached Files"))
                    res = dia.startProcess(interpreter, args,
                                           showArgs=False)
                    if res:
                        dia.exec()
    
    def cachePurge(self, venvName):
        """
        Public method to remove all files from the pip cache.
        
        @param venvName name of the virtual environment to be used
        @type str
        """
        if venvName:
            interpreter = self.getVirtualenvInterpreter(venvName)
            if interpreter:
                ok = EricMessageBox.yesNo(
                    None,
                    self.tr("Purge Cache"),
                    self.tr("Do you really want to purge the pip cache? All"
                            " files need to be downloaded again."))
                if ok:
                    args = ["-m", "pip", "cache", "purge"]
                    dia = PipDialog(self.tr("Purge Cache"))
                    res = dia.startProcess(interpreter, args,
                                           showArgs=False)
                    if res:
                        dia.exec()
    
    #######################################################################
    ## Dependency tree handling methods below
    #######################################################################
    
    def getDependecyTree(self, envName, localPackages=True, usersite=False,
                         reverse=False):
        """
        Public method to get the dependency tree of installed packages.
        
        @param envName name of the environment to get the packages for
        @type str
        @param localPackages flag indicating to get the tree for local
            packages only
        @type bool
        @param usersite flag indicating to get the tree for packages
            installed in user-site directory only
        @type bool
        @param reverse flag indicating to get the dependency tree in
            reverse order (i.e. list packages needed by other)
        @type bool
        @return list of nested dictionaries resembling the requested
            dependency tree
        @rtype list of dict
        """
        dependencies = []
        
        if envName:
            interpreter = self.getVirtualenvInterpreter(envName)
            if interpreter:
                args = [
                    "-m", "pipdeptree",
                    "--json-tree",
                    "--python", interpreter,
                ]
                if localPackages:
                    args.append("--local-only")
                if usersite:
                    args.append("--user-only")
                if reverse:
                    args.append("--reverse")
                
                proc = QProcess()
                proc.start(Globals.getPythonExecutable(), args)
                if proc.waitForStarted(15000) and proc.waitForFinished(30000):
                    output = str(proc.readAllStandardOutput(),
                                 Preferences.getSystem("IOEncoding"),
                                 'replace').strip()
                    with contextlib.suppress(json.JSONDecodeError):
                        dependencies = json.loads(output)
        
        return dependencies
    
    #######################################################################
    ## License handling methods below
    #######################################################################
    
    def getLicenses(self, envName, localPackages=True, usersite=False,
                    summary=False):
        """
        Public method to get the licenses per package for a given environment.
        
        @param envName name of the environment to get the licenses for
        @type str
        @param localPackages flag indicating to get the licenses for local
            packages only
        @type bool
        @param usersite flag indicating to get the licenses for packages
            installed in user-site directory only
        @type bool
        @param summary flag indicating to get a summary listing (defaults to
            False)
        @type bool (optional)
        @return list of dictionaries containing the license and version per
            package
        @rtype dict
        """
        licenses = []
        
        if envName:
            interpreter = self.getVirtualenvInterpreter(envName)
            if interpreter:
                from . import piplicenses
                with open(piplicenses.__file__, "r") as f:
                    content = f.read()
                args = [
                    "-c",
                    content,
                    "--from",
                    "mixed",
                    "--with-system",
                    "--with-authors",
                    "--with-urls",
                    "--with-description",
                ]
                if localPackages:
                    args.append("--local-only")
                if usersite:
                    args.append("--user-only")
                if summary:
                    args.append("--summary")
                
                proc = QProcess()
                proc.start(interpreter, args)
                if proc.waitForStarted(15000) and proc.waitForFinished(30000):
                    output = str(proc.readAllStandardOutput(),
                                 Preferences.getSystem("IOEncoding"),
                                 'replace').strip()
                    with contextlib.suppress(json.JSONDecodeError):
                        licenses = json.loads(output)
        
        return licenses
    
    def getLicensesSummary(self, envName, localPackages=True, usersite=False):
        """
        Public method to get a summary of licenses found in a given
        environment.
        
        @param envName name of the environment to get the licenses summary for
        @type str
        @param localPackages flag indicating to get the licenses summary for
            local packages only
        @type bool
        @param usersite flag indicating to get the licenses summary for
            packages installed in user-site directory only
        @type bool
        @return list of dictionaries containing the license and the count of
            packages
        @rtype dict
        """
        return self.getLicenses(envName, localPackages=localPackages,
                                usersite=usersite, summary=True)
