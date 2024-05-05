using CP;

// ----- Structures de données pour décrire une instance de problème -----

// Modélisation des informations caractérisant une tâche
tuple Tache{
    string code;        // le code de la tache
    int duree;          // la duree de la tache
    int puissance;      // la puissance consommee par la tache
}

// Modélisation des contraintes d'ordonnancement à respecter
tuple Ord{
   string avant;        // le code de la tache qui doit se derouler en premier
   string apres;        // le code de la tache qui doit se derouler en second   
}

// variable qui répresente le code et la duree 

tuple CodeDuree{
   string code;
   int duree;
}

//----------------------- Données ---------------------------
{Tache} taches = ...;        // les taches du probleme
{Ord}   cords = ...;       // les contraintes d'ordonnancement entre taches
int   puissanceMax = ...;   // la puissance maximale de l'usine

//----------------------- Pretraitement ---------------------------     
    
{string} codes = {t.code | t in taches}; // Extraction des codes de taches

int duree[ codes ] = [ t.code : t.duree | t in taches ]; //Extraction des durees de taches
int minDuree = min( t in taches )t.duree; // temps minimal des taches
int sumDuree = sum( t in taches )t.duree; // temps total des taches
int maxDuree = max( t in taches)t.duree;  // temps maximal des taches


//----------------------- Modèle ---------------------------


// -- variables de décisions --

// Utilisation de variables intervalles pour représenter les tâches
dvar interval itv_taches[c in codes] in 0..sumDuree size duree[c];

minimize
    max(c in codes) endOf(itv_taches[c]); // Minimiser l'heure de fin de la derniere tache

subject to {

     // Respecter les contraintes d'ordonnancement specifiques
     forall(c in cords)
         endBeforeStart(itv_taches[c.avant], itv_taches[c.apres]);
   
}  

//----------------------- Affichage Solution ---------------------------

execute {
   writeln("Planning des taches");
   for(var c in codes){
      writeln("Tache ", c, 
              " commence à ", Opl.startOf(itv_taches[c]), 
              " et finit à ", Opl.endOf(itv_taches[c]));
   }
}