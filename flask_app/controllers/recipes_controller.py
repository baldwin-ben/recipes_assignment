from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user_model import User
from flask_app.models.recipe_model import Recipe
from flask_bcrypt import Bcrypt

# Renders new recipe page

@app.route('/recipes/new')
def new_recipe_form():
    return render_template("recipe_new.html")

# Creates recipe post

@app.route('/recipes/create', methods=["POST"])
def create_recipe():
    if 'user_id' not in session:
        return redirect('/')
    if not Recipe.validator(request.form):
        return redirect('/recipes/new')
    data = {
        **request.form,
        'user_id': session['user_id']
    }
    Recipe.create(data)
    return redirect('/dashboard')

# View one recipe

@app.route('/recipes/<int:id>')
def one_recipe(id):
    if 'user_id' not in session:
        return redirect('/')
    user_data = {
        'id': session['user_id']
    }
    logged_user = User.get_by_id(user_data)
    this_recipe = Recipe.get_by_id({'id':id})
    return render_template("recipe_one.html", this_recipe=this_recipe, logged_user=logged_user)

# Delete one recipe

@app.route('/recipes/<int:id>/delete')
def delete_recipe(id):
    if 'user_id' not in session:
        return redirect('/')
    Recipe.destroy({'id':id})
    return redirect("/dashboard")

# Renders recipe update page

@app.route('/recipes/<int:id>/edit')
def update_recipe_form(id):
    if 'user_id' not in session:
        return redirect('/')
    this_recipe = Recipe.get_by_id({'id':id})
    return render_template("recipe_edit.html", this_recipe=this_recipe)

# Update recipe post

@app.route('/recipes/<int:id>/post', methods=["POST"])
def update_recipe(id):
    if 'user_id' not in session:
        return redirect('/')
    if not Recipe.validator(request.form):
        return redirect('/recipes/new')
    data = {
        **request.form,
        'id':id
    }
    Recipe.update(data)
    return redirect('/dashboard')