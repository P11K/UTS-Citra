from tkinter import Tk, Frame, Button, Canvas, filedialog, Scale
from PIL import Image, ImageTk, ImageEnhance

class ImageEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Editor")
        self.root.geometry("400x457")

        self.image_path = None
        self.loaded_image = None
        self.displayed_image = None
        self.angle = 0  # Sudut rotasi default
        self.mode = "rotate"  # Mode default
        self.rotated_image = None  # Menyimpan gambar yang diputar
        self.brightness_level = 1.0  # Tingkat kecerahan default

        self.canvas = Canvas(root, width=300, height=300)
        self.canvas.pack(pady=20)

        self.load_button = Button(root, text="Muat Gambar", command=self.load_image)
        self.load_button.pack()

        self.rotate_button = Button(root, text="Putar", command=self.set_rotate_mode)
        self.rotate_button.pack(side="left")

        self.brightness_button = Button(root, text="Kecerahan", command=self.set_brightness_mode)
        self.brightness_button.pack(side="left", padx=10)

        self.slider = Scale(root, from_=0, to=360, orient="horizontal", label="Sudut Rotasi")
        self.slider.pack_forget()
        self.slider_value = 0  # Menyimpan nilai slider

    def load_image(self):
        self.image_path = filedialog.askopenfilename()
        if self.image_path:
            self.loaded_image = Image.open(self.image_path)
            self.loaded_image.thumbnail((300, 300))  
            self.displayed_image = ImageTk.PhotoImage(self.loaded_image)
            self.canvas.create_image(0, 0, anchor="nw", image=self.displayed_image)
            # Menyetel ulang gambar yang diputar dan tingkat kecerahan saat memuat gambar baru
            self.rotated_image = None
            self.brightness_level = 1.0

    def set_rotate_mode(self):
        if self.mode == "brightness":
            self.mode = "rotate"
            self.slider_value = self.slider.get()  # Menyimpan nilai slider saat ini
        self.show_ui()

    def set_brightness_mode(self):
        if self.mode == "rotate":
            self.mode = "brightness"
            self.slider_value = self.slider.get()  # Menyimpan nilai slider saat ini
        self.show_ui()

    def show_ui(self):
        if self.mode == "rotate":
            self.slider.config(label="Sudut Rotasi")
            self.slider.pack()
            self.slider.set(self.slider_value)  # Mengatur posisi slider ke nilai yang disimpan
            self.slider.config(command=self.rotate_image)
        elif self.mode == "brightness":
            self.slider.config(label="Kecerahan")
            self.slider.pack()
            self.slider.set(100 * self.brightness_level)  # Mengatur posisi slider ke tingkat kecerahan saat ini
            self.slider.config(command=self.adjust_brightness)
        self.update_preview()

    def rotate_image(self, angle):
        self.angle = int(angle)
        if self.image_path:
            if self.rotated_image is None:
                self.rotated_image = self.loaded_image.rotate(self.angle)
            else:
                self.rotated_image = self.rotated_image.rotate(self.angle - self.slider_value)
        print("Gambar diputar dengan sukses.")
        self.slider_value = self.angle
        self.update_preview()

    def adjust_brightness(self, value):
        self.brightness_level = float(value) / 100.0
        if self.image_path:
            enhancer = ImageEnhance.Brightness(self.rotated_image if self.rotated_image else self.loaded_image)  # Menyesuaikan kecerahan gambar yang diputar jika ada, jika tidak menyesuaikan gambar asli
            self.rotated_image = enhancer.enhance(self.brightness_level)
        print("Kecerahan diatur dengan sukses.")
        self.update_preview()

    def update_preview(self):
        if self.rotated_image:
            preview_image = self.rotated_image
        else:
            preview_image = self.loaded_image
        self.displayed_image = ImageTk.PhotoImage(preview_image)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.displayed_image)

def main():
    root = Tk()
    app = ImageEditorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
