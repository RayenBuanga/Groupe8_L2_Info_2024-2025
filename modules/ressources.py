import tkinter as tk
from db_config import get_connection

def ajouter(nom, type_):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO ressources (nom, type) VALUES (%s, %s)", (nom, type_))
    conn.commit()
    conn.close()

def build_interface(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    tk.Label(frame, text="Nom").pack()
    nom = tk.Entry(frame); nom.pack()
    tk.Label(frame, text="Type").pack()
    type_ = tk.Entry(frame); type_.pack()

    def action():
        ajouter(nom.get(), type_.get())
        from tkinter import messagebox
        messagebox.showinfo("Succès", "Ressource ajoutée avec succès !")

    tk.Button(frame, text="Ajouter", command=action).pack(pady=10)
