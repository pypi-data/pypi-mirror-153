# Skills Extraction Algorithm

## Development Environment
- Ubuntu 20.04
- Conda

## Project Structure
```
├── .dvc
│   ├── .gitignore 
│   └── config
├── .github
│   └── workflows
│       └── ci.yml
├── data
│   ├── .gitignore 
│   ├── apps_tools_alias.xlsx.dvc
│   ├── output_original_code.csv.dvc
│   ├── database.sqlite.dvc 
│   └── test_course_data.csv.dvc                    
├── src                
│   ├── __init__.py    
│   ├── utils.py 
│   ├── load_data.py
│   ├── process_data.py
│   └── extract_skills.py
├── tests                   
│   ├── test_load_data.py
│   ├── test_process_data.py
│   └── test_extract_data.py
├── .dvcignore
├── .gitignore
├── main.py
├── dvc.lock
├── dvc.yaml 
├── params.yaml 
├── dvc.yaml 
├── Procfile
├── Aptfile
├── runtime.txt
├── README.md
├── model_card.md
├── environment.yml
└── requirements.txt 
```

## Create Project Environment

Create Conda environment from yaml

`conda env create -f environment.yml`

Activate the project environment

`conda activate skills-extraction`

## Retrieval of Data/Model Artefact

1. Obtain the access right to the dvc remote repository (contact the dvc repo owner)
2. Execute `dvc pull` in the terminal

## Execute the Model Pipeline

Execute `dvc repro` in the terminal

## To run the API

Execute `python main.py` in the terminal