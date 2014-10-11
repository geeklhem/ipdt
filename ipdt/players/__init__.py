"""In this modules, each player is stored as a submodule with a
"Player" class inheriting from ipdt.player.Player"""
import pkgutil
import logging
logger = logging.getLogger("ipdt")

__all__ = []

for loader, module_name, is_pkg in  pkgutil.iter_modules(__path__):  
    __all__.append(module_name)
    __import__("ipdt.players."+module_name)

logger.debug("loaded {} players: {}".format(len(__all__),__all__))
