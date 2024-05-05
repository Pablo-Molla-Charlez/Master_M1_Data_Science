// Script bloc for displaying statistics from previous call to solve()
execute {
	writeln("Solve Time : ", cp.info.solveTime);
	writeln("TotalTime : ", cp.info.TotalTime);
	writeln("NbOfFails : ", cp.info.numberOfFails);
}

 