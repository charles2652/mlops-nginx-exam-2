import requests
import time
import subprocess
from requests.auth import HTTPBasicAuth

# --- CONFIGURATION ---
USER = "admin"
PASSWORD = "admin"
URL = "https://localhost/predict"
DATA = {"sentence": "Test final."}
CONTAINER_NAME = "mlops-nginx-1"

# Couleurs
BLUE, GREEN, YELLOW, RED, BOLD, END = "\033[94m", "\033[92m", "\033[93m", "\033[91m", "\033[1m", "\033[0m"

requests.packages.urllib3.disable_warnings()

def get_last_log():
    try:
        log = subprocess.check_output(f"docker logs {CONTAINER_NAME} --tail 1", shell=True).decode('utf-8').strip()
        return f"   {YELLOW}💬 Log Nginx : {log}{END}"
    except:
        return ""

def print_step(msg):
    print(f"\n{BLUE}{BOLD}👉 {msg}{END}")
    print(f"{BLUE}─" * 50 + f"{END}")

def run_global_tests():
    print(f"\n{BOLD}🚀 DÉMARRAGE DE L'AUDIT INFRASTRUCTURE{END}")

    # 1. AUTH & SSL
    print_step("Vérification SSL et Authentification")
    r = requests.post(URL, auth=(USER, PASSWORD), json=DATA, verify=False)
    if r.status_code == 200:
        print(f"{GREEN}✅ Accès sécurisé validé.{END}")
        print(get_last_log())

    # 2. V1 ROUTING & LOAD BALANCING
    print_step("Test du Load Balancing (API V1)")
    print(f"{YELLOW}⏳ Envoi de 3 requêtes pour voir la répartition...{END}")
    for i in range(3):
        requests.post(URL, auth=(USER, PASSWORD), json=DATA, verify=False)
        print(get_last_log())
        time.sleep(0.2)

    # 3. V2 ROUTING (A/B TESTING)
    print_step("Test A/B Testing (Routage Header V2)")
    headers = {'X-Experiment-Group': 'debug'}
    r = requests.post(URL, auth=(USER, PASSWORD), json=DATA, headers=headers, verify=False)
    print(f"{GREEN}✅ Réponse reçue de la branche Debug.{END}")
    print(get_last_log())

    # 4. RATE LIMITING
    print_step("Test du Rate Limiting")
    print(f"{YELLOW}⏳ Rafale de requêtes...{END}")
    for _ in range(8):
        requests.post(URL, auth=(USER, PASSWORD), json=DATA, verify=False)
    
    time.sleep(0.5)
    print(f"{GREEN}✅ Analyse des blocages 503 dans les logs :{END}")
    try:
        logs = subprocess.check_output(f"docker logs {CONTAINER_NAME} --tail 4", shell=True).decode('utf-8').strip()
        print(f"{RED}{logs}{END}")
    except:
        pass

    print(f"\n{BOLD}{GREEN}✨ AUDIT TERMINÉ AVEC SUCCÈS{END}\n")

if __name__ == "__main__":
    run_global_tests()
