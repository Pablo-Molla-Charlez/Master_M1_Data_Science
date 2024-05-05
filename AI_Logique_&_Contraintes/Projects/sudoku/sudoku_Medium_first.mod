/**************************************************************
 * Modèle pour le problème du sudoku nxn
 * avec le niveau d'inférence avanccé pour la contrainte allDifferent
 * calculant la première solution et affichant les statistiques
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

// --- Main (pour trouver la première solutions + statistiques) ---
include "shared/stats.mod";
