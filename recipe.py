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

    def import_recipe(self):
        """
        Function to import recipe dictionary from "cocktail_recipe.pkl" file
        """

        with open(os.path.join(os.getcwd(), "cocktail_recipe.pkl"), "rb") as f:
            self.__recipe = pickle.load(f)["recipe"]
            self.__created_time = pickle.load(f)["timestamp"]

    def export_recipe(self):
        """
        Function to export recipe dictionary to "cocktail_recipe.pkl" file
        """

        pickle_data = {
            "timestamp": time.strftime("%Y년%m월%d일 %H시%M분%S초", time.localtime()),
            "recipe": self.__recipe,
        }

        with open(os.path.join(os.getcwd(), "cocktail_recipe.pkl"), "wb") as f:
            pickle.dump(pickle_data, f)

    def get_recipe(self) -> dict:
        """
        Function to return recipe dictionary

        Returns:
            Recipe dictionary
        """
        return self.__recipe

    def get_created_time(self) -> str:
        """
        Function to return the time the recipe was created

        Returns:
            Time the recipe was created in string format(YYYY년MM월DD일 HH시MM분SS초)
        """
        return self.__created_time
