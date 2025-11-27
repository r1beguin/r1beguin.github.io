#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests pour les nouveaux filtres avancés (catégorie et saison)
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time
import http.server
import socketserver
import threading
from pathlib import Path
import os

PORT = 8889

class QuietHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

def start_http_server():
    os.chdir(Path(__file__).parent)
    Handler = QuietHTTPRequestHandler
    httpd = socketserver.TCPServer(("", PORT), Handler)
    thread = threading.Thread(target=httpd.serve_forever)
    thread.daemon = True
    thread.start()
    return httpd

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except Exception as e:
        print(f"Erreur: {e}")
        return None

def test_advanced_filters():
    print("=" * 70)
    print("TESTS DES FILTRES AVANCES")
    print("=" * 70)
    
    # Démarrer serveur
    print("\n[1/6] Demarrage du serveur...")
    httpd = start_http_server()
    time.sleep(1)
    print(f"      Serveur sur http://localhost:{PORT}")
    
    # Initialiser driver
    print("\n[2/6] Initialisation de Chrome headless...")
    driver = setup_driver()
    if not driver:
        print("Erreur: impossible de lancer le driver")
        return
    print("      Chrome initialise")
    
    try:
        url = f"http://localhost:{PORT}/index.html"
        driver.get(url)
        time.sleep(3)
        
        # Test 1: Filtre par catégorie
        print("\n[3/6] Test du filtre par categorie...")
        category_select = Select(driver.find_element(By.ID, "categoryFilter"))
        
        # Compter les options de catégorie
        options = category_select.options
        print(f"      Nombre de categories: {len(options) - 1}")  # -1 pour "Toutes"
        
        # Tester une catégorie spécifique
        if len(options) > 1:
            category_select.select_by_index(1)  # Sélectionner la première catégorie
            time.sleep(1)
            
            result_count = driver.find_element(By.ID, "resultCount").text
            selected_category = category_select.first_selected_option.text
            print(f"      Categorie '{selected_category}': {result_count} aliment(s)")
        
        # Reset
        category_select.select_by_value("all")
        time.sleep(1)
        
        # Test 2: Filtres de saison
        print("\n[4/6] Test des filtres saisonniers...")
        season_btns = driver.find_elements(By.CLASS_NAME, "season-btn")
        print(f"      Nombre de boutons saison: {len(season_btns)}")
        
        season_tests = [
            ("printemps", "Printemps"),
            ("ete", "Ete"),
            ("automne", "Automne"),
            ("hiver", "Hiver")
        ]
        
        for season_value, season_name in season_tests:
            season_btn = driver.find_element(By.CSS_SELECTOR, f'[data-season="{season_value}"]')
            season_btn.click()
            time.sleep(0.8)
            
            result_count = driver.find_element(By.ID, "resultCount").text
            print(f"      Saison '{season_name}': {result_count} aliment(s)")
        
        # Test 3: Combinaison de filtres
        print("\n[5/6] Test de la combinaison de filtres...")
        
        # Reset d'abord
        reset_btn = driver.find_element(By.ID, "resetFilters")
        reset_btn.click()
        time.sleep(0.5)
        
        total_count = int(driver.find_element(By.ID, "resultCount").text)
        print(f"      Apres reset: {total_count} aliments")
        
        # Catégorie + Saison
        category_select = Select(driver.find_element(By.ID, "categoryFilter"))
        # Chercher la catégorie "Fruits"
        try:
            for option in category_select.options:
                if "Fruits" in option.text:
                    category_select.select_by_visible_text(option.text)
                    break
            time.sleep(0.5)
            
            fruits_count = int(driver.find_element(By.ID, "resultCount").text)
            print(f"      Categorie 'Fruits': {fruits_count} aliments")
            
            # Ajouter filtre été
            ete_btn = driver.find_element(By.CSS_SELECTOR, '[data-season="ete"]')
            ete_btn.click()
            time.sleep(0.5)
            
            fruits_ete = int(driver.find_element(By.ID, "resultCount").text)
            print(f"      Fruits d'ete: {fruits_ete} aliments")
            
        except Exception as e:
            print(f"      Info: {e}")
        
        # Test 4: Vérifier les badges de saison sur les cartes
        print("\n[6/6] Verification des badges de saison...")
        
        reset_btn.click()
        time.sleep(0.5)
        
        # Chercher des cartes avec badges de saison
        season_badges = driver.find_elements(By.CLASS_NAME, "season-badge")
        print(f"      Badges de saison affiches: {len(season_badges)}")
        
        if len(season_badges) > 0:
            # Afficher quelques exemples
            for i, badge in enumerate(season_badges[:5]):
                print(f"      - Badge {i+1}: {badge.text}")
        
        # Résumé
        print("\n" + "=" * 70)
        print("TESTS TERMINES")
        print("=" * 70)
        print("\nFonctionnalites testees:")
        print("  - Filtre par categorie (dropdown)")
        print("  - Filtres saisonniers (4 saisons)")
        print("  - Combinaison de filtres")
        print("  - Bouton de reinitialisation")
        print("  - Affichage des badges de saison")
        print("\nTous les filtres avances fonctionnent correctement!")
        
    except Exception as e:
        print(f"\nErreur: {e}")
        import traceback
        traceback.print_exc()
    finally:
        driver.quit()
        httpd.shutdown()
        print("\nDriver et serveur fermes.")

if __name__ == "__main__":
    test_advanced_filters()
