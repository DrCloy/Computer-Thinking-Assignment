import tkinter as tk
import tkinter.scrolledtext as tkst
import tkinter.ttk as ttk
import threading
import traceback
from recipe import Recipe


class MainView:
    """
    Class to create GUI for Cocktail Recipe Application
    """

    def __init__(self, recipe: Recipe) -> None:
        self.__recipe = recipe
        self.__width = 1000
        self.__height = 800
        self.__padx = 10
        self.__pady = 5
        self.__combobox_width = 10
        self.__combobox_list = []
        self.__category_selected = set()
        self.__add_button = None

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
        self.__root.grid_rowconfigure(1, weight=7)
        self.__root.grid_rowconfigure(2, weight=7)
        self.__root.grid_rowconfigure(3, weight=17)
        self.__root.grid_rowconfigure(4, weight=3)

        self.__recipe_detail_frame = tk.Frame(self.__root, highlightbackground="white", highlightthickness=1, width=self.__width)
        self.__recipe_detail_frame.pack_propagate(False)
        self.__recipe_detail_frame.grid(row=0, column=0, padx=self.__padx, pady=self.__pady, sticky="nsew")

        self.__recipe_detail_label = tk.Label(self.__recipe_detail_frame, text="Recipe Details", font=("Helvetica", 20, "bold"))
        self.__recipe_detail_label.pack(pady=self.__pady)

        self.__recipe_detail_text = tkst.ScrolledText(self.__recipe_detail_frame, wrap=tk.WORD, width=self.__width - self.__padx, state=tk.DISABLED, highlightbackground="white", highlightthickness=1)
        self.__recipe_detail_text.config(cursor="arrow")
        self.__recipe_detail_text.pack(fill=tk.BOTH, expand=True)

        self.__category_select_frame = tk.Frame(self.__root, highlightbackground="white", highlightthickness=1, width=self.__width)
        self.__category_select_frame.pack_propagate(False)
        self.__category_select_frame.grid(row=1, column=0, padx=self.__padx, pady=self.__pady, sticky="nsew")

        self.__category_select_label = tk.Label(self.__category_select_frame, text="Select Category", anchor="w", font=("Helvetica", 16, "bold"))
        self.__category_select_label.pack(padx=self.__padx, pady=self.__pady, anchor="w")

        self.__category_manage_frame = tk.Frame(self.__root, highlightbackground="white", highlightthickness=1, width=self.__width)
        self.__category_manage_frame.pack_propagate(False)
        self.__category_manage_frame.grid(row=2, column=0, padx=self.__padx, pady=self.__pady, sticky="nsew")

        self.__category_manage_label = tk.Label(self.__category_manage_frame, text="Manage Categories", font=("Helvetica", 16, "bold"))
        self.__category_manage_label.pack(padx=self.__padx, pady=self.__pady, anchor="w")

        self.__category_combobox = ttk.Combobox(self.__category_manage_frame, values=['--Select--'], width=self.__combobox_width, state="disabled")
        self.__category_combobox.set("--Select--")
        self.__category_combobox.pack(padx=self.__padx, pady=self.__pady, side=tk.LEFT)

        self.__category_delete_button = tk.Button(self.__category_manage_frame, text="Delete", state=tk.DISABLED, command=self.__delete_selected_category)
        self.__category_delete_button.pack(padx=self.__padx, pady=self.__pady, side=tk.LEFT)

        self.__recipe_select_frame = tk.Frame(self.__root, highlightbackground="white", highlightthickness=1, width=self.__width)
        self.__recipe_select_frame.grid_propagate(False)
        self.__recipe_select_frame.grid(row=3, column=0, padx=self.__padx, pady=self.__pady, sticky="nsew")

        self.__recipe_select_label = tk.Label(self.__recipe_select_frame, text="Select Recipe", font=("Helvetica", 13, "bold"))
        self.__recipe_select_label.grid(row=0, column=0, padx=self.__padx, pady=self.__pady, sticky="w")

        self.__recipe_option_label = tk.Label(self.__recipe_select_frame, text="Option", font=("Helvetica", 13, "bold"))
        self.__recipe_option_label.grid(row=1, column=0, padx=self.__padx, pady=self.__pady, sticky="w")

        self.__recipe_option_ingredient_label = tk.Label(self.__recipe_select_frame, text="Ingredient")
        self.__recipe_option_ingredient_label.grid(row=2, column=0, padx=self.__padx, pady=self.__pady, sticky="w")

        self.__recipe_option_ingredient = tk.IntVar()
        self.__recipe_option_ingredient.set(0)

        self.__recipe_ingredient_exist = tk.Radiobutton(self.__recipe_select_frame, text="Exist", variable=self.__recipe_option_ingredient, value=0, state=tk.DISABLED)
        self.__recipe_ingredient_exist.grid(row=2, column=1, padx=self.__padx, pady=self.__pady, sticky="w")

        self.__recipe_ingredient_full = tk.Radiobutton(self.__recipe_select_frame, text="Full", variable=self.__recipe_option_ingredient, value=1, state=tk.DISABLED)
        self.__recipe_ingredient_full.grid(row=2, column=2, padx=self.__padx, pady=self.__pady, sticky="w")

        self.__recipe_option_style_label = tk.Label(self.__recipe_select_frame, text="Style")
        self.__recipe_option_style_label.grid(row=3, column=0, padx=self.__padx, pady=self.__pady, sticky="w")

        self.__recipe_style = {
            "stirred": tk.BooleanVar(),
            "shaken": tk.BooleanVar(),
            "top": tk.BooleanVar()
        }

        self.__recipe_option_stir = tk.Checkbutton(self.__recipe_select_frame, text="Stirred",
                                                   variable=self.__recipe_style['stirred'], onvalue=True, offvalue=False, state=tk.DISABLED)
        self.__recipe_option_stir.grid(row=3, column=1, padx=self.__padx, pady=self.__pady, sticky="w")

        self.__recipe_option_shake = tk.Checkbutton(self.__recipe_select_frame, text="Shaken", variable=self.__recipe_style['shaken'], onvalue=True, offvalue=False, state=tk.DISABLED)
        self.__recipe_option_shake.grid(row=3, column=2, padx=self.__padx, pady=self.__pady, sticky="w")

        self.__recipe_option_top = tk.Checkbutton(self.__recipe_select_frame, text="Top", variable=self.__recipe_style['top'], onvalue=True, offvalue=False, state=tk.DISABLED)
        self.__recipe_option_top.grid(row=3, column=3, padx=self.__padx, pady=self.__pady, sticky="w")

        self.__recipe_search_button = tk.Button(self.__recipe_select_frame, text="Search", state=tk.DISABLED, command=self.__search_recipes)
        self.__recipe_search_button.grid(row=4, column=0, padx=self.__padx, pady=self.__pady, sticky="w")

        self.__recipe_select_combobox = ttk.Combobox(self.__recipe_select_frame, values=['--Select--'], width=self.__combobox_width, state="disabled")
        self.__recipe_select_combobox.set("--Select--")
        self.__recipe_select_combobox.bind("<<ComboboxSelected>>", self.__on_recipe_select)
        self.__recipe_select_combobox.grid(row=5, column=0, padx=self.__padx, pady=self.__pady, sticky="w")

        self.__control_frame = tk.Frame(self.__root, highlightbackground="white", highlightthickness=1, width=self.__width)
        self.__control_frame.grid(row=4, column=0, padx=self.__padx, pady=self.__pady, sticky="nsew")
        self.__control_frame.grid_propagate(False)
        self.__control_frame.grid_columnconfigure(0, weight=1)
        self.__control_frame.grid_columnconfigure(1, weight=1)

        self.__status_label = tk.Label(self.__control_frame, text="Loading...", font=("Helvetica", 20))
        self.__status_label.grid(row=0, column=0, padx=self.__padx, pady=self.__pady, sticky="nsw")

        self.__control_button_frame = tk.Frame(self.__control_frame)
        self.__control_button_frame.grid(row=0, column=1, padx=self.__padx, pady=self.__pady, sticky="nse")
        self.__control_button_frame.grid_columnconfigure(0, weight=1)
        self.__control_button_frame.grid_columnconfigure(1, weight=1)
        self.__control_button_frame.grid_columnconfigure(2, weight=1)
        self.__control_button_frame.grid_columnconfigure(3, weight=1)

        self.__import_button = tk.Button(self.__control_button_frame, text="Import", command=self.__import_recipe, state=tk.DISABLED)
        self.__import_button.grid(row=0, column=0, padx=2, sticky="e")

        self.__export_button = tk.Button(self.__control_button_frame, text="Export", command=self.__export_recipe, state=tk.DISABLED)
        self.__export_button.grid(row=0, column=1, padx=2, sticky="e")

        self.__generate_button = tk.Button(self.__control_button_frame, text="Generate", command=self.__generate_recipe, state=tk.DISABLED)
        self.__generate_button.grid(row=0, column=2, padx=2, sticky="e")

        self.__exit_button = tk.Button(self.__control_button_frame, text="Exit", command=self.__root.quit)
        self.__exit_button.grid(row=0, column=3, padx=2, sticky="e")

        self.__root.protocol("WM_DELETE_WINDOW", self.__root.quit)
        self.__root.after(1000, self.__escape_loading_state)
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
        combobox = ttk.Combobox(self.__category_select_frame, values=['--Select--'] + list(data.keys()), width=self.__combobox_width, state="readonly")
        combobox.set("--Select--")
        combobox.pack(padx=self.__padx, pady=self.__pady, side=tk.LEFT)
        combobox.bind("<<ComboboxSelected>>", lambda event: self.__on_combobox_select(event, data))
        self.__combobox_list.append(combobox)

    def __add_category(self):
        keys = []
        for combobox in self.__combobox_list:
            keys.append(combobox.get())
        if "--Select--" in keys:
            return
        if '-'.join(keys) in self.__category_selected:
            return
        self.__category_selected.add('-'.join(keys))
        self.__update_category_select_combobox()
        self.__reset_after_combobox(self.__combobox_list[0])
        self.__combobox_list[0].set("--Select--")
        if self.__category_delete_button.cget("state") == tk.DISABLED:
            self.__category_delete_button.config(state=tk.NORMAL)

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
        else:
            self.__add_add_button()

    def __update_category_select_combobox(self):
        self.__category_combobox.config(values=['--Select--'] + sorted(list(self.__category_selected)))
        self.__category_combobox.set("--Select--")

    def __delete_selected_category(self):
        selected_key = self.__category_combobox.get()
        if selected_key == "--Select--":
            return
        self.__category_selected.remove(selected_key)
        self.__update_category_select_combobox()

        if not self.__category_selected:
            self.__category_delete_button.config(state=tk.DISABLED)

    def __search_recipes_full_ingredient(self, category_selected: set):
        recipe_category = self.__recipe.get_category()
        recipe_set = set(self.__recipe.get_all_recipe_names())

        def __search_recipes_recursive(data: dict, keys: list, category_selected: set):
            nonlocal recipe_set
            for key, value in data.items():
                if isinstance(value, dict):
                    __search_recipes_recursive(value, keys + [key], category_selected)
                else:
                    if '-'.join(keys + [key]) not in category_selected:
                        recipe_set -= set(value)

        __search_recipes_recursive(recipe_category, [], category_selected)

        return recipe_set

    def __search_recipes(self):
        recipe_set = set()
        if self.__recipe_option_ingredient.get() == 0:
            for category in self.__category_selected:
                keys = list(category.split('-'))
                data = self.__recipe.get_category()[keys[0]]
                for key in keys[1:]:
                    data = data[key]
                recipe_set.update(data)
        else:
            recipe_set = self.__search_recipes_full_ingredient(self.__category_selected)

        filtered_recipe = []
        for recipe in recipe_set:
            recipe_detail = self.__recipe.get_recipe_detail(recipe)
            if self.__recipe_style['stirred'].get() or self.__recipe_style['shaken'].get() or self.__recipe_style['top'].get():
                if self.__recipe_style['stirred'].get() and 'stirred' not in list(map(str.lower, recipe_detail['style'])):
                    continue
                if not self.__recipe_style['stirred'].get() and 'stirred' in list(map(str.lower, recipe_detail['style'])):
                    continue
                if self.__recipe_style['shaken'].get() and 'shaken' not in list(map(str.lower, recipe_detail['style'])):
                    continue
                if not self.__recipe_style['shaken'].get() and 'shaken' in list(map(str.lower, recipe_detail['style'])):
                    continue
                if self.__recipe_style['top'].get() and 'top' not in list(map(str.lower, recipe_detail['style'])):
                    continue
                if not self.__recipe_style['top'].get() and 'top' in list(map(str.lower, recipe_detail['style'])):
                    continue
                filtered_recipe.append(recipe)
            else:
                filtered_recipe.append(recipe)

        self.__recipe_select_combobox.config(values=['--Select--'] + sorted(filtered_recipe))
        self.__recipe_select_combobox.set("--Select--")

    def __on_recipe_select(self, event):
        cocktail_name = event.widget.get()
        if cocktail_name == "--Select--":
            return
        recipe = self.__recipe.get_recipe_detail(cocktail_name)

        self.__recipe_detail_text.config(state=tk.NORMAL)
        self.__recipe_detail_text.delete(1.0, tk.END)

        self.__recipe_detail_text.insert(tk.END, f"{cocktail_name}\n", 'big')
        self.__recipe_detail_text.insert(tk.END, f"\n", 'mid')

        self.__recipe_detail_text.insert(tk.END, f"Ingredients\n", 'mid')
        for key, value in recipe['ingredients'].items():
            self.__recipe_detail_text.insert(tk.END, f"{key.capitalize()} {value['quantity']} {value['unit']}\n", 'small')
        self.__recipe_detail_text.insert(tk.END, f"\n", 'mid')

        self.__recipe_detail_text.insert(tk.END, f"Recipe\n", 'mid')
        for i, step in enumerate(recipe['recipe']):
            self.__recipe_detail_text.insert(tk.END, f"{i + 1}. {step}\n", 'small')

        self.__recipe_detail_text.tag_config('big', font=('Helvetica', 25, 'bold'))
        self.__recipe_detail_text.tag_config('mid', font=('Helvetica', 20, 'bold'))
        self.__recipe_detail_text.tag_config('small', font=('Helvetica', 15))

        self.__recipe_detail_text.config(state=tk.DISABLED)

    def __activate(self):
        for combobox in self.__combobox_list:
            combobox.destroy()
        self.__combobox_list = []
        if self.__add_button:
            self.__add_button.destroy()
        self.__category_selected = set()
        self.__add_button = None
        self.__add_combobox(self.__recipe.get_category())
        self.__category_combobox.config(state="readonly", width=self.__combobox_width * self.__recipe.get_recipe_depth())
        self.__recipe_select_combobox.config(state="readonly")
        self.__category_delete_button.config(state=tk.NORMAL)
        self.__recipe_ingredient_exist.config(state=tk.NORMAL)
        self.__recipe_ingredient_full.config(state=tk.NORMAL)
        self.__recipe_option_stir.config(state=tk.NORMAL)
        self.__recipe_option_shake.config(state=tk.NORMAL)
        self.__recipe_option_top.config(state=tk.NORMAL)
        self.__recipe_search_button.config(state=tk.NORMAL)

    def __import_recipe(self):
        try:
            if not self.__recipe:
                return
            self.__recipe.import_recipe()
            self.__status_label.config(text="Created At: " + self.__recipe.get_created_time())
            self.__activate()
        except Exception as e:
            print(e)
            traceback.print_exc()
            self.__status_label.config(text="Error")

    def __export_recipe(self):
        try:
            self.__recipe.export_recipe()
            self.__status_label.config(text="Exported")
            threading.Timer(3, lambda: self.__status_label.config(text="Created At: " + self.__recipe.get_created_time())).start()
        except Exception as e:
            print(e)
            traceback.print_exc()
            self.__status_label.config(text="Error")

    def __generate_recipe(self):
        try:
            self.__recipe.generate_recipe()
            self.__status_label.config(text="Generated")
            self.__activate()
            threading.Timer(3, lambda: self.__status_label.config(text="Created At: " + self.__recipe.get_created_time())).start()
        except Exception as e:
            print(e)
            traceback.print_exc()
            self.__status_label.config(text="Error")


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
        self.__text_input.focus()
        self.__text_input.bind("<Return>", lambda event: self.__submit())

        self.__submit_button = tk.Button(self.__root, text="Submit", command=self.__submit)
        self.__submit_button.pack(pady=10)

        self.__root.protocol("WM_DELETE_WINDOW", self.__on_exit_click)
        self.__root.mainloop()

    def __on_exit_click(self):
        self.__is_active = False
        print("Application closed")
        self.__root.destroy()

    def __submit(self):
        try:
            self.__root_directory = self.__text_input.get()
            if not self.__root_directory:
                return
            self.__root.destroy()
        except Exception as e:
            print(e)

    def get_root_directory(self):
        return self.__root_directory

    def is_active(self):
        return self.__is_active
