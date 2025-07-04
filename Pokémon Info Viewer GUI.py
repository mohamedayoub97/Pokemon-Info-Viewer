import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from io import BytesIO

# --- Fetch Pokémon Data ---
def fetch_pokemon_data():
    name = entry.get().strip().lower()
    if not name:
        messagebox.showerror("Error", "Please enter a Pokémon name.")
        return

    url = f"https://pokeapi.co/api/v2/pokemon/{name}"
    response = requests.get(url)

    if response.status_code != 200:
        messagebox.showerror("Error", f"Pokémon '{name}' not found.")
        return

    data = response.json()
    display_info(data)

# --- Display Pokémon Data ---
def display_info(data):
    for widget in result_frame.winfo_children():
        widget.destroy()

    name = data["name"].capitalize()
    id_ = data["id"]
    height = data["height"]
    weight = data["weight"]

    # Sprite
    sprite_url = data["sprites"]["front_default"]
    if sprite_url:
        sprite_image = Image.open(BytesIO(requests.get(sprite_url).content))
        sprite_photo = ImageTk.PhotoImage(sprite_image)
        img_label = tk.Label(result_frame, image=sprite_photo, bg="#000000")
        img_label.image = sprite_photo
        img_label.pack()

    tk.Label(result_frame, text=f"{name} (ID: {id_})", font=("Arial", 18, "bold"),
             bg="#000000", fg="#FFD700").pack(pady=5)
    tk.Label(result_frame, text=f"Height: {height} | Weight: {weight}",
             font=("Arial", 12), bg="#000000", fg="#FFFFFF").pack()

    types = ", ".join([t["type"]["name"].capitalize() for t in data["types"]])
    tk.Label(result_frame, text=f"Type(s): {types}", font=("Arial", 12, "bold"),
             bg="#000000", fg="#00FFFF").pack()

    abilities = ", ".join(
        [f"{a['ability']['name'].capitalize()}{' (Hidden)' if a['is_hidden'] else ''}"
         for a in data["abilities"]])
    tk.Label(result_frame, text=f"Abilities: {abilities}", font=("Arial", 12),
             bg="#000000", fg="#7CFC00").pack()

    tk.Label(result_frame, text="Base Stats", font=("Arial", 14, "underline"),
             bg="#000000", fg="#FF69B4").pack(pady=5)

    for stat in data["stats"]:
        stat_name = stat["stat"]["name"].capitalize()
        stat_value = stat["base_stat"]
        tk.Label(result_frame, text=f"{stat_name}: {stat_value}", font=("Arial", 11),
                 bg="#000000", fg="#FFA07A").pack()

# --- Hover Button Effects ---
def on_enter(e):
    fetch_btn["background"] = "#FF6347"
    fetch_btn["fg"] = "#FFFFFF"

def on_leave(e):
    fetch_btn["background"] = "#FF4500"
    fetch_btn["fg"] = "#FFFFFF"

# --- Main GUI Setup ---
root = tk.Tk()
root.title("Pokémon Info Viewer")
root.geometry("420x650")
root.resizable(False, False)

# Gradient Background via Canvas
gradient = tk.Canvas(root, width=420, height=650)
gradient.pack(fill="both", expand=True)

# Draw gradient manually
for i in range(0, 650):
    r = int(17 + (34-17)*(i/650))
    g = int(17 + (68-17)*(i/650))
    b = int(34 + (119-34)*(i/650))
    color = f'#{r:02x}{g:02x}{b:02x}'
    gradient.create_line(0, i, 420, i, fill=color)

# Widgets on top of gradient
input_frame = tk.Frame(root, bg="#222")
input_frame.place(relx=0.5, rely=0.05, anchor="n")

tk.Label(input_frame, text="Enter Pokémon Name:", font=("Arial", 13),
         bg="#222", fg="#00FF7F").grid(row=0, column=0, padx=5)
entry = tk.Entry(input_frame, font=("Arial", 13), width=15)
entry.grid(row=0, column=1, padx=5)

# Stylish button
fetch_btn = tk.Button(root, text="🔍 Fetch Info", command=fetch_pokemon_data,
                      font=("Arial", 13, "bold"), bg="#FF4500", fg="white", activebackground="#FF6347",
                      cursor="hand2", bd=0, relief="raised", padx=10, pady=5)
fetch_btn.place(relx=0.5, rely=0.13, anchor="n")

fetch_btn.bind("<Enter>", on_enter)
fetch_btn.bind("<Leave>", on_leave)

# Result Display Frame
result_frame = tk.Frame(root, bg="#000000", bd=2, relief="ridge")
result_frame.place(relx=0.5, rely=0.2, anchor="n", width=380, height=410)

root.mainloop()
