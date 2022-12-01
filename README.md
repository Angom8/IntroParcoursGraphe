# IntroParcoursGraphe
Minicours de découverte au parcours de graphe par M.BOISSON

### Algorithme génétique pour la détermination d'un plus court chemin de parcours d'une liste de points / villes

On considère le "score" comme la somme des distances entre ville sur le parcours (la liste de villes).

Le code peut prendre en entrée tout fichier tsp (à condition évidemment qu'il respecte le format). Il a principalement été testé avec gr17, gr120, si535 et brasil.

Il y a 2 conditions de sortie :

    Arrivée à la dernière génération (500)
    Détermination par le quick mode.

Le quick mode détermine si les scores des populations se stabilisent, ou non. Par défaut, il regarde sur 10 générations avant d'arreter l'execution.

A la fin, une sortie écran affiche le nombre d'évaluations, le meilleur score et le parcours concerné. Toutes les informations des générations sont au fur et à mesure ajoutées dans un fichier .csv (par défaut, tsp_resultats.csv).
