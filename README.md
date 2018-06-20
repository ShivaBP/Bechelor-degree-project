
Author:
Qi Li, Shiva Besharat Pour

Examinar:
Gerald Q. Maguire Jr.

Academic adviser:
Anders Västberg

Examin Insitutution:
KTH Royal Institute of Technology
School of Electrical Engineering and Computer Science (EECS))
Department of Communication Systems
Stockholm, Sweden


Project Outline:
Polls is the Connecting Silo application. The Connecting Silo project is build base on Under Professor Gerald Q. Maguire Jr toolbox. The source code for the toolbox can be found in KTH internal github. application bibutils_6.2_for_DiVA is a tool that can batch convert mods generate from Connecting Silo(folder polls) into bibtex. The application bibutils_6.2_for_DiVA is build base on Professor Gerald Q. Maguire Jr. from Royal Institute of Technology Sweden [1] 
Polls:
Name of the module will be changed later.....
Process Module: src/parse/kth_extract
Canvas RestAPI Operation: src/Canvas
DiVA Operation: src/Diva
KTH API:er : src/KTH
Output Data: output

bibutils_6.2_for_DiVA:
Main class:xml2bib_loop.py
Rest of the class and method information can be found under professor Gerald Q. Maguire Jr repositiory: https://github.com/gqmaguirejr/bibutils_6.2_for_DiVA [1] 

Install project requisition:
run './install_requisition.sh'
project is using python pip3,pip,conda,selenium, lxml and geckodriver for firefox
Project is build upon Django framwork
User need to configure config.json under 'polls/src/Canvas/canvas' and KTHconfig.json under 'polls/src/KTH' for the program to excecute properly
Under config.json user need to input oauth token and the address of the Canvas server.

General start up:
bibutils_6.2_for_DiVA:
python xml2bib_loop.py 'path of the output folder'
For this project the 'path of the output folder' is '../polls/output/parse_result' Polls:
The data in the thesis report is partially automated with module: test_accuracy.py 

DiVA location for thesis report:

Note:
Thesis: document_type = 0
Proporsal: document_type = 1


The project intended to serve the KTH - Royal Institute of Technology Sweden Canvas LMS. If user need to implement the program in the Canvas LMS that other Institute deployed, user might need to modify specific setting. The setting that need to modified is unknown.

[1]Jr, Gerald Q. Maguire. Bibutils_6.2_for_DiVA: A Version of Bibutils_6.2 for Use with DiVA. C, 2018. https://github.com/gqmaguirejr/bibutils_6.2_for_DiVA.
