/* Modèle utilisant des variables de décision entières
   et ne prenant pas en compte les contraintes de consommation
*/



using CP;

// ----- Structures de données pour décrire une instance de problème -----

// Modélisation des informations caractérisant une tâche
tuple Tache{
    string code;     // le code de la tache
    int duree;        // la duree de la tache
    int puissance;      // la puissance consommee par la tache
}

// Modélisation des contraintes d'ordonnancement à respecter
tuple Ord{
   string avant;     // le code de la tache qui doit se derouler en premier
   string apres;     // le code de la tache qui doit se derouler en second    
}

//----------------------- Données ---------------------------
{Tache} taches = ...;        // les taches du probleme
{Ord}   cords = ...;       // les contraintes d'ordonnancement entre taches
int     puissanceMax = ...;   // la puissance maximale de l'usine

//----------------------- Pretraitement ---------------------------     
   
{string} codes = {t.code | t in taches}; // Extraction des codes de taches
int minDuree = min( t in taches )t.duree; // temps minimal des taches
int sumDuree = sum( t in taches )t.duree; // temps total des taches
int maxDuree = max( t in taches)t.duree;  // temps maximal des taches


//----------------------- Modèle ---------------------------

// -- variables de décisions --

dvar int debut[codes] in 0..(sumDuree - minDuree); // temps du début de chaque tâches

// -- variables de commodité --

dvar int fin[codes] in minDuree..sumDuree; // temps final de chaque tâches


minimize 
    max(c in codes) fin[c]; // Minimiser l'heure de fin de la derniere.

subject to {

     // la fin de chaque tache est le debut plus sa duree
     forall(t in taches){
       fin[t.code] == debut[t.code]+t.duree;
     }

     // Respecter les constraints d'ordonnancement specifiques
     forall(c in cords){
       fin[c.avant] <= debut[c.apres];
     }
    

    // Electrical consumption at each time unit must not exceed puissanceMax
    forall(i in 0..sumDuree) {
        sum(t in taches) ((i >= debut[t.code]) && (i < fin[t.code])) * t.puissance <= puissanceMax;
    }
}  


//----------------------- Affichage Solution ---------------------------

execute {
   writeln("Planning des taches");
   for(var c in codes){
      writeln("Tache ",c," commence à",debut[c]," et finit à ",fin[c]);
   }
}