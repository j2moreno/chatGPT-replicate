# chatGPT-replicate

This project attempts to replicate chatGPT frontend and backend functionality using Django. 

## Goals

- [X] Have a conversational chatbox that will answer any question you have
  - [X] Create GPT4 API call to handle responses
  - [X] Display responses as conversational bubbles, similar to Apple's iMessage
- [X] Retain past conversations
- [ ] Display all conversations on a left sidebar
  - [ ] If a conversation is selected, the conversation is displayed

### Stretch Goals 
- [ ] Have the ability to switch between GPT3.5 and GPT4
- [ ] Have the ability to provide documents to the chatbox 

## Set openAI API Key

Set your openAI API key as an environment variable:
```
export OPENAI_API_KEY='sk....111'
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
