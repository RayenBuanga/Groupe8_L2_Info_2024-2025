import tkinter as tk
from db_config import get_connection

def ajouter(nom, prenom, contact, role):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO membres (nom, prenom, contact, role) VALUES (%s, %s, %s, %s)", (nom, prenom, contact, role))
    conn.commit()
    conn.close()

def build_interface(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    tk.Label(frame, text="Nom").pack()
    nom = tk.Entry(frame); nom.pack()
    tk.Label(frame, text="Prénom").pack()
    prenom = tk.Entry(frame); prenom.pack()
    tk.Label(frame, text="Contact").pack()
    contact = tk.Entry(frame); contact.pack()
    tk.Label(frame, text="Rôle").pack()
    role = tk.Entry(frame); role.pack()

    def action():
        ajouter(nom.get(), prenom.get(), contact.get(), role.get())
        from tkinter import messagebox
        messagebox.showinfo("Succès", "Membre ajouté avec succès !")

    tk.Button(frame, text="Ajouter", command=action).pack(pady=10)
