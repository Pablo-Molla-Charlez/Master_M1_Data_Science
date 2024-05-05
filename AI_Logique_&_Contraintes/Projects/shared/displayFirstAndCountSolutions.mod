/*********************************************
 * Generic main bloc for displaying the first found solution 
 * and displaying the total number of solutions
 *********************************************/
 
main {
     //start generation
     thisOplModel.generate();
     if (!cp.solve()) {
        writeln("No solutions were found.");
     }
     // print the first solution
     writeln("First Solution:======================");
     thisOplModel.postProcess();
     writeln();
     //Begin to compute all solutions but do not print
     cp.startNewSearch();
     var nbSolution = 0; //init le compteur soluveur;
     while(cp.next()){
        nbSolution++; //increment de solutions
    }
  	 cp.endSearch();
  	 writeln("Number of solutions for the problem: ", nbSolution);
}

