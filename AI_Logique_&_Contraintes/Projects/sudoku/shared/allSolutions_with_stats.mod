/******************************************************************
 * Generic main block for finding and post processing all solutions
 * of a problem and displaying search statistics.
 ******************************************************************/

 // Visualizing all solutions (to be included in a model)
main {
	var solNb = 0;
	thisOplModel.generate();
	cp.startNewSearch();
	while (cp.next()) {
	   	solNb++;
	    writeln("----------- Solution "+solNb+"-------------\n");
		thisOplModel.postProcess();	
	}
	writeln("No (more) solution\n");
	
	writeln("Solve Time : ", cp.info.solveTime);
	writeln("Nb Solutions : ", cp.info.numberOfSolutions);
	writeln("TotalTime : ", cp.info.TotalTime);
	writeln("NbOfFails : ", cp.info.numberOfFails);
}

 