import tkinter as tk
from tkinter import ttk, messagebox, font
import math

class MetalCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор металла.")
        self.root.geometry("550x600")
        self.root.resizable(False, False)

        self.DENSITIES = {
            "Сталь углеродистая обыкновенная (Ст3, Ст20, Ст45)": 7.85,
            "Сталь конструкционная легированная (40Х, 30ХГСА)": 7.85,
            "Сталь инструментальная (У8, У10)": 7.85,
            "Сталь нержавеющая аустенитная (12Х18Н10Т, 08Х18Н10)": 7.9,
            "Сталь нержавеющая ферритная (08Х13, 12Х17)": 7.7,
            "Сталь быстрорежущая (Р6М5)": 8.1,
            "Сталь жаропрочная (ХН77ТЮР)": 8.2,

            "Чугун серый (СЧ20)": 7.2,
            "Чугун высокопрочный (ВЧ60)": 7.3,
            "Чугун ковкий (КЧ30)": 7.3,
            "Чугун легированный": 7.4,

            "Алюминий чистый (АД0, АД1)": 2.7,
            "Алюминиевый сплав деформируемый (Д16, АМг6)": 2.78,
            "Алюминиевый сплав литейный (АК12, АЛ9)": 2.65,
            "Алюминиевый сплав высокопрочный (В95)": 2.85,

            "Медь чистая (М1, М2)": 8.94,
            "Латунь (Л63, ЛС59-1)": 8.5,
            "Латунь алюминиевая (ЛА77-2)": 8.3,
            "Латунь марганцовистая (ЛМц58-2)": 8.4,

            "Бронза оловянно-цинковая (ГОСТ 6511–60)": 8.7,
            "Бронза оловянная (ГОСТ 5017-2006)": 8.8,
            "Бронза оловянно-фосфористая (ГОСТ 10025-78)": 8.8,
            "Бронза берилловая (ГОСТ 15835-70)": 8.2,
            "Бронза безоловянная (ГОСТ 18175-78)": 7.5,
            "Бронза литейная оловянная (ГОСТ 613-79)": 8.6,
            "Бронза оловянная литейная (ГОСТ 493-79)": 8.6,
            "Бронза алюминиевая (БрАЖ9-4)": 7.5,
            "Бронза кремнистая (БрКМц3-1)": 8.4,

            "Титан чистый (ВТ1-0)": 4.5,
            "Титановый сплав (ВТ6, ВТ22)": 4.4,
            "Титановый сплав жаропрочный (ВТ8)": 4.5,

            "Никель чистый (НП2)": 8.9,
            "Монель (НМЖМц28-2.5-1.5)": 8.8,
            "Инвар (36Н)": 8.1,

            "Цинк чистый (Ц0, Ц1)": 7.1,
            "Цинковый сплав (ЦАМ4-1)": 6.7,

            "Магний чистый": 1.74,
            "Магниевый сплав (МА2-1)": 1.8,

            "Свинец (С1, С2)": 11.34,
            "Олово (О1)": 7.3,
            "Вольфрам": 19.3,
            "Молибден": 10.2,
            "Кобальт": 8.9,
            "Хром": 7.2,
            "Ниобий": 8.6,
            "Тантал": 16.6,
            "Цирконий": 6.5,
            "Серебро": 10.5,
            "Золото": 19.3,
            "Платина": 21.45,
        }
        self.FONT = font.Font(family="Helvetica", size=10, weight="normal")

        self.create_widgets()
        self.update_fields()

    def create_widgets(self):
        ttk.Label(self.root, text="Сортамент:", font=self.FONT).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.sortament = tk.StringVar(value="Лист")
        self.sortament_combo = ttk.Combobox(self.root, textvariable=self.sortament, values=[
            "Арматура", "Двутавр", "Швеллер", "Уголок",
            "Труба круглая", "Труба профильная", "Круг", "Квадрат",
            "Шестигранник", "Лента", "Лист"
        ], state="readonly", width=30, font=self.FONT)
        self.sortament_combo.grid(row=0, column=1, padx=10, pady=10)
        self.sortament_combo.bind("<<ComboboxSelected>>", lambda e: self.update_fields())

        self.fields_frame = ttk.LabelFrame(self.root, padding=10)
        self.fields_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.entries = {}

        ttk.Label(self.root, text="Металл:", font=self.FONT).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.metal_var = tk.StringVar(value="Сталь углеродистая обыкновенная (Ст3, Ст20, Ст45)")
        self.metal_combo = ttk.Combobox(self.root, textvariable=self.metal_var, values=list(self.DENSITIES.keys()), state="readonly", width=30)
        self.metal_combo.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        self.metal_combo.bind("<<ComboboxSelected>>", lambda e: self.update_density_from_metal())

        ttk.Label(self.root, text="Плотность (г/см³):", font=self.FONT).grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.density_var = tk.DoubleVar(value=7.85)
        self.density_entry = ttk.Entry(self.root, textvariable=self.density_var, width=15)
        self.density_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        self.calc_btn = ttk.Button(self.root, text="Рассчитать", command=self.calculate)
        self.calc_btn.grid(row=4, column=0, padx=10, pady=20)

        self.reset_btn = ttk.Button(self.root, text="Сбросить", command=self.reset)
        self.reset_btn.grid(row=4, column=1, padx=10, pady=20, sticky="w")

        self.result_text = tk.Text(self.root, height=5, width=60, state="disabled", highlightthickness=0, borderwidth=0, font=self.FONT, bg=self.root.cget("bg"))
        self.result_text.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def update_fields(self):
        for widget in self.fields_frame.winfo_children():
            widget.destroy()
        self.entries.clear()

        sortament = self.sortament.get()
        fields = []
        defaults = []

        if sortament == "Арматура":
            fields = [("Радиус R (мм):", "R"), ("Длина L (мм):", "L")]
            defaults = [10, 1000]
        elif sortament == "Двутавр":
            fields = [("Высота H (мм):", "H"), ("Ширина полки B (мм):", "B"),
                      ("Толщина стенки s (мм):", "s"), ("Толщина полки t (мм):", "t"),
                      ("Длина L (мм):", "L")]
            defaults = [100, 50, 5, 8, 1000]
        elif sortament == "Швеллер":
            fields = [("Высота H (мм):", "H"), ("Ширина полки B (мм):", "B"),
                      ("Толщина стенки s (мм):", "s"), ("Толщина полки t (мм):", "t"),
                      ("Длина L (мм):", "L")]
            defaults = [100, 50, 5, 8, 1000]
        elif sortament == "Уголок":
            fields = [("Ширина полки A (мм):", "A"), ("Толщина t (мм):", "t"), ("Длина L (мм):", "L")]
            defaults = [50, 5, 1000]
        elif sortament == "Труба круглая":
            fields = [("Внешний диаметр D (мм):", "D"), ("Толщина стенки s (мм):", "s"), ("Длина L (мм):", "L")]
            defaults = [100, 5, 1000]
        elif sortament == "Труба профильная":
            fields = [("Ширина a (мм):", "a"), ("Высота b (мм):", "b"),
                      ("Толщина стенки s (мм):", "s"), ("Длина L (мм):", "L")]
            defaults = [80, 40, 3, 1000]
        elif sortament == "Круг":
            fields = [("Радиус R (мм):", "R"), ("Длина L (мм):", "L")]
            defaults = [10, 1000]
        elif sortament == "Квадрат":
            fields = [("Сторона a (мм):", "a"), ("Длина L (мм):", "L")]
            defaults = [20, 1000]
        elif sortament == "Шестигранник":
            fields = [("Сторона a (мм):", "a"), ("Длина L (мм):", "L")]
            defaults = [20, 1000]
        elif sortament == "Лента":
            fields = [("Ширина b (мм):", "b"), ("Толщина t (мм):", "t"), ("Длина L (мм):", "L")]
            defaults = [50, 2, 1000]
        elif sortament == "Лист":
            fields = [("Длина a (мм):", "a"), ("Ширина b (мм):", "b"), ("Толщина t (мм):", "t")]
            defaults = [100, 100, 10]
        else:
            return

        for i, (label_text, key) in enumerate(fields):
            ttk.Label(self.fields_frame, text=label_text).grid(row=i, column=0, padx=5, pady=5, sticky="w")
            var = tk.DoubleVar(value=defaults[i])
            entry = ttk.Entry(self.fields_frame, textvariable=var, width=15)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries[key] = var

    def update_density_from_metal(self):
        metal = self.metal_var.get()
        self.density_var.set(self.DENSITIES[metal])

    def reset(self):
        self.sortament.set("Лист")
        self.metal_var.set("Сталь углеродистая обыкновенная (Ст3, Ст20, Ст45)")
        self.density_var.set(7.85)
        self.update_fields()
        self.result_text.config(state="normal")
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state="disabled")

    def calculate(self):
        try:
            density_g_cm3 = self.density_var.get()
            if density_g_cm3 <= 0:
                raise ValueError("Плотность должна быть положительной")
            density_g_mm3 = density_g_cm3 / 1000

            sortament = self.sortament.get()
            mass = None

            if sortament == "Арматура" or sortament == "Круг":
                R = self.entries["R"].get()
                L = self.entries["L"].get()
                mass = math.pi * R * R * L * density_g_mm3

            elif sortament == "Двутавр" or sortament == "Швеллер":
                H = self.entries["H"].get()
                B = self.entries["B"].get()
                s = self.entries["s"].get()
                t = self.entries["t"].get()
                L = self.entries["L"].get()
                area = 2 * B * t + (H - 2 * t) * s
                mass = area * L * density_g_mm3

            elif sortament == "Уголок":
                A = self.entries["A"].get()
                t = self.entries["t"].get()
                L = self.entries["L"].get()
                area = (2 * A - t) * t
                mass = area * L * density_g_mm3

            elif sortament == "Труба круглая":
                D = self.entries["D"].get()
                s = self.entries["s"].get()
                L = self.entries["L"].get()
                if s >= D/2:
                    raise ValueError("Толщина стенки не может превышать радиус")
                area = math.pi * s * (D - s)
                mass = area * L * density_g_mm3

            elif sortament == "Труба профильная":
                a = self.entries["a"].get()
                b = self.entries["b"].get()
                s = self.entries["s"].get()
                L = self.entries["L"].get()
                if 2*s >= a or 2*s >= b:
                    raise ValueError("Толщина стенки слишком велика")
                area = 2 * s * (a + b - 2 * s)
                mass = area * L * density_g_mm3

            elif sortament == "Квадрат":
                a = self.entries["a"].get()
                L = self.entries["L"].get()
                mass = a * a * L * density_g_mm3

            elif sortament == "Шестигранник":
                a = self.entries["a"].get()
                L = self.entries["L"].get()
                area_factor = (3 * math.sqrt(3)) / 2
                mass = area_factor * a * a * L * density_g_mm3

            elif sortament == "Лента":
                b = self.entries["b"].get()
                t = self.entries["t"].get()
                L = self.entries["L"].get()
                mass = b * t * L * density_g_mm3

            elif sortament == "Лист":
                a = self.entries["a"].get()
                b = self.entries["b"].get()
                t = self.entries["t"].get()
                mass = a * b * t * density_g_mm3

            if mass is None:
                return

            self.result_text.config(state="normal")
            self.result_text.delete(1.0, tk.END)
            result_str = f"Масса: {mass:.2f} г"
            if mass >= 1000:
                result_str += f"  (около {mass/1000:.2f} кг)"
            self.result_text.insert(1.0, result_str)
            self.result_text.config(state="disabled")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Некорректный ввод: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MetalCalculator(root)
    root.mainloop()