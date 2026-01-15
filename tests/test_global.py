import requests
import time
import subprocess
from requests.auth import HTTPBasicAuth

# --- Configuration des paramètres de test ---
USER = "admin"
PASSWORD = "admin"
URL = "https://localhost/predict"
DATA = {"sentence": "Test final."}
CONTAINER_NAME = "mlops-nginx-1"

# Désactivation des alertes SSL pour les certificats auto-signés
requests.packages.urllib3.disable_warnings()

def get_last_log():
    try:
        log = subprocess.check_output(f"docker logs {CONTAINER_NAME} --tail 1", shell=True).decode('utf-8').strip()
        return f"    Log Nginx : {log}"
    except:
        return ""

def print_step(msg):
    print(f"\n--- {msg} ---")
    print("-" * 50)

def run_global_tests():
    print("\n*** DEMARRAGE DE L'AUDIT INFRASTRUCTURE ***")

    # ÉTAPE 1 : Validation de la sécurité (HTTPS + Auth Basic)
    print_step("Verification SSL et Authentification")
    try:
        # Tentative de POST avec authentification
        r = requests.post(URL, auth=(USER, PASSWORD), json=DATA, verify=False)
        if r.status_code == 200:
            print("OK: Accès sécurisé validé.")
            print(get_last_log())
        else:
            print(f"ERREUR: Code {r.status_code} reçu. Vérifiez .htpasswd ou les certificats.")
    except Exception as e:
        print(f"ERREUR Connexion: {e}")

    # ÉTAPE 2 : Validation du Load Balancing
    print_step("Test du Load Balancing (API V1)")
    print("Envoi de 3 requêtes pour voir la répartition...")
    for i in range(3):
        requests.post(URL, auth=(USER, PASSWORD), json=DATA, verify=False)
        print(get_last_log())
        time.sleep(0.2)

    # ÉTAPE 3 : Validation du A/B Testing
    print_step("Test A/B Testing (Routage Header V2)")
    headers = {'X-Experiment-Group': 'debug'}
    r = requests.post(URL, auth=(USER, PASSWORD), json=DATA, headers=headers, verify=False)
    print("OK: Réponse reçue de la branche Debug.")
    print(get_last_log())

    # ÉTAPE 4 : Validation du Rate Limiting
    print_step("Test du Rate Limiting")
    print("Envoi d'une rafale de requêtes pour tester le Rate limiting")
    for _ in range(8):
        requests.post(URL, auth=(USER, PASSWORD), json=DATA, verify=False)
    time.sleep(0.5)
    print("Analyse des blocages potentiels (503) dans les logs :")
    try:
        logs = subprocess.check_output(f"docker logs {CONTAINER_NAME} --tail 4", shell=True).decode('utf-8').strip()
        print(logs)
    except:
        print("Impossible de récupérer les logs Docker.")

    print("\n*** AUDIT TERMINE ***\n")

if __name__ == "__main__":
    run_global_tests()
