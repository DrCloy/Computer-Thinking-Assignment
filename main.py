from recipe import Recipe
from view import MainView, InitView


if __name__ == "__main__":
    init_view = InitView()

    while True:
        if init_view.get_root_directory():
            break

    root_directory = init_view.get_root_directory()
    print(root_directory)
    # root_directory = init_view.get_root_directory()

    # recipe = Recipe(root_directory)
    # recipe.import_recipe()

    # main_view = MainView()
    # main_view.init()
