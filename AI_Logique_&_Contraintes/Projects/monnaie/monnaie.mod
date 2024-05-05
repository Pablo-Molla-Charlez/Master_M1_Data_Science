// ---------------- Variables et Domaines ----------------

// nb représente les nombre différent de monnaies 1, 2, 5, 10, 20 et 50 centimes
range nb = 0..5;

// maxValeur représente le nombre maximum de valeurs strictement inférieur à 1€ = 99 centimes
int maxValeur = 99;

// quantitePossible représente les domaines des 6 types de monnaies à considérer
// originalement chaque monnaie peut être prise une quantité de 0 à 99 fois, cependant on peut réduire les domaines pour accélerer le temps d'éxécution en ne considérant pas la grande majorité des cas qui sont innécessaires. Un domaine de 0..9 pour la quantité de fois de chaque pièce génère déjà plus de cas qu'on a besoin pour l'optimisation.
range quantitePossible = 0..9;

// valeurPossible représente toutes les possibles valeurs de 1 jusqu'à 99 qu'il faut considérer
range valeurPossible = 0..maxValeur;

// centimes représente les 6 valeurs différentes de chaque pièce
{int} centimes = {1, 2, 5, 10, 20, 50};

// minCombi est une variable de décision qui considère toutes les possibles combinaisons de quantité pour chacune des pièces
dvar int minCombi[centimes] in nb;

// nbPieceUtilise représente la matrice où les lignes sont les possibles valeurs et les colonnes les centimes. 
// Chaque cellule de la matrice est la quantité de fois qu'une certaine pièce est considérée
dvar int nbPieceUtilise[valeurPossible][centimes] in quantitePossible;


// ---------------- Contraintes et critère d'optimisation ----------------
// minCombi représente la variable à minimiser et correspond à la somme des quantités de pièces utilisée pour chaque monnaie
minimize sum(c in centimes) minCombi[c];

subject to {
   
   // Contrainte qui garantie que l'on utilise le minimum de pièces possibles
   forall(v in valeurPossible, c in centimes)
      nbPieceUtilise[v][c] <= minCombi[c];

  // Contrainte qui garantie que la somme du produit valeur et quantité pour chaque pièce vaut chacune des valeurs de 0 jusqu'à 99
  forall(v in valeurPossible)
     sum(c in centimes) (nbPieceUtilise[v][c] * c) == v;

  // Contrainte qui garantie que la combinaison ne dépasse pas 99
  sum(c in centimes)(c * minCombi[c])<= 99;
}