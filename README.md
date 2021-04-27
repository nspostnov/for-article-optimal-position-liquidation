This repository consists of the supplementary materials for the solution of optimal liquidation problem according to Almgren & Chriss' approach. 

The package was made using Python 3.8.2. All requirements are provided with the file requirements.txt. 

1. Create environment like 
```{python}
python -m venv env;\
. ./env/bin/activate;\
pip install -r requirements.txt;
```
2. Create .env file and add the password for db like 
```{bash}
ARTICLE_DB_PASSWORD=qwerty12345
```
3. Change the global variables in config file (config.py)

4. master.py solves the optimization problem.
5. Other .py files calculates the additional information for further analysis.
