# -*- coding: utf-8 -*- #
"""
    ***** Client Pur beurre *****
  Rappel des actions disponibles auxquelles ce menu fait appel
  via le service 'pur_beurre.py' :
  -gpi GET_PRODUCT_BY_ID, --get_product_by_id GET_PRODUCT_BY_ID
                        Get product object by id
  -gci GET_CATEGORY_BY_ID, --get_category_by_id GET_CATEGORY_BY_ID
                        Get category object by id
  -gcl, --get_category_list
                        Get category list
  -gplc GET_PRODUCT_LIST_BY_CATEGORY_ID, --get_product_list_by_category_id
                        GET_PRODUCT_LIST_BY_CATEGORY_ID
                        Get product list by category_id
  -gpsl GET_PRODUCTS_SUBST_LIST, --get_products_subst_list
                        GET_PRODUCTS_SUBST_LIST
                        Get product subsitute list by id
  -gplm GET_PRODUCTS_LIST_BY_MATCH, --get_products_list_by_match
                        GET_PRODUCTS_LIST_BY_MATCH
                        Get product by match on key words between the names of
                        products or categories. Wildcad '*' is allowed.
  -ssp SET_SUBSTITUTE_PRODUCT, --set_substitute_product SET_SUBSTITUTE_PRODUCT
                        Set relation product,substitute by id
  -gsp, --get_recorded_substitutes_product
                        Get recorded substitutes list
  -r, --reload          Reload database from Openfactsfood services

# note l'"import" du module "os" est necessaire pour le code des fct eval()
"""

from __future__ import print_function
import os
import sys

SERVICE_PB = './pur_beurre.py'
CURR_PYTHON = sys.executable

TRANSITIONS_POSSIBLES = {
    'A': {'Label': 'Acceder au menu principal',
          'Trigger': ''},
    'B': {'Label': 'Recharger la base',
          'Trigger':
              'os.system("{} {} -r")'.format(
                  CURR_PYTHON, SERVICE_PB)},
    'C': {'Label': 'Lister les categories',
          'Trigger':
              'os.system("{} {} -gcl")'.format(
                  CURR_PYTHON, SERVICE_PB)},
    'D': {'Label': 'Lister les produits d\'une categorie',
          'Trigger':
              'os.system("{} {} -gplc _curr_category_")'.format(
                  CURR_PYTHON, SERVICE_PB),
          'InputValues': {'curr_category': 'un identifiant categorie'}},
    'E': {'Label': 'Lister les produits par mots clés',
          'Trigger':
              'os.system("{} {} -gplm _key_words_")'.format(
                  CURR_PYTHON, SERVICE_PB),
          'InputValues': {'key_words': 'les mot(s)'
                                       ' clé(s) wildcard "*" accepté'}},
    'F': {'Label': 'Afficher le détail d\'une categorie',
          'Trigger': 'os.system("{} {} -gci _curr_category_")'.format(
              CURR_PYTHON, SERVICE_PB),
          'InputValues': {'curr_category': 'un identifiant categorie'}},
    'G': {'Label': 'Afficher le détail d\'un produit',
          'Trigger': 'os.system("{} {} -gpi _curr_product_")'.format(
              CURR_PYTHON, SERVICE_PB),
          'InputValues': {'curr_product': 'un identifiant produit'}},
    'H': {'Label': 'Sélectionner un produit par son ean',
          'Trigger': ''},
    'I': {'Label': 'Enregistrer un produit de susbstitution',
          'Trigger':
              'os.system("{} {} -ssp _curr_product_,_curr_subsitution_")'
              .format(CURR_PYTHON, SERVICE_PB),
          'InputValues': {'curr_subsitution': 'un identifiant subtitution'},
          'LastValues': {'curr_product': 'Identifiant produit'}},
    'J': {'Label': 'Enregistrer un produit à subsituer',
          'Trigger':
              'curr_product = registered_values[\'un identifiant produit\']'},
    'K': {'Label': 'Lister les susbstitutions pour un produit',
          'Trigger': 'os.system("{} {} -gpsl _curr_product_")'.format(
              CURR_PYTHON, SERVICE_PB),
          'InputValues': {'curr_product': 'un identifiant produit'}},
    'L': {'Label': 'Lister les susbstitutions pour ce produit',
          'Trigger': 'os.system("{} {} -gpsl _curr_product_")'.format(
              CURR_PYTHON, SERVICE_PB),
          'LastValues': {'curr_product': 'Identifiant produit'}},
    'M': {'Label': 'Lister la base de substitutions',
          'Trigger': 'os.system("{} {} -gsp")'.format(
              CURR_PYTHON, SERVICE_PB)},
    'N': {'Label': 'Quitter',
          'Trigger': 'sys.exit()'},
    'O': {'Label': 'Revenir au menu principal',
          'Trigger': ''},
    'P': {'Label': 'Lister les produits de cette catégorie',
          'Trigger': 'os.system("{} {} -gplc _curr_category_")'.format(
              CURR_PYTHON, SERVICE_PB),
          'LastValues': {'curr_category': 'Identifiant catégorie'}}
}

