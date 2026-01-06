import requests

# Configuration
USER = "admin"
PASSWORD = "admin"
# Notez le double /predict : le 1er pour Nginx, le 2ème pour la route FastAPI
URL = "https://localhost/predict/predict" 

requests.packages.urllib3.disable_warnings()

def test_prediction(name, group_header=None):
    print(f"--- Test : {name} ---")
    headers = {}
    if group_header:
        headers = {'X-Experiment-Group': group_header}
    
    # Donnée conforme au modèle Pydantic "Sentence" de votre main.py
    data = {"sentence": "Ceci est un test de cohérence"}

    try:
        response = requests.post(
            URL, 
            auth=(USER, PASSWORD), 
            json=data, 
            headers=headers, 
            verify=False
        )
        
        print(f"Statut: {response.status_code}")
        if response.status_code == 200:
            print(f"✅ Réponse API: {response.json()}")
        else:
            print(f"❌ Erreur: {response.text}")
    except Exception as e:
        print(f"💥 Erreur de connexion: {e}")
    print("-" * 30)

if __name__ == "__main__":
    test_prediction("API V1 (Standard)")
    test_prediction("API V2 (Debug)", group_header="debug")
