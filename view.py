import tkinter as tk
from recipe import Recipe


class View:
    """
    Class to create GUI for Cocktail Recipe Application
    """

    def __init__(self, recipe: Recipe) -> None:
        self.__recipe = recipe

    def create_window(self):
        window = tk.Tk()
        window.title("Cocktail Recipe Application")
        window.geometry("800x600")
        window.resizable(False, False)

        window.mainloop()
