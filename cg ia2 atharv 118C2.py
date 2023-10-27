import tkinter as tk
from tkinter import ttk
from tkinter.colorchooser import askcolor
from PIL import Image, ImageDraw, ImageTk, ImageGrab
import random

class DrawingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Advanced Drawing App")
        self.geometry("800x600")

        # Custom ttk style
        style = ttk.Style()
        style.configure("TButton", padding=10, relief="flat", font=("Helvetica", 12))
        style.configure("TLabel", font=("Helvetica", 12))

        self.current_tool = "pencil"
        self.start_x, self.start_y = 0, 0
        self.color = "black"
        self.size = 2

        self.text_to_place = ""
        self.placing_text = False

        self.canvas = tk.Canvas(self, width=800, height=600, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.tools_frame = ttk.Frame(self, padding=(10, 10))
        self.tools_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.tools_box = ttk.LabelFrame(self.tools_frame, text="Tools")
        self.shapes_box = ttk.LabelFrame(self.tools_frame, text="Shapes")
        self.tools_box.pack(pady=10, padx=10, fill=tk.X)
        self.shapes_box.pack(pady=10, padx=10, fill=tk.X)

        self.tool_buttons = {
            "Pencil": ttk.Button(self.tools_box, text="Pencil", command=lambda: self.set_tool("pencil")),
            "Eraser": ttk.Button(self.tools_box, text="Eraser", command=lambda: self.set_tool("eraser")),
            "Spray": ttk.Button(self.tools_box, text="Spray", command=lambda: self.set_tool("spray")),
            "Text": ttk.Button(self.tools_box, text="Text", command=self.show_text_input),
        }

        for button in self.tool_buttons.values():
            button.pack(pady=5, fill=tk.X)

        self.shape_buttons = {
            "Line": ttk.Button(self.shapes_box, text="Line", command=lambda: self.set_tool("line")),
            "Rectangle": ttk.Button(self.shapes_box, text="Rectangle", command=lambda: self.set_tool("rectangle")),
            "Circle": ttk.Button(self.shapes_box, text="Circle", command=lambda: self.set_tool("circle")),
        }

        for button in self.shape_buttons.values():
            button.pack(pady=5, fill=tk.X)

        self.brush_size_label = ttk.Label(self.tools_box, text="Brush Size:")
        self.brush_size_label.pack(pady=5, fill=tk.X)

        self.brush_size_frame = ttk.Frame(self.tools_box)
        self.brush_size_frame.pack(pady=5, fill=tk.X)

        self.size_minus_button = ttk.Button(self.brush_size_frame, text="-", command=self.decrease_brush_size)
        self.size_minus_button.grid(row=0, column=0, padx=5)

        self.brush_size_entry = ttk.Label(self.brush_size_frame, text=str(self.size))
        self.brush_size_entry.grid(row=0, column=1)

        self.size_plus_button = ttk.Button(self.brush_size_frame, text="+", command=self.increase_brush_size)
        self.size_plus_button.grid(row=0, column=2, padx=5)

        self.text_input_frame = ttk.Frame(self.tools_box)
        self.text_entry = ttk.Entry(self.text_input_frame)
        self.text_button = ttk.Button(self.text_input_frame, text="Place Text", command=self.place_text)

        self.clear_button = ttk.Button(self.tools_frame, text="Clear", command=self.clear_canvas)
        self.clear_button.pack(pady=5, fill=tk.X)

        self.canvas.bind("<Button-1>", self.on_start)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_drop)

        self.set_tool_cursor()

        self.menu = tk.Menu(self)
        self.config(menu=self.menu)

    def set_tool(self, tool_name):
        self.current_tool = tool_name
        self.set_tool_cursor()

    def set_color(self):
        color_code = askcolor()
        if color_code:
            self.color = color_code[1]

    def increase_brush_size(self):
        self.size += 1
        self.update_brush_size_label()

    def decrease_brush_size(self):
        if self.size > 1:
            self.size -= 1
            self.update_brush_size_label()

    def update_brush_size_label(self):
        self.brush_size_entry.config(text=str(self.size))

    def show_text_input(self):
        self.text_input_frame.pack(pady=5, fill=tk.X)
        self.text_entry.pack(pady=5, fill=tk.X)
        self.text_button.pack(pady=5, fill=tk.X)

    def hide_text_input(self):
        self.text_input_frame.pack_forget()
        self.text_entry.delete(0, "end")
        self.placing_text = False

    def set_tool_cursor(self):
        cursor = "arrow"
        if self.current_tool == "pencil":
            cursor = "pencil"
        elif self.current_tool == "eraser":
            cursor = "X_cursor"
        elif self.current_tool == "spray":
            cursor = "spraycan"
        self.canvas.config(cursor=cursor)

    def on_start(self, event):
        if self.current_tool == "text":
            self.text_to_place = self.text_entry.get()
            self.placing_text = True
            self.hide_text_input()
        else:
            self.start_x, self.start_y = event.x, event.y

    def on_drag(self, event):
        x, y = event.x, event.y
        if self.current_tool == "pencil":
            self.canvas.create_line(self.start_x, self.start_y, x, y, fill=self.color, width=self.size)
            self.start_x, self.start_y = x, y
        elif self.current_tool == "eraser":
            self.canvas.create_line(self.start_x, self.start_y, x, y, fill="white", width=self.size)
            self.start_x, start_y = x, y
        elif self.current_tool == "spray":
            for _ in range(50):
                spray_x = x + random.randint(-self.size, self.size)
                spray_y = y + random.randint(-self.size, self.size)
                self.canvas.create_oval(spray_x, spray_y, spray_x + 1, spray_y + 1, fill=self.color)

    def on_drop(self, event):
        x, y = event.x, event.y
        if self.current_tool == "line":
            self.canvas.create_line(self.start_x, self.start_y, x, y, fill=self.color, width=self.size)
        elif self.current_tool == "rectangle":
            self.canvas.create_rectangle(self.start_x, self.start_y, x, y, outline=self.color, width=self.size)
        elif self.current_tool == "circle":
            self.canvas.create_oval(self.start_x, self.start_y, x, y, outline=self.color, width=self.size)

    def clear_canvas(self):
        self.canvas.delete("all")

    def place_text(self):
        if self.text_to_place:
            self.placing_text = True
            self.hide_text_input()
        else:
            self.show_text_input()

if __name__ == "__main__":
    app = DrawingApp()
    app.mainloop()
