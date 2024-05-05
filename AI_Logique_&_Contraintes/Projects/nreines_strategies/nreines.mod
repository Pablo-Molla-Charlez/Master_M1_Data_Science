/*********************************************
 * Modèle pour le problème des n-reines
 *
   Binôme : Chen Junjie
            Mollá Pablo
 
 *
 *********************************************/
using CP;
int n = ...;

/*** Données du problème  ***/
range values = 1..n;

// Each variable represents the column in which the queen of the corresponding row resides
dvar int Queens[values] in values;

/*** Contraintes  ***/
constraints{
  // Queens of different rows are not in the same column
  forall(i,j in values : i < j){
      Queens[i] != Queens[j];
  }
  //for diagonal, il n'existe pas different queens in the same column
  forall(i,j in values: i < j){
      abs(Queens[i] - Queens[j]) != abs(i - j);
  }          
} 

/*** Post-traitement  ***/
execute{
   for(var i in values){
      writeln("Queen is in the ",i," row, "+Queens[i]+" column");
     }
  }

include "../shared/displayFirstAndCountSolutions.mod";
