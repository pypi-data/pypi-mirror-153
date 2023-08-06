import imp
from jdw.mfc.anode.conor import Conor
from jdw.mfc.anode.conor import INACTIVE_STATUSES
from jdw.mfc.anode.conor import STATE

def create_engine(name):
    return Conor(name)