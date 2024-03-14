# chatGPT-replicate

This project attempts to replicate chatGPT frontend and backend functionality using Django. 

## Set openAI API Key

Set your openAI API key as an environment variable:
```
export OPENAI_API_KEY=sk....111`
```

## Install conda environment

```
conda env create -f environment.yml
```

## Run Sever

```
cd chatGPT_replicate
python manage.py runserver
```

Go to http://127.0.0.1:8000/chatGPT/ to see application.
