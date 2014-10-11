import logging
logger = logging.getLogger("ipdt")


DEFAULT_PARAM = {
    "T": 100, # Number of iterations
    "cc": 10, # Payoff if I cooperated and the other too
    "cd": -5, # Payoff if I cooperated but the other defected
    "dc": 20, # Payoff if I defected and the other cooperated
    "dd": 0, # Payoff if everyone defected 
}


def match(Player1Class,Player2Class,param):
    
    for k,v in DEFAULT_PARAM.items():
        if k not in param:
            param[k] = v
            logger.debug("Parameter {} set to default value: {}".format(k,v))
        else:
            logger.debug("Parameter {} set to value: {}".format(k,param[k]))


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
