import tkinter as tk
from tkinter import Frame, Menubutton, ttk, filedialog, messagebox
from collections import Counter
import csv
import fitz  # PyMuPDF
import re
import matplotlib.pyplot as plt

# Fenêtre principale et menu

fen_princ = tk.Tk()
fen_princ.title("Application Multifonction")
fen_princ.geometry("300x200")
fen_princ.maxsize(480, 180)


# Configuration du redimensionnement
fen_princ.grid_rowconfigure(0, weight=1,)
fen_princ.grid_rowconfigure(1, weight=1)
fen_princ.grid_rowconfigure(2, weight=1)

fen_princ.grid_columnconfigure(0, weight=1)
fen_princ.grid_rowconfigure(0, weight=1)


# Fonctionnalité 1 : Calculateur d'IMC

def imc_calculator():
    imc_window = tk.Toplevel(fen_princ)
    imc_window.title("Calculatrice IMC")
    imc_window.iconbitmap("téléchargement.ico")
    imc_window.geometry("400x300")
    imc_window.configure(bg="gray30")
    imc_window.grid_columnconfigure(0, weight=1)
    imc_window.grid_rowconfigure(0, weight=1)

    

    def calculer_imc():
        try:
            poids = float(entry_poids.get())
            taille = float(entry_taille.get())
            if poids <= 0 or taille <= 0:
                raise ValueError
            imc = poids / (taille ** 2)
            resultat = f"Votre IMC est : {imc:.2f}\n\n"
            if imc < 18.5:
                interpretation = "Insuffisance pondérale (maigreur)"
            elif 18.5 <= imc < 25:
                interpretation = "Corpulence normale"
            elif 25 <= imc < 30:
                interpretation = "Surpoids"
            elif 30 <= imc < 35:
                interpretation = "Obésité modérée"
            elif 35 <= imc < 40:
                interpretation = "Obésité sévère"
            else:
                interpretation = "Obésité morbide ou massive"
            label_resultat.config(text=resultat + interpretation)
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des valeurs numériques valides.")

    tk.Label(imc_window, text="Calculateur d'IMC", font=("Arial", 16, "bold"), bg="gray30", fg="white").pack(pady=10)
    
    tk.Label(imc_window, text="Poids (en Kg) :", bg="gray30", fg="white").pack(pady=5)
    entry_poids = tk.Entry(imc_window, font=("Arial", 12), width=10)
    entry_poids.pack(pady=5)

    tk.Label(imc_window, text="Taille (en m) :", bg="gray30", fg="white").pack(pady=5)
    entry_taille = tk.Entry(imc_window, font=("Arial", 12), width=10)
    entry_taille.pack(pady=5)

    tk.Button(imc_window, text="Calculer IMC",bg='green', command=calculer_imc).pack(pady=10)

    label_resultat = tk.Label(imc_window, text="", font=("Arial", 12), bg="gray30", fg="white")
    label_resultat.pack(pady=10)

# Fonctionnalité 2 : Analyseur de texte

