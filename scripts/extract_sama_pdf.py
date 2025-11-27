#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script d'extraction de données du PDF SAMA
Génère un fichier JSON structuré pour une application web
"""

import pdfplumber
import json
from pathlib import Path

def extract_pdf_data(pdf_path):
    """
    Extrait les données du PDF SAMA et les structure en JSON
    """
    data = {
        "metadata": {},
        "pages": [],
        "text_content": "",
        "tables": []
    }
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            # Métadonnées du PDF
            data["metadata"] = {
                "num_pages": len(pdf.pages),
                "filename": Path(pdf_path).name
            }
            
            all_text = []
            
            # Extraire le contenu de chaque page
            for i, page in enumerate(pdf.pages):
                page_data = {
                    "page_number": i + 1,
                    "text": page.extract_text() or "",
                    "tables": []
                }
                
                # Extraire les tableaux de la page
                tables = page.extract_tables()
                if tables:
                    for j, table in enumerate(tables):
                        table_data = {
                            "table_number": j + 1,
                            "rows": table
                        }
                        page_data["tables"].append(table_data)
                        data["tables"].append({
                            "page": i + 1,
                            "table_number": j + 1,
                            "data": table
                        })
                
                data["pages"].append(page_data)
                all_text.append(page_data["text"])
            
            # Tout le texte concaténé
            data["text_content"] = "\n\n".join(all_text)
    
    except Exception as e:
        print(f"Erreur lors de l'extraction du PDF: {e}")
        return None
    
    return data

def save_to_json(data, output_path):
    """
    Sauvegarde les données extraites en JSON
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"[OK] Donnees sauvegardees dans {output_path}")
        return True
    except Exception as e:
        print(f"Erreur lors de la sauvegarde JSON: {e}")
        return False

def main():
    """
    Fonction principale
    """
    # Chemins des fichiers
    pdf_path = Path(__file__).parent / "SAMA.pdf"
    output_path = Path(__file__).parent / "sama_data.json"
    
    print(f"Extraction des donnees de {pdf_path}...")
    
    if not pdf_path.exists():
        print(f"Erreur: Le fichier {pdf_path} n'existe pas.")
        return
    
    # Extraire les données
    data = extract_pdf_data(pdf_path)
    
    if data is None:
        print("Echec de l'extraction des donnees.")
        return
    
    # Afficher un résumé
    print(f"\n--- Resume de l'extraction ---")
    print(f"Nombre de pages: {data['metadata']['num_pages']}")
    print(f"Nombre de tableaux: {len(data['tables'])}")
    print(f"Longueur du texte: {len(data['text_content'])} caracteres")
    
    # Sauvegarder en JSON
    if save_to_json(data, output_path):
        print(f"\n[OK] Extraction terminee avec succes!")
        print(f"Fichier JSON cree: {output_path}")
    else:
        print(f"\n[ERREUR] Echec de la sauvegarde du fichier JSON.")

if __name__ == "__main__":
    main()
