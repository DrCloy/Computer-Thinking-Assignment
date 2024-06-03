# Cocktail Recipe Class

# Importing necessary libraries
import json
import os
import pickle


class Recipe:
    """
    Class to manage cocktail recipes 
    """

    __recipe = {}

    def __init__(self, recipe_directory: str) -> None:
        """
        Constructor for Recipe class

        Args:
            recipe_directory (str): Directory containing recipe files
        """
        self.__recipe_directory = recipe_directory

    def generate_recipe(self):
        """
        Function to generate recipe dictionary from directory of recipe files
        """
        pass

    def import_recipe(self):
        """
        Function to import recipe dictionary from "cocktail_recipe.pkl" file
        """
        pass

    def export_recipe(self):
        """
        Function to export recipe dictionary to "cocktail_recipe.pkl" file
        """
        pass

    def get_recipe(self) -> dict:
        """
        Function to return recipe dictionary

        Returns:
            Recipe dictionary
        """
        return self.__recipe