def text_analise():
    analyzer_window = tk.Toplevel(fen_princ)
    analyzer_window.title("Analyseur de texte avancé")
    analyzer_window.iconbitmap("appmachine-icon.ico")
    analyzer_window.geometry("900x700")
    analyzer_window.configure(bg="gray30")
    analyzer_window.grid_columnconfigure(0, weight=1)
    analyzer_window.grid_rowconfigure(0, weight=1)

    # Définition des mots à ignorer (stop words)
    STOP_WORDS = {"le", "la", "les", "de", "du", "des", "et", "un", "une", "en", "à", "pour", "par", "que", "qui", "dans", "sur", "avec"}

    def analyser_texte():
        texte = text_input.get("1.0", tk.END).strip()
        if not texte:
            messagebox.showwarning("Avertissement", "Veuillez coller ou importer un texte avant d'analyser.")
            return
        mots = texte.split()
        total_mots = len(mots)
        # Filtrer les mots de plus de 4 lettres hors stop words
        mots_long = [mot.lower().strip(",.!?;:") for mot in mots if len(mot) > 4 and mot.lower() not in STOP_WORDS]
        if not mots_long:
            messagebox.showinfo("Résultat", "Aucun mot de plus de 4 lettres trouvé dans le texte.")
            return
        compteur = Counter(mots_long)
        total_mots_long = sum(compteur.values())
        # On affiche les 10 mots les plus fréquents
        mots_frequences = compteur.most_common(10)
        for row in tree.get_children():
            tree.delete(row)
        for mot, freq in mots_frequences:
            pourcentage = round((freq / total_mots_long) * 100, 2)
            tree.insert("", tk.END, values=(mot, freq, f"{pourcentage}%"))
        label_total_mots.config(text=f"Total de mots : {total_mots}")
        label_total_mots_long.config(text=f"Mots > 4 lettres : {total_mots_long}")

    def importer_fichier():
        fichier = filedialog.askopenfilename(filetypes=[("Fichiers texte", "*.txt")])
        if fichier:
            try:
                with open(fichier, "r", encoding="utf-8") as f:
                    contenu = f.read()
                text_input.delete("1.0", tk.END)
                text_input.insert(tk.END, contenu)
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de lire le fichier : {e}")

    def exporter_resultats():
        fichier = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Fichiers CSV", "*.csv")])
        if fichier:
            try:
                with open(fichier, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(["Mot", "Fréquence", "Pourcentage"])
                    for row in tree.get_children():
                        writer.writerow(tree.item(row)["values"])
                messagebox.showinfo("Succès", "Résultats exportés avec succès.")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible d'exporter les résultats : {e}")

    tk.Label(analyzer_window, text="Analyseur de texte avancé", font=("Arial", 16, "bold"), bg="gray30", fg="white").pack(pady=10)

    frame_input = tk.Frame(analyzer_window, bg="gray30")
    frame_input.pack(pady=10, fill=tk.X, padx=10)
    tk.Label(frame_input, text="Collez ou importez votre texte :", font=("Arial", 12), bg="gray30", fg="white").pack(anchor="w")
    text_input = tk.Text(frame_input, height=10, font=("Arial", 12))
    text_input.pack(fill=tk.BOTH, pady=5)

    frame_buttons = tk.Frame(analyzer_window, bg="gray30")
    frame_buttons.pack(pady=10)
    tk.Button(frame_buttons, text="Importer fichier", command=importer_fichier,
              font=("Arial", 12, "bold"), bg="#2196F3", fg="white", padx=10, pady=5).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_buttons, text="Analyser texte", command=analyser_texte,
              font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", padx=10, pady=5).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_buttons, text="Exporter résultats", command=exporter_resultats,
              font=("Arial", 12, "bold"), bg="#FF9800", fg="white", padx=10, pady=5).pack(side=tk.LEFT, padx=5)

    frame_results = tk.Frame(analyzer_window, bg="gray30")
    frame_results.pack(pady=10, fill=tk.BOTH, expand=True)
    columns = ("Mot", "Fréquence", "Pourcentage")
    tree = ttk.Treeview(frame_results, columns=columns, show="headings")
    tree.heading("Mot", text="Mot")
    tree.heading("Fréquence", text="Fréquence")
    tree.heading("Pourcentage", text="Pourcentage")
    tree.pack(fill=tk.BOTH, expand=True)

    frame_info = tk.Frame(analyzer_window, bg="gray30")
    frame_info.pack(pady=10, fill=tk.X, padx=10)
    label_total_mots = tk.Label(frame_info, text="Total de mots : 0", font=("Arial", 12), bg="gray30", fg="white")
    label_total_mots.pack(side=tk.LEFT, padx=5)
    label_total_mots_long = tk.Label(frame_info, text="Mots > 4 lettres : 0", font=("Arial", 12), bg="gray30", fg="white")
    label_total_mots_long.pack(side=tk.LEFT, padx=5)

