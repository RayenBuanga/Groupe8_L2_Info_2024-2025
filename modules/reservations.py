import tkinter as tk
from db_config import get_connection

def ajouter(act_id, res_id, date, h_debut, h_fin):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO reservations (activite_id, ressource_id, date, heure_debut, heure_fin) VALUES (%s, %s, %s, %s, %s)", 
                (act_id, res_id, date, h_debut, h_fin))
    conn.commit()
    conn.close()

def build_interface(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    labels = ["ID Activité", "ID Ressource", "Date (YYYY-MM-DD)", "Heure début", "Heure fin"]
    entries = []

    for label in labels:
        tk.Label(frame, text=label).pack()
        entry = tk.Entry(frame)
        entry.pack()
        entries.append(entry)

    def action():
        ajouter(*[e.get() for e in entries])
        from tkinter import messagebox
        messagebox.showinfo("Succès", "Réservation ajoutée avec succès !")

    tk.Button(frame, text="Ajouter", command=action).pack(pady=10)
