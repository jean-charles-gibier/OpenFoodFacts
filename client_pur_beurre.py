import sys
import os

"""
    ***** Client Purre beurre *****
  Rappel des services disponibles :
    
 -gpi GET_PRODUCT_BY_ID, --get_product_by_id GET_PRODUCT_BY_ID
                        Get product object by id
  -gcl, --get_category_list
                        Get category list
  -gplc GET_PRODUCT_LIST_BY_CATEGORY_ID, --get_product_list_by_category_id GET_PRODUCT_LIST_BY_CATEGORY_ID
                        Get product list by category_id
  -gpsl GET_PRODUCTS_SUBST_LIST, --get_products_subst_list GET_PRODUCTS_SUBST_LIST
                        Get product subsitute list by id
  -gplm GET_PRODUCTS_LIST_BY_MATCH, --get_products_list_by_match GET_PRODUCTS_LIST_BY_MATCH
                        Get product by match on key words between the names of
                        products or categories. Wildcad '*' is allowed.
  -ssp SET_SUBSTITUTE_PRODUCT, --set_substitute_product SET_SUBSTITUTE_PRODUCT
                        Set relation product,substitute by id
  -r, --reload          Reload database from Openfactsfood services
"""

SERVICE_PB = './pur_beurre.py'
CURR_PYTHON = sys.executable
curr_category = 0
curr_product = 0
curr_subsitution = 0

transitions_possibles = {
    'A': {'Label': 'Acceder au menu principal',
          'Trigger': ''},
    'B': {'Label': 'Recharger la base',
          'Trigger': 'os.system("{} {} -r")'.format(CURR_PYTHON, SERVICE_PB)},
    'C': {'Label': 'Lister les categories',
          'Trigger': 'os.system("{} {} -gcl")'.format(CURR_PYTHON, SERVICE_PB)},
    'D': {'Label': 'Lister les produits d''une categorie',
          'Trigger': 'os.system("{} {} -gplc _curr_category_")'.format(CURR_PYTHON, SERVICE_PB),
          'AskForValues': {'curr_category' : 'un identifiant categorie'}},
    'E': {'Label': 'Lister les produits par mots clés',
          'Trigger': 'os.system("{} {} -gplm _key_words_")'.format(CURR_PYTHON, SERVICE_PB),
           'AskForValues': {'key_words' : 'le(s) mot(s) clé(s) (wildcard "*" accepté)'}},
    'F': {'Label': 'Afficher une categorie',
          'Trigger': 'os.system("{} {} -gci _curr_category_")'.format(CURR_PYTHON, SERVICE_PB),
          'AskForValues': {'curr_category' : 'un identifiant categorie'}},
    'G': {'Label': 'Afficher un produit',
          'Trigger': ''},
    'H': {'Label': 'Afficher un produit par ean',
          'Trigger': ''},
    'I': {'Label': 'Enregistrer un produit de susbstitution',
          'Trigger': ''},
    'J': {'Label': 'Enregistrer un produit à subsituer',
          'Trigger': ''},
    'K': {'Label': 'Lister les susbstitutions d'' un produit',
          'Trigger': ''},
    'L': {'Label': 'Quitter',
          'Trigger': 'sys.exit()'},
    'M': {'Label': 'Revenir au menu principal',
          'Trigger': ''}
}

etats_possibles = {
    1: 'Menu principal',
    2: 'Base chargée',
    3: 'Resultat lister les categories',
    4: 'Resultat lister les produits d''une categorie',
    5: 'Resultat lister les produits par mots clés',
    6: 'Resultat affichage d''une categorie',
    7: 'Resultat affichage d''un produit par id',
    8: 'Resultat affichage d''un produit par ean',
    9: 'Resultat subsitution enregistrée',
    10: 'Resultat subsitutable enregistré',
    11: 'Resultat liste de subsitutions',
    12: 'Bye'
}

