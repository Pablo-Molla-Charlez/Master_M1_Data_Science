/**************************************************************
 * Modèle "pur" pour le problème du sudoku nxn
 * (i.e. sans "using CP;"
 *
 * (à inclure dans  un modèle contenant 
 * - l'entête "using CP;" 
 * - le paramétrage du solveur
 * - affichages des stats pour la stragégie
  **************************************************************/
// --- Données ---
// Taille du Sudoku
int n = ... ;             
int racine_n = ftoi(sqrt(n)); // square order
// Range lignes
range rsud = 1..n;

//// Instance de Sudoku
int instance[rsud][rsud] = ...;


// --- Pretraitement ---
// Decision variables
dvar int Case[rsud][rsud] in 1..n;


// --- Modèle ---

constraints {
  // Chaque chiffre doit apparaître une seule fois par ligne
  forall(i in 1..n)
    allDifferent(all(j in 1..n) Case[i][j]);
  
  // Chaque chiffre doit apparaître une seule fois par colonne
  forall(j in 1..n)
    allDifferent(all(i in 1..n) Case[i][j]);
  
  // Chaque chiffre doit apparaître une seule fois dans chaque bloc racine_n * racine_n
  forall(p in 1..racine_n, q in 1..racine_n)
    allDifferent(all(i in racine_n*p-racine_n+1..racine_n*p, j in racine_n*p-racine_n+1..racine_n*p) Case[i][j]);
  
  // Contraintes pour respecter les chiffres déjà donnés dans la grille
  forall(i in 1..n, j in 1..n: instance[i][j] != 0)
    Case[i][j] == instance[i][j];
}

// --- PostTraitement --- (affichage solution)
execute {
  writeln("Solution du Sudoku:");
  for(var i in rsud) {
    for(var j in rsud) {
      write(Case[i][j] + " ");
    }
    writeln();
  }
}