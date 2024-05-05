
/**************************************************************
 * Modèle pour le problème du sudoku nxn
 * avec le niveau d'inférence simple pour la contrainte allDifferent
 * calculant toutes les solutions et affichant les statistiques
 * (donc parcours tout l'arbre de recherce)
 **************************************************************/
using CP;

// --- Parametrage Solveur ---
execute {
  // Configure le type de recherche pour être en profondeur d'abord (Depth-First Search).
  cp.param.searchType="DepthFirst";
  // Définit le nombre de threads de travail à 1 (ce qui signifie que la recherche est effectuée de manière séquentielle, sans parallélisme).
  cp.param.workers = 1;
  // Définit le niveau d'inférence pour la contrainte allDifferent sur "Basic", ce qui signifie que le niveau de filtrage le plus élémentaire sera utilisé.               
  cp.param.allDiffInferenceLevel = "Basic"; 
}

// --- Modèle ---
include "sudoku.mod";

