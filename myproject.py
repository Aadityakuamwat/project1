# Directory structure assumed:
# ai_recipe_generator/
# ├── data/
# │   └── nlu.yml, recipes.json
# ├── actions/
# │   └── actions.py
# ├── domain.yml
# ├── config.yml
# ├── rules.yml
# ├── stories.yml
# ├── run.py

# ------------------------------
# domain.yml
# ------------------------------
domain_yaml = '''
version: "3.1"

intents:
  - greet
  - goodbye
  - get_recipe
  - get_ingredients
  - cooking_steps
  - thanks

entities:
  - dish_type
  - flavor
  - diet

slots:
  dish_type:
    type: text
  flavor:
    type: text
  diet:
    type: text

responses:
  utter_greet:
    - text: "Hello! What kind of pasta recipe are you looking for?"
  utter_goodbye:
    - text: "Goodbye! Enjoy your meal."
  utter_thanks:
    - text: "You're welcome!"

actions:
  - action_provide_recipe
  - action_provide_ingredients
  - action_provide_steps
'''

# ------------------------------
# data/nlu.yml
# ------------------------------
nlu_yml = '''
version: "3.1"
nlu:
- intent: greet
  examples: |
    - hi
    - hello
    - hey

- intent: goodbye
  examples: |
    - bye
    - see you
    - goodbye

- intent: thanks
  examples: |
    - thank you
    - thanks a lot
    - appreciate it

- intent: get_recipe
  examples: |
    - I want a [spicy](flavor) [pasta](dish_type) recipe
    - Give me a [vegan](diet) [spaghetti](dish_type) dish
    - How to cook [cheesy](flavor) [macaroni](dish_type)?

- intent: get_ingredients
  examples: |
    - What ingredients are needed for [pasta](dish_type)?
    - List ingredients for [spicy](flavor) [macaroni](dish_type)

- intent: cooking_steps
  examples: |
    - What are the steps to cook [vegan](diet) [pasta](dish_type)?
    - How do I prepare [cheesy](flavor) [spaghetti](dish_type)?
'''

# ------------------------------
# config.yml
# ------------------------------
config_yaml = '''
version: "3.1"

language: en
pipeline:
  - name: SpacyNLP
    model: en_core_web_md
  - name: SpacyTokenizer
  - name: SpacyFeaturizer
  - name: RegexFeaturizer
  - name: LexicalSyntacticFeaturizer
  - name: CountVectorsFeaturizer
  - name: DIETClassifier
  - name: EntitySynonymMapper
  - name: ResponseSelector
  - name: FallbackClassifier

policies:
  - name: RulePolicy
'''

# ------------------------------
# rules.yml
# ------------------------------
rules_yml = '''
version: "3.1"
rules:
- rule: Say goodbye
  steps:
    - intent: goodbye
    - action: utter_goodbye

- rule: Say hello
  steps:
    - intent: greet
    - action: utter_greet

- rule: Provide recipe
  steps:
    - intent: get_recipe
    - action: action_provide_recipe

- rule: Provide ingredients
  steps:
    - intent: get_ingredients
    - action: action_provide_ingredients

- rule: Provide steps
  steps:
    - intent: cooking_steps
    - action: action_provide_steps
'''

# ------------------------------
# stories.yml
# ------------------------------
stories_yml = '''
version: "3.1"
stories:
- story: recipe flow
  steps:
  - intent: greet
  - action: utter_greet
  - intent: get_recipe
  - action: action_provide_recipe
  - intent: get_ingredients
  - action: action_provide_ingredients
  - intent: cooking_steps
  - action: action_provide_steps
  - intent: thanks
  - action: utter_thanks
'''

# ------------------------------
# actions/actions.py
# ------------------------------
actions_py = '''
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import json

# Load recipe data
with open("data/recipes.json") as f:
    RECIPES = json.load(f)

def find_recipe(dish_type, flavor=None, diet=None):
    for recipe in RECIPES:
        if recipe["dish_type"] == dish_type:
            if (not flavor or flavor in recipe["tags"]) and (not diet or diet in recipe["tags"]):
                return recipe
    return None

class ActionProvideRecipe(Action):
    def name(self) -> Text:
        return "action_provide_recipe"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dish_type = tracker.get_slot("dish_type")
        flavor = tracker.get_slot("flavor")
        diet = tracker.get_slot("diet")

        recipe = find_recipe(dish_type, flavor, diet)

        if recipe:
            dispatcher.utter_message(text=f"Here's a {flavor or ''} {diet or ''} {dish_type} recipe: {recipe['name']}")
        else:
            dispatcher.utter_message(text="Sorry, I couldn't find a matching recipe.")

        return []

class ActionProvideIngredients(Action):
    def name(self) -> Text:
        return "action_provide_ingredients"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dish_type = tracker.get_slot("dish_type")
        recipe = find_recipe(dish_type)

        if recipe:
            ingredients = ", ".join(recipe['ingredients'])
            dispatcher.utter_message(text=f"Ingredients: {ingredients}")
        else:
            dispatcher.utter_message(text="I couldn't find the ingredients.")

        return []

class ActionProvideSteps(Action):
    def name(self) -> Text:
        return "action_provide_steps"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dish_type = tracker.get_slot("dish_type")
        recipe = find_recipe(dish_type)

        if recipe:
            steps = " ".join(recipe['steps'])
            dispatcher.utter_message(text=f"Steps: {steps}")
        else:
            dispatcher.utter_message(text="No steps found for this recipe.")

        return []
'''

# ------------------------------
# run.py (Optional CLI launcher)
# ------------------------------
run_py = '''
# Run using `rasa run actions` in one terminal
# And `rasa shell` in another
print("Run 'rasa run actions' and 'rasa shell' to start the bot.")
'''


