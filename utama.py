from tkinter import Tk, Frame, Button, Canvas, filedialog, Scale
from PIL import Image, ImageTk, ImageEnhance, ImageOps, ImageFilter


class photoshop_lite:
    def __init__(self, root):
        self.root = root
        self.root.title("PhotoShop Ala Ala")
        self.root.geometry("500x468")

        self.image_path = None
        self.loaded_image = None
        self.displayed_image = None
        self.angle = 0  # Sudut rotasi default
        self.mode = "putar"  # Mode default
        self.gambar_putar = None  # Menyimpan gambar yang diputar
        self.tingkat_kecerahan = 1.0  # Tingkat kecerahan default
        self.crop_mode = False  # Mode crop
        self.crop_start_x = None
        self.crop_start_y = None

        self.canvas = Canvas(root, width=300, height=300)
        self.canvas.pack(pady=20)

        self.tombol_muat = Button(root, text="Muat Gambar", command=self.loadgmbr)
        self.tombol_muat.pack()

        self.tombol_simpan = Button(root, text="Simpan", command=self.save_image, state="disabled")
        self.tombol_simpan.pack()

        self.tombol_putar = Button(root, text="Putar", command=self.rotate)
        self.tombol_putar.pack(side="left")

        self.tombol_kecerahan = Button(root, text="Kecerahan", command=self.kecerahan)
        self.tombol_kecerahan.pack(side="left", padx=10)

        self.tombol_mirror = Button(root, text="Mirror", command=self.mirror)
        self.tombol_mirror.pack(side="left", padx=10)

        self.tombol_negatif = Button(root, text="Negatif", command=self.negatif)
        self.tombol_negatif.pack(side="left", padx=10)

        self.tombol_grayscale = Button(root, text="Grayscale", command=self.grayscale)
        self.tombol_grayscale.pack(side="left", padx=10)

        self.tombol_blur = Button(root, text="Blur", command=self.blur)
        self.tombol_blur.pack(side="left", padx=10)

        self.tombol_crop = Button(root, text="Crop", command=self.crop)
        self.tombol_crop.pack(side="left", padx=10)

        self.slider = Scale(root, from_=0, to=360, orient="horizontal", label="Sudut Rotasi")
        self.slider.pack_forget()
        self.slider_value = 0  # Menyimpan nilai slider

    def loadgmbr(self):
        self.image_path = filedialog.askopenfilename()
        if self.image_path:
            self.loaded_image = Image.open(self.image_path)
            width, height = self.loaded_image.size
            aspect_ratio = width / height
            canvas_width = 500
            canvas_height = int(canvas_width / aspect_ratio)
            self.canvas.config(width=canvas_width, height=canvas_height)
            self.loaded_image = self.loaded_image.resize((canvas_width, canvas_height))
            self.displayed_image = ImageTk.PhotoImage(self.loaded_image)
            self.canvas.create_image(0, 0, anchor="nw", image=self.displayed_image)
            self.gambar_putar = None
            self.tingkat_kecerahan = 1.0
            self.tombol_simpan.config(state="normal")
    def save_image(self):
        if self.loaded_image:
            save_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")])
            if save_path:
                self.loaded_image.save(save_path)
    def rotate(self):
        if self.mode == "putar":
            self.slider_value = self.slider.get()  
            self.ui()
        else:
            self.mode = "putar"
            self.slider_value = self.slider.get()  
            self.ui()

    def kecerahan(self):
        if self.mode == "putar" or self.mode == "mirror" or self.mode == "negatif" or self.mode == "grayscale" or self.mode == "blur":
            self.mode = "kecerahan"
            self.slider_value = self.slider.get()
            self.ui()

    def mirror(self):
        if self.mode == "putar" or self.mode == "kecerahan" or self.mode == "negatif" or self.mode == "grayscale" or self.mode == "blur":
            self.mode = "mirror"
            self.ui()

    def negatif(self):
        if self.mode == "putar" or self.mode == "kecerahan" or self.mode == "mirror" or self.mode == "grayscale" or self.mode == "blur":
            self.mode = "negatif"
            self.ui()

    def grayscale(self):
        if self.mode == "putar" or self.mode == "kecerahan" or self.mode == "mirror" or self.mode == "negatif" or self.mode == "blur":
            self.mode = "grayscale"
            self.ui()

    def blur(self):
        if self.mode == "putar" or self.mode == "kecerahan" or self.mode == "mirror" or self.mode == "negatif" or self.mode == "grayscale":
            self.mode = "blur"
            self.ui()

    def crop(self):
        if self.crop_mode:
            self.canvas.unbind("<Button-1>")
            self.tombol_crop.config(text="Crop")
            self.crop_mode = False
            self.crop_image()  # Memanggil crop_image setelah crop selesai
            self.ui()
        else:
            self.canvas.bind("<Button-1>", self.start_crop)
            self.tombol_crop.config(text="Done")
            self.crop_mode = True

    def start_crop(self, event):
        self.crop_start_x = event.x
        self.crop_start_y = event.y
        self.canvas.bind("<B1-Motion>", self.draw_crop)

    def draw_crop(self, event):
        self.canvas.delete("crop_rect")
        self.canvas.create_rectangle(self.crop_start_x, self.crop_start_y, event.x, event.y, outline="red", tag="crop_rect")

    def ui(self):
        if self.mode == "putar":
            self.slider.config(label="Sudut Rotasi")
            self.slider.pack()
            self.slider.set(self.slider_value)
            self.slider.config(command=self.putar_gambar)
        elif self.mode == "kecerahan":
            self.slider.config(label="Kecerahan")
            self.slider.pack()
            self.slider.set(100 * self.tingkat_kecerahan)
            self.slider.config(command=self.atur_kecerahan)
        elif self.mode == "mirror":
            self.slider.pack_forget()
            self.perbarui_pratinjau()
        elif self.mode == "negatif":
            self.slider.pack_forget()
            self.perbarui_pratinjau()
        elif self.mode == "grayscale":
            self.slider.pack_forget()
            self.perbarui_pratinjau()
        elif self.mode == "blur":
            self.slider.pack_forget()
            self.perbarui_pratinjau()
            

    def perbarui_pratinjau(self):
        if self.gambar_putar:
            gambar_pratinjau = self.gambar_putar
        else:
            gambar_pratinjau = self.loaded_image
        self.displayed_image = ImageTk.PhotoImage(gambar_pratinjau)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.displayed_image)

    def putar_gambar(self, sudut):
        self.angle = int(sudut)
        if self.image_path:
            self.gambar_putar = self.loaded_image.rotate(self.angle)
        self.perbarui_pratinjau()

    def atur_kecerahan(self, nilai):
        self.tingkat_kecerahan = float(nilai) / 100.0
        if self.image_path:
            enhancer = ImageEnhance.Brightness(self.loaded_image)
            self.gambar_putar = enhancer.enhance(self.tingkat_kecerahan)
        self.perbarui_pratinjau()

    def mirror(self):
        if self.image_path:
            mirrored_image = self.loaded_image.transpose(Image.FLIP_LEFT_RIGHT)
            self.gambar_putar = mirrored_image
        self.perbarui_pratinjau()

    def negatif(self):
        if self.image_path:
            self.gambar_putar = ImageOps.invert(self.loaded_image)
            self.perbarui_pratinjau()

    def grayscale(self):
        if self.image_path:
            self.gambar_putar = self.loaded_image.convert("L")
            self.perbarui_pratinjau()

    def blur(self):
        if self.image_path:
            self.gambar_putar = self.loaded_image.filter(ImageFilter.BLUR)
            self.perbarui_pratinjau()

    def crop_image(self):
        if self.image_path and self.crop_start_x is not None and self.crop_start_y is not None:
            x0, y0 = self.crop_start_x, self.crop_start_y
            x1, y1 = self.canvas.winfo_pointerx() - self.canvas.winfo_rootx(), self.canvas.winfo_pointery() - self.canvas.winfo_rooty()
            cropped_image = self.loaded_image.crop((x0, y0, x1, y1))
            self.gambar_putar = cropped_image
            self.perbarui_pratinjau()


def main():
    root = Tk()
    app = photoshop_lite(root)
    root.mainloop()


if __name__ == "__main__":
    main()
