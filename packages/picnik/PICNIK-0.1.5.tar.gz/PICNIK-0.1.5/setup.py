# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['picnik']
install_requires = \
['derivative>=0.3.1,<0.4.0',
 'matplotlib>=3.1.2,<4.0.0',
 'numpy>=1.19.1,<2.0.0',
 'pandas>=1.2.2,<2.0.0',
 'scipy>=1.6.3,<2.0.0']

setup_kwargs = {
    'name': 'picnik',
    'version': '0.1.5',
    'description': 'A package to make isoconversional computations for non-isothermal kinetics',
    'long_description': '# pICNIK \n\npICNIK is a module with implemented isoconversional computations for non-isothermal kinetcis.\\\nThe package has an object oriented interface with two classes: DataExtraction and ActivationEnergy, with the purpose of managing the experimental data and computing activation energies  with the next isoconversional methods: \n\n- Ozawa-Flynn-Wall (OFW)\\\n- Kissinger-Akahira-Sunose (KAS)\\ \n- Friedman (Fr)\\\n- Vyazovkin (Vy)\\\n- Advanced method of Vyazovkin (aVy)\\\n\n\nThe repository consist in the following directories:\n- picnik.py. Contains the package\n- examples. Contains a script (example.py) which executes some commmands of picnik in order to ilustrate the suggested procedure. And three more directories which contain data to use with example.py:\n    - Constant_E. Simulated TGA data for a process with constant activation energy.\n    - Two_Steps. Simulated TGA data for a process with two steps, each with constant activation energy.\n    - Variable_E. Simulated TGA data for a process with variable activation energy.\n\n\n### Installation\n\n`picnik` can be installed from PyPi with `pip`:\n`$ pip install picnik`\n\n\n### DataExtractioin class\n\nIt has methods to open the .csv files containing the thermogravimetric data as pandas DataFrames for the experimental data, computing and adding the conversion for the process and the conversion rate as columns in the DataFrame.\\\nThe class also has methods for creating isoconversional DataFrames of time, temperature, conversion rates (for the OFW, KAS, Fr and Vy methods) and also "advanced" DataFrames of time and temperature (for the aVy method).\\\nExample:\n\n    import picnik as pnk\n \n    files = ["HR_1.csv","HR_2.csv",...,"HR_n.csv"]\n    xtr = pnk.DataExtraction()\n    Beta, T0 = xtr.read_files(files,encoding)\n    xtr.Conversion(T0,Tf)\n    TDF,tDF,dDF,TaDF,taDF = xtr.Isoconversion(advanced=(bool))\n    \n    \nThe DataFrames are also stored as attributes of the `xtr` object \n\n\n### ActivationEnergy class\n\nThis class has methods to compute the activation energies with the DataFrames created with the `xtr` object along with its associated error. The `Fr()`,`OFW()`,`KAS()` methods return a tuple of three, two and two elements respectively. The first element of the tuples is a numpy array containing the isoconversional activation energies. The second element contains the associated error within a 95\\% confidence interval. The third element in the case of the `Fr()` method is a numpy array containing the intercept of the Friedman method. The `Vy()` and `aVy()` only return a numpy array of isoconversional activation energies, the error associated to this methods are obtained with the `Vy_error()` and `aVy_error()` methods\nExample:\n\n    ace = pnk.ActivationEnergy(Beta,\n                               T0,\n                               TDF,\n                               dDF,\n                               TaDF,\n                               taDF)\n    E_Fr, E_OFW, E_KAS, E_Vy, E_aVy = ace.Fr(), ace.OFW(), ace.KAS(), ace.Vy(), ace.aVy()\n    \nThe constructor of this class needs six arguments, a list/array/tuple of Temperature rates, a list/array of initial temperatures and four DataFrames: one of temperature, one of convertsion rates and two "advanced" one of temperature and the other of time.\n\n### Exporting results\n\nThe DataExtractionclass also has a method to export the results as .csv or .xlsx files:\n\n    xtr.export_Ea(E_Fr = (Bool), \n                  E_OFW = (Bool), \n                  E_KAS = (Bool), \n                  E_Vy = (Bool), \n                  E_aVy = (Bool),\n                  file_t="xlsx" )\n\nSet to True the method which values want to be exported. Set `file_t` to `xlsx` to export results as as an Excel spreadsheet or to `csv` to export results as a CSV file.\n\n\n\n',
    'author': 'ErickErock',
    'author_email': 'ramirez.orozco.erick@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ErickErock/pICNIK',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7.13,<3.10',
}


setup(**setup_kwargs)
