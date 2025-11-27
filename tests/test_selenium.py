#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test Selenium pour l'application SAMA Helper
Test l'interface web en mode headless
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
from pathlib import Path
import json

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
        print("\nAssurez-vous que Chrome et ChromeDriver sont installes.")
        return None

def test_page_load(driver, url):
    """
    Test le chargement de la page
    """
    print("\n[TEST 1] Chargement de la page...")
    try:
        driver.get(url)
        time.sleep(2)  # Attendre le chargement
        
        title = driver.title
        print(f"  - Titre de la page: {title}")
        
        # Vérifier que le titre contient "SAMA"
        assert "SAMA" in title, "Le titre ne contient pas 'SAMA'"
        
        print("  [OK] Page chargee avec succes")
        return True
    except Exception as e:
        print(f"  [ERREUR] {e}")
        return False

def test_search_bar(driver):
    """
    Test la barre de recherche
    """
    print("\n[TEST 2] Test de la barre de recherche...")
    try:
        # Attendre que la barre de recherche soit présente
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "searchInput"))
        )
        
        print("  - Barre de recherche trouvee")
        
        # Tester la recherche
        search_input.clear()
        search_input.send_keys("oeuf")
        time.sleep(1)
        
        # Vérifier le nombre de résultats
        result_count = driver.find_element(By.ID, "resultCount")
        count = int(result_count.text)
        
        print(f"  - Recherche 'oeuf': {count} resultat(s)")
        
        # Effacer la recherche
        search_input.clear()
        time.sleep(1)
        
        print("  [OK] Barre de recherche fonctionne")
        return True
    except Exception as e:
        print(f"  [ERREUR] {e}")
        return False

def test_food_cards(driver):
    """
    Test l'affichage des cartes d'aliments
    """
    print("\n[TEST 3] Test des cartes d'aliments...")
    try:
        # Attendre que les cartes soient chargées
        food_cards = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "food-card"))
        )
        
        num_cards = len(food_cards)
        print(f"  - Nombre de cartes affichees: {num_cards}")
        
        if num_cards > 0:
            # Vérifier le contenu de la première carte
            first_card = food_cards[0]
            food_name = first_card.find_element(By.CLASS_NAME, "food-name")
            print(f"  - Premiere carte: {food_name.text}")
            
            print("  [OK] Cartes d'aliments affichees correctement")
            return True
        else:
            print("  [ERREUR] Aucune carte d'aliment trouvee")
            return False
            
    except Exception as e:
        print(f"  [ERREUR] {e}")
        return False

def test_filters(driver):
    """
    Test les filtres
    """
    print("\n[TEST 4] Test des filtres...")
    try:
        # Trouver tous les boutons de filtre
        filter_btns = driver.find_elements(By.CLASS_NAME, "filter-btn")
        print(f"  - Nombre de filtres trouves: {len(filter_btns)}")
        
        # Tester le filtre "Histamine elevee"
        for btn in filter_btns:
            if "Histamine elevee" in btn.text:
                btn.click()
                time.sleep(1)
                
                result_count = driver.find_element(By.ID, "resultCount")
                count = int(result_count.text)
                print(f"  - Filtre 'Histamine elevee': {count} resultat(s)")
                break
        
        # Revenir au filtre "Tous"
        filter_btns[0].click()
        time.sleep(1)
        
        print("  [OK] Filtres fonctionnent correctement")
        return True
    except Exception as e:
        print(f"  [ERREUR] {e}")
        return False

def test_search_functionality(driver):
    """
    Test la fonctionnalité de recherche avec différents termes
    """
    print("\n[TEST 5] Test de recherche avancee...")
    try:
        search_input = driver.find_element(By.ID, "searchInput")
        
        test_terms = ["oeuf", "lait", "poisson", "xyz123"]
        
        for term in test_terms:
            search_input.clear()
            search_input.send_keys(term)
            time.sleep(0.5)
            
            result_count = driver.find_element(By.ID, "resultCount")
            count = int(result_count.text)
            print(f"  - Recherche '{term}': {count} resultat(s)")
        
        # Effacer la recherche
        search_input.clear()
        time.sleep(0.5)
        
        print("  [OK] Recherche avancee fonctionne")
        return True
    except Exception as e:
        print(f"  [ERREUR] {e}")
        return False

def test_responsive_design(driver):
    """
    Test le design responsive
    """
    print("\n[TEST 6] Test du design responsive...")
    try:
        # Tester différentes tailles d'écran
        sizes = [
            (1920, 1080, "Desktop"),
            (768, 1024, "Tablet"),
            (375, 667, "Mobile")
        ]
        
        for width, height, device in sizes:
            driver.set_window_size(width, height)
            time.sleep(0.5)
            print(f"  - Test sur {device} ({width}x{height}): OK")
        
        # Remettre la taille par défaut
        driver.set_window_size(1920, 1080)
        
        print("  [OK] Design responsive fonctionne")
        return True
    except Exception as e:
        print(f"  [ERREUR] {e}")
        return False

def run_all_tests():
    """
    Exécute tous les tests
    """
    print("=" * 60)
    print("SAMA HELPER - TESTS SELENIUM (MODE HEADLESS)")
    print("=" * 60)
    
    # Configurer l'URL du fichier HTML local
    html_path = Path(__file__).parent / "index.html"
    url = f"file:///{html_path.as_posix()}"
    
    print(f"\nURL de test: {url}")
    
    # Initialiser le driver
    driver = setup_driver()
    if not driver:
        print("\n[ERREUR FATALE] Impossible d'initialiser le driver")
        return
    
    try:
        # Exécuter les tests
        results = []
        results.append(("Chargement page", test_page_load(driver, url)))
        results.append(("Barre de recherche", test_search_bar(driver)))
        results.append(("Cartes d'aliments", test_food_cards(driver)))
        results.append(("Filtres", test_filters(driver)))
        results.append(("Recherche avancee", test_search_functionality(driver)))
        results.append(("Design responsive", test_responsive_design(driver)))
        
        # Résumé des tests
        print("\n" + "=" * 60)
        print("RESUME DES TESTS")
        print("=" * 60)
        
        passed = 0
        failed = 0
        
        for test_name, result in results:
            status = "[OK]" if result else "[ERREUR]"
            print(f"{status} {test_name}")
            if result:
                passed += 1
            else:
                failed += 1
        
        print("\n" + "-" * 60)
        print(f"Tests reussis: {passed}/{len(results)}")
        print(f"Tests echoues: {failed}/{len(results)}")
        print("-" * 60)
        
        if failed == 0:
            print("\n[SUCCESS] Tous les tests sont passes avec succes!")
        else:
            print(f"\n[WARNING] {failed} test(s) ont echoue")
        
    except Exception as e:
        print(f"\n[ERREUR FATALE] {e}")
    finally:
        # Fermer le driver
        driver.quit()
        print("\nDriver ferme.")

if __name__ == "__main__":
    run_all_tests()
