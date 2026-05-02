import random
import tkinter as tk
from tkinter import messagebox
import time


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Logique du jeu
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Sudoku:

    def __init__(self):
        self.grille = self.grille_valable()
        self.grille_depart = None

    def grille_valable(self):
        ligne1 = list(range(1, 10))
        random.shuffle(ligne1)
        ligne2 = ligne1[3:6] + ligne1[6:9] + ligne1[0:3]
        ligne3 = ligne2[3:6] + ligne2[6:9] + ligne2[0:3]
        bloc1 = [ligne1, ligne2, ligne3]

        ligne4 = ligne3[1:9] + ligne3[0:1]
        ligne5 = ligne4[3:6] + ligne4[6:9] + ligne4[0:3]
        ligne6 = ligne5[3:6] + ligne5[6:9] + ligne5[0:3]
        bloc2 = [ligne4, ligne5, ligne6]

        ligne7 = ligne6[1:9] + ligne6[0:1]
        ligne8 = ligne7[3:6] + ligne7[6:9] + ligne7[0:3]
        ligne9 = ligne8[3:6] + ligne8[6:9] + ligne8[0:3]
        bloc3 = [ligne7, ligne8, ligne9]

        blocs = [bloc1, bloc2, bloc3]
        random.shuffle(blocs[0])
        random.shuffle(blocs[1])
        random.shuffle(blocs[2])
        random.shuffle(blocs)

        resultat = []
        for bloc in blocs:
            for ligne in bloc:
                resultat.append(ligne)
        return resultat

    def enlever_case(self, nb):
        nv_grille = [ligne.copy() for ligne in self.grille]
        supprimees = 0
        while supprimees < nb:
            l = random.randint(0, 8)
            c = random.randint(0, 8)
            if nv_grille[l][c] != 0:
                nv_grille[l][c] = 0
                supprimees += 1
        self.grille_depart = [ligne.copy() for ligne in nv_grille]
        return nv_grille

    def case_modifiable(self, l, c):
        return self.grille_depart[l][c] == 0

    def facile(self):
        return self.enlever_case(random.randint(36, 46))

    def moyen(self):
        return self.enlever_case(random.randint(46, 51))

    def difficile(self):
        return self.enlever_case(random.randint(51, 56))

    def verifier_case(self, grille, l, c):
        """Retourne True si la valeur en (l,c) est correcte."""
        val = grille[l][c]
        if val == 0:
            return True
        # Ligne
        if grille[l].count(val) > 1:
            return False
        # Colonne
        if [grille[i][c] for i in range(9)].count(val) > 1:
            return False
        # Bloc 3×3
        bl, bc = (l // 3) * 3, (c // 3) * 3
        vals_bloc = [grille[bl + di][bc + dj] for di in range(3) for dj in range(3)]
        if vals_bloc.count(val) > 1:
            return False
        return True


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Interface principale
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
COULEURS = {
    "fond":          "#1a1a2e",
    "fond2":         "#16213e",
    "accent":        "#e94560",
    "accent2":       "#0f3460",
    "texte":         "#eaeaea",
    "texte_dim":     "#8888aa",
    "case_sel":      "#7a2535",
    "case_meme":     "#1a3a6e",
    "case_erreur":   "#8b1a2a",
    "case_normale":  "#1a1a2e",
    "grille_fond":   "#0d0d1a",
    "bouton":        "#e94560",
    "bouton_hover":  "#c73652",
    "bouton_texte":  "#ffffff",
    "depart":        "#eaeaea",
    "joueur":        "#5bc8f5",
}

POLICE_TITRE  = ("Georgia", 32, "bold")
POLICE_GRILLE = ("Georgia", 20, "bold")
POLICE_UI     = ("Georgia", 12)
POLICE_BTN    = ("Georgia", 11, "bold")
POLICE_CHRONO = ("Courier", 22, "bold")


class InterfaceSudoku:

    TC = 62  # taille d'une case en pixels

    def __init__(self, fenetre):
        self.fenetre = fenetre
        self.fenetre.title("Sudoku")
        self.fenetre.configure(bg=COULEURS["fond"])
        self.fenetre.resizable(True, True)

        self.jeu = None
        self.grille = None
        self.selection = None
        self.cases_erreurs = set()
        self.soumis = False

        self._chrono_depart = 0
        self._chrono_job = None
        self._chrono_stoppe = False
        self._temps_final = 0

        self._construire_page_accueil()

    # ~~ PAGE D'ACCUEIL ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _construire_page_accueil(self):
        self.frame_accueil = tk.Frame(self.fenetre, bg=COULEURS["fond"])
        self.frame_accueil.pack(expand=True, fill="both")

        # Titre
        tk.Label(
            self.frame_accueil,
            text="✦  SUDOKU  ✦",
            font=("Georgia", 40, "bold"),
            bg=COULEURS["fond"], fg=COULEURS["accent"],
        ).pack(pady=(50, 5))

        tk.Label(
            self.frame_accueil,
            text="Un jeu de logique et de patience",
            font=("Georgia", 13, "italic"),
            bg=COULEURS["fond"], fg=COULEURS["texte_dim"],
        ).pack(pady=(0, 35))

        # Bloc règles
        frame_regles = tk.Frame(self.frame_accueil, bg=COULEURS["fond2"], padx=30, pady=20)
        frame_regles.pack(padx=60, pady=5)

        tk.Label(
            frame_regles,
            text="Règles du jeu",
            font=("Georgia", 15, "bold"),
            bg=COULEURS["fond2"], fg=COULEURS["accent"],
        ).pack(anchor="w", pady=(0, 10))

        regles = [
            "① Remplissez la grille 9×9 avec des chiffres de 1 à 9.",
            "② Chaque ligne doit contenir chaque chiffre exactement une fois.",
            "③ Chaque colonne doit contenir chaque chiffre exactement une fois.",
            "④ Chaque bloc 3×3 doit contenir chaque chiffre exactement une fois.",
            "⑤ Les cases grises sont fixes ; les cases bleues sont les vôtres.",
        ]
        for r in regles:
            tk.Label(
                frame_regles, text=r,
                font=("Georgia", 11),
                bg=COULEURS["fond2"], fg=COULEURS["texte"],
                justify="left",
            ).pack(anchor="w", pady=2)

        # Choix de difficulté
        tk.Label(
            self.frame_accueil,
            text="Choisissez un niveau",
            font=("Georgia", 13, "bold"),
            bg=COULEURS["fond"], fg=COULEURS["texte"],
        ).pack(pady=(30, 10))

        frame_niveaux = tk.Frame(self.frame_accueil, bg=COULEURS["fond"])
        frame_niveaux.pack()

        niveaux = [("Facile", "facile", "#27ae60"),
                   ("Moyen",  "moyen",  "#f39c12"),
                   ("Difficile", "difficile", "#e94560")]

        for texte, niveau, couleur in niveaux:
            btn = tk.Button(
                frame_niveaux,
                text=texte,
                font=POLICE_BTN,
                bg=couleur, fg="white",
                activebackground=couleur, activeforeground="white",
                relief="flat", bd=0,
                padx=24, pady=10,
                cursor="hand2",
                command=lambda n=niveau: self._demarrer(n),
            )
            btn.pack(side="left", padx=10, pady=5)

    # ~~ DÉMARRAGE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _demarrer(self, niveau):
        self.jeu = Sudoku()
        if niveau == "facile":
            self.grille = self.jeu.facile()
        elif niveau == "moyen":
            self.grille = self.jeu.moyen()
        else:
            self.grille = self.jeu.difficile()

        self.niveau_actuel = niveau
        self.selection = None
        self.cases_erreurs = set()
        self.soumis = False

        # Nettoyer l'accueil / ancienne partie
        for w in self.fenetre.winfo_children():
            w.destroy()

        self._construire_interface_jeu()
        self._demarrer_chrono()

    def _rejouer(self):
        if self._chrono_job:
            self.fenetre.after_cancel(self._chrono_job)
            self._chrono_job = None
        self._demarrer(self.niveau_actuel)

    def _accueil(self):
        if self._chrono_job:
            self.fenetre.after_cancel(self._chrono_job)
            self._chrono_job = None
        for w in self.fenetre.winfo_children():
            w.destroy()
        self._construire_page_accueil()

    # ~~ INTERFACE DE JEU ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _construire_interface_jeu(self):
        # ~~ Barre du haut ~~
        self.frame_haut = tk.Frame(self.fenetre, bg=COULEURS["fond"], pady=12)
        self.frame_haut.pack(fill="x", padx=20)

        tk.Label(
            self.frame_haut, text="✦ SUDOKU ✦",
            font=("Georgia", 22, "bold"),
            bg=COULEURS["fond"], fg=COULEURS["accent"],
        ).pack(side="left")

        self.label_chrono = tk.Label(
            self.frame_haut, text="00:00",
            font=POLICE_CHRONO,
            bg=COULEURS["fond"], fg=COULEURS["texte"],
        )
        self.label_chrono.pack(side="right", padx=10)

        tk.Label(
            self.frame_haut, text="⏱",
            font=("Georgia", 16),
            bg=COULEURS["fond"], fg=COULEURS["texte_dim"],
        ).pack(side="right")

        # ~~ Canvas grille ~~
        taille = self.TC * 9
        self.frame_grille = tk.Frame(
            self.fenetre,
            bg=COULEURS["grille_fond"],
            padx=4, pady=4,
        )
        self.frame_grille.pack(pady=5)

        self.canvas = tk.Canvas(
            self.frame_grille,
            width=taille, height=taille,
            bg=COULEURS["grille_fond"],
            highlightthickness=0,
        )
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self._clic)
        self.fenetre.bind("<Key>", self._clavier)

        # ~~ Barre du bas ~~
        self.frame_bas = tk.Frame(self.fenetre, bg=COULEURS["fond"], pady=12)
        self.frame_bas.pack(fill="x", padx=20)

        self._btn(self.frame_bas, "⟳  Rejouer",  self._rejouer,  "#0f3460").pack(side="left",  padx=6)
        self._btn(self.frame_bas, "⌂  Accueil",  self._accueil,  "#333355").pack(side="left",  padx=6)
        self._btn(self.frame_bas, "✔  Soumettre", self._soumettre, "#e94560").pack(side="right", padx=6)

        self._draw()

    def _btn(self, parent, texte, cmd, couleur):
        return tk.Button(
            parent, text=texte,
            font=POLICE_BTN,
            bg=couleur, fg="white",
            activebackground=couleur, activeforeground="white",
            relief="flat", bd=0,
            padx=16, pady=8,
            cursor="hand2",
            command=cmd,
        )

    # ~~ CHRONOMÈTRE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _demarrer_chrono(self):
        self._chrono_depart = time.time()
        self._chrono_stop = False
        self._tick()

    def _tick(self):
        if self._chrono_stop:
            return
        elapsed = int(time.time() - self._chrono_depart)
        m, s = divmod(elapsed, 60)
        self.label_chrono.config(text=f"{m:02d}:{s:02d}")
        self._chrono_job = self.fenetre.after(1000, self._tick)

    def _stopper_chrono(self):
        self._chrono_stop = True
        self._temps_final = int(time.time() - self._chrono_depart)
        if self._chrono_job:
            self.fenetre.after_cancel(self._chrono_job)

    # ~~ DESSIN ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _draw(self):
        self.canvas.delete("all")
        self._dessiner_fonds()
        self._dessiner_chiffres()
        self._dessiner_lignes()

    def _valeur_selection(self):
        """Retourne la valeur dans la case sélectionnée (0 si vide ou rien)."""
        if self.selection is None:
            return 0
        l, c = self.selection
        return self.grille[l][c]

    def _dessiner_fonds(self):
        TC = self.TC
        val_sel = self._valeur_selection()

        for i in range(9):
            for j in range(9):
                x1, y1 = j * TC, i * TC
                x2, y2 = x1 + TC, y1 + TC
                val = self.grille[i][j]

                if self.soumis and (i, j) in self.cases_erreurs:
                    couleur = COULEURS["case_erreur"]
                elif self.selection == (i, j):
                    couleur = COULEURS["case_sel"]
                elif val != 0 and val == val_sel:
                    # Même chiffre que la sélection
                    couleur = COULEURS["case_meme"]
                else:
                    couleur = COULEURS["case_normale"]

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=couleur, outline="")

    def _dessiner_chiffres(self):
        TC = self.TC
        for i in range(9):
            for j in range(9):
                val = self.grille[i][j]
                if val == 0:
                    continue
                x = j * TC + TC // 2
                y = i * TC + TC // 2
                if self.jeu.grille_depart[i][j] != 0:
                    couleur = COULEURS["depart"]
                else:
                    couleur = COULEURS["joueur"]
                self.canvas.create_text(x, y, text=str(val), font=POLICE_GRILLE, fill=couleur)

    def _dessiner_lignes(self):
        TC = self.TC
        total = TC * 9
        for i in range(10):
            ep = 3 if i % 3 == 0 else 1
            col = COULEURS["accent"] if i % 3 == 0 else "#444466"
            self.canvas.create_line(0, i * TC, total, i * TC, width=ep, fill=col)
            self.canvas.create_line(i * TC, 0, i * TC, total, width=ep, fill=col)

    # ~~ INTERACTIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _clic(self, event):
        c = event.x // self.TC
        l = event.y // self.TC
        if 0 <= l < 9 and 0 <= c < 9:
            self.selection = (l, c)
        self._draw()

    def _clavier(self, event):
        if self.selection is None or self.soumis:
            return
        l, c = self.selection

        # Navigation clavier
        touches_direction = {
            "Up":    (-1, 0), "Down":  (1, 0),
            "Left":  (0, -1), "Right": (0, 1),
        }
        if event.keysym in touches_direction:
            dl, dc = touches_direction[event.keysym]
            nl, nc = max(0, min(8, l + dl)), max(0, min(8, c + dc))
            self.selection = (nl, nc)
            self._draw()
            return

        if not self.jeu.case_modifiable(l, c):
            return

        if event.char in "123456789":
            self.grille[l][c] = int(event.char)
        elif event.keysym in ("BackSpace", "Delete") or event.char == "0":
            self.grille[l][c] = 0

        self._draw()

    # ~~ SOUMETTRE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _soumettre(self):
        if self.soumis:
            return

        # Vérifier si la grille est complète
        vide = any(self.grille[i][j] == 0 for i in range(9) for j in range(9))

        # Trouver les erreurs
        self.cases_erreurs = set()
        for i in range(9):
            for j in range(9):
                if self.grille[i][j] != 0 and not self.jeu.verifier_case(self.grille, i, j):
                    self.cases_erreurs.add((i, j))

        if not vide and not self.cases_erreurs:
            # Victoire !
            self.soumis = True
            self._stopper_chrono()
            m, s = divmod(self._temps_final, 60)
            self._draw()
            messagebox.showinfo(
                "Félicitations !",
                f"✦ Bravo, vous avez résolu le Sudoku ! ✦\n\nTemps : {m:02d}:{s:02d}"
            )
        else:
            # Afficher les erreurs en rouge (soumis=True active le rendu rouge)
            self.soumis = True
            self._draw()
            nb = len(self.cases_erreurs)
            if vide:
                msg = "La grille n'est pas encore complète.\nLes cases incorrectes sont surlignées en rouge."
            else:
                msg = f"{nb} erreur(s) détectée(s).\nLes cases incorrectes sont surlignées en rouge."
            messagebox.showwarning("Résultat", msg)
            # Laisser le joueur continuer à corriger
            self.soumis = False
            self.cases_erreurs = set()
            self._draw()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Lancement
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    fenetre = tk.Tk()
    fenetre.title("Sudoku")
    fenetre.configure(bg="#1a1a2e")
    app = InterfaceSudoku(fenetre)
    fenetre.mainloop()
