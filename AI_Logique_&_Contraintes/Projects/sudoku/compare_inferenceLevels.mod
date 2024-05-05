/**************************************************************
 * Modèle pour comparer les performances de différentes niveaux
 * d'inférence sur la contrainte globale allDiffs sur différentes instances
 * sur diff
  **************************************************************/

// --- Données ---

// Ensemble des chemins vers les instances de sudoku à comparer
{string} instancesAComparer = ...;
	
// modèles à comparer (avec différentes niveaux d'inférence)
{string} modelesAComparer = ...;

// --- Prétraitement ---

// structures de données pour la synthèse des résultats


// nbEchec[i][m] représente le nombre d'échecs de l'arbre pour résoudre
// l'instance i avec le modèle m
int nbEchecs[instancesAComparer][modelesAComparer];

// tempsCPU[i][m] représente le temps CPU utilisé pour  résoudre
// l'instance i avec le modèle m
float tempsCPU[instancesAComparer][modelesAComparer];


// --- Bloc Main ---

main {
	// Pour chaque instance dans l'ensemble des instances à comparer
	for(var instance in thisOplModel.instancesAComparer) {
		// Affiche l'instance actuellement utilisée
    	writeln("Instance : ", instance);

    	// Crée une nouvelle source de données à partir de l'instance
    	var data = new IloOplDataSource(instance);  

    	// Pour chaque modèle dans l'ensemble des modèles à comparer
    	for(var modele in thisOplModel.modelesAComparer) {
    		// Affiche le modèle actuellement utilisé
        	writeln("Modèle : ", modele);  

        	// Crée une source de modèle OPL à partir du fichier modèle
        	var maSource = new IloOplModelSource( modele );

            // Définit un modèle OPL à partir de la source
        	var maDefinition = new IloOplModelDefinition( maSource );

        	// Crée une nouvelle instance de solveur de programmation par contraintes
        	var monCPSolver = new IloCP();

        	// Crée un modèle OPL en liant la définition du modèle et le solveur
        	var monModele = new IloOplModel( maDefinition, monCPSolver);  

        	// Ajoute la source de données au modèle
        	monModele.addDataSource(data);  

        	// Génère le modèle
        	monModele.generate();  

        	// Démarre une nouvelle recherche de solution
        	monCPSolver.startNewSearch();  

        	// Continue la recherche jusqu'à ce qu'il n'y ait plus de solution
        	while (monCPSolver.next()) {}  

        	// Enregistre le nombre d'échecs et le temps CPU pour l'instance et le modèle actuels dans les structures de données
        	thisOplModel.nbEchecs[instance][modele] = monCPSolver.info.numberOfFails;
        	thisOplModel.tempsCPU[instance][modele] = monCPSolver.info.TotalTime;

        	// Termine le modèle, le solveur et les sources pour libérer la mémoire
        	monModele.end();
        	monCPSolver.end();
        	maDefinition.end();
        	maSource.end();
    	}

    	// Termine la source de données de l'instance
    	data.end();
	}

	// Affiche les résultats dans un format tabulaire
	writeln();
	write("Instance                      |");  // Ajoute une en-tête pour les noms des instances

	// Imprime les en-têtes pour les modèles avec un formatage fixe pour aligner les colonnes
	for(var modele in thisOplModel.modelesAComparer) {
    	// Utilise un formatage pour aligner les noms des modèles et ajoute un espace pour séparer les colonnes
    	write("  " + modele + "(nbre/temps)       ");
	}
	writeln();  // Passe à la nouvelle ligne après les en-têtes

	// Imprime une ligne de séparation
	writeln("-----------------------------------------------------------------------------------------------------------------------------------------------");

	// Pour chaque instance, affiche les résultats
	for(var instance in thisOplModel.instancesAComparer) {
    	// Affiche l'instance avec un espacement fixe pour aligner toutes les entrées
    	write(instance + "      |");

    	// Pour chaque modèle, affiche le nombre d'échecs et le temps CPU
    	for(var modele in thisOplModel.modelesAComparer) {
       		// Formatte la sortie pour que chaque colonne soit alignée
        	var nbEchecs = thisOplModel.nbEchecs[instance][modele];
        	var tempsCPU = thisOplModel.tempsCPU[instance][modele];
        	var formattedResult = nbEchecs + "/" + tempsCPU;
        	write(formattedResult + "                     ");  
    }

    // Passe à la ligne suivante après chaque instance
    writeln();  
	}

}
