from recipe import Recipe
from view import View

if __name__ == "__main__":
    recipe = Recipe("Cocktail")
    view = View(recipe)
    view.create_window()