ETATS_POSSIBLES = {
    1: 'Menu principal',
    2: 'Base chargée',
    3: 'Resultat lister les categories',
    4: 'Resultat lister les produits d\'une categorie',
    5: 'Resultat lister les produits par mots clés',
    6: 'Resultat affichage d\'une categorie',
    7: 'Resultat affichage d\'un produit par id',
    8: 'Resultat affichage d\'un produit par ean',
    9: 'Resultat liste de subsitutions pdt en cours',
    10: 'Resultat subsitutions enregistrées',
    11: 'Resultat liste de subsitutions proposées',
    12: 'Resultat affichage de la base de subsitutions',
    13: 'Resultat liste de pdt de la categorie en cours',
    14: 'Bye'
}

PATHS = {
    # menu principal
    (1, 2): 'B',  # recharger base
    (1, 3): 'C',  # Lister categories
    (1, 5): 'E',  # Lister produits par mots clés
    (1, 12): 'M',  # Lister la base des substitutions
    (1, 14): 'N',  # Quitter
    # Base chargee
    (2, 1): 'O',  # revenir au menu principal
    (2, 14): 'N',  # Quitter
    # Lister les categories
    (3, 4): 'D',  # Lister les produits d'une categorie
    (3, 6): 'F',  # Afficher une catégorie par id
    (3, 1): 'O',  # revenir au menu principal
    (3, 14): 'N',  # Quitter
    # Lister  les produits d'une categorie
    (4, 7): 'G',  # Afficher un produit
    (4, 1): 'O',  # revenir au menu principal
    (4, 14): 'N',  # Quitter
    # Lister les produits par mots clés
    (5, 7): 'G',  # Afficher un produit par id
    (5, 1): 'O',  # revenir au menu principal
    (5, 14): 'N',  # Quitter
    # Afficher  les catégories par id
    (6, 13): 'P',  # Lister les produits de la categorie en cours
    (6, 4): 'D',  # Lister les produits d'une categorie
    (6, 1): 'O',  # revenir au menu principal
    (6, 14): 'N',  # Quitter
    # Afficher un produit
    (7, 9): 'L',  # Lister les substitutions du pdt en cours
    (7, 11): 'K',  # Lister les substitutions
    (7, 1): 'O',  # revenir au menu principal
    (7, 14): 'N',  # Quitter
    # Afficher un produit Par Ean
    (8, 9): 'L',  # Lister les substitutions du pdt en cours
    (8, 11): 'K',  # Lister les substitutions
    (8, 1): 'O',  # revenir au menu principal
    (8, 14): 'N',  # Quitter
    # choisir comme subsitituable
    (9, 10): 'I',  # Enregistrer subsitution
    (9, 1): 'O',  # revenir au menu principal
    (9, 14): 'M',  # Quitter
    # choisir comme subsititution
    (10, 12): 'M',  # Lister la base des substitutions
    (10, 1): 'O',  # revenir au menu principal
    (10, 14): 'N',  # Quitter
    # Afficher une liste de subtitution
    (11, 7): 'G',  # Afficher le produit
    (11, 1): 'O',  # revenir au menu principal
    (11, 14): 'N',  # Quitter
    # Afficher la base de subtitution
    (12, 1): 'O',  # revenir au menu principal
    (12, 14): 'N',  # Quitter
    # Afficher une liste de produit de la categorie en cours
    (13, 7): 'G',  # Afficher un produit
    (13, 1): 'O',  # revenir au menu principal
    (13, 14): 'N',  # Quitter

}


