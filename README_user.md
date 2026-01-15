Ce projet explique comment nous avons transformé une API de Machine Learning en un service robuste, sécurisé et capable de tenir la charge.

Étape 1 : Assurer la disponibilité (Le Load Balancing)
En production, on ne peut pas compter sur un seul serveur. Si l'un tombe, tout s'arrête.
Ce qu'on a fait : Nous avons lancé 3 copies de notre API (V1).
Le rôle de Nginx : Il agit comme un chef d'orchestre. Chaque nouvelle requête est envoyée à un serveur différent (Round-Robin). Si un serveur est surchargé, les autres prennent le relais.

Étape 2 : Sécuriser les échanges (SSL & Auth)
Un modèle de ML peut contenir des données sensibles ou être coûteux à utiliser. Il faut le protéger.
Le Verrou (Authentification) : Seuls ceux qui ont le mot de passe (admin) peuvent demander une prédiction.
Le Tunnel (SSL) : Nous avons activé le HTTPS. Même si quelqu'un intercepte la communication, il ne pourra pas lire le texte envoyé au modèle.

Étape 3 : Tester sans casser (A/B Testing)
Nous avons  testé une nouvelle version du modèle (V2) sans risquer de tout couper pour les utilisateurs.

Le Header magique : Nous avons configuré Nginx pour lire les "étiquettes" des requêtes.
Le résultat : Si vous ajoutez X-Experiment-Group: debug à votre demande, Nginx vous envoie vers la V2. Sinon, vous restez sur la V1 stable. C'est transparent pour l'utilisateur.

Étape 4 : Éviter l'explosion (Le Rate Limiting)
Calculer une prédiction demande beaucoup de puissance (CPU). 
Le serveur peut se bloquer lors de l'envoie de milliers de messages.
C'est pourquoi Nous avons limité le nombre de requetes par seconde.

Si l'on dépasse cette limite, Nginx bloque la requête immédiatement avec une erreur 503 (Service Indisponible).
L'API ne "voit" même pas l'attaque tout en restant disponible pour les autres.

Étape 5 : Vérifier que tout fonctionne (L'Audit)
Pour prouver que l'installation est parfaite, nous avons créé un script de test automatique.
Pour lancer les tests il suffit d'exécuter la commande suivante sur le serveur : Make test
