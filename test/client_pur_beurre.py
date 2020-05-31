import sys

transitions_possibles = {
    'A': {'Label': 'Acceder au menu principal', 'Trigger': ''},
    'B': {'Label': 'Recharger la base', 'Trigger': 'print("Base rechargée.")'},
    'C': {'Label': 'Lister les categories', 'Trigger': ''},
    'D': {'Label': 'Lister les produits d''une categorie', 'Trigger': ''},
    'E': {'Label': 'Lister les produits par mots clés', 'Trigger': ''},
    'F': {'Label': 'Afficher une categorie par id', 'Trigger': ''},
    'G': {'Label': 'Afficher un produit par id', 'Trigger': ''},
    'H': {'Label': 'Afficher un produit par ean', 'Trigger': ''},
    'I': {'Label': 'Enregistrer un c hoix de susbstitution', 'Trigger': ''},
    'J': {'Label': 'Afficher liste des susbstitutions', 'Trigger': ''},
    'K': {'Label': 'Quitter', 'Trigger': 'sys.exit()'},
    'L': {'Label': 'Revenir au menu principal', 'Trigger': ''}
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
    10: 'Resultat liste de subsitutions',
    11: 'Bye'
}

paths = {
    # menu principal
    (1, 2): 'B', # recharger base
    (1, 3): 'C', # Lister categories
    (1, 5): 'E',  # Lister produits par mots clés
    (1, 11): 'K', # Quitter
    # Base chargee
    (2, 1): 'L', # revenir au menu principal
    (2, 11): 'K', # Quitter
    # Lister les categories
    (3, 1): 'L', # revenir au menu principal
    (3, 6): 'F', # Afficher une catégorie
    (3, 4): 'D', # Lister les produits d'une categorie
    (3, 11): 'K',  # Quitter
    # Lister  les produits d'une categorie
    (4, 1): 'L',  # revenir au menu principal
    (4, 7): 'G',  # Afficher un produit
    (4, 11): 'K'  # Quitter

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
                print("Choix : {}".format(menu_list[choix]))
                next_trans = new_trans[choix]
                cmd = str(next_trans.params['Trigger'])
                if cmd != "":
                    eval(cmd)
            else:
                print("Choisissez une option entre 1 et {}".format(nb_choix))

            return choix

        choix = int(entry)
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
    root = Menu.load()
    Menu.start(1)


if __name__ == '__main__':
    main()
