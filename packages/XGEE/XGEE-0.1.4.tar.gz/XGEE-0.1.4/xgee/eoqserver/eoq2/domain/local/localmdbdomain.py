'''
 2019 Bjoern Annighoefer
'''

from ..cmdrunnerbaseddomain import CmdRunnerBasedDomain
from ...command.commandrunner import CmdRunner
from ...util.logger import NoLogging
from ...serialization import TextSerializer

class LocalMdbDomain(CmdRunnerBasedDomain):
    def __init__(self,mdbAccessor,maxChanges=100,logger=NoLogging(),serializer=TextSerializer(),enableBenchmark=False):
        self.mdbAccessor = mdbAccessor
        self.cmdRunner = CmdRunner(mdbAccessor,maxChanges=maxChanges,logger=logger,enableBenchmark=enableBenchmark)
        super().__init__(self.cmdRunner,logger=logger,serializer=serializer,enableBenchmark=enableBenchmark)
        
        
        
        