# elisa-do-little

### Requirements

This should run off linux, mac and windows but I have only tested it in windows subsytem for linux.

1. Some version of conda, I recommend Miniconda3. Can be downloaded from [here](https://docs.conda.io/en/latest/miniconda.html)
2. A plate plan excel file named "*plateID*-pplan.xlsx". See 'template-pplan.xlsx' as an example.
3. A plate reader file saved in ".xlsx" format named "*plateID*-preader.xlsx" . Our plate reader will generate an ".xls" file which will not work so you need to make this change manually with 'save as'
4. You can add an optional ignore file if you want to exclude certain wells from the analysis. See the example in the directory for an example

### Install elisa-dl 

1. Clone this repository and ``cd elisa-dl``
2. ``conda env create -f environment.yml``

If you get an error message related to wkhtmltopdf then:
1. Download it manually from [here](https://wkhtmltopdf.org/downloads.html)
2. Open the environment.yml file with any text editor. I recommend [notepad++](https://notepad-plus-plus.org/downloads/v7.8.6/).
3. Delete the line '- wkhtmltopdf=0.12.3' and save the file.
4. Retry ``conda env create -f environment.yml``
5. If this stil does not work then you can exclude the pdf generation using the command below


### Running elisa-dl

1. Make sure you are within the elisa-dl directory ``cd elisa-dl``
2. ``conda activate elisa-dl``
3. ``python elisa_dl.py plateID antigen include-pdf std-curve pos-neg-method`` In place of 'antigen' type "s", "n", "n2" for Spike, Nucleoprotein, Nuceloprotein2 (accepted alternative for "n" is "N-Spec" and "N-Sens" in place of "n2"). In place of include-pdf type "yes" or "no". In place of std-curve type "hero" or "who-s" or "who-n". There are 2 options for the positive/negative sample call "index" or "conc". 
5. You can do a test run with ``python elisa_dl.py test``
6. Onced finished ``conda deactivate`` to exit the environment

### Output
1. *plateID*.pdf to inspect the standard curve and see the sample concentrations. 
2. *plateID*.html in html_reports/
3. *plateID*.csv with the result in csv format

### Important considerations
Re-running the script with the same plateID will overwrite any previously generated files in the elisa-dl directory with the same filename. So if you have modified the input files in someway and want to generate a second report move the report to another directory before running the script.
