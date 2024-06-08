import tkinter as tk
from recipe import Recipe


class MainView:
    """
    Class to create GUI for Cocktail Recipe Application
    """

    # Recipe class instance
    __recipe = None
    __dropdown_width = None
    __width = 900
    __height = 600
    __padx = 10
    __pady = 5

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

        self.__recipe_detail_frame = tk.Frame(self.__root, highlightbackground="white", highlightthickness=1, width=self.__width, height=(self.__height // 7) * 4)
        self.__recipe_detail_frame.pack_propagate(False)
        self.__recipe_detail_frame.pack(padx=self.__padx, pady=self.__pady, fill=tk.BOTH)

        self.__recipe_detail_text = tk.Text(self.__recipe_detail_frame, wrap=tk.WORD, width=self.__width - self.__padx, height=((self.__height // 7) * 4 - 2 * self.__pady), state=tk.DISABLED)
        self.__recipe_detail_text.place(relwidth=1, relheight=1)
        # self.__recipe_detail_text.pack(padx=self.__padx, pady=self.__pady)

        self.__recipe_detail_scrollbar = tk.Scrollbar(self.__recipe_detail_frame, command=self.__recipe_detail_text.yview)
        self.__recipe_detail_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.__recipe_detail_text.config(yscrollcommand=self.__recipe_detail_scrollbar.set)

        self.__category_select_frame = tk.Frame(self.__root, highlightbackground="white", highlightthickness=1, width=self.__width, height=self.__height // 7)
        self.__category_select_frame.pack(padx=self.__padx, pady=self.__pady, fill=tk.BOTH, expand=True)

        self.__category_manage_frame = tk.Frame(self.__root, highlightbackground="white", highlightthickness=1, width=self.__width, height=self.__height // 7)
        self.__category_manage_frame.pack(padx=self.__padx, pady=self.__pady, fill=tk.BOTH, expand=True)

        self.__control_frame = tk.Frame(self.__root, highlightbackground="white", highlightthickness=1, width=self.__width, height=self.__height // 7)
        self.__control_frame.pack(padx=self.__padx, pady=self.__pady, fill=tk.BOTH, expand=True)

        self.__root.mainloop()


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
