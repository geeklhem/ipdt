"""In this modules, each player is stored as a submodule with a
"Player" class inheriting from ipdt.player.Player.

This __init__ files load all the submodules in the ipdt.players
namespace.
"""
import pkgutil
import logging
logger = logging.getLogger("ipdt")

__all__ = []

for loader, module_name, is_pkg in  pkgutil.iter_modules(__path__):
    try:
        __import__("ipdt.players."+module_name)
    except Exception as e:
        logger.critical("Strategy {} thrown an exception on import: {}.".format(module_name,e))
    else:
        __all__.append(module_name)

logger.debug("loaded {} players: {}".format(len(__all__),__all__))