# Fonctionnalité 3 : Analyseur de PDF

def pdf_analise():
    pdf_window = tk.Toplevel(fen_princ)
    pdf_window.title("Analyseur de PDF")
    pdf_window.iconbitmap("pdf.ico")
    pdf_window.geometry("500x400")
    pdf_window.configure(bg="gray30")
    pdf_window.grid_columnconfigure(0, weight=1)
    pdf_window.grid_rowconfigure(0, weight=1)

    words_data = []  # variable pour stocker les résultats

    def extract_text(pdf_path):
        doc = fitz.open(pdf_path)
        return " ".join(page.get_text("text") for page in doc).lower()

    def analyze_text(text):
        words = re.findall(r'\b[a-zA-Z]{4,}\b', text)
        return Counter(words).most_common(10)

    def open_file():
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            text = extract_text(file_path)
            top_words = analyze_text(text)
            display_results(top_words)

    def display_results(top_words):
        listbox.delete(0, tk.END)
        nonlocal words_data
        words_data = top_words
        for word, count in top_words:
            listbox.insert(tk.END, f"{word}: {count} fois")
        btn_pie_chart.config(state=tk.NORMAL)

    def plot_pie_chart():
        if words_data:
            words, counts = zip(*words_data)
            plt.pie(counts, labels=words, autopct='%1.1f%%', colors=plt.cm.Paired.colors)
            plt.title("Répartition des mots les plus fréquents")
            plt.show()
        else:
            messagebox.showwarning("Avertissement", "Aucune donnée à afficher.")

    tk.Label(pdf_window, text="Analyseur de PDF", font=("Arial", 16, "bold"), bg="gray30", fg="white").pack(pady=10)
    tk.Button(pdf_window, text="Choisir un PDF", command=open_file,
              font=("Arial", 12), bg="#2196F3", fg="white", padx=10, pady=5).pack(pady=5)

    listbox = tk.Listbox(pdf_window, width=50, height=10)
    listbox.pack(pady=10)

    btn_pie_chart = tk.Button(pdf_window, text="Graphique Camembert", command=plot_pie_chart,
                              state=tk.DISABLED, font=("Arial", 12), bg="#FF9800", fg="white", padx=10, pady=5)
    btn_pie_chart.pack(pady=5)



zoneMenu = Frame(fen_princ,borderwidth=3, bg ='#557788')
zoneMenu.grid(row=0, column=0, sticky="nsew")
zoneMenu.grid_columnconfigure(0, weight=1)
zoneMenu.grid_rowconfigure(0, weight=1)
zoneMenu.grid_rowconfigure(1, weight=1)
zoneMenu.grid_rowconfigure(2, weight=1)



menuCalcutrice = tk.Button(zoneMenu, text='Calculatrice IMC', width=20, height=2,borderwidth=2, bg='green', activebackground='darkorange',command=imc_calculator, relief = tk.RAISED )
menuCalcutrice.grid(row=0, column=0, padx=5, pady=5, columnspan=2)  # En haut

menuTexte = tk.Button(zoneMenu, text='Analyse texte', width=20, height=2,borderwidth=2, bg='#2196F3', activebackground='darkorange', command=text_analise, relief = tk.RAISED )
menuTexte.grid(row=1, column=0,  padx=5, pady=5, columnspan=2)  # Au milieu

menuPdf = tk.Button(zoneMenu, text='Analyse pdf', width=20, height=2,borderwidth=2, bg='#FF9800', activebackground='darkorange',command=pdf_analise, relief = tk.RAISED )
menuPdf.grid(row=2, column=0, padx=5, pady=5, columnspan=2)  # En bas

# Placement vertical des boutons
# Placement dans la grille




fen_princ.mainloop()