import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import os

# Funções de operação
# Funções de operação
def open_images():
    global images
    filetypes = [("All Image Files", "*.jpg *.jpeg *.png *.gif *.bmp *.webp *.tiff *.ico *.heic *.jfif *.svg *.dds")]
    img_paths = filedialog.askopenfilenames(title="Open Images", filetypes=filetypes)

    if img_paths:
        images.clear()
        loaded_canvas.delete("all")
        for index, path in enumerate(img_paths[:20]):  # Limita a 20 imagens
            img = Image.open(path)
            img.thumbnail((50, 50))
            images.append({"path": path, "thumbnail": ImageTk.PhotoImage(img)})
            draw_loaded_item(index, os.path.basename(path), images[-1]["thumbnail"])


def draw_loaded_item(index, filename, thumbnail):
    y_position = index * 60
    color = "#FFFFFF" if index % 2 == 0 else "#E0E0E0"

    # Retângulo de fundo (listrado)
    loaded_canvas.create_rectangle(5, y_position, 285, y_position + 60, fill=color, outline="")

    # Ícone da imagem
    loaded_canvas.create_image(30, y_position + 30, image=thumbnail)

    # Nome do arquivo
    loaded_canvas.create_text(80, y_position + 30, text=filename, anchor="w", font=("Arial", 10))

def convert_images():
    if not images:
        messagebox.showerror("No Images", "Please add images before converting.")
        return
    
    file_extension = output_format_var.get()
    if not file_extension:
        messagebox.showerror("Select Format", "Please select a format to convert.")
        return

    save_directory = filedialog.askdirectory(title="Select Output Folder")
    if not save_directory:
        return

    try:
        converted_canvas.delete("all")
        for index, img_data in enumerate(images):
            img = Image.open(img_data["path"])
            file_name = os.path.splitext(os.path.basename(img_data["path"]))[0]
            save_path = f"{save_directory}/{file_name}_converted{file_extension}"
            img.save(save_path)
            
            # Exibir arquivos convertidos com o mesmo padrão listrado
            draw_converted_item(index, os.path.basename(save_path))
        
        messagebox.showinfo("Conversion Complete", "Images converted successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Could not save images: {e}")

def draw_converted_item(index, filename):
    y_position = index * 30
    color = "#FFFFFF" if index % 2 == 0 else "#E0E0E0"

    # Retângulo de fundo (listrado)
    converted_canvas.create_rectangle(5, y_position, 285, y_position + 30, fill=color, outline="")

    # Nome do arquivo convertido
    converted_canvas.create_text(10, y_position + 15, text=filename, anchor="w", font=("Arial", 10))

def choose_output_folder():
    folder = filedialog.askdirectory(title="Select Output Folder")
    if folder:
        messagebox.showinfo("Folder Selected", f"Output folder set to: {folder}")

def show_history():
    messagebox.showinfo("History", "Feature coming soon!")

def exit_app():
    root.quit()

# Interface principal com Tkinter
root = tk.Tk()
root.title("Universal Conversor")
root.geometry("960x600")
root.configure(bg="#F5F5F5")

images = []

# Layout principal
sidebar = tk.Frame(root, bg="#A53D3D", width=200)
sidebar.pack(side="left", fill="y")

# Barra lateral
title_label = tk.Label(sidebar, text="Universal Conversor", font=("Metamorphous", 16), bg="#A53D3D", fg="white")
title_label.pack(pady=(20, 10))

# Ícones (substitua pelos caminhos corretos dos seus ícones)
add_icon = ImageTk.PhotoImage(file="plus.png")
convert_icon = ImageTk.PhotoImage(file="img.png")
menu_icon = ImageTk.PhotoImage(file="menu.png")
history_icon = ImageTk.PhotoImage(file="history.png")
exit_icon = ImageTk.PhotoImage(file="exit.png")
arrow_icon = ImageTk.PhotoImage(file="arrow.png")
cream_icon = ImageTk.PhotoImage(file="cre.png")

add_button = tk.Button(sidebar, image=add_icon, text=" ADICIONAR", compound="left", font=("Metamorphous", 12), bg="#A53D3D", fg="white", command=open_images, borderwidth=0)
add_button.pack(anchor="w", padx=10, pady=5)

convert_button = tk.Button(sidebar, image=convert_icon, text=" Converter", compound="left", font=("Metamorphous", 12), bg="#A53D3D", fg="white", command=convert_images, borderwidth=0)
convert_button.pack(anchor="w", padx=10, pady=5)

cream_label = tk.Label(sidebar, image=cream_icon, bg="#A53D3D")
cream_label.pack(pady=(30, 5))

creators_label = tk.Label(sidebar, text="Creator: joelysom o Generoso", font=("Metamorphous", 8), bg="#A53D3D", fg="white")
creators_label.pack()

# Conteúdo principal
header = tk.Frame(root, bg="white", height=50)
header.pack(fill="x")

menu_button = tk.Button(header, image=menu_icon, command=choose_output_folder, bg="white", borderwidth=0)
menu_button.pack(side="left", padx=10)

history_button = tk.Button(header, image=history_icon, command=show_history, bg="white", borderwidth=0)
history_button.pack(side="right", padx=10)

exit_button = tk.Button(header, image=exit_icon, command=exit_app, bg="white", borderwidth=0)
exit_button.pack(side="right", padx=10)

# Área de pré-visualização de carregados e convertidos
content = tk.Frame(root, bg="white")
content.pack(fill="both", expand=True, pady=20)

loaded_label = tk.Label(content, text="Carregados", font=("Metamorphous", 12), bg="white")
loaded_label.grid(row=0, column=0, padx=20, sticky="w")

loaded_canvas = tk.Canvas(content, width=290, height=400, bg="white", highlightthickness=0)
loaded_canvas.grid(row=1, column=0, padx=20, sticky="n")

arrow_label = tk.Label(content, image=arrow_icon, bg="white")
arrow_label.grid(row=1, column=1, padx=10)

converted_label = tk.Label(content, text="Convertidos", font=("Metamorphous", 12), bg="white")
converted_label.grid(row=0, column=2, padx=20, sticky="w")

converted_canvas = tk.Canvas(content, width=290, height=400, bg="white", highlightthickness=0)
converted_canvas.grid(row=1, column=2, padx=20, sticky="n")

# Opções de formato
output_format_var = tk.StringVar()
format_options = [".jpg", ".png", ".gif", ".bmp", ".webp", ".tiff", ".ico", ".heic", ".jfif", ".svg",".dds"]
format_menu = ttk.Combobox(content, textvariable=output_format_var, values=format_options, state="readonly")
format_menu.set("Escolher FileType")
format_menu.grid(row=2, column=1, pady=10)

root.mainloop()
