# Copyright 2023 <Saafi Achref SAAA87070201>
#Copyright 2023 <Boudaoud Wassim BOUW05109506>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import Flask
from flask import render_template
from flask import g
from flask import request
import random
from .database import Database
app = Flask(__name__, static_url_path="", static_folder="static")

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database
    
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()

@app.route('/')
def index():
    database = Database()
    liste_animaux = random.sample(get_db().get_animaux(), k=5)
    return render_template('index.html', liste_animaux=liste_animaux)
    
@app.route('/listeanimaux')
def liste():
    database = Database()
    liste_animaux = get_db().get_animaux()
    return render_template('animaux.html', liste_animaux=liste_animaux)
    
@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')   

@app.route('/form')
def form():
    # À remplacer par le contenu de votre choix.
    return render_template('form.html')
    
    
@app.route('/envoieFormulaire', methods=["POST"])
def soumettreformulaire():
    error = False
    nom = request.form["nomAnimal"]
    espece = request.form["Espece"]
    race = request.form["Race"]
    age = request.form["age"]
    description = request.form["description"]
    email = request.form["email"]
    adresse = request.form["adresse"]
    ville = request.form["ville"]
    code = request.form["codePostal"]

    if not nom or not nom.strip():
        error = True
    elif any(char.isdigit() for char in nom):
        error = True
    elif "," in nom:
        error = True
    elif len(nom) < 3 or len(nom) > 20:
        error = True

    if not espece or not espece.strip():
        error = True
    elif any(char.isdigit() for char in espece):
        error = True    
    elif "," in espece:
        error = True

    if not race or not race.strip():
        error = True
    elif any(char.isdigit() for char in race):
        error = True    
    elif "," in race:
        error = True

    if not age or not age.strip():
        error = True
    elif int(age) < 0 or int(age) > 30:
        error = True

    if not description or not description.strip():
        error = True
    elif "," in description:
        error = True

    if not email or not email.strip():
        error = True
    elif "," in email:
        error = True

    if not adresse or not adresse.strip():
        error = True
    elif "," in adresse:
        error = True

    if not ville or not ville.strip():
        error = True
    elif "," in ville:
        error = True

    if not code or not code.strip():
        error = True
    elif "," in code:
        error = True

    if error:
        return f"Oops, vous n'êtes pas assez intelligent pour pirater mon site. Essayez d'autres méthodes",500
    else:
        database = Database()
        database.add_animal(nom, espece, race, age,
                            description, email, adresse,
                            ville, code)

    return render_template("confirmation.html", animal_nom=nom,
    					   animal_espece=espece, animal_race=race,
    					   animal_age=age,animal_description=description,
    					   animal_courriel=email, animal_adresse=adresse,
    					    animal_ville=ville, animal_code=code) 

@app.route('/animal/<int:animalId>')
def animal(animalId):
    database = Database()
    db= get_db()
    animal = db.get_animal(animalId)
    return render_template('animal.html', animal=animal)

@app.route('/recherche')
def recherche():
    query = request.args.get('query').lower()
    animaux = get_db().get_animaux()
    recherche_animaux = _recherche_animaux(animaux, query)
    return render_template('resultat.html', animaux=recherche_animaux)    
    
def _recherche_animaux(animaux, query):
    recherche_animaux = []
    for animal in animaux:
        if animal['espece'].lower() in query or animal['nom'].lower() in query:
            recherche_animaux.append(animal)
    return recherche_animaux    
