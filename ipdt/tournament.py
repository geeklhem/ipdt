from __future__ import division
import logging
import itertools 
logger = logging.getLogger("ipdt")


DEFAULT_PARAM = {
    "T": 100, # Number of iterations
    "cc": 1, # Payoff if I cooperated and the other too
    "cd": -1, # Payoff if I cooperated but the other defected
    "dc": 2, # Payoff if I defected and the other cooperated
    "dd": 0, # Payoff if everyone defected
    "replicas":3,
}


def tournament(players,param):
    """ A simple tournament.
    Args: 
        players (list): The list of player's classes.
        param (dict) Match parameters.

    Returns: 
        (list): ranked of players (score,name) 
    """
    for k,v in DEFAULT_PARAM.items():
        if k not in param:
            param[k] = v
            logger.debug("Parameter {} set to default value: {}".format(k,v))
        else:
            logger.debug("Parameter {} set to value: {}".format(k,param[k]))

    
    pl = {}
    points = {}
    for p in players:
        if p.name not in pl:
            pl[p.name] = p
            points[p.name] = 0
        else:
            raise ValueError("Two players have the same name.")

    for i in range(param["replicas"]):
        for P in pl.keys():
            try:
                payoff = match(pl[P],pl[P],param)
            except Exception as e:
                logger.critical("{0} throw an exception playing against itself : {} ".format(P,e))
            else:
                points[P] += payoff[0] + payoff[1]
                logger.info("{0} against itself ({1}pts)".format(P,points[P]))

                            
        for P1,P2 in itertools.combinations(pl.keys(),2):

            payoff = match(pl[P1],pl[P2],param)          

            points[P1] += payoff[0]
            points[P2] += payoff[1]

            
            logger.info("{0} ({2}pts) vs {1} ({3}pts)".format(P1,P2,
                                                              payoff[0],payoff[1]))        

    # Sort the players by their points ranking
    ranking = [(v,k) for k,v in points.items()]
    ranking = sorted(ranking,key=lambda x:-x[0])

    return ranking


def match(Player1Class,Player2Class,param):
    """ A simple match between two players
    Args:
        Player1class (class inherited from ipdt.player.Player): First player
        Player2class (class inherited from ipdt.player.Player): Second player
        param (dict): Match parameters, T is the number of moves. 

    Returns:
        (tuple) tuple of payoffs (player1,player2)
    """
    
    for k,v in DEFAULT_PARAM.items():
        if k not in param:
            param[k] = v
            logger.debug("Parameter {} set to default value: {}".format(k,v))


    player1 = Player1Class(param)
    player2 = Player2Class(param)


    p1, p2 = None, None
    payoff = [0,0]
    for turn in range(param["T"]):

        # Let them play
        newp1 = player1.play(p2)
        newp2 = player2.play(p1)      
        p1,p2 = newp1, newp2

        # Compute payoff
        if p1:
            p1_char = "c"
        else:
            p1_char = "d"
        if p2:
            p2_char = "c"
        else:
            p2_char = "d"

        payoff[0] += param[p1_char+p2_char]
        payoff[1] += param[p2_char+p1_char]

    return payoff 
