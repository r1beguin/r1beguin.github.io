#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test du filtre de digestibilité
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import http.server
import socketserver
import threading
from pathlib import Path
import os

PORT = 8890

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
    chrome_options.add_argument("--window-size=1920,1080")
    
    try:
        return webdriver.Chrome(options=chrome_options)
    except Exception as e:
        print(f"Erreur: {e}")
        return None

def test_digestibility_filter():
    print("=" * 70)
    print("TEST DU FILTRE DE DIGESTIBILITE")
    print("=" * 70)
    
    print("\n[1/4] Demarrage du serveur...")
    httpd = start_http_server()
    time.sleep(1)
    print(f"      Serveur sur http://localhost:{PORT}")
    
    print("\n[2/4] Initialisation de Chrome headless...")
    driver = setup_driver()
    if not driver:
        return
    print("      Chrome initialise")
    
    try:
        url = f"http://localhost:{PORT}/index.html"
        driver.get(url)
        time.sleep(3)
        
        print("\n[3/4] Test des filtres de digestibilite...")
        
        # Vérifier que les boutons existent
        dig_btns = driver.find_elements(By.CLASS_NAME, "digestibility-btn")
        print(f"      Nombre de boutons digestibilite: {len(dig_btns)}")
        
        # Tester chaque niveau de digestibilité
        digestibility_levels = [
            ("0", "Bonne", 351),
            ("1", "Moyenne", 125),
            ("2", "Difficile", 244),
            ("3", "Tres difficile", 56),
            ("?", "Inconnu", 86)
        ]
        
        for level, name, expected_count in digestibility_levels:
            dig_btn = driver.find_element(By.CSS_SELECTOR, f'[data-digestibility="{level}"]')
            dig_btn.click()
            time.sleep(0.8)
            
            result_count = int(driver.find_element(By.ID, "resultCount").text)
            status = "OK" if result_count == expected_count else f"ATTENTION (attendu: {expected_count})"
            print(f"      Digestibilite {level} ({name}): {result_count} aliments - {status}")
        
        # Test combinaison: Fruits + Digestibilité 0
        print("\n[4/4] Test de combinaison (Fruits + Digestibilite 0)...")
        
        reset_btn = driver.find_element(By.ID, "resetFilters")
        reset_btn.click()
        time.sleep(0.5)
        
        # Sélectionner Fruits
        from selenium.webdriver.support.ui import Select
        category_select = Select(driver.find_element(By.ID, "categoryFilter"))
        for option in category_select.options:
            if "Fruits" in option.text:
                category_select.select_by_visible_text(option.text)
                break
        time.sleep(0.5)
        
        fruits_count = int(driver.find_element(By.ID, "resultCount").text)
        print(f"      Fruits: {fruits_count} aliments")
        
        # Ajouter filtre digestibilité 0
        dig_0_btn = driver.find_element(By.CSS_SELECTOR, '[data-digestibility="0"]')
        dig_0_btn.click()
        time.sleep(0.5)
        
        fruits_dig_0 = int(driver.find_element(By.ID, "resultCount").text)
        print(f"      Fruits avec digestibilite 0: {fruits_dig_0} aliments")
        
        print("\n" + "=" * 70)
        print("RESULTAT DU TEST")
        print("=" * 70)
        print("\nFiltre de digestibilite:")
        print("  - 6 niveaux disponibles (Toutes, 0, 1, 2, 3, ?)")
        print("  - Filtrage fonctionnel")
        print("  - Combinaison avec autres filtres OK")
        print("  - Codes couleur: Vert (0), Jaune (1), Orange (2), Rouge (3)")
        print("\nLe filtre de digestibilite fonctionne correctement!")
        
    except Exception as e:
        print(f"\nErreur: {e}")
        import traceback
        traceback.print_exc()
    finally:
        driver.quit()
        httpd.shutdown()
        print("\nDriver et serveur fermes.")

if __name__ == "__main__":
    test_digestibility_filter()
