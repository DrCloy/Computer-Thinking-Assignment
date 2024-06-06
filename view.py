import tkinter as tk
from recipe import Recipe


class MainView:
    """
    Class to create GUI for Cocktail Recipe Application
    """

    def __init__(self) -> None:
        pass

    def init(self):
        """
        Function to initialize GUI
        """

    def __create_window(self):
        window = tk.Tk()
        window.title("Cocktail Recipe Application")
        window.geometry("800x600")
        window.resizable(False, False)

        window.mainloop()


class InitView:
    """
    Class to create initialization view
    """

    def __init__(self) -> None:
        self.__root = tk.Tk()
        self.__root.title("Cocktail Recipe Application")

        self.__label = tk.Label(self.__root, text="Enter the root directory of recipe files")
        self.__label.pack(pady=10)

        self.__text_input = tk.Entry(self.__root)
        self.__text_input.pack(pady=10)

        self.__submit_button = tk.Button(self.__root, text="Submit", command=self.__submit)
        self.__submit_button.pack(pady=10)

        self.__root.mainloop()

    def __submit(self):
        self.__root_directory = self.__text_input.get()
        if not self.__root_directory:
            return
        self.__root.destroy()

    def get_root_directory(self):
        return self.__root_directory
