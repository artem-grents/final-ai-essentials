# AI Essentials course project
## HR Analytics

## Dataset

Data is from [kaggle](https://www.kaggle.com/datasets/anshika2301/hr-analytics-dataset?select=HR_Analytics.csv)

## Juptyer Notebook

`jupytext` and `pre-commit` is used to convert jupyter files to trackable file.

Commiting:

1. Convert your Jupyter changes to plain python files
```bash
pre-commit
```

Pulling:
1. Commit your local Jupyter changes. They will be lost during conversion from `.py` to `.ipynb`
2. Convert tracked `.py` to `.ipynb`
```bash
./convert_to_notebook.py
```

## Screenshot

![Screenshot](./assets/image.png)