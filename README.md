# chatGPT-replicate

This project attempts to replicate chatGPT frontend and backend functionality using Django. 

<img width="1395" alt="image" src="https://github.com/j2moreno/chatGPT-replicate/assets/13912964/ed1be686-68d1-40e4-88a7-d5830f624af3">


## Goals

- [X] Have a conversational chatbox that will answer any question you have
  - [X] Create GPT4 API call to handle responses
  - [X] Display responses as conversational bubbles, similar to Apple's iMessage
- [X] Retain past conversations
- [X] Display all conversations on a left sidebar
  - [X] Add new conversations 
  - [X] If a conversation is selected, the conversation is displayed
  - [X] Ability to delete conversation
  - [X] Highlight active conversation

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