paths = {
    # menu principal
    (1, 2): 'B', # recharger base
    (1, 3): 'C', # Lister categories
    (1, 5): 'E',  # Lister produits par mots clés
    (1, 12): 'L', # Quitter
    # Base chargee
    (2, 1): 'M', # revenir au menu principal
    (2, 12): 'L', # Quitter
    # Lister les categories
    (3, 1): 'M', # revenir au menu principal
    (3, 4): 'D', # Lister les produits d'une categorie
    (3, 6): 'F', # Afficher une catégorie par id
    (3, 12): 'L',  # Quitter
    # Lister  les produits d'une categorie
    (4, 1): 'M',  # revenir au menu principal
    (4, 7): 'G',  # Afficher un produit
    (4, 12): 'L',  # Quitter
    # Lister les produits par mots clés
    (5, 1): 'M',  # revenir au menu principal
    (5, 7): 'G',  # Afficher un produit par id
    (5, 12): 'L',  # Quitter
    # Afficher  les catégories par id
    (6, 1): 'M',  # revenir au menu principal
    (6, 4): 'D', # Lister les produits d'une categorie
    (6, 12): 'L',  # Quitter
    # Afficher un produit
    (7, 1): 'M',  # revenir au menu principal
    (7, 9): 'I',  # choisir comme subsitituable
    (7, 10): 'J',  # choisir comme subsititution
    (7, 12): 'L',  # Quitter
    # Afficher un produit Par Ean
    (8, 1): 'M',  # revenir au menu principal
    (8, 9): 'I',  # choisir comme subsitituable
    (8, 10): 'J',  # choisir comme subsititution
    (8, 12): 'L',  # Quitter
    # choisir comme subsitituable
    (9, 1): 'M',  # revenir au menu principal
    (9, 12): 'L',  # Quitter
    # choisir comme subsititution
    (10, 1): 'M',  # revenir au menu principal
    (10, 12): 'L',  # Quitter
    # Afficher une liste de subtitution
    (11, 1): 'M',  # revenir au menu principal
    (11, 7): 'G',  # Afficher le produit
    (10, 12): 'L',  # Quitter

}


class Menu:
    """ Menu process """
    transitions = None
    etats = None

    @classmethod
    def load(cls):
        cls.etats = dict()
        for num, etat in etats_possibles.items():
            cls.etats.update({num: Etat(etat)})

        cls.transitions = dict()
        for letter, transition in transitions_possibles.items():
            cls.transitions.update({letter: Transition(transition)})

        cls.root = None
        for path, action in paths.items():
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
                if 'AskForValues' in next_trans.params:
                    for val,label in next_trans.params['AskForValues'].items():
                        local_val = eval("input('Choisissez " + label + " :')")
                        cmd = cmd.replace('_' + val + '_', local_val)

                if cmd != "":
                    eval(cmd)
            else:
                print("Choisissez une option entre 1 et {}".format(nb_choix))

            return choix

        next_etat = Menu.etats[entry]
        while True:
            local_dico = next_etat.liaisons
            new_etats = [trans_etat[1] for num, trans_etat in enumerate(local_dico.items())]
            new_trans = [trans_etat[0] for num, trans_etat in enumerate(local_dico.items())]
            menu_list = [str(num + 1) + ': ' + trans_etat[0].params['Label']
                         for num, trans_etat
                         in enumerate(local_dico.items())]
            menu_string = " | ".join(menu_list)
            print("Choisissez parmi l'une des options suivantes :\n[{}]".format(menu_string))
            entry = input('>>> ')
            choix = process_input(entry, new_trans)
            if choix is not None and choix < len(new_etats):
                next_etat = new_etats[choix]

    @classmethod
    def start(cls, entry):
        cls.show(entry)

    def __init__(self):
        pass


class Etat:
    def __init__(self, params):
        if isinstance(params, str):
            self.description = params
            self.liaisons = dict()
        pass

    def aller_vers(self, autre_etat, avec_transition):
        avec_transition.lier(self, autre_etat)
        self.liaisons[avec_transition] = autre_etat
        pass


class Transition:
    def __init__(self, params):
        self.params = params
        self.transitions = list()

    def lier(self, un_etat, un_autre_etat):
        self.transitions.append((un_etat, un_autre_etat))


def main():
    try:
        f = open(SERVICE_PB)
        f.close()
    except IOError:
        print("Le fichier {} doit être présent dans le repertoire courant.".format(SERVICE_PB))
        sys.exit(-1)

    Menu.load()
    Menu.start(1)


if __name__ == '__main__':
    main()
