"""Popdyn.py: population dynamics facilities. """

from __future__ import division
import logging
from ipdt.tournament import tournament
import random 
logger = logging.getLogger("ipdt")


def new_proportions(proportions,payoffs):
    """Compute the new proportion of each strategy given the old
    proportion and the payoff matrix
    
    Args:
         proportions (list): proportion of each strategy.
         payoff (dict of dict): payoff of strategy i against j in the tournament.
    Returns:
         (list): new proportion of each strategy.

    """
    payoff_w = {} # Payoff weighted by proportions.
    out = {} # New proportions 
    
    for i,ai in proportions.items():
        payoff_w[i] = sum([ai*aj*payoffs[i][j]
                           for j,aj in proportions.items()])

    total = sum([aj*payoff_w[j] for j,aj in proportions.items()])

    for i,ai in proportions.items():
        out[i] = (ai * payoff_w[i]/total)
    return out


def mutation(proportions,mu=1e-2):
    N = len(proportions)

    # Get a random partition of the unit segment:
    mt = sorted([random.random() for x in range(N-1)]) + [1]
    mt = [mt[0]*mu] + [(x-y)*mu for x,y in zip(mt[1:],mt[:-1])]
        
    # Take the opposite 
    mmt = [-x for x in mt]

    # Suffle everything
    random.shuffle(mt)
    random.shuffle(mmt)

    # Add to each proportion a positive and a negative number
    # so the sum of proportion does not change.
    for k,p,m in zip(proportions.keys(),mt,mmt):
        proportions[k] += p - m

    return proportions

def normalize_po(payoffs):
    out = {}
    order = payoffs.keys()
    max_po = max([max(payoffs[k].values()) for k in order])
    min_po = min([min(payoffs[k].values()) for k in order])
    
    norm = lambda x: int(100*(x - min_po) / (max_po-min_po)) if (max_po-min_po) else x

    for k in order:
        out[k] = {}
        for j in order:
            out[k][j] = norm(payoffs[k][j])
    return out 

def popdyn(players,param):

    # Strategies start in equiproportion.
    proportions = dict([(P.name, 1/len(players)) for P in players])
    # General payoff as given by the tournament.
    _,payoffs = tournament(players,param)

    payoffs = normalize_po(payoffs)
    
    time_series = dict([(k,[v]) for k,v in proportions.items()])
    for g in range(param["generations"]):
        proportions = mutation(new_proportions(proportions,payoffs),param["mu"])
        for k,v in proportions.items():
            time_series[k].append(v)
        logger.debug("{}\n{}\n\n".format(g,",\n".join(["{1:<6.0%} {0}".format(n,x)
                                                       for n,x in proportions.items()])))

    print "Population dynamics ended: {} generations.".format(g+1)
    print "\n".join(["{1:<6.1%} {0}".format(n,x)
                     for n,x in proportions.items()])
            
    return time_series,payoffs
