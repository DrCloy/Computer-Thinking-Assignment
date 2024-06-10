from recipe import Recipe
from view import MainView, InitView


if __name__ == "__main__":
    init_view = InitView()

    while True:
        if not init_view.is_active():
            exit()
        elif init_view.get_root_directory():
            break

    root_directory = init_view.get_root_directory()
    print(root_directory)

    recipe = Recipe(root_directory)

    main_view = MainView(recipe)
    main_view.init()
