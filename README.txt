CSF NUMERIQUE - PROTOTYPE V2
============================

1) Installer Python 3.10 ou plus récent.
2) Ouvrir un terminal dans ce dossier.
3) Installer les dépendances :
   pip install -r requirements.txt
4) Lancer :
   streamlit run app.py
5) Ouvrir l'adresse locale affichée par Streamlit (souvent http://localhost:8501).

FONCTIONNALITES
- Interface rose et blanche.
- Langue française et arabe (RTL simplifié).
- Espaces Femme, Médecin, Sage-femme, Infirmier/ère, Administration.
- Création de dossiers fictifs.
- Consultations et suivi de grossesse.
- Vaccinations, dépistages, rendez-vous et documents.
- Base SQLite locale créée automatiquement.

IMPORTANT - LIMITES
Cette application est une maquette académique uniquement.
Ne saisissez aucune donnée personnelle ou médicale réelle.
Le choix du rôle est une simulation et non une authentification.
La base SQLite n'est pas chiffrée.
Avant tout usage réel : authentification robuste, contrôle d'accès serveur,
chiffrement en transit et au repos, sauvegardes, journalisation, gestion du
consentement, hébergement approprié, tests de sécurité et validation juridique
et réglementaire au Maroc sont indispensables.
Les champs et parcours médicaux doivent être validés par des professionnels
de santé et comparés au carnet officiel en vigueur.
