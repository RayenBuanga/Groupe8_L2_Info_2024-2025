import tkinter as tk
from tkinter import ttk
from db_config import get_connection
from modules import membres, activites, ressources, reservations

def afficher_table(frame, table, colonnes):
    for widget in frame.winfo_children():
        widget.destroy()
    tree = ttk.Treeview(frame, columns=colonnes, show='headings')
    for col in colonnes:
        tree.heading(col, text=col)
        tree.column(col, width=120)

    tree.tag_configure('oddrow', background='#eaf0fa')
    tree.tag_configure('evenrow', background='#f5f6fa')
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table}")
    rows = cur.fetchall()
    conn.close()
    for i, row in enumerate(rows):
        tag = 'evenrow' if i % 2 == 0 else 'oddrow'
        tree.insert('', 'end', values=row, tags=(tag,))
    tree.pack(expand=True, fill='both')

def interface():
    root = tk.Tk()
    root.geometry("1000x600")
    root.title("Club Culturel")
    root.configure(bg="#f5f6fa")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TFrame", background="#f5f6fa")
    style.configure("TButton", font=("Segoe UI", 12, "bold"), background="#4078c0", foreground="white", padding=8)
    style.map("TButton",
        background=[('active', '#274472'), ('!active', '#4078c0')],
        foreground=[('active', 'white'), ('!active', 'white')]
    )
    style.configure("TCombobox", font=("Segoe UI", 12), padding=6)
    style.map("TCombobox",
        fieldbackground=[('readonly', '#eaf0fa')],
        background=[('readonly', '#eaf0fa')]
    )
    style.configure("Treeview", font=("Segoe UI", 11), rowheight=28, background="#f5f6fa", fieldbackground="#f5f6fa")
    style.configure("Treeview.Heading", font=("Segoe UI", 12, "bold"), background="#4078c0", foreground="white")
    style.map("Treeview",
        background=[('selected', '#dbeafe')],
        foreground=[('selected', '#274472')]
    )

    sidebar = tk.Frame(root, bg="#274472", width=180)
    sidebar.pack(side="left", fill="y")

    logo = tk.Label(sidebar, text="🧑‍💼", font=("Segoe UI", 32), bg="#274472", fg="white")
    logo.pack(pady=(30, 10))
    tk.Label(sidebar, text="Club Culturel", font=("Segoe UI", 16, "bold"), bg="#274472", fg="white").pack(pady=(0, 30))

    def sidebar_btn(text, icon, command):
        btn = tk.Button(sidebar, text=f"{icon}  {text}", font=("Segoe UI", 13), bg="#4078c0", fg="white", bd=0, relief="flat", activebackground="#1b2838", activeforeground="white", padx=10, pady=10, command=command, anchor="w", cursor="hand2")
        btn.pack(fill="x", pady=6, padx=18)
        btn.bind("<Enter>", lambda e: btn.config(bg="#274472"))
        btn.bind("<Leave>", lambda e: btn.config(bg="#4078c0"))
        return btn

    sidebar_btn("Membres", "👤", lambda: membres.build_interface(content_frame))
    sidebar_btn("Activités", "📅", lambda: activites.build_interface(content_frame))
    sidebar_btn("Ressources", "📦", lambda: ressources.build_interface(content_frame))
    sidebar_btn("Réservations", "📝", lambda: reservations.build_interface(content_frame))

    main_area = tk.Frame(root, bg="#f5f6fa")
    main_area.pack(side="left", fill="both", expand=True)

    title_label = tk.Label(main_area, text="Gestion du club culturel", font=("Segoe UI", 22, "bold"), bg="#f5f6fa", fg="#274472")
    title_label.pack(pady=(20, 10))

    tk.Label(sidebar, text="Afficher", font=("Segoe UI", 13, "bold"), bg="#274472", fg="white").pack(pady=(10, 2), padx=18, anchor="w")
    affichage_menu = ttk.Combobox(sidebar, values=[
        "👤 Membres", "📅 Activités", "📦 Ressources", "📝 Réservations"
    ], state="readonly", width=18)
    affichage_menu.set("Afficher...")
    affichage_menu.pack(pady=(0, 18), padx=18, anchor="w")
    def on_afficher_hover(event):
        affichage_menu.configure(background="#dbeafe")
    def on_afficher_leave(event):
        affichage_menu.configure(background="#eaf0fa")
    affichage_menu.bind("<Enter>", on_afficher_hover)
    affichage_menu.bind("<Leave>", on_afficher_leave)

    content_frame = ttk.Frame(main_area)
    content_frame.pack(fill="both", expand=True, padx=20, pady=20)

    def on_select(event):
        choix = affichage_menu.get()
        if "Membres" in choix:
            afficher_table(content_frame, "membres", ["id", "nom", "prenom", "contact", "role"])
        elif "Activités" in choix:
            afficher_table(content_frame, "activites", ["id", "titre", "date", "heure_debut", "heure_fin", "responsable_id"])
        elif "Ressources" in choix:
            afficher_table(content_frame, "ressources", ["id", "nom", "type"])
        elif "Réservations" in choix:
            afficher_table(content_frame, "reservations", ["id", "activite_id", "ressource_id", "date", "heure_debut", "heure_fin"])
    affichage_menu.bind("<<ComboboxSelected>>", on_select)

    root.mainloop()

if __name__ == "__main__":
    interface()
