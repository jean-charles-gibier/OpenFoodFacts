# coding: utf8
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

SERVICE_PB = r'./pur_beurre.py'
CURR_PYTHON = str(sys.executable).replace('\\', '/')

TRANSITIONS_POSSIBLES = {
    'A': {'Label': 'Acceder au menu principal',
          'TriggerAfter': ''},

    'B': {'Label': 'Quel aliment souhaitez vous remplacer ?',
          'TriggerBefore': r'os.system("{} {} -gcl")'.format(
              CURR_PYTHON, SERVICE_PB),
          'InputValues': {'curr_category': 'un identifiant categorie'},
          'TriggerAfter': 'os.system("{} {} -gci _curr_category_")'.format(
              CURR_PYTHON, SERVICE_PB),
          },

    'C': {'Label': 'Retrouver mes aliments substitués',
          'TriggerAfter': r'os.system("{} {} -gsp")'.format(
              CURR_PYTHON, SERVICE_PB)},

    'D': {'Label': 'Sélectionner un produit dans cette catégorie',
          'TriggerBefore': r'os.system("{} {} -gplc _curr_category_")'.format(
              CURR_PYTHON, SERVICE_PB),
          'PreviousValues': {'curr_category': 'Identifiant catégorie'}
          },

    'E': {'Label': 'Sélectionner une autre catégorie',
          'TriggerAfter': 'os.system("{} {} -gci _curr_category_")'.format(
              CURR_PYTHON, SERVICE_PB),
          'InputValues': {'curr_category': 'un autre identifiant categorie'},
          },

    'F': {'Label': 'Sélectionner un produit à substituer',
          'TriggerAfter': 'os.system("{} {} -gpi _curr_product_")'.format(
              CURR_PYTHON, SERVICE_PB),
          'InputValues': {'curr_product': 'un identifiant produit'},
          },

    'G': {'Label': 'Sélectionner un autre produit à substituer',
          'TriggerAfter': 'os.system("{} {} -gpi _curr_product_")'.format(
              CURR_PYTHON, SERVICE_PB),
          'InputValues': {'curr_product': 'un identifiant produit'},
          },

    'H': {'Label': 'Lister les produits de substitution',
          'TriggerBefore': 'os.system("{} {} -gpsl _curr_product_")'.format(
              CURR_PYTHON, SERVICE_PB),
          'PreviousValues': {'curr_product': 'Identifiant produit'}
          },

    'I': {'Label': 'Enregistrer le produit de substitution',
          'TriggerAfter':
              'os.system("{} {} -ssp _curr_product_,_curr_subsitution_")'
                  .format(CURR_PYTHON, SERVICE_PB),
          'InputValues': {'curr_subsitution': 'un identifiant subtitution'},
          'PreviousValues': {'curr_product': 'Identifiant produit'}
          },

    'J': {'Label': 'Lister les produits par mots clés',
          'TriggerAfter':
              'os.system("{} {} -gplm _key_words_")'.format(
                  CURR_PYTHON, SERVICE_PB),
          'InputValues': {'key_words': 'les mot(s)'
                                       ' clé(s) wildcard "*" accepté'}},

    'Z': {'Label': 'Quitter',
          'TriggerAfter': 'sys.exit()'}
}

ETATS_POSSIBLES = {
    1: 'Menu principal',
    2: 'Reponse à Quel élément souhaitez vous remplacer ?',
    3: 'Reponse à Retrouver mes aliments substitués',
    4: 'Reponse à Selectionner categorie, produit demandé',
    5: 'Reponse à Selectionner une autre catégorie',
    6: 'Reponse à rechercher /lister les produits de substitution',
    7: 'Reponse à Selectionner le produit de substitution',
    8: 'Reponse à lister les aliments par mots clés',
    14: 'Bye'
}

PATHS = {
    # menu principal
    (1, 2): 'B',  # Quel aliment souhaitez vous remplacer ?
    (1, 1): 'C',  # Retrouver mes aliments substitués
    (1, 4): 'J',  # Retrouver un aliment par des mots clés
    (1, 14): 'Z',  # Quitter
    # "Quel élément souhaitez vous remplacer" demandé
    (2, 4): 'D',  # Produit demandé dans la categorie courante
    (2, 2): 'E',  # Produit demandé dans une autre catégorie
    (2, 1): 'A',  # revenir au menu principal
    (2, 14): 'Z',  # Quitter
    # Lister  les produits d'une categorie
    (4, 5): 'F',  # Selectionner un produit à subsituer
    (4, 1): 'A',  # revenir au menu principal
    (4, 14): 'Z',  # Quitter
    # selectionner un produit à subsituer
    (5, 6): 'H',  # Rechercher la substitution pour ce produit
    (5, 5): 'G',  # choisir un autre produit a substituer
    (5, 1): 'A',  # revenir au menu principal
    (5, 14): 'Z',  # Quitter
    # Rechercher la substitution pour ce produit
    (6, 7): 'I',  # Enregistrer le produit de substitution
    (6, 1): 'A',  # revenir au menu principal
    (6, 14): 'Z',  # Quitter
    # menu principal (copie) pb de conception du menu :-(
    (7, 2): 'B',  # Quel élément souhaitez vous remplacer ?
    (7, 1): 'C',  # Retrouver mes aliments substitués
    (7, 14): 'Z',  # Quitter

}


class Menu():
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

        # ------------------
        def do_triggers(next_trans):
            """
            process the transition
            by activate triggers (before / after)
            arround a potential asking value(s)
            """
            if 'TriggerBefore' in next_trans.params:
                cmd_b = str(next_trans.params['TriggerBefore'])
            else:
                cmd_b = ""

            if cmd_b != "":
                # replace previous values in cmd_b in TriggerBefore
                if 'PreviousValues' in next_trans.params:
                    ipv = next_trans.params['PreviousValues'].items()
                    for val, label in ipv:
                        cmd_b = cmd_b.replace('_' + val + '_',
                                              registered_values[val])
                # execute TriggerBefore
                eval(cmd_b)

            if 'TriggerAfter' in next_trans.params:
                cmd_a = str(next_trans.params['TriggerAfter'])
            else:
                cmd_a = ""

            # here we execute the piece of code
            # linked with the selected item menu
            if 'InputValues' in next_trans.params:
                for val, label in next_trans.params['InputValues'].items():
                    local_val = eval("input('Choisissez " + label + " :')")
                    cmd_a = cmd_a.replace('_' + val + '_', local_val)
                    registered_values[val] = local_val

            if cmd_a != "":
                # replace previous values in cmd_a in TriggerAfter
                if 'PreviousValues' in next_trans.params:
                    ipv = next_trans.params['PreviousValues'].items()
                    for val, label in ipv:
                        cmd_a = cmd_a.replace('_' + val + '_',
                                              registered_values[val])
                # execute TriggerAfter
                eval(cmd_a)
        # ------------------

        def process_input(entry, new_trans):
            """ sub process validates choice and executes
            Trigger before & Trigger after"""
            nb_choix = len(new_trans)
            choix = None

            if str(entry).isnumeric():
                choix = int(entry) - 1

            if choix in range(0, nb_choix):
                print("Vous avez choisi : {}".format(menu_list[choix]))
                next_trans = new_trans[choix]
                do_triggers(next_trans)
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
