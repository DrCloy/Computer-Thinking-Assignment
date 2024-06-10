import tkinter as tk
import tkinter.scrolledtext as tkst
import tkinter.ttk as ttk
import threading
from recipe import Recipe


class MainView:
    """
    Class to create GUI for Cocktail Recipe Application
    """

    # Recipe class instance
    __recipe = None
    __width = 800
    __height = 600
    __padx = 10
    __pady = 5
    __combobox_width = 10
    __combobox_list = []
    __category_selected = []
    __add_button = None

    def __init__(self, recipe: Recipe) -> None:
        self.__recipe = recipe

    def init(self):
        """
        Function to initialize GUI
        """
        self.__create_window()

    def __create_window(self):
        self.__root = tk.Tk()
        self.__root.title("Cocktail Recipe Application")
        self.__root.geometry(f"{self.__width + 2 * self.__padx}x{self.__height + 2 * 4 * self.__pady}")
        self.__root.resizable(False, False)
        self.__root.grid_rowconfigure(0, weight=30)
        self.__root.grid_rowconfigure(1, weight=10)
        self.__root.grid_rowconfigure(2, weight=10)
        self.__root.grid_rowconfigure(3, weight=1)

        self.__recipe_detail_frame = tk.Frame(self.__root, highlightbackground="white", highlightthickness=1, width=self.__width)
        self.__recipe_detail_frame.pack_propagate(False)
        self.__recipe_detail_frame.grid(row=0, column=0, padx=self.__padx, pady=self.__pady, sticky="nsew")

        self.__recipe_detail_label = tk.Label(self.__recipe_detail_frame, text="Recipe Details", font=("Helvetica", 16, "bold"))
        self.__recipe_detail_label.pack(pady=self.__pady)

        self.__recipe_detail_text = tkst.ScrolledText(self.__recipe_detail_frame, wrap=tk.WORD, width=self.__width - self.__padx, state=tk.DISABLED, highlightbackground="white", highlightthickness=1)
        self.__recipe_detail_text.config(cursor="arrow")
        self.__recipe_detail_text.pack(fill=tk.BOTH, expand=True)

        self.__category_select_frame = tk.Frame(self.__root, highlightbackground="white", highlightthickness=1, width=self.__width)
        self.__category_select_frame.grid(row=1, column=0, padx=self.__padx, pady=self.__pady, sticky="nsew")

        self.__category_select_label = tk.Label(self.__category_select_frame, text="Select Category", anchor="w")
        self.__category_select_label.pack(padx=self.__padx, pady=self.__pady, anchor="w")

        self.__category_manage_frame = tk.Frame(self.__root, highlightbackground="white", highlightthickness=1, width=self.__width)
        self.__category_manage_frame.grid(row=2, column=0, padx=self.__padx, pady=self.__pady, sticky="nsew")

        self.__category_manage_label = tk.Label(self.__category_manage_frame, text="Manage Categories")
        self.__category_manage_label.pack(padx=self.__padx, pady=self.__pady, anchor="w")

        self.__control_frame = tk.Frame(self.__root, highlightbackground="white", highlightthickness=1, width=self.__width)
        self.__control_frame.grid(row=3, column=0, padx=self.__padx, pady=self.__pady, sticky="nsew")
        self.__control_frame.grid_columnconfigure(0, weight=6)
        self.__control_frame.grid_columnconfigure(1, weight=1)
        self.__control_frame.grid_columnconfigure(2, weight=1)
        self.__control_frame.grid_columnconfigure(3, weight=1)
        self.__control_frame.grid_columnconfigure(4, weight=1)

        self.__status_label = tk.Label(self.__control_frame, text="Loading...", font=("Helvetica", 20))
        self.__status_label.grid(row=0, column=0, padx=self.__padx, pady=self.__pady, sticky="nsw")

        self.__import_button = tk.Button(self.__control_frame, text="Import", command=self.__import_recipe, state=tk.DISABLED)
        self.__import_button.grid(row=0, column=1, padx=2, sticky="e")

        self.__export_button = tk.Button(self.__control_frame, text="Export", command=self.__export_recipe, state=tk.DISABLED)
        self.__export_button.grid(row=0, column=2, padx=2, sticky="e")

        self.__generate_button = tk.Button(self.__control_frame, text="Generate", command=self.__generate_recipe, state=tk.DISABLED)
        self.__generate_button.grid(row=0, column=3, padx=2, sticky="e")

        self.__exit_button = tk.Button(self.__control_frame, text="Exit", command=self.__root.quit)
        self.__exit_button.grid(row=0, column=4, padx=2, sticky="e")

        self.__root.protocol("WM_DELETE_WINDOW", self.__root.quit)
        self.__root.after(2000, self.__escape_loading_state)
        self.__root.mainloop()

    def __escape_loading_state(self):
        self.__status_label.config(text="Import Recipe to Start")
        self.__import_button.config(state=tk.NORMAL)
        self.__export_button.config(state=tk.NORMAL)
        self.__generate_button.config(state=tk.NORMAL)

    def __reset_after_combobox(self, widget):
        for combobox in self.__combobox_list[self.__combobox_list.index(widget) + 1:]:
            combobox.destroy()
        self.__combobox_list = self.__combobox_list[:self.__combobox_list.index(widget) + 1]

        if self.__add_button:
            self.__add_button.destroy()

    def __add_combobox(self, data: dict):
        combobox = ttk.Combobox(self.__category_select_frame, values=['--Select--'] + list(data.keys()), width=self.__combobox_width)
        combobox.set("--Select--")
        combobox.pack(pady=self.__pady, side=tk.LEFT)
        combobox.bind("<<ComboboxSelected>>", lambda event: self.__on_combobox_select(event, data))
        self.__combobox_list.append(combobox)

    def __add_category(self):
        keys = []
        for combobox in self.__combobox_list:
            keys.append(combobox.get())
        self.__category_selected.append('-'.join(keys))

    def __add_add_button(self):
        self.__add_button = tk.Button(self.__category_select_frame, text="Add", command=lambda: self.__add_category())
        self.__add_button.pack(pady=self.__pady, side=tk.LEFT)

    def __on_combobox_select(self, event, data: dict):
        selected_key = event.widget.get()
        self.__reset_after_combobox(event.widget)
        if selected_key == "--Select--":
            return

        next_data = data[selected_key]
        if isinstance(next_data, dict):
            self.__add_combobox(next_data)
        elif isinstance(next_data, list):
            self.__add_add_button()

    def __import_recipe(self):
        try:
            if not self.__recipe:
                return
            self.__recipe.import_recipe()
            self.__status_label.config(text="Created At: " + self.__recipe.get_created_time())
            self.__combobox_list = []
            self.__category_selected = []
            self.__add_button = None
            self.__add_combobox(self.__recipe.get_category())
        except Exception as e:
            print(e)
            self.__status_label.config(text="Error")

    def __export_recipe(self):
        self.__recipe.export_recipe()
        self.__status_label.config(text="Exported")
        threading.Timer(3, lambda: self.__status_label.config(text="Created At: " + self.__recipe.get_created_time())).start()

    def __generate_recipe(self):
        self.__recipe.generate_recipe()
        self.__status_label.config(text="Generated")
        threading.Timer(3, lambda: self.__status_label.config(text="Created At: " + self.__recipe.get_created_time())).start()


class InitView:
    """
    Class to create initialization view
    """

    def __init__(self) -> None:
        self.__is_active = True

        self.__root = tk.Tk()
        self.__root.title("Cocktail Recipe Application")
        self.__root.geometry("400x200")

        self.__label = tk.Label(self.__root, text="Enter the root directory of recipe files")
        self.__label.pack(pady=10)

        self.__text_input = tk.Entry(self.__root)
        self.__text_input.pack(pady=10)
        self.__text_input.bind("<Return>", lambda _: self.__submit())

        self.__submit_button = tk.Button(self.__root, text="Submit", command=self.__submit)
        self.__submit_button.pack(pady=10)

        self.__root.protocol("WM_DELETE_WINDOW", self.__on_exit_click)
        self.__root.mainloop()

    def __on_exit_click(self):
        self.__is_active = False
        print("Application closed")
        self.__root.destroy()

    def __submit(self):
        self.__root_directory = self.__text_input.get()
        if not self.__root_directory:
            return
        self.__root.destroy()

    def get_root_directory(self):
        return self.__root_directory

    def is_active(self):
        return self.__is_active
