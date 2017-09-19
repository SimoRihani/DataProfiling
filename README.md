# DataProfiling

 ## Synopsis

 Here are some Data Profiling scripts that aim to profile raw data, comput statistics in order to get insights of the selected Data.
 Based on one or a set of xls documents, in `Input/` directory, that contains catches of a table, which correspond to an activity history.  The main script generate an excel file with statistics in a record for each xls file, and with a label : Regular or Unregular.


 ## Motivation

 This project is part of the *M2 Miage ID* training at [Paris-Dauphine][] University, in particular for my final Thesis : How to make reliable the impacts on applications in interaction, following an evolution of a solution ?  https://mrihani.vvv.enseirb-matmeca.fr/donnee/memoireRIHANI.pdf      


 ## Deploy

 Make sure that you have **Python** (2.7) installed on your system. If not, please download it beforehand.  

 Clone DataProfiling with `git clone https://github.com/SimoRihani/DataProfiling.git`
 Save some files of Regular or Unregular label in `Ìnput/`directory (examples of input files are in the `Data/Regular/` and `Data/Unregular/` directories).

 Then run the following :

    cd DataProfiling/
    chmod +x *.sh
    ./clean.sh
    ./script.sh

 And follow instructions.

 ## License

 This project is licensed under the GNU LGPL, Version 3.0. See LICENSE for full license text.
 
 ## Useful links
 
- A demonstration of Data Progiling process : https://www.youtube.com/watch?v=DyV9JNdT1Q0&feature=youtu.be 
- A demonstration of a prediction of a profil by a trained model RapidMiner (Naive Bayes classifier) : https://www.youtube.com/watch?v=DK4asVZL42U&feature=youtu.be
- Repport : https://mrihani.vvv.enseirb-matmeca.fr/donnee/memoireRIHANI.pdf
- Presentation : https://mrihani.vvv.enseirb-matmeca.fr/donnee/soutenanceRIHANI.pdf

 ## Contributors

 ### Student

 - Mohammed *RIHANI* - Mohammed.Rihani@dauphine.eu

 ### Supervisor

 - Jamal *ATIF* - Jamal.Atif@dauphine.fr



 [Paris-Dauphine]: http://www.dauphine.fr/fr/index.html
