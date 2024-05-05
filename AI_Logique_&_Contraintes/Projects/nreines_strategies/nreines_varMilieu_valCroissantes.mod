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

int middle = (n+1) div 2;

int scores[1..n];

// Each variable represents the column in which the queen of the corresponding row resides
dvar int Queens[values] in values;

execute{
  for(var i in values){
     scores[i] = Math.abs(i-middle);
    }
  var f = cp.factory ;
  cp.setSearchPhases (
    f.searchPhase(Queens,
            f.selectSmallest(f.explicitVarEval(Queens,scores)),
            f.selectSmallest(f.value()))
    );
  }

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
   writeln("Solve time:", cp.info.solveTime,"seconds");
   writeln("Number of fails: ", cp.info.numberOfFails);
   for(var i in values){
      writeln("Queen is in the ",i," row, "+Queens[i]+" column");
     }
  }

//include "../shared/displayFirstAndCountSolutions.mod";