# -*- coding: utf-8 -*-
from __future__ import division
import ipdt.player

# D'abord, des réponses générales à tes questions :
# __init__ et play sont des fonctions un peu spéciales appelées "méthodes".
# En gros ce sont des fonctions comme les autres à la différence près qu'elles
# ont accès aux attributs (les cases mémoire) de l'objet "Player". Ca permet
# de diminuer la taille du code en évitant de passer les cases mémoire
# en argument aux fonctions -- on pourra directement y accéder grace à la
# notation "self.nom_de_la_case_mémoire". Tu peux checker le code ci-dessous
# pour des exemples.
# 
# Donc play est une méthode comme une autre, on la définit en écrivant
# "def play(argument1, argument2, ..., argumentn) : comme une brave fonction.
# Sauf que comme on le fait dans le corps de la définition d'une classe, on
# lui donne la propriété spéciale d'être une méthode et de pouvoir accéder aux
# attributs de l'objet, modifier leur contenu, etc...
#
# __init__ par contre est une méthode un peu spéciale : elle est utiliser pour
# instancier l'object, c'est à dire pour le créer. En gros : elle sert à
# initialiser les attribus de l'objet.

class Player(ipdt.player.Player):
      """Begginer: Coopération garantie dans 75% des cas."""
      name="Begginer"
      author="Marc Oudart"

      def __init__(self, param):

          # True et False sont des mots réservés en Python, il ne faut donc pas
          # les redéfinir. C'est un peu comme si tu redéfinissais 0 ou 1. Du
          # coup, on va leur donner un autre nom.
          self.nb_true = 0
          self.nb_false = 0

          # Quand tu définie un attribu en écrivant "self.a", tu demandes juste
          # à l'object qu'est ton joueur de créer une case mémoire pour stocker
          # une valeur appelée "a". Donc si tu écris quelque chose comme
          # self.a = True dans la fonction __init__, alors quand tu rappeleras
          # self.a il te renverra la valeur "vraie", et pas une fonction.
          # Pour faire ce que tu veux faire (incrémenter un compteur), il
          # existes deux manières de faire :
          # 1. écrire directement :
          #    self.compteur += 1
          # à l'endroit du code où tu veux que ton compteur soit incrémenté
          # 2. définir une fonction liée à l'object appelée méthode qui
          # incrémente le compteur quand tu l'appelles. La solution 2 permet
          # de faire moins d'erreurs en programmant, mais comme ici c'est un
          # petit programme simple et que la solution 2 est un tout petit peu
          # plus compliquée à expliquer, on va se contenter de la 1 (ceci dit,
          # c'est TRES bien que tu aies raisonné en terme de "j'incrémente le
          # compteur en appelant une fonction dédiée plutôt qu'en le faisant à
          # la main", donc ça m'embête vraiment de te recommander la solution 1)
	  
      def play(self, last_move):
      	  if last_move == None : 
             # Après l'instruction "return", on sort de la fonction ! Donc si
             # tu veux que ton code soit exécuté, il faut le mettre avant
             # cette instruction.
	     self.nb_false += 1
	     return False
          # J'ai remplacé le "if" par un "elif" (else if). Ca fait pas de
          # différence ici mais c'est plus logique, et plus facile à lire.
          elif self.nb_true / self.nb_false < 0.75 :
             self.nb_true += 1
	     return True
	  else :
             self.nb_false += 1
	     return False
