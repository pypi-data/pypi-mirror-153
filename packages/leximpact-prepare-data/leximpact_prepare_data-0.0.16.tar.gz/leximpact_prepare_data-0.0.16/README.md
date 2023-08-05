# LexImpact Prepare Data



Ce projet regroupe les scripts permettant de préparer les données des différents projets [Leximpact](https://leximpact.an.fr).

## Schéma complet de préparation et d'utilisation des données
![LexImpact Pipeline](notebooks/schemas/leximpact_pipeline.png)


    
Le pipeline prepare-data est donc le suivant :

Input: erfs_flat_2018.h5

### 01_db_reduce.ipynb   
Objectif: Réduit le nombre de variables dans la base

Output: 01_erfs_reduced_2018.h5

### 02_db_enlarge.ipynb
Objectif: Ajoute des gens fictifs dans la base pour pouvoir calibrer


Output: 02_erfs_enlarged_2018.h5


### 03_db_add_rfr.ipynb
Input : CalibPote-2018-revkire.json

Objectifs: 
-	Calculer le RFR dans OpenFisca
-	Calibrer le RFR ERFS_2018 sur POTE_2018

Output: 03_erfs_rfr_2018.h5


### 04_db_add_var
0403_db_add_var_copules.ipynb

0401_db_add_var_copules-algo_monte-carlo.ipynb  


0402_db_add_var_copules-validate.ipynb

Input : ExportCopule-2018-variable.json

Objectif: Ajoute les variables issues de POTE 2018 dans la base ERFS 2018

Output:  04_erfs_var_copules_2018.h5


### 05_db_calib_var_copules.ipynb

Input : CalibPote-2019-variable.json

Objectifs: 
-	Vieillit la base ERFS_2018 vers 2019 (nos données les plus récentes) : inflation économique et inflation des foyers
-	Calibre chacune des variables issues de POTE sur POTE 2019

Output:  05_erfs_calibrated_ff_2018_to_2019.h5

### 06_db_aging_final.ipynb
Objectifs:

-	Vieillit la base ERFS_2019 vers 2021 (année voulue pour les calculs) : inflation économique et inflation des foyers
-	Bruitage statistique de la base pour anonymisation

Output: 06_erfs_ff_2018_aged_2021.h5

    

# How to contribute

Please see the [contributing page](https://documentation.leximpact.dev/leximpact_prepare_data/contributing).
