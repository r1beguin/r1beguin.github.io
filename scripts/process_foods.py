#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour traiter et nettoyer les données d'aliments du JSON SAMA
"""

import json
from pathlib import Path

def clean_category_name(category):
    """
    Nettoie et complète les noms de catégories tronqués
    """
    # Mapping des catégories tronquées vers leurs noms complets
    category_map = {
        'iment\nŒufs': 'Aliments - Œufs',
        'iment\n�ufs': 'Aliments - Œufs',
        'Produ': 'Produits laitiers',
        'iment\nSourc': 'Aliments - Sources de protéines',
        'Viand': 'Viande et volaille',
        'Poiss': 'Poisson et fruits de mer',
        'Grain': 'Graines et noix',
        'Noix': 'Noix et graines',
        'Legu': 'Légumes',
        'Fruits': 'Fruits',
        'ondim': 'Condiments et épices',
        'Herbe': 'Herbes et épices',
        'Huiles': 'Huiles et graisses',
        'dulcor': 'Édulcorants',
        'Alcoo': 'Alcools et boissons',
        'nfusi': 'Infusions et thés',
        'Jus d\'': 'Jus de fruits',
        'dditifs': 'Additifs alimentaires',
        'hampi': 'Champignons',
        'tamin': 'Vitamines et compléments',
        'Conte': 'Contenu divers',
        'Divers': 'Divers',
        'Limon': 'Limonades et sodas',
        'Subst': 'Substituts'
    }
    
    # Nettoyer les sauts de ligne
    cleaned = category.replace('\n', ' ').strip()
    
    # Chercher une correspondance exacte
    if category in category_map:
        return category_map[category]
    
    # Chercher une correspondance partielle
    for key, value in category_map.items():
        if category.startswith(key) or key.startswith(category):
            return value
    
    return cleaned

def process_food_data(json_path):
    """
    Traite les données brutes pour créer une liste d'aliments structurée
    
    Format des tableaux SAMA (à partir du tableau 2, page 3):
    Col 0: Catégorie
    Col 1: Digestibilité
    Col 2: Histamine
    Col 3: Autres amines
    Col 4: Libérateur
    Col 5: Inhibiteur
    Col 6: Nom de l'aliment (Ingrédients)
    Col 7: Remarques
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    foods = []
    current_category = ""
    
    # Parcourir tous les tableaux à partir du tableau 2 (index 1)
    # Le premier tableau est la légende, on l'ignore
    for table_idx, table in enumerate(data['tables']):
        # Ignorer le premier tableau (légende)
        if table_idx == 0:
            continue
            
        table_data = table['data']
        page = table['page']
        
        # Pour le tableau 2 (index 1), ignorer la ligne d'en-tête
        start_row = 1 if table_idx == 1 else 0
        
        # Parcourir toutes les lignes
        for row in table_data[start_row:]:
            if not row or len(row) < 7:
                continue
            
            # Format des colonnes (fixe pour tous les tableaux)
            category_col = row[0] if row[0] else ""
            digestibility = row[1] if row[1] else ""
            histamine = row[2] if row[2] else ""
            other_amines = row[3] if row[3] else ""
            liberator = row[4] if row[4] else ""
            inhibitor = row[5] if row[5] else ""
            name = row[6] if row[6] else ""
            remarks = row[7] if len(row) > 7 and row[7] else ""
            
            # Mettre à jour la catégorie si présente
            if category_col and category_col.strip():
                current_category = category_col.strip()
            
            # Si le nom est vide, ignorer cette ligne
            if not name or not name.strip():
                continue
            
            # Créer l'objet aliment
            food = {
                'name': name.strip(),
                'category': clean_category_name(current_category),
                'page': page,
                'digestibility': digestibility.strip() if digestibility else '',
                'histamine': histamine.strip() if histamine else '',
                'other_amines': other_amines.strip() if other_amines else '',
                'liberator': liberator.strip() if liberator else '',
                'inhibitor': inhibitor.strip() if inhibitor else '',
                'remarks': remarks.strip() if remarks else ''
            }
            
            foods.append(food)
    
    return foods

def main():
    json_path = Path(__file__).parent / "sama_data.json"
    output_path = Path(__file__).parent / "foods.json"
    
    print("Traitement des donnees d'aliments...")
    
    foods = process_food_data(json_path)
    
    print(f"\nNombre d'aliments extraits: {len(foods)}")
    
    # Afficher quelques exemples
    print("\n=== Exemples d'aliments ===")
    for food in foods[:5]:
        print(f"- {food['name']} (Categorie: {food['category']}, Page: {food['page']})")
    
    # Sauvegarder
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(foods, f, ensure_ascii=False, indent=2)
    
    print(f"\n[OK] Donnees sauvegardees dans {output_path}")

if __name__ == "__main__":
    main()
