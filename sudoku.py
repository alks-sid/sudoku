import random
import tkinter as tk
from tkinter import messagebox

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


#jeu = Sudoku()
#grille = jeu.difficulter()
#jeu.jouer(grille)


class InterfaceSudoku:
    def __init__(self, fenetre):
        self.jeu = Sudoku()
        self.grille = None
        self.selection = None
        self.fenetre = fenetre
        self.taille_case = 50

        self.frame_menu = tk.Frame(fenetre)
        self.frame_menu.pack()

        tk.Button(self.frame_menu, text="Facile",    command=lambda: self.demarrer("facile")).pack()
        tk.Button(self.frame_menu, text="Moyen",     command=lambda: self.demarrer("moyen")).pack()
        tk.Button(self.frame_menu, text="Difficile", command=lambda: self.demarrer("difficile")).pack()

    def demarrer(self, niveau):
        if niveau == "facile":
            self.grille = self.jeu.facile()
        elif niveau == "moyen":
            self.grille = self.jeu.moyen()
        elif niveau == "difficile":
            self.grille = self.jeu.difficile()

        self.frame_menu.pack_forget()
        self.canvas = tk.Canvas(self.fenetre, width=self.taille_case*9, height=self.taille_case*9)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.clic)
        self.fenetre.bind("<Key>", self.clavier)
        self.draw()

    def draw(self):
        self.canvas.delete("all")
        self.dessiner_selection()
        self.dessiner_chiffres()
        self.dessiner_lignes()

    def dessiner_chiffres(self):
        for i in range(9):
            for j in range(9):
                valeur = self.grille[i][j]
                x = j * self.taille_case + self.taille_case // 2
                y = i * self.taille_case + self.taille_case // 2

                if self.jeu.grille_depart[i][j] != 0:
                    couleur = "black"
                else:
                    couleur = "blue"
                
                if valeur != 0:
                    self.canvas.create_text(x, y, text=str(valeur), fill=couleur)
    
    def dessiner_lignes(self):
        taille_totale = self.taille_case*9

        for i in range(10):
            epaisseur = 3 if i%3 == 0 else 1
            self.canvas.create_line(0, i*self.taille_case, taille_totale, i*self.taille_case, width=epaisseur)
            self.canvas.create_line(i*self.taille_case, 0, i*self.taille_case, taille_totale, width=epaisseur)
    
    def clic(self, event):
        colone = event.x // self.taille_case
        ligne = event.y // self.taille_case
        self.selection = (ligne, colone)
        self.draw()
    
    def dessiner_selection(self):
        if self.selection is None:
            return
        ligne, colone = self.selection
        x1 = colone * self.taille_case
        y1 = ligne * self.taille_case
        x2 = x1 + self.taille_case
        y2 = y1 + self.taille_case
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="lightblue", outline="")

    def clavier(self, event):
        if self.selection is None:
            return
        ligne, colone = self.selection

        if not self.jeu.case_modifiable(ligne, colone):
            return
        
        if event.char in "1123456789":
            self.grille[ligne][colone] = int(event.char)
        elif event.keysym in ("BackSpace", "Delete", "0"):
            self.grille[ligne][colone] = 0
        
        self.draw()
        self.verifier_victoire()

    def verifier_victoire(self):
        if 0 not in [val for ligne in self.grille for val in ligne]:
            tk.messagebox.showinfo("Vous avez resolu le sudoku !")



fenetre = tk.Tk()
fenetre.title("Sudoku")
fenetre.geometry("1080x720")
app = InterfaceSudoku(fenetre)
fenetre.mainloop()