/*********************************************
 * Generic main bloc for computing and displaying all solutions
 * as well as the total number of solutions
 *********************************************/
 
/* Contrôle de Flux pour énumérer toutes les solutions

Here's a breakdown of what the code does:

1. `thisOplModel.generate();`: 

This line invokes the `generate` method on the current OPL model. 
The `generate` method typically compiles the OPL model, prepares the
data, and builds the optimization problem that is ready to be solved.

2. `cp.startNewSearch();`: 

This instructs the Constraint Programming (CP) solver to begin
a new search for solutions. CP solvers are used to solve combinatorial
problems where you want to satisfy a set of constraints.

3. `var solution = 0;`: Initializes a variable named `solution` to zero.
This variable is intended to count the number of solutions found.

4. `while (cp.next()) { ... }`: The `while` loop calls the `next` 
method on the CP solver object, which iterates over possible solutions.
Each time `next` returns `true`, it means a new solution has been found.

    - Inside the loop:
        - `writeln("Solution ", solution+1, ":");`: Prints the current solution number to the output.
        - `thisOplModel.postProcess();`: After each solution is found, `postProcess` is called,
        which is typically used to perform any required analysis or data manipulation based on the solution.
        - `solution++;`: Increments the solution counter.

5. `if (solution == 0) { ... }`: After the while loop, this `if` statement
checks if no solutions were found (i.e., `solution` is still 0). If this is
the case, it prints out a message saying "No solutions found."

6. `else { ... }`: If the `if` condition is not met (meaning at least one solution was found),
it prints out the total number of solutions found.

*/
 
main {
   // Affich enfant des résultats optimisé
     thisOplModel.generate();
     cp.startNewSearch();
     var nbSolution = 0; //init le compteur soluveur;
     while(cp.next()){
        nbSolution++; //increment de solutions
        writeln("Solution ", nbSolution, ": ============================");
        thisOplModel.postProcess();
    }
    if (nbSolution == 0) {
        writeln();
        writeln("No solutions were found.");
        writeln();
    }
    else{
        writeln();
        writeln("Number of solutions for the problem: ", nbSolution);
        writeln();
    }      
}