class Menu(object):
    """ Menu process """
    transitions = {}
    etats = {}

    @classmethod
    def load(cls):
        """ loads configurtion menu """
        cls.etats = dict()
        for num, etat in ETATS_POSSIBLES.items():
            cls.etats.update({num: Etat(etat)})

        cls.transitions = dict()
        for letter, transition in TRANSITIONS_POSSIBLES.items():
            cls.transitions.update({letter: Transition(transition)})

        cls.root = None
        for path, action in PATHS.items():
            e_from, e_to = path
            node = Menu.etats[e_from]
            node.aller_vers(
                Menu.etats[e_to],
                Menu.transitions[action])
            cls.root = node if cls.root is None else cls.root
        return cls.root

    @classmethod
    def show(cls, entry):
        """ run the configured menu """
        # valeurs colectées
        registered_values = {}

        def process_input(entry, new_trans):
            """ sub process validates choice and executes trigger"""
            nb_choix = len(new_trans)
            choix = None

            if str(entry).isnumeric():
                choix = int(entry) - 1

            if choix in range(0, nb_choix):
                print("Vous avez choisi : {}".format(menu_list[choix]))
                next_trans = new_trans[choix]

                cmd = str(next_trans.params['Trigger'])
                # here we execute the piece of code
                # linked with the selected item menu
                if 'InputValues' in next_trans.params:
                    for val, label in next_trans.params['InputValues'].items():
                        local_val = eval("input('Choisissez " + label + " :')")
                        cmd = cmd.replace('_' + val + '_', local_val)
                        registered_values[val] = local_val
                if 'LastValues' in next_trans.params:
                    for val, label in next_trans.params['LastValues'].items():
                        cmd = cmd.replace('_' + val + '_',
                                          registered_values[val])
                if cmd != "":
                    eval(cmd)
            else:
                print("Choisissez une option entre 1 et {}".format(nb_choix))

            return choix

        next_etat = Menu.etats[entry]
        while True:
            local_dico = next_etat.liaisons
            new_etats = [trans_etat[1] for num, trans_etat
                         in enumerate(local_dico.items())]
            new_trans = [trans_etat[0] for num, trans_etat
                         in enumerate(local_dico.items())]
            menu_list = [str(num + 1) + ': ' + trans_etat[0].params['Label']
                         for num, trans_etat
                         in enumerate(local_dico.items())]
            menu_string = " | ".join(menu_list)
            print("Choisissez l'une des options suivantes :\n[{}]"
                  .format(menu_string))
            entry = input('>>> ')
            choix = process_input(entry, new_trans)
            if choix is not None and choix < len(new_etats):
                next_etat = new_etats[choix]

    @classmethod
    def start(cls, entry):
        """ just show """
        cls.show(entry)

    def __init__(self):
        pass


class Etat(object):
    """ definit les etats du menu"""
    def __init__(self, params):
        """ instancie les etats du menu"""
        if isinstance(params, str):
            self.description = params
            self.liaisons = dict()

    def aller_vers(self, autre_etat, avec_transition):
        """ action permettant de passer à un autre etat """
        avec_transition.lier(self, autre_etat)
        self.liaisons[avec_transition] = autre_etat


class Transition(object):
    """ definit les transitions du menu"""
    def __init__(self, params):
        """ instancie les transitions du menu"""
        self.params = params
        self.transitions = list()

    def lier(self, un_etat, un_autre_etat):
        """ Autorise le passage d'un etat à l'autre """
        self.transitions.append((un_etat, un_autre_etat))


def main():
    """ demarre le menu
    On verifie que le script 'service' est présent en local """
    try:
        f_test = open(SERVICE_PB)
        f_test.close()
    except IOError:
        print("Le fichier {} doit être présent dans"
              " le repertoire courant.".format(SERVICE_PB))
        sys.exit(-1)

    Menu.load()
    Menu.start(1)


if __name__ == '__main__':
    main()
