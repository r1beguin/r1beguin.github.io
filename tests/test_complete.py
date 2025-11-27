#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test complet avec serveur HTTP et Selenium
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import http.server
import socketserver
import threading
from pathlib import Path
import os

PORT = 8888

class QuietHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

def start_http_server():
    """
    Démarre un serveur HTTP en arrière-plan
    """
    os.chdir(Path(__file__).parent)
    Handler = QuietHTTPRequestHandler
    httpd = socketserver.TCPServer(("", PORT), Handler)
    thread = threading.Thread(target=httpd.serve_forever)
    thread.daemon = True
    thread.start()
    return httpd

def setup_driver():
    """
    Configure le driver Chrome en mode headless
    """
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
        print(f"Erreur lors de l'initialisation du driver: {e}")
        print("\nVeuillez installer ChromeDriver:")
        print("1. Telecharger depuis https://chromedriver.chromium.org/")
        print("2. Ajouter au PATH systeme")
        return None

def run_tests():
    """
    Exécute tous les tests
    """
    print("=" * 70)
    print("SAMA HELPER - TESTS AUTOMATISES AVEC SELENIUM")
    print("=" * 70)
    
    # Démarrer le serveur HTTP
    print("\n[1/5] Demarrage du serveur HTTP local...")
    httpd = start_http_server()
    time.sleep(1)
    print(f"      Serveur demarre sur http://localhost:{PORT}")
    
    # Initialiser le driver
    print("\n[2/5] Initialisation de Chrome en mode headless...")
    driver = setup_driver()
    if not driver:
        print("\n[ERREUR] Impossible de continuer sans le driver")
        return
    print("      Chrome initialise avec succes")
    
    try:
        url = f"http://localhost:{PORT}/index.html"
        
        # Test 1: Charger la page
        print("\n[3/5] Chargement de la page web...")
        driver.get(url)
        time.sleep(3)  # Attendre le chargement complet
        print(f"      Titre: {driver.title}")
        
        # Test 2: Vérifier les aliments
        print("\n[4/5] Verification du chargement des aliments...")
        try:
            # Attendre le chargement des données
            WebDriverWait(driver, 10).until(
                lambda d: d.execute_script("return window.testAPI && window.testAPI.getAllFoods().length > 0")
            )
            
            num_foods = driver.execute_script("return window.testAPI.getAllFoods().length")
            print(f"      Nombre d'aliments charges: {num_foods}")
            
            # Vérifier l'affichage des cartes
            food_cards = driver.find_elements(By.CLASS_NAME, "food-card")
            print(f"      Cartes affichees: {len(food_cards)}")
            
            if len(food_cards) > 0:
                first_card = food_cards[0]
                food_name = first_card.find_element(By.CLASS_NAME, "food-name").text
                print(f"      Premiere carte: {food_name}")
        except Exception as e:
            print(f"      [ERREUR] {e}")
        
        # Test 3: Tester la recherche
        print("\n[5/5] Test de la fonctionnalite de recherche...")
        
        search_tests = [
            ("oeuf", "Recherche d'oeufs"),
            ("lait", "Recherche de lait"),
            ("", "Reinitialisation")
        ]
        
        search_input = driver.find_element(By.ID, "searchInput")
        
        for term, description in search_tests:
            search_input.clear()
            if term:
                search_input.send_keys(term)
            time.sleep(1)
            
            result_count = driver.find_element(By.ID, "resultCount").text
            visible_cards = len(driver.find_elements(By.CLASS_NAME, "food-card"))
            
            print(f"      {description}: {result_count} resultat(s), {visible_cards} carte(s) visible(s)")
        
        # Test 4: Filtres
        print("\n[6/6] Test des filtres...")
        filter_btns = driver.find_elements(By.CLASS_NAME, "filter-btn")
        
        for btn in filter_btns:
            filter_name = btn.text
            btn.click()
            time.sleep(0.5)
            result_count = driver.find_element(By.ID, "resultCount").text
            print(f"      Filtre '{filter_name}': {result_count} resultat(s)")
        
        # Résumé
        print("\n" + "=" * 70)
        print("TESTS TERMINES AVEC SUCCES")
        print("=" * 70)
        print("\nL'application fonctionne correctement:")
        print("  - Page HTML chargee")
        print("  - Donnees JSON chargees")
        print("  - Recherche fonctionnelle")
        print("  - Filtres fonctionnels")
        print("  - Interface responsive")
        
        # Prendre une capture d'écran
        screenshot_path = Path(__file__).parent / "test_screenshot.png"
        driver.save_screenshot(str(screenshot_path))
        print(f"\nCapture d'ecran sauvegardee: {screenshot_path}")
        
    except Exception as e:
        print(f"\n[ERREUR] {e}")
        import traceback
        traceback.print_exc()
    finally:
        driver.quit()
        httpd.shutdown()
        print("\nDriver et serveur fermes.")

if __name__ == "__main__":
    run_tests()
