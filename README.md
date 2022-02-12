# Lancement
curl -L https://install.meilisearch.com | sh
lancer meilisearch : ./meilisearch
décommenter sur le fichier app.py (le recommenter après première utilisation) : 
cache = get_metadata_cache()
cache.populate()
pip install meilisearch 
pip install gutenberg
lancer py app.py 

# Si fail de l'installation sur WINDOWS de gutenberg
Si bsdd3 manquant : https://www.lfd.uci.edu/~gohlke/pythonlibs/#bsddb3 
Prendre le ficher avec la version de python courante (cpXX) et la version windows (ex : amd64 ou win32)
Puis pip install bsddb3‑6.2.9‑cp39‑cp39‑win_amd64.whl 



