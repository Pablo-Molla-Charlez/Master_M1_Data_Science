/**************************************************************
 * Modèle pour le problème du sudoku nxn
 * avec le niveau d'inférence avancé pour la contrainte allDifferent
 * calculant toutes les solutions et affichant les statistiques
 * (donc parcours tout l'arbre de recherce)
 **************************************************************/
using CP;

// --- Parametrage Solveur + niveau d'inférence alldiff---
execute {
  // Configure le type de recherche pour être en profondeur d'abord (Depth-First Search).
  cp.param.searchType="DepthFirst";
  // Définit le nombre de threads de travail à 1 (ce qui signifie que la recherche est effectuée de manière séquentielle, sans parallélisme).
  cp.param.workers = 1;
  // Définit le niveau d'inférence pour la contrainte allDifferent sur "Medium", ce qui signifie que le niveau de filtrage est élaboré que le "Basic", mais pas plus que "Extended"          
  cp.param.allDiffInferenceLevel = "Medium"; 
}

// --- Modèle ---
include "sudoku.mod";

// (statistiques)  
include "shared/allSolutions_with_stats.mod";

