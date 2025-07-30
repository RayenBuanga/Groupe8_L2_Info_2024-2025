import tkinter as tk
from db_config import get_connection

def ajouter(titre, date, h_debut, h_fin, responsable_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO activites (titre, date, heure_debut, heure_fin, responsable_id) VALUES (%s, %s, %s, %s, %s)", 
                (titre, date, h_debut, h_fin, responsable_id))
    conn.commit()
    conn.close()

def build_interface(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    labels = ["Titre", "Date (YYYY-MM-DD)", "Heure début", "Heure fin", "ID Responsable"]
    entries = []

    for label in labels:
        tk.Label(frame, text=label).pack()
        entry = tk.Entry(frame)
        entry.pack()
        entries.append(entry)

    def action():
        ajouter(*[e.get() for e in entries])
        from tkinter import messagebox
        messagebox.showinfo("Succès", "Activité ajoutée avec succès !")

    tk.Button(frame, text="Ajouter", command=action).pack(pady=10)
