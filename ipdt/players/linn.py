# -*- coding: utf-8 -*-
"""LINN (Linn Is a Neural Network) is a strategy for iterated
 prisoner's dilemma tournaments.

You can train it and improve the coefficient by launching this module
with the python command (ipdt must be installed):

$ python linn.py

It will run an infinite number of tournament, mutating slightly one
random coefficient each time. If the rank is better than the previous
best rank, the mutation is kept. (if ranks are equal, scores are compared)

When you are bored or think it is enough you can stop the trainer by
typing Crtl+C. It will output the new best coefficient and exit. You
can now copy and paste the new best coefficient in this file as the
default coefficients.
"""

from __future__ import division 
import ipdt.player
import math

def neuron(inputs,weights,activation_function):
    """An artificial neuron. Get an input, produce an output according to
    its underlying coefficients and activation function.

    Args:
        inputs (list): x_i 
        weights (list): w_i
        activation_function (list):
    Return:
        (float): f(Sum_j w_i*x_j)

    """
    output = 0
    for i,w in zip(inputs,weights):
        output += w*i
    return activation_function(output)

class Player(ipdt.player.Player): 
    """LINN (Linn Is a Neural Network) - A simple neural network of a strategy.

    Linn is a simple neural network with one hidden layer.
    
    Its inputs-neurons are:
    - A biais (1)
    - the proportion of the iteration elapsed
    - the last 3 move of its oponent (Linn has a good memory of the direct past)
    - the proportion of times Linn cooperated
    - the proportion of times its oponent cooperated (Linn has a vague memory 
      of the not so direct past)
    """

    name = "LINN"
    author = "Guilhem Doulcier"

    coefficients =      ([[-0.3101539927586602, 0.07998691022815119, 1.401349642771804, 0.26698205290562665, 2.0501789391524294, 0.730456964559066], [0.7013233982439165, 0.7435895423786191, 0.008362006206010242, 0.7288925032970454, 0.3323849954650683, 0.6828589552154556], [0.9839774323939298, -1.1106792700213513, 0.0794359231940811, 0.07361687522448923, 1.4272289935986653, 0.8465892719590087], [0.3388438236636021, -0.40492712111426743, 0.8006234023032021, 0.45593978729464046, -0.19023138266976025, 0.8114693273816412], [1.0348044261528146, 0.8007503365239114, -0.3093852675339047, 0.1735562059673818, 2.324353723148839, 1.4606036718909077], [1.9328652725456292, 0.7736017313715543, -1.020824807777106, 1.3293263221758589, 0.49807659233952073, 0.17733456763602332]], [[0.5168159070444658, -2.294052680249433, 0.896947032174488, 0.9417332626537528, -0.6135469079951664, 0.6897143157711071]])

    def __init__(self,param):
        self.alter_coop = 0
        self.coop = 0
        self.coups = 0
        self.a = 1
        self.length = param["T"]
        self.last_three = [-1,-1,-1]

        self.coefficients = self.__class__.coefficients
        self.af = ([lambda x:1/(1+math.exp(-self.a*x))]*6,[lambda x:(1/(1+math.exp(-self.a*x)))>0.5])

    def perceptron(self,*inputs):
        """
        An artificial neural network with one hidden layer. 

        Args:
            *inputs (list): The inputs for the first layer of the perceptron.
        Uses:
            self.coefficient[layer][neuron][input] (list): the weights.
            self.af[layer][neuron] (list): the activation functions.
        Returns: 
            (float) the output of the last layer.

        """
        for layer,coefs in enumerate(self.coefficients):
            output = [0] * len(coefs)
            for n,c in enumerate(coefs):
                output[n] = neuron(inputs,
                                   c,
                                   self.af[layer][n])
            inputs = output
        return output[0]

    def play(self,last_move):
        self.coups += 1 

        if self.coups > 1:
            if last_move:
                self.alter_coop += 1
            self.last_three[1:] = self.last_three[:-1]
            self.last_three[0] = last_move
        
        output = self.perceptron(1,
                                 self.coups/self.length,
                                 self.last_three[0],
                                 self.last_three[1],
                                 self.last_three[2],
                                 self.coop/self.coups,
                                 self.alter_coop/self.coups)
        if output:
            self.coop += 1
        return output
        


if __name__ == "__main__":
    import ipdt.tournament
    import pkgutil
    import copy
    import random
    print "~~ Linn Trainer ~~"

    ## LOAD THE OTHERS STRATEGIES 
    code_players = []
    for loader, module_name, is_pkg in  pkgutil.iter_modules("."):
        if module_name != "linn":
            try:
                __import__("ipdt.players."+module_name)
            except Exception as e:
                print("Strategy {} thrown an exception on import: {}.".format(module_name,e))
            else:
                code_players.append(module_name)
    players = [ getattr(ipdt.players, name).Player for name in code_players]
    players.append(Player)

    # INIT SOME VARIABLES 
    score = 0
    n = 0
    best_rank = len(players)+1

    n_neurones = len(Player.coefficients[0]) + len(Player.coefficients[1])
    n_locus = len(Player.coefficients[0][0])

    coef = copy.deepcopy(Player.coefficients)

    while 1: #Infinite loop stoped if we catch a KeyboardInterrupt exception. 
        n+=1
        try:
            ## MUTATE SOMEWHERE
            neurone = random.randint(0, n_neurones-1)
            layer = int(neurone/n_locus)
            neurone = neurone%n_locus
            locus = random.randint(0, n_locus-1)
            Player.coefficients[layer][neurone][locus] += random.normalvariate(0,1)

            ## PLAY A TOURNAMENT 
            ranking,_ = ipdt.tournament.tournament(players,ipdt.tournament.DEFAULT_PARAM)

            ## KEEP THE MUTATION IF THE SCORE IS BETTER 
            for rank,(s,name) in enumerate(ranking):
                if name == Player.name:
                    if rank < best_rank or (rank==best_rank and s>score):
                        score = s
                        best_rank = rank
                        kept = "Kept."
                        coef = copy.deepcopy(Player.coefficients)
                    else:
                        kept = "(Best is {} - {})".format(best_rank+1,score)
                        Player.coefficients = copy.deepcopy(coef)

                    print "Tournament {}, rank {} score {}. {}".format(n,rank+1,s,kept)    
                    break
        except KeyboardInterrupt:
            break
    print "Training ended ! \n New best coefficients:\n {}".format(coef) 
