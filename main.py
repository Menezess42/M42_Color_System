from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk
import numpy as np
from conversor import Conversor
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as figCanTk
from matplotlib.figure import Figure


class App(Tk):
    def __init__(self):
        super().__init__()
        self.ar_xy = StringVar()
        self.rgbValue = StringVar()
        self.hsi_string = StringVar()
        self.cmy_string = StringVar()
        self.rgbValue_lu = StringVar()
        self.hsi_string_lu = StringVar()
        self.cmy_string_lu = StringVar()
        self.mainframe = None
        self.colorsframe = None
        self.mainframe_luminancia = None
        self.colorsframe_luminancia = None
        self.mainframe_luminancia_bts = None
        self.mainframe_hist = None
        self.mainframe_hist_graph = None
        self.mainframe_hist_graph_bts = None
        self.imgNumpy_mod = np.array((0, 0), dtype=np.int8)
        self.Images()
        self.Frames()
        self.create_menu()
        self.Labels()
        self.histogram_buts()
        self.luminancia_btus()
        self.column = 0
        self.row = 0

    def create_menu(self):
        menu_bar = Menu(self)
        self.config(menu=menu_bar)

        file_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open Image", command=self.open_image)

    def open_image(self):
        filetypes = (
            ("JPEG files", "*.jpg"),
            ("PNG files", "*.png"),
            ("All files", "*.*"),
        )
        filename = filedialog.askopenfilename(title="Select Image", filetypes=filetypes)
        if filename:
            self.Images(filename)

    def mainWindow_config(self):
        self.title("ColorSystem")
        self.iconbitmap("./images/lena.ico")
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.geometry("1500x800")
        self.tk.call("source", "./themes/Azure-ttk-theme-main/azure.tcl")
        self.tk.call("set_theme", "dark")

    def Frames(self):
        self.mainframe_luminancia = ttk.Frame(
            self, padding="5", relief="groove", borderwidth=1
        )
        self.mainframe_luminancia.grid(column=0, row=0, sticky=(N, W, S))
        self.mainframe_luminancia_bts = ttk.Frame(self.mainframe_luminancia)
        self.mainframe_luminancia_bts.grid(column=3, row=1, sticky=(N, S))
        self.colorsframe_luminancia = ttk.Frame(self.mainframe_luminancia, padding="5")
        self.colorsframe_luminancia.grid(column=3, row=2, sticky=(N, S))

        self.mainframe = ttk.Frame(self, padding="5", relief="groove", borderwidth=1)
        self.mainframe.grid(column=2, row=0, sticky=(N, E, S))
        self.colorsframe = ttk.Frame(self.mainframe, padding="20")
        self.colorsframe.grid(column=3, row=1, sticky=(N, S))

        self.mainframe_hist = ttk.Frame(
            self, padding="5", relief="groove", borderwidth=1
        )
        self.mainframe_hist.grid(column=1, row=0, sticky=(N, W, E, S))

        self.mainframe_hist_graph = ttk.Frame(self.mainframe_hist)
        self.mainframe_hist_graph.grid(column=1, row=1, sticky=(N, S, E, W))
        self.mainframe_hist_graph.place(relx=0.5, rely=0.25, anchor=CENTER)

        self.mainframe_hist_graph_bts = ttk.Frame(self.mainframe_hist)
        self.mainframe_hist_graph_bts.grid(column=1, row=2, sticky=(N, S, E, W))
        self.mainframe_hist_graph_bts.place(relx=0.5, rely=0.49, anchor=CENTER)
        # self.Labels()           #

    def Labels(self):
        self.imgLabel = ttk.Label(self.mainframe, image=self.img)
        self.imgLabel.grid(column=3, row=0, sticky=(N, W, E, S))
        self.rgb_label = ttk.Label(
            self.colorsframe, text="R  G  B", font=("Hack NF", 21)
        )
        self.rgb_label.grid(column=0, row=0, sticky=(N, S))

        self.imgLabel.bind("<Motion>", self.Motion)
        self.rgbValue_label = ttk.Label(
            self.colorsframe, textvariable=self.rgbValue, font=("Hack NF", 15)
        )
        self.rgbValue_label.grid(column=0, row=1, sticky=(N, S))

        self.h_label = ttk.Label(self.colorsframe, text="H S I", font=("Hack NF", 21))
        self.h_label.grid(column=0, row=2, sticky=(N, S))
        self.h_Valuelabel = ttk.Label(
            self.colorsframe, textvariable=self.hsi_string, font=("Hack NF", 15)
        )
        self.h_Valuelabel.grid(column=0, row=3, sticky=(N, S))

        self.cmy_label = ttk.Label(
            self.colorsframe, text="C  M  Y", font=("Hack NF", 21)
        )
        self.cmy_label.grid(column=0, row=4, sticky=(N, S))
        self.cmy_Valuelabel = ttk.Label(
            self.colorsframe, textvariable=self.cmy_string, font=("Hack NF", 15)
        )
        self.cmy_Valuelabel.grid(column=0, row=5, sticky=(N, S))

        self.imgLabel_lu = ttk.Label(self.mainframe_luminancia, image=self.img_mod)
        self.imgLabel_lu.bind("<Motion>", self.Motion)
        self.imgLabel_lu.grid(column=3, row=0, sticky=(N, W, E, S))
        self.rgb_label = ttk.Label(
            self.colorsframe_luminancia, text="R  G  B", font=("Hack NF", 21)
        )
        self.rgb_label.grid(column=0, row=0, sticky=(N, S))

        self.rgbValue_label_lu = ttk.Label(
            self.colorsframe_luminancia,
            textvariable=self.rgbValue_lu,
            font=("Hack NF", 15),
        )
        self.rgbValue_label_lu.grid(column=0, row=1, sticky=(N, S))
        self.h_label = ttk.Label(
            self.colorsframe_luminancia, text="H S I", font=("Hack NF", 21)
        )
        self.h_label.grid(column=0, row=2, sticky=(N, S))
        self.h_Valuelabel_lu = ttk.Label(
            self.colorsframe_luminancia,
            textvariable=self.hsi_string_lu,
            font=("Hack NF", 15),
        )
        self.h_Valuelabel_lu.grid(column=0, row=3, sticky=(N, S))
        self.cmy_label = ttk.Label(
            self.colorsframe_luminancia, text="C  M  Y", font=("Hack NF", 21)
        )
        self.cmy_label.grid(column=0, row=4, sticky=(N, S))
        self.cmy_Valuelabel = ttk.Label(
            self.colorsframe_luminancia,
            textvariable=self.cmy_string_lu,
            font=("Hack NF", 15),
        )
        self.cmy_Valuelabel.grid(column=0, row=5, sticky=(N, S))
        self.label_hist = ttk.Label(
            self.mainframe_hist, text="Histogram", font=("Hack NF", 21)
        )
        self.label_hist.grid(column=0, row=0, sticky=(N, W, E, S))
        self.label_hist.place(relx=0.5, rely=0.03, anchor=CENTER)
        self.canvas = figCanTk(self.fig, master=self.mainframe_hist_graph)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(column=0, row=0, sticky=(N, S, E))
        self.imgLabel_gray = ttk.Label(self.mainframe_hist, image=self.img_pil_gray)
        self.imgLabel_gray.grid(column=1, row=3, sticky=(N, W, E, S))
        self.imgLabel_gray.place(relx=0.5, rely=0.76, anchor=CENTER)

    def Hist(self, img):
        fig = Figure(figsize=(4, 3), dpi=100)
        ax = fig.add_subplot(111)
        n, bins, patches = ax.hist(img.flatten(), bins=256, range=(0, 255))
        self.fig = fig
        self.canvas = figCanTk(self.fig, master=self.mainframe_hist_graph)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(column=0, row=0, sticky=(N, S, E))

    def equalize(self):
        img_equalized = self.conversor.equalize(self.img_gray_saved)
        self.img_gray = img_equalized
        self.pil_image_gray = Image.fromarray(self.img_gray)
        self.pil_image_gray = self.pil_image_gray.resize((400, 350))
        self.img_pil_gray = ImageTk.PhotoImage(self.pil_image_gray)
        self.imgLabel_gray.configure(image=self.img_pil_gray)
        self.Hist(self.img_gray)

    def default_hist(self):
        self.img_gray = self.img_gray_saved
        self.pil_image_gray = Image.fromarray(self.img_gray)
        self.pil_image_gray = self.pil_image_gray.resize((400, 350))
        self.img_pil_gray = ImageTk.PhotoImage(self.pil_image_gray)
        self.imgLabel_gray.configure(image=self.img_pil_gray)
        self.Hist(self.img_gray)

    def hi_2_default(self):
        self.imgNumpy_mod = self.imgNumpy
        self.imgHsi_mod = self.imgHsi
        self.pil_image = Image.fromarray(self.imgNumpy_mod)
        self.img_pil = ImageTk.PhotoImage(self.pil_image)
        self.imgLabel_lu.configure(image=self.img_pil)

    def h_down(self):
        h = self.imgHsi_mod[:, :, 0]
        new_h = np.zeros_like(h)
        new_h[h > 10] = h[h > 10] - 10
        self.imgHsi_mod[:, :, 0] = np.where(h <= 10, 0, new_h)
        self.imgNumpy_mod = self.conversor.hsi_to_rgb(self.imgHsi_mod)
        self.imgCmy_mod = self.conversor.convert_rgb_to_cmy(self.imgNumpy_mod)
        self.pil_image = Image.fromarray(self.imgNumpy_mod)
        self.img_pil = ImageTk.PhotoImage(self.pil_image)
        self.imgLabel_lu.configure(image=self.img_pil)

    def h_up(self):
        h = self.imgHsi_mod[:, :, 0]
        new_h = np.minimum(h + 10, 360)
        new_h = np.where(h >= 350, 360, new_h)
        self.imgHsi_mod[:, :, 0] = new_h
        self.imgNumpy_mod = self.conversor.hsi_to_rgb(self.imgHsi_mod)
        self.imgCmy_mod = self.conversor.convert_rgb_to_cmy(self.imgNumpy_mod)
        self.pil_image = Image.fromarray(self.imgNumpy_mod)
        self.img_pil = ImageTk.PhotoImage(self.pil_image)
        self.imgLabel_lu.configure(image=self.img_pil)

    def i_down(self):
        i = self.imgHsi_mod[:, :, 2]
        new_i = np.zeros_like(i)
        new_i[i > 10] = i[i > 10] - 10
        self.imgHsi_mod[:, :, 2] = new_i
        self.imgNumpy_mod = self.conversor.hsi_to_rgb(self.imgHsi_mod)
        self.imgCmy_mod = self.conversor.convert_rgb_to_cmy(self.imgNumpy_mod)
        self.pil_image = Image.fromarray(self.imgNumpy_mod)
        self.img_pil = ImageTk.PhotoImage(self.pil_image)
        self.imgLabel_lu.configure(image=self.img_pil)

    def i_up(self):
        i = self.imgHsi_mod[:, :, 2]
        new_i = np.minimum(i + 10, 255)
        new_i = np.where(i >= 245, 255, new_i)
        self.imgHsi_mod[:, :, 2] = new_i
        self.imgNumpy_mod = self.conversor.hsi_to_rgb(self.imgHsi_mod)
        self.imgCmy_mod = self.conversor.convert_rgb_to_cmy(self.imgNumpy_mod)
        self.pil_image = Image.fromarray(self.imgNumpy_mod)
        self.img_pil = ImageTk.PhotoImage(self.pil_image)
        self.imgLabel_lu.configure(image=self.img_pil)

    def luminancia_btus(self):
        h_down_bt = ttk.Button(
            self.mainframe_luminancia_bts,
            text="-",
            command=self.h_down,
        )
        h_down_bt.grid(column=0, row=0, sticky=(N, S), pady=2)
        hue = ttk.Label(
            self.mainframe_luminancia_bts, text="   Hue   ", font=("Hack NF", 21)
        )
        hue.grid(column=1, row=0, sticky=(N, W, E, S))
        h_up_bt = ttk.Button(
            self.mainframe_luminancia_bts,
            text="+",
            command=self.h_up,
        )
        h_up_bt.grid(column=2, row=0, sticky=(N, S), pady=2)
        # ------------------
        i_down_bt = ttk.Button(
            self.mainframe_luminancia_bts,
            text="-",
            command=self.i_down,
        )
        i_down_bt.grid(column=0, row=1, sticky=(N, S), pady=2)
        intensity = ttk.Label(
            self.mainframe_luminancia_bts, text="Intensity", font=("Hack NF", 21)
        )
        intensity.grid(column=1, row=1, sticky=(N, W, E, S))
        i_up_bt = ttk.Button(
            self.mainframe_luminancia_bts,
            text="+",
            command=self.i_up,
        )
        i_up_bt.grid(column=2, row=1, sticky=(N, S), pady=2)
        default_bt = ttk.Button(
            self.mainframe_luminancia_bts, text="Deafult", command=self.hi_2_default
        )
        default_bt.grid(column=1, row=2, sticky=(N, S), pady=2)

    def histogram_buts(self):
        equalize_bt = ttk.Button(
            self.mainframe_hist_graph_bts, text="EQUALIZE", command=self.equalize
        )
        equalize_bt.grid(column=0, row=2, sticky=(N, S), pady=2)
        Default_bt = ttk.Button(
            self.mainframe_hist_graph_bts, text="DEFAULT", command=self.default_hist
        )
        Default_bt.grid(column=2, row=2, sticky=(N, S), pady=2)
        bin_value = StringVar(value="125")
        bin_entry = ttk.Entry(self.mainframe_hist_graph_bts, textvariable=bin_value)
        bin_entry.grid(column=1, row=1, sticky=(N, S), pady=2)
        if bin_value == "":
            bin_value.set("125")
        bin_bt = ttk.Button(
            self.mainframe_hist_graph_bts,
            text="BIN",
            command=lambda: self.binarize(0, int(bin_value.get())),
        )
        bin_bt.grid(column=0, row=1, sticky=(N, S), pady=2)
        bin_Otsu_bt = ttk.Button(
            self.mainframe_hist_graph_bts,
            text="BIN_OTSU",
            command=lambda: self.binarize(1, int(bin_value.get())),
        )
        bin_Otsu_bt.grid(column=2, row=1, sticky=(N, S), pady=2)

    def binarize(self, opt: int, th: int):
        if opt == 0:
            if th >= 0 and th <= 255:
                th = th
            elif th < 0:
                th = 0
            elif th > 255:
                th = 255
            bin_img = np.zeros_like(self.img_gray_saved)
            bin_img[self.img_gray_saved > th] = 255
            self.img_gray = bin_img
            self.pil_image_gray = Image.fromarray(self.img_gray)
            self.pil_image_gray = self.pil_image_gray.resize((400, 350))
            self.img_pil_gray = ImageTk.PhotoImage(self.pil_image_gray)
            self.imgLabel_gray.configure(image=self.img_pil_gray)
            self.Hist(self.img_gray)
        elif opt == 1:
            pass

    def Images(self, path=""):
        if path == "":
            image = Image.open("./images/lena.png").resize((500, 500))
        else:
            image = Image.open(path).resize((500, 500))
        image = image.convert("RGB")
        self.imgNumpy = np.array(image)
        self.conversor = Conversor(self.imgNumpy)

        self.imgHsi = self.conversor.normHsi_to_hsi()
        self.imgHsi = np.uint16(self.imgHsi)
        self.imgCmy = self.conversor.convert_rgb_to_cmy()
        self.img = ImageTk.PhotoImage(image)

        self.img_gray = self.conversor.conver_rgb_to_gray()
        self.pil_image_gray = Image.fromarray(self.img_gray)
        self.pil_image_gray = self.pil_image_gray.resize((400, 350))
        self.img_pil_gray = ImageTk.PhotoImage(self.pil_image_gray)

        self.img_gray_saved = self.img_gray
        self.pil_image_mod = Image.fromarray(self.imgNumpy_mod)
        self.img_pil_mod = ImageTk.PhotoImage(self.pil_image_mod)
        img_equalized = self.conversor.equalize(self.img_gray_saved)

        self.imgNumpy_mod = self.imgNumpy.copy()
        self.imgHsi_mod = self.imgHsi.copy()
        self.imgCmy_mod = self.imgCmy.copy()
        self.img_mod = self.img
        if path:
            self.imgLabel.configure(image=self.img)
            self.imgLabel.image = self.img
            self.imgLabel_lu.configure(image=self.img_mod)
            self.imgLabel_lu.image = self.img_mod
            self.imgLabel_gray.configure(image=self.img_pil_gray)
            self.imgLabel_gray.image = self.img_pil_gray
        self.Hist(self.img_gray)

    def Motion(self, event):
        x, y = event.x, event.y
        try:
            self.rgbValue.set(
                f"{self.imgNumpy[x,y][0]}   {self.imgNumpy[x,y][1]}  {self.imgNumpy[x,y][2]}"
            )
            self.hsi_string.set(
                f"{self.imgHsi[x,y][0]}  {self.imgHsi[x,y][1]}  {self.imgHsi[x,y][2]}"
            )
            self.cmy_string.set(
                f"{self.imgCmy[x,y][0]}  {self.imgCmy[x,y][1]}  {self.imgCmy[x,y][2]}"
            )

            self.rgbValue_lu.set(
                f"{self.imgNumpy_mod[x,y][0]}   {self.imgNumpy_mod[x,y][1]}  {self.imgNumpy_mod[x,y][2]}"
            )
            self.hsi_string_lu.set(
                f"{self.imgHsi_mod[x,y][0]}  {self.imgHsi_mod[x,y][1]}  {self.imgHsi_mod[x,y][2]}"
            )
            self.cmy_string_lu.set(
                f"{self.imgCmy_mod[x,y][0]}  {self.imgCmy_mod[x,y][1]}  {self.imgCmy_mod[x,y][2]}"
            )
        except:
            pass


app = App()
app.mainWindow_config()
app.mainloop()
