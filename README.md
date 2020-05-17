# elisa-do-little

### Requirements

This should run off linux, mac and windows but I have only tested it in windows subsytem for linux.

1. Some version of conda, I recommend Miniconda3. Can be downloaded from [here](https://docs.conda.io/en/latest/miniconda.html)
2. A plate plan excel file named "*plateID*-pplan.xlsx". See 'template-pplan.xlsx' as an example.
3. A plate reader file saved in ".xlsx" format named "*plateID*-preader.xlsx" . Our plate reader will generate an ".xls" file which will not work so you need to make this change manually with 'save as'

### Install elisa-dl 

1. Clone this repository and ``cd elisa-dl``
2. ``conda env create -f environment.yml``

If you get an error message related to wkhtmltopdf then:
1. Download it manually from [here](https://wkhtmltopdf.org/downloads.html)
2. Open the environment.yml file with any text editor. I recommend [notepad++](https://notepad-plus-plus.org/downloads/v7.8.6/).
3. Delete the line '- wkhtmltopdf=0.12.3' and save the file.
4. Retry ``conda env create -f environment.yml``


### Running elisa-dl

1. For now you have to be with in the elisa-dl directory
2. ``conda activate elisa-dl``
3. ``python elisa_dl.py plateID``
5. You can do a test run with ``python elisa_dl.py test``
6. Onced finished ``conda deactivate`` to exit the environment

### Output
This should automatically generate a report named *plateID*.pdf to inspect the standard curve and see the sample concentrations.
