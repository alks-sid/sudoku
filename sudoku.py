import random

class Sudoku:

    def __init__(self):
        self.grille = self.grille_valable()

    def grille_valable(self):
        grille = []
        bloc1 = []
        bloc2 = []
        bloc3 = []
        ligne1 = [i for i in range(1,10)]
        random.shuffle(ligne1)
        bloc1.append(ligne1)
        ligne2 = ligne1[3:6] + ligne1[6:9] + ligne1[0:3]
        bloc1.append(ligne2)
        ligne3 = ligne2[3:6] + ligne2[6:9] + ligne2[0:3]
        bloc1.append(ligne3)

        ligne4 = ligne3[1:9] + ligne3[0:1]
        bloc2.append(ligne4)
        ligne5 = ligne4[3:6] + ligne4[6:9] + ligne4[0:3]
        bloc2.append(ligne5)
        ligne6 = ligne5[3:6] + ligne5[6:9] + ligne5[0:3]
        bloc2.append(ligne6)

        ligne7 = ligne6[1:9] + ligne6[0:1]
        bloc3.append(ligne7)
        ligne8 = ligne7[3:6] + ligne7[6:9] + ligne7[0:3]
        bloc3.append(ligne8)
        ligne9 = ligne8[3:6] + ligne8[6:9] + ligne8[0:3]
        bloc3.append(ligne9)

        random.shuffle(bloc1)
        random.shuffle(bloc2)
        random.shuffle(bloc3)
        grille.append(bloc1)
        grille.append(bloc2)
        grille.append(bloc3)
        random.shuffle(grille)
        resultat = []
        for bloc in grille:
            for ligne in bloc:
                resultat.append(ligne)
        return resultat
    
    def enlever_case(self, nb):
        nv_grille = []
        for ligne in self.grille:
            nv_grille.append(ligne.copy())
        case_supp = 0
        while case_supp < nb:
            l = random.randint(0, 8)
            c = random.randint(0, 8)
            if nv_grille[l][c] != 0:
                nv_grille[l][c] = 0
                case_supp += 1
        self.grille_depart = [ligne.copy() for ligne in nv_grille]
        return nv_grille
    
    def case_modifiable(self, l, c):
        return self.grille_depart[l][c] == 0
    
    def afficher_grille(self, grille):
        for i, ligne in enumerate(grille):
            if i % 3 == 0 and i != 0:
                print("-" * 21)  # séparation blocs de lignes
            for j, val in enumerate(ligne):
                if j % 3 == 0 and j != 0:
                    print("|", end=" ")
                print(val if val != 0 else ".", end=" ")
            print()

    def jouer(self, grille):
        while 0 in [val for ligne in grille for val in ligne]:
            # tant qu’il reste des cases vides
            self.afficher_grille(grille)
            ligne = int(input("Ligne (0-8) : "))
            colonne = int(input("Colonne (0-8) : "))
            valeur = int(input("Valeur (1-9) : "))

            if not self.case_modifiable(ligne, colonne):
                print("Case verrouillée !")
            else:
                grille[ligne][colonne] = valeur

    def facile(self):
        print("Mode facile")
        return self.enlever_case(random.randint(36, 46))

    def moyen(self):
        print("Mode moyen")
        return self.enlever_case(random.randint(46, 51))

    def difficile(self):
        print("Mode difficile")
        return self.enlever_case(random.randint(51, 56))

    def difficulter(self):
        niveau = input("Choisissez un niveau (facile, moyen, difficile) : ").lower()
        if niveau == "facile":
            return self.facile()
        elif niveau == "moyen":
            return self.moyen()
        elif niveau == "difficile":
            return self.difficile()
        else:
            print("Ecris bien stp")
            return self.difficulter()


jeu = Sudoku()
grille = jeu.difficulter()
jeu.jouer(grille)
