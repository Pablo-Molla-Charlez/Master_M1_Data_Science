using CP;

// ----------------- Données -----------------
int n = 8;
range taille = 1..n;
range diag = 2..(2*n);
range bool = 0..1;

// -------- Variables et domaines  ----------------

// Echequier de taille n
// Si case = 1 alors il y a une reine sur la case
dvar int Echiquier[taille][taille] in bool;

// -------- Parametrage Solveur ----------------  
execute {
  cp.param.searchType="DepthFirst";
  cp.param.workers = 1;
  cp.param.logPeriod = 100000;
  cp.param.logVerbosity = "Quiet";
}

// ----------------- Prétraitement -----------------

// Nombre de reine sur l'échiquier
dexpr int nbReine = sum (i, j in taille) Echiquier[i][j];

// Nombre de reine par ligne
dexpr int sumLigne[i in taille] = sum(j in taille) Echiquier[i][j];

// Nombre de reine par colonne
dexpr int sumCol[j in taille] = sum(i in taille) Echiquier[i][j];

// Nombre de reine par diagonale
dexpr int sumDiag[d in diag] = sum(i,j in taille : i + j == d) Echiquier[i][j];

// Nombre de reine par anti-diagonale
dexpr int sumADiag[d in diag] = sum(i,j in taille : i - j == d - n) Echiquier[i][j];

// ----------------- Modèle et critère d'optimisation -----------------
minimize nbReine;

subject to {
    forall(i, j in taille) {
        sumLigne[i] + sumCol[j] + sumDiag[i+j] + sumADiag[i - j + n]> 0;
    }
}
// ----------------- Postraitement (Affichage) -----------------
execute {
    writeln("Echiquier :")
    for (var i in taille) {
        for(var j in taille){
            if (Echiquier[i][j] == 1){
                write("X ");
            } else {
                write(". ");
            }

        }
        writeln();
    }
}