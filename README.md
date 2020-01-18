# ASC
Directorio del 3º trabajo practico de la asignatura
## Primera Aproximación
En la primera implementacion del algoritmo con ZDT3 implemento la reproducción sin mutacion. Tras unas cuantas evaluaciones el algoritomo optimiza F1 bastante bien, pero no optimiza F2. Aqui una imagen de la primera y ultima iteraccion. 
<p align="center">
  <img width="460" height="300" src="https://i.ibb.co/B29RyT2/grafica-0.png">
  </br>
  Evaluacion de individuos aleatorios
</p>  
<p align="center">
  <img width="460" height="300" src="https://i.ibb.co/4fXw2Kj/grafica-100.png">
  </br>
  100 Generaciones
</p>
 
 ## Segunda Aproximación   
 En esta segunda aproximacion se usa la mutacion. En la primera cometi el error de usar directamente la combinacion de los 3 vectores vecinos, sin combinarlos con el indiciduo actual, al igual que solo utilizaba 3 vecinos. En esta se han subsanado dichos errores, pero no consigo que el algortiomo llegue al frente de pareto(PF.dat). La unicaforma de que este se acerque es dismuir la dimensionalidad del individuo 30 a 4.  
 
 <p align="center">
  <img width="460" height="300" src="https://i.ibb.co/3cshsPB/grafica-0.png">
  </br>
  Evaluacion de individuos aleatorios (Dimensionalidad 30)
</p>  
<p align="center">
  <img width="460" height="300" src="https://i.ibb.co/wYrgkxr/grafica-100.png">
  </br>
  100 Generaciones (Dimensionalidad 30)
</p>
 
 
 
 
 




