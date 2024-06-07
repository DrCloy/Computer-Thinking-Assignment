# Cocktail Recipe Class

# Importing necessary libraries
import json
import os
import pickle
import time


class Recipe:
    """
    Class to manage cocktail recipes 
    """

    # Private attributes
    __recipe: dict = {}
    __recipe_depth: int = 0
    __recipe_directory: str = ""

    def __init__(self, recipe_directory: str) -> None:
        """
        Constructor for Recipe class

        Args:
            recipe_directory (str): Directory containing recipe files
        """
        self.__recipe_directory = recipe_directory
        self.__recipe_depth = 0

    def generate_recipe(self):
        """
        Function to generate recipe dictionary from directory of recipe files
        """

        recipe_details = {}

        def __parse_directory(path: str):
            """
            Function to parse directory and return a list of dictionaries

            Args:
                path (str): Path to directory

            Returns:
                Dictionary
            """

            global recipe_details
            result = {}
            for entry in os.listdir(path):
                full_path = os.path.join(path, entry)

                if os.path.isdir(full_path):
                    sub_result = __parse_directory(full_path)
                    result[entry] = sub_result
                elif entry.endswith(".json"):
                    if isinstance(result, dict):
                        result = []
                    result.append(entry[:-5])
                    with open(full_path, "r") as f:
                        recipe_details[entry[:-5]] = json.load(f)
            return result

        self.__recipe["created_at"] = time.strftime("%Y년%m월%d일 %H시%M분%S초", time.localtime())
        self.__recipe["category"] = __parse_directory(self.__recipe_directory)
        self.__recipe["recipe_details"] = recipe_details
        self.__recipe_depth = self.__calculate_recipe_depth()

    def import_recipe(self):
        """
        Function to import recipe dictionary from "cocktail_recipe.pkl" file
        """

        try:
            with open(os.path.join(os.getcwd(), "cocktail_recipe.pkl"), "rb") as f:
                self.__recipe = pickle.load(f)
            self.__recipe_depth = self.__calculate_recipe_depth()
        except FileNotFoundError:
            self.__recipe = {
                "created_at": "No recipe found",
                "category": {},
                "recipe_details": {}
            }
            self.__recipe_depth = 0

    def export_recipe(self):
        """
        Function to export recipe dictionary to "cocktail_recipe.pkl" file
        """

        with open(os.path.join(os.getcwd(), "cocktail_recipe.pkl"), "wb") as f:
            pickle.dump(self.__recipe, f)

    def __calculate_recipe_depth(self):
        """
        Function to return the depth of the recipe dictionary

        Returns:
            int: Depth of the recipe dictionary
        """

        def __get_depth(dictionary: dict, depth: int = 0) -> int:
            """
            Function to return the depth of the dictionary

            Args:
                dictionary (dict): Dictionary to check the depth
                depth (int): Depth of the dictionary

            Returns:
                int: Depth of the dictionary
            """

            if not isinstance(dictionary, dict):
                return depth

            return max(__get_depth(value, depth + 1) for value in dictionary.values())

        return __get_depth(self.__recipe["category"])

    def get_category(self) -> dict:
        """
        Function to return recipe dictionary

        Returns:
            Recipe dictionary
        """
        return self.__recipe["category"]

    def get_created_time(self) -> str:
        """
        Function to return the time the recipe was created

        Returns:
            Time the recipe was created in string format(YYYY년MM월DD일 HH시MM분SS초)
        """
        return self.__recipe["created_at"]

    def get_recipe_detail(self, name: str) -> dict:
        """
        Function to find cocktail recipe by name and return the recipe details

        Args:
            name (str): Name of the cocktail

        Returns:
            dict: Recipe details
        """

        return self.__recipe["recipe_details"][name]

    def get_recipe_depth(self) -> int:
        """
        Function to return the depth of the recipe dictionary

        Returns:
            int: Depth of the recipe dictionary
        """
        return self.__recipe_depth
