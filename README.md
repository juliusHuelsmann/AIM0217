# Required software 
- Install python v.3 
- Install apache spark
- `(pip install  pyspark)` __might__ be used.
- Install the required pip packages. Attached you can find the pip packages
   installed  on this machine. Otherwise just have a look at the jupyter
notebook. `pip install []`.

```bash
appdirs==1.4.3
argh==0.26.2
attrs==17.3.0
bleach==2.1.1
click==6.7
cycler==0.10.0
decorator==4.1.2
entrypoints==0.2.3
gmpy==1.17
graphviz==0.8.1
html5lib==1.0b10
ipykernel==4.6.1
ipython==6.2.1
ipython-genutils==0.2.0
ipywidgets==7.0.3
jedi==0.11.0
Jinja2==2.10
jsonschema==2.6.0
jupyter==1.0.0
jupyter-client==5.1.0
jupyter-console==5.2.0
jupyter-core==4.3.0
louis==3.3.0
MarkdownPP==1.3
MarkupSafe==1.0
matplotlib==2.1.0
mistune==0.8
mxnet==0.11.0
nbconvert==5.3.1
nbformat==4.4.0
notebook==5.2.0
numpy==1.13.3
packaging==16.8
pandas==0.21.0
pandocfilters==1.4.2
parso==0.1.0
pathtools==0.1.2
pexpect==4.2.1
pickleshare==0.7.4
prompt-toolkit==1.0.15
ptyprocess==0.5.2
py4j==0.10.4
pycairo==1.15.4
pyfiglet==0.7.5
Pygments==2.2.0
pygobject==3.26.1
pygraphviz==1.4rc1
pyparsing==2.2.0
pyPEG2==2.15.2
pyspark==2.2.0
python-dateutil==2.6.1
pytz==2017.3
PyYAML==3.12
pyzmq==16.0.2
qtconsole==4.3.1
qutebrowser==1.0.4
ranger==1.8.1
scikit-learn==0.19.1
scipy==1.0.0
simplegeneric==0.8.1
six==1.11.0
sklearn==0.0
team==1.0
termdown==1.12.1
terminado==0.6
testpath==0.3.1
tornado==4.5.2
traitlets==4.3.2
watchdog==0.8.3
wcwidth==0.1.7
webencodings==0.5.1
widgetsnbextension==3.0.6
```
-  Optional (like that's already provided by pip) 
   `sudo pacman -S jupyter-notebook` or `sudo apt-get install jupyter-notebook`
or ..

# 1 Some results ...
... can be found inside  the [`00_documentation`](00_documentation) folder.



# 1 Exploring data
01_exploreData/Sports - Data exploration generation and inital analys.ipynb  contains 
our initial exploration analysis on the sports dataset. Download and setup
instructions are provided. The referenced python script containing code is
located in the same directory.  


## 1.  Exploration and data gathering
1. Download the [Dataset](https://archive.ics.uci.edu/ml/datasets/Daily+and+Sports+Activities)
and unpack it, move the content of the `data` folder into [01_exploreData/raw/sports](01_exploreData/raw/sports) directory. 

### a) Do you want to have a look on our data exploration? 
1. launch the jupyter notebook, open the file
2. Execute at least the loading of the data and the export of the data to be
   used by spark. 

### b) otherwise
`./quickSetup.sh`



## 2.  spark 

In case you'd like to be able to execute the entire analysis (including
selection of k), execute
```bash
cd 02_pyspark/ 
./bulkscript.sh
```
Otherwise there will be errors (file not found) for some visualizations.

```bash
cd 02_pyspark
spark-submit main2.py
```      
And launch the [jupyter notebook (Analyser.ipynb)](02_pyspark/Analyser.ipynb) in `02_pyspark`.


