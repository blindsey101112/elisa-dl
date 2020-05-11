# elisa-do-little

### Requirements

This should run off linux, mac and windows but I have only tested it in windows subsytem for linux.

1. Some version of conda, I recommend Miniconda3. Can be downloaded from [here](https://docs.conda.io/en/latest/miniconda.html)
2. A plate plan excel file named "*plateID*-pplan.xlsx". See 'template-pplan.xlsx' as an example.
3. A plate reader file saved in ".xlsx" format named "*plateID*-preader.xlsx" . Our plate reader will generate an ".xls" file which will not work so you need to make this change manually with 'save as'

### Install elisa-dl 

1. Clone this repository and ``cd elisa-dl``
2. ``conda env create -f environment.yml``

### Running elisa-dl

1. For now you have to be with in the elisa-dl directory
2. ``conda activate elisa-dl``
3. ``python elisa_dl.py plateID``
4. ``conda activate elisa-dl``
5. You can do a test run with ``python elisa_dl.py test``

### Output
This should automatically generate a report named *plateID*.pdf to inspect the standard curve and see the sample concentrations.
