#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour ajouter les données de saisonnalité aux fruits et légumes
"""

import json
from pathlib import Path

# Dictionnaire de saisonnalité pour les fruits (France/Europe)
FRUIT_SEASONS = {
    # Printemps (Mars-Mai)
    'fraise': ['printemps'],
    'fraises': ['printemps'],
    'cerise': ['printemps', 'ete'],
    'cerises': ['printemps', 'ete'],
    'rhubarbe': ['printemps'],
    'abricot': ['ete'],
    'abricots': ['ete'],
    
    # Été (Juin-Août)
    'melon': ['ete'],
    'pastèque': ['ete'],
    'pasteque': ['ete'],
    'pêche': ['ete'],
    'peche': ['ete'],
    'pêches': ['ete'],
    'peches': ['ete'],
    'nectarine': ['ete'],
    'prune': ['ete'],
    'prunes': ['ete'],
    'mirabelle': ['ete'],
    'groseille': ['ete'],
    'cassis': ['ete'],
    'myrtille': ['ete'],
    'myrtilles': ['ete'],
    'framboise': ['ete'],
    'framboises': ['ete'],
    'mûre': ['ete', 'automne'],
    'mure': ['ete', 'automne'],
    'figue': ['ete', 'automne'],
    'figues': ['ete', 'automne'],
    
    # Automne (Septembre-Novembre)
    'pomme': ['automne', 'hiver'],
    'pommes': ['automne', 'hiver'],
    'poire': ['automne', 'hiver'],
    'poires': ['automne', 'hiver'],
    'raisin': ['automne'],
    'raisins': ['automne'],
    'coing': ['automne'],
    'châtaigne': ['automne'],
    'chataigne': ['automne'],
    'noix': ['automne'],
    'noisette': ['automne'],
    
    # Hiver (Décembre-Février)
    'orange': ['hiver'],
    'oranges': ['hiver'],
    'mandarine': ['hiver'],
    'clémentine': ['hiver'],
    'clementine': ['hiver'],
    'pamplemousse': ['hiver'],
    'citron': ['toute_annee'],
    'kiwi': ['hiver'],
    'kiwis': ['hiver'],
    
    # Toute l'année
    'banane': ['toute_annee'],
    'bananes': ['toute_annee'],
    'ananas': ['toute_annee'],
    'mangue': ['toute_annee'],
    'avocat': ['toute_annee'],
    'avocats': ['toute_annee']
}

# Dictionnaire de saisonnalité pour les légumes
VEGETABLE_SEASONS = {
    # Printemps
    'asperge': ['printemps'],
    'asperges': ['printemps'],
    'radis': ['printemps', 'ete'],
    'petit pois': ['printemps'],
    'pois': ['printemps'],
    'épinard': ['printemps', 'automne'],
    'epinard': ['printemps', 'automne'],
    'laitue': ['printemps', 'ete'],
    'artichaut': ['printemps', 'ete'],
    
    # Été
    'tomate': ['ete'],
    'tomates': ['ete'],
    'concombre': ['ete'],
    'courgette': ['ete'],
    'courgettes': ['ete'],
    'aubergine': ['ete'],
    'aubergines': ['ete'],
    'poivron': ['ete'],
    'poivrons': ['ete'],
    'haricot': ['ete'],
    'haricots': ['ete'],
    'maïs': ['ete'],
    'mais': ['ete'],
    
    # Automne
    'potiron': ['automne'],
    'citrouille': ['automne'],
    'courge': ['automne'],
    'champignon': ['automne'],
    'champignons': ['automne'],
    'brocoli': ['automne', 'hiver'],
    'chou-fleur': ['automne', 'hiver'],
    'chou': ['automne', 'hiver'],
    'choux': ['automne', 'hiver'],
    
    # Hiver
    'poireau': ['hiver'],
    'poireaux': ['hiver'],
    'endive': ['hiver'],
    'endives': ['hiver'],
    'navet': ['hiver'],
    'navets': ['hiver'],
    'panais': ['hiver'],
    'topinambour': ['hiver'],
    'chou de bruxelles': ['hiver'],
    'céleri': ['hiver'],
    'celeri': ['hiver'],
    
    # Toute l'année
    'carotte': ['toute_annee'],
    'carottes': ['toute_annee'],
    'pomme de terre': ['toute_annee'],
    'oignon': ['toute_annee'],
    'oignons': ['toute_annee'],
    'ail': ['toute_annee'],
    'échalote': ['toute_annee'],
    'echalote': ['toute_annee'],
    'betterave': ['toute_annee']
}

def get_seasons_for_food(food_name):
    """
    Détermine les saisons pour un aliment donné
    """
    name_lower = food_name.lower()
    
    # Vérifier dans les fruits
    for fruit_key, seasons in FRUIT_SEASONS.items():
        if fruit_key in name_lower:
            return seasons
    
    # Vérifier dans les légumes
    for veg_key, seasons in VEGETABLE_SEASONS.items():
        if veg_key in name_lower:
            return seasons
    
    return []

def add_seasonality(foods):
    """
    Ajoute les informations de saisonnalité aux aliments
    """
    for food in foods:
        category = food.get('category', '').lower()
        
        # Déterminer si c'est un fruit ou légume
        is_fruit = 'fruit' in category
        is_vegetable = 'legu' in category or 'légume' in category
        
        seasons = []
        if is_fruit or is_vegetable:
            seasons = get_seasons_for_food(food['name'])
        
        food['seasons'] = seasons
        food['is_seasonal'] = len(seasons) > 0
    
    return foods

def main():
    input_path = Path(__file__).parent / "foods.json"
    output_path = Path(__file__).parent / "foods.json"
    
    print("Ajout des donnees de saisonnalite...")
    
    # Charger les données
    with open(input_path, 'r', encoding='utf-8') as f:
        foods = json.load(f)
    
    print(f"Nombre d'aliments: {len(foods)}")
    
    # Ajouter la saisonnalité
    foods = add_seasonality(foods)
    
    # Compter les aliments avec saisonnalité
    seasonal_foods = [f for f in foods if f['is_seasonal']]
    print(f"Aliments avec saisonnalite: {len(seasonal_foods)}")
    
    # Afficher quelques exemples
    print("\n=== Exemples d'aliments saisonniers ===")
    for food in seasonal_foods[:10]:
        seasons_str = ', '.join(food['seasons'])
        print(f"- {food['name']}: {seasons_str}")
    
    # Sauvegarder
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(foods, f, ensure_ascii=False, indent=2)
    
    print(f"\n[OK] Donnees sauvegardees dans {output_path}")

if __name__ == "__main__":
    main()
