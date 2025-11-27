"""
Tests Selenium pour la fonctionnalité de liste personnalisée
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import os

def setup_driver():
    """Configure le driver Chrome"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=1920,1080')
    return webdriver.Chrome(options=chrome_options)

def test_add_food_to_list():
    """Test 1: Ajouter un aliment a la liste"""
    driver = setup_driver()
    try:
        # Charger la page
        driver.get("http://localhost:8000")
        
        # Attendre que les aliments soient chargés
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "food-card")))
        
        # Vérifier que le badge est à 0
        list_count = driver.find_element(By.ID, "listCount")
        assert list_count.text == "0", "Le compteur devrait être à 0 au départ"
        
        # Trouver le premier bouton + et cliquer dessus
        add_buttons = driver.find_elements(By.CLASS_NAME, "add-to-list-btn")
        assert len(add_buttons) > 0, "Devrait y avoir des boutons +"
        
        first_button = add_buttons[0]
        first_button.click()
        time.sleep(0.3)
        
        # Vérifier que le compteur est maintenant à 1
        assert list_count.text == "1", "Le compteur devrait être à 1 après ajout"
        
        # Vérifier que le bouton a changé (classe in-list)
        assert "in-list" in first_button.get_attribute("class"), "Le bouton devrait avoir la classe 'in-list'"
        
        print("[OK] Test 1 reussi: Ajout d'un aliment a la liste")
        return True
        
    except Exception as e:
        print(f"[FAIL] Test 1 echoue: {str(e)}")
        return False
    finally:
        driver.quit()

def test_open_sidebar():
    """Test 2: Ouvrir la sidebar"""
    driver = setup_driver()
    try:
        driver.get("http://localhost:8000")
        
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "floating-list-btn")))
        
        # Ouvrir la sidebar
        floating_btn = driver.find_element(By.CLASS_NAME, "floating-list-btn")
        floating_btn.click()
        time.sleep(0.5)
        
        # Vérifier que la sidebar est ouverte
        sidebar = driver.find_element(By.ID, "listSidebar")
        assert "open" in sidebar.get_attribute("class"), "La sidebar devrait avoir la classe 'open'"
        
        print("[OK] Test 2 reussi: Ouverture de la sidebar")
        return True
        
    except Exception as e:
        print(f"[FAIL] Test 2 echoue: {str(e)}")
        return False
    finally:
        driver.quit()

def test_add_and_view_in_sidebar():
    """Test 3: Ajouter un aliment et le voir dans la sidebar"""
    driver = setup_driver()
    try:
        driver.get("http://localhost:8000")
        
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "food-card")))
        
        # Ajouter un aliment
        add_buttons = driver.find_elements(By.CLASS_NAME, "add-to-list-btn")
        add_buttons[0].click()
        time.sleep(0.3)
        
        # Ouvrir la sidebar
        floating_btn = driver.find_element(By.CLASS_NAME, "floating-list-btn")
        floating_btn.click()
        time.sleep(0.5)
        
        # Vérifier qu'il y a un élément dans la liste
        list_items = driver.find_elements(By.CLASS_NAME, "list-item")
        assert len(list_items) == 1, "Il devrait y avoir 1 élément dans la liste"
        
        print("[OK] Test 3 reussi: L'aliment ajoute apparait dans la sidebar")
        return True
        
    except Exception as e:
        print(f"[FAIL] Test 3 echoue: {str(e)}")
        return False
    finally:
        driver.quit()

def test_remove_from_list():
    """Test 4: Retirer un aliment de la liste"""
    driver = setup_driver()
    try:
        driver.get("http://localhost:8000")
        
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "food-card")))
        
        # Ajouter un aliment
        add_buttons = driver.find_elements(By.CLASS_NAME, "add-to-list-btn")
        add_buttons[0].click()
        time.sleep(0.3)
        
        # Ouvrir la sidebar
        floating_btn = driver.find_element(By.CLASS_NAME, "floating-list-btn")
        floating_btn.click()
        time.sleep(0.5)
        
        # Cliquer sur le bouton de suppression
        remove_btn = driver.find_element(By.CLASS_NAME, "remove-btn")
        remove_btn.click()
        time.sleep(0.3)
        
        # Vérifier que la liste est vide
        empty_message = driver.find_element(By.CLASS_NAME, "empty-list")
        assert empty_message.is_displayed(), "Le message 'liste vide' devrait être affiché"
        
        # Vérifier que le compteur est à 0
        list_count = driver.find_element(By.ID, "listCount")
        assert list_count.text == "0", "Le compteur devrait être à 0"
        
        print("[OK] Test 4 reussi: Suppression d'un aliment de la liste")
        return True
        
    except Exception as e:
        print(f"[FAIL] Test 4 echoue: {str(e)}")
        return False
    finally:
        driver.quit()

