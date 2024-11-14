import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk, ImageDraw, ImageFilter
from decouple import config

root = None
label_image = None
canvas = None
line_id = None
text_id = None

def sleep():
    global root, label_image, line_id, text_id
    if canvas and line_id:
        canvas.itemconfig(line_id, fill='red')
        canvas.itemconfig(text_id, text="Sleeping...Zzz...")

def awaken():
    global root, label_image, line_id, text_id
    root.deiconify()
    if canvas and line_id:
        canvas.itemconfig(line_id, fill='green')
        canvas.itemconfig(text_id, text="At your service")

def disappear():
    global root
    root.iconify()

def restore():
    global root
    root.deiconify()

def update_text_listener(new_text):
    global canvas, text_id
    new_text = new_text[:170] + ("..." if len(new_text) > 170 else "")
    if canvas and text_id:
        canvas.itemconfig(text_id, text=new_text, fill='#0096FF')

def update_text_speaker(new_text):
    global canvas, text_id
    new_text = new_text[:170] + ("..." if len(new_text) > 170 else "")
    if canvas and text_id:
        canvas.itemconfig(text_id, text=new_text, fill='yellow')

def update_text(new_text):
    global canvas, text_id
    if canvas and text_id:
        canvas.itemconfig(text_id, text=new_text)

def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    points = [x1 + radius, y1, x1 + radius, y1,
              x2 - radius, y1, x2 - radius, y1,
              x2, y1, x2, y1 + radius,
              x2, y1 + radius, x2, y2 - radius,
              x2, y2 - radius, x2, y2,
              x2 - radius, y2, x2 - radius, y2,
              x1 + radius, y2, x1 + radius, y2,
              x1, y2, x1, y2 - radius,
              x1, y2 - radius, x1, y1 + radius,
              x1, y1 + radius, x1, y1]
    return canvas.create_polygon(points, **kwargs, smooth=True)

def appear():
    global root, label_image, canvas, line_id, text_id

    if root is not None:
        print("Window Already Open")
        restore()
        return

    root = tk.Tk()
    root.title("The Virtual Assistant")
    root.geometry("550x400")
    root.wm_attributes("-alpha", 0.9)
    root.configure(bg='#1e1e1e')  

    # Header Frame with Gradient Background
    header_frame = tk.Frame(root, bg='#333333', height=100, width=550)
    header_frame.pack_propagate(False)
    header_frame.grid(row=0, column=0, sticky="ew")

    # Adding a Logo Image
    logo = config("MEDIA_DIR") + "/" + "va.jpeg"
    image = Image.open(logo)
    image = image.resize((80, 80), Image.LANCZOS)
    photo = ImageTk.PhotoImage(image)

    label_image = tk.Label(header_frame, image=photo, bg='#333333')
    label_image.image = photo
    label_image.pack(side="left", padx=15, pady=10)

    # Assistant Name Label
    assistant_name = tk.Label(header_frame, text="Virtual Assistant", font=("Helvetica", 20, "bold"), fg="white", bg='#333333')
    assistant_name.pack(side="left", padx=10)

    # Body Canvas with Rounded Rectangle and Gradient
    canvas = tk.Canvas(root, width=520, height=250, bg='#1e1e1e', highlightthickness=0)
    canvas.grid(row=1, column=0, pady=(10, 10), padx=10)

    # Draw Rounded Rectangle Background for text area
    create_rounded_rectangle(canvas, 10, 10, 510, 240, radius=20, fill="#2b2b2b", outline="")

    # Line for Active/Inactive Status
    line_id = canvas.create_line(125, 20, 395, 20, width=6, fill='green')  

    # Display Text Message in Assistant Canvas
    text_id = canvas.create_text(260, 130, text="At your service", fill='#00ffcc', font=("Arial", 16, "italic"), width=450)

    # Footer Frame for Action Buttons
    footer_frame = tk.Frame(root, bg='#1e1e1e')
    footer_frame.grid(row=2, column=0, pady=(10, 10), padx=10)

    # Action Buttons with Styling
    button_font = font.Font(family="Helvetica", size=10, weight="bold")
    button_style = {"width": 12, "height": 2, "bg": "#007acc", "fg": "white", "relief": "raised", "bd": 2, "font": button_font}

    tk.Button(footer_frame, text="Awaken", command=awaken, **button_style).grid(row=0, column=0, padx=5, pady=5)
    tk.Button(footer_frame, text="Sleep", command=sleep, **button_style).grid(row=0, column=1, padx=5, pady=5)
    tk.Button(footer_frame, text="Hide", command=disappear, **button_style).grid(row=0, column=2, padx=5, pady=5)
    tk.Button(footer_frame, text="Close", command=lambda: close_window(exit_event=None), **button_style).grid(row=0, column=3, padx=5, pady=5)

    root.resizable(False, False)
    root.mainloop()

def close_window(exit_event):
    global root
    if root:
        root.quit()
        root.update_idletasks()
        if exit_event:
            exit_event.set()
