"""Test simple pour la fonctionnalite de liste"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

# Configuration du driver
chrome_options = Options()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')

driver = webdriver.Chrome(options=chrome_options)

try:
    print("Test: Connexion au serveur...")
    driver.get("http://localhost:8000")
    print("[OK] Connexion reussie")
    
    print("\nTest: Chargement des aliments...")
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "food-card")))
    print("[OK] Aliments charges")
    
    print("\nTest: Verification du compteur initial...")
    list_count = driver.find_element(By.ID, "listCount")
    print(f"Compteur: {list_count.text}")
    assert list_count.text == "0", "Le compteur devrait etre a 0"
    print("[OK] Compteur initial correct")
    
    print("\nTest: Ajout d'un aliment...")
    add_btn = driver.find_element(By.CLASS_NAME, "add-to-list-btn")
    add_btn.click()
    time.sleep(0.5)
    print(f"Compteur apres ajout: {list_count.text}")
    assert list_count.text == "1", "Le compteur devrait etre a 1"
    print("[OK] Aliment ajoute")
    
    print("\nTest: Ouverture de la sidebar...")
    floating_btn = driver.find_element(By.CLASS_NAME, "floating-list-btn")
    floating_btn.click()
    time.sleep(0.5)
    sidebar = driver.find_element(By.ID, "listSidebar")
    assert "open" in sidebar.get_attribute("class"), "La sidebar devrait etre ouverte"
    print("[OK] Sidebar ouverte")
    
    print("\nTest: Verification de l'aliment dans la liste...")
    list_items = driver.find_elements(By.CLASS_NAME, "list-item")
    print(f"Nombre d'elements dans la liste: {len(list_items)}")
    assert len(list_items) == 1, "Il devrait y avoir 1 element"
    print("[OK] Aliment present dans la liste")
    
    print("\n" + "="*50)
    print("TOUS LES TESTS SONT PASSES!")
    print("="*50)
    
except Exception as e:
    print(f"\n[ERREUR] {str(e)}")
    import traceback
    traceback.print_exc()
    
finally:
    time.sleep(2)
    driver.quit()