def test_add_multiple_foods():
    """Test 5: Ajouter plusieurs aliments"""
    driver = setup_driver()
    try:
        driver.get("http://localhost:8000")
        
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "food-card")))
        
        # Ajouter 5 aliments
        add_buttons = driver.find_elements(By.CLASS_NAME, "add-to-list-btn")
        for i in range(5):
            add_buttons[i].click()
            time.sleep(0.2)
        
        # Vérifier que le compteur est à 5
        list_count = driver.find_element(By.ID, "listCount")
        assert list_count.text == "5", "Le compteur devrait être à 5"
        
        # Ouvrir la sidebar et vérifier
        floating_btn = driver.find_element(By.CLASS_NAME, "floating-list-btn")
        floating_btn.click()
        time.sleep(0.5)
        
        list_items = driver.find_elements(By.CLASS_NAME, "list-item")
        assert len(list_items) == 5, "Il devrait y avoir 5 éléments dans la liste"
        
        print("[OK] Test 5 reussi: Ajout de plusieurs aliments")
        return True
        
    except Exception as e:
        print(f"[FAIL] Test 5 echoue: {str(e)}")
        return False
    finally:
        driver.quit()

def test_toggle_food():
    """Test 6: Toggle un aliment (ajouter puis retirer avec le bouton +)"""
    driver = setup_driver()
    try:
        driver.get("http://localhost:8000")
        
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "food-card")))
        
        # Ajouter un aliment
        add_buttons = driver.find_elements(By.CLASS_NAME, "add-to-list-btn")
        first_button = add_buttons[0]
        first_button.click()
        time.sleep(0.3)
        
        # Vérifier que le compteur est à 1
        list_count = driver.find_element(By.ID, "listCount")
        assert list_count.text == "1", "Le compteur devrait être à 1"
        
        # Re-cliquer pour retirer
        first_button.click()
        time.sleep(0.3)
        
        # Vérifier que le compteur est à 0
        assert list_count.text == "0", "Le compteur devrait être à 0 après toggle"
        
        print("[OK] Test 6 reussi: Toggle d'un aliment")
        return True
        
    except Exception as e:
        print(f"[FAIL] Test 6 echoue: {str(e)}")
        return False
    finally:
        driver.quit()

def test_clear_list():
    """Test 7: Vider toute la liste"""
    driver = setup_driver()
    try:
        driver.get("http://localhost:8000")
        
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "food-card")))
        
        # Ajouter 3 aliments
        add_buttons = driver.find_elements(By.CLASS_NAME, "add-to-list-btn")
        for i in range(3):
            add_buttons[i].click()
            time.sleep(0.2)
        
        # Ouvrir la sidebar
        floating_btn = driver.find_element(By.CLASS_NAME, "floating-list-btn")
        floating_btn.click()
        time.sleep(0.5)
        
        # Cliquer sur "Vider la liste"
        clear_btn = driver.find_element(By.CLASS_NAME, "clear-list-btn")
        clear_btn.click()
        time.sleep(0.3)
        
        # Accepter l'alerte de confirmation
        alert = driver.switch_to.alert
        alert.accept()
        time.sleep(0.3)
        
        # Vérifier que la liste est vide
        list_count = driver.find_element(By.ID, "listCount")
        assert list_count.text == "0", "Le compteur devrait être à 0"
        
        empty_message = driver.find_element(By.CLASS_NAME, "empty-list")
        assert empty_message.is_displayed(), "Le message 'liste vide' devrait être affiché"
        
        print("[OK] Test 7 reussi: Vidage complet de la liste")
        return True
        
    except Exception as e:
        print(f"[FAIL] Test 7 echoue: {str(e)}")
        return False
    finally:
        driver.quit()

def test_persistence():
    """Test 8: Test de la persistance (localStorage)"""
    driver = setup_driver()
    try:
        driver.get("http://localhost:8000")
        
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "food-card")))
        
        # Ajouter un aliment
        add_buttons = driver.find_elements(By.CLASS_NAME, "add-to-list-btn")
        add_buttons[0].click()
        time.sleep(0.3)
        
        # Recharger la page
        driver.refresh()
        time.sleep(1)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "food-card")))
        
        # Vérifier que le compteur est toujours à 1
        list_count = driver.find_element(By.ID, "listCount")
        assert list_count.text == "1", "Le compteur devrait être toujours à 1 après rechargement"
        
        # Vérifier que le bouton est toujours marqué comme 'in-list'
        first_button = driver.find_elements(By.CLASS_NAME, "add-to-list-btn")[0]
        assert "in-list" in first_button.get_attribute("class"), "Le bouton devrait toujours avoir la classe 'in-list'"
        
        print("[OK] Test 8 reussi: Persistance avec localStorage")
        return True
        
    except Exception as e:
        print(f"[FAIL] Test 8 echoue: {str(e)}")
        return False
    finally:
        driver.quit()

def run_all_tests():
    """Execute tous les tests"""
    print("\n" + "="*60)
    print("TESTS DE LA FONCTIONNALITE DE LISTE PERSONNALISEE")
    print("="*60 + "\n")
    
    tests = [
        test_add_food_to_list,
        test_open_sidebar,
        test_add_and_view_in_sidebar,
        test_remove_from_list,
        test_add_multiple_foods,
        test_toggle_food,
        test_clear_list,
        test_persistence
    ]
    
    results = []
    for test in tests:
        results.append(test())
        time.sleep(1)
    
    # Resume
    print("\n" + "="*60)
    passed = sum(results)
    total = len(results)
    print(f"RESUME: {passed}/{total} tests reussis")
    
    if passed == total:
        print("[OK] Tous les tests sont passes avec succes!")
    else:
        print(f"[FAIL] {total - passed} test(s) echoue(s)")
    print("="*60 + "\n")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
