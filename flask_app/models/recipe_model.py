from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
from flask_app.models import user_model
import re

class Recipe:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.under = data['under']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.description = data['description']
        self.user_id = data['user_id']

# Get all join. 
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id"
        results = connectToMySQL(DATABASE).query_db(query)
        if len(results) > 0:
            all_recipes = []
            for row in results:
                this_recipe = cls(row)
                user_data = {
                    **row,
                    'id': row['users.id'],
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at']
                }
                this_user = user_model.User(user_data)
                this_recipe.creator = this_user
                all_recipes.append(this_recipe)
            return all_recipes
        return []

# Validator Recipe

    @staticmethod
    def validator(potential_recipe):
        is_valid = True
        if len(potential_recipe['name']) < 2:
            flash("name of recipe is required","reg")
            is_valid = False
        if len(potential_recipe['description']) < 2:
            flash("description of recipe is required","reg")
            is_valid = False
        if len(potential_recipe['instructions']) < 2:
            flash("recipe instructions are required","reg")
        if len(potential_recipe['description']) < 2:
            flash("recipe description is required","reg")
        if len(potential_recipe['instructions']) > 255:
            flash("recipe instructions are too long","reg")
        if len(potential_recipe['date_made']) < 2:
            flash("recipe date made are required","reg")
            is_valid = False
        return is_valid

# Create a recipe

    @classmethod
    def create(cls,data):
        query = "INSERT INTO recipes (name, under, instructions, date_made, description, user_id,) VALUES "\
        "(%(name)s, %(under)s, %(instructions)s, %(date_made)s, %(description)s, %(user_id)s)"
        return connectToMySQL(DATABASE).query_db(query,data)

# view a recipe page.

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id WHERE recipes.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if len(results) < 1:
            return False
        row = results[0]
        this_recipe = cls(row)
        user_data = {
            **row,
            'id': row['users.id'],
            'created_at': row['users.created_at'],
            'updated_at': row['users.updated_at']
        }
        this_user = user_model.User(user_data)
        this_recipe.creator = this_user
        return this_recipe

# Delete a recipe

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)

# Update a recipe

    @classmethod
    def update(cls,data):
        query = "UPDATE recipes SET name = %(name)s, under = %(under)s, instructions = %(instructions)s, date_made = %(date_made)s, description = %(description)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)