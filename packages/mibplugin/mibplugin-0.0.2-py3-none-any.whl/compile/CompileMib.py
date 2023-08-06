from pysnmp.smi import compiler
from pysmi.parser.dialect import smiV1Relaxed
from pysmi.codegen.pysnmp import PySnmpCodeGen
from pysmi.borrower.pyfile import PyFileBorrower
from pysmi.writer.pyfile import PyFileWriter
from pysmi.reader.url import getReadersFromUrls
from pysmi.searcher.stub import StubSearcher
from pysmi.searcher.pypackage import PyPackageSearcher
from pysnmp.smi.builder import DirMibSource, MibBuilder
from pyasn1.error import PyAsn1Error
from pysnmp.smi.error import MibNotFoundError
from pysnmp.debug import Debug

debug_log = Debug()


DEFAULT_SOURCES = []
DEFAULT_DEST = []
DEFAULT_BORROWERS = []

baseMibs = PySnmpCodeGen.baseMibs

class CompileMib:

    def __init__(self):

        self._mibSources = []
        self._mibDestination = None
        self._asn1sources = []
        self._mibBuilder = MibBuilder()

    def AsnSources(self, sources = []):
        for each_source in sources:
            if each_source not in self._asn1sources:
                self._asn1sources.append(each_source)

    def removeAsn1Sources(self, sources = []):
        for each_source in sources:
            if each_source in self._asn1sources:
                self._asn1sources.remove(each_source)

    def addPyMibSource(self, sources = []):

        for each_source in sources:
            if DirMibSource(each_source) not in self._mibSources:
                self._mibSources.append(DirMibSource(each_source))

    def removePyMibsource(self, sources = []):

        for each_source in sources:
            if DirMibSource(each_source) in self._mibSources:
                self._mibSources.remove(DirMibSource(each_source))

    def __prepareMibCompiler(self, **kwargs):
        """
        Mib compiler code -
        Author - Illya Etingof

        Derivative work
        """

        compiler.addMibCompiler(self._mibBuilder, sources=kwargs.get('sources', []), destination=kwargs.get('destination'))

    def compileMib(self, mib_names = [], **kwargs):

        for each_mib in mib_names:
            try:
                self.__prepareMibCompiler(**kwargs)
                print(kwargs.get('sources'))
                print(kwargs.get('destination'))
                status_compile = self._mibBuilder.getMibCompiler().compile(each_mib)
                print(status_compile)
                if status_compile[each_mib] == 'failed':
                    return False
                else:
                    return True
            except PyAsn1Error as error_compile:
                debug_log("Error in compilation in %s and error is %s"%(each_mib, error_compile))
                return False

    def loadMib(self, mib_path, mib_names = []):

        self.addPyMibSource(sources=[mib_path])
        self._mibBuilder.addMibSources(*self._mibSources)

        try:
            self._mibBuilder.loadModules(*mib_names)

        except (PyAsn1Error, MibNotFoundError) as err:
            did_compile = self.compileMib(mib_names=mib_names, sources=self._asn1sources, destination=mib_path)

            if not did_compile:
                raise PyAsn1Error("Unable to compile mibs")

            self._mibBuilder.loadModules(*mib_names)

    def getMibBuilder(self):
        return self._mibBuilder





