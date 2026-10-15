# unipdFisppaIdentityResearch

## Setup

### Install and Setup Repository

You will need python3, brew, and pip3 installed on your computer

`git clone https://github.com/dhaberst/unipdFisppaIdentityResearch.git`

Next navigate to project folder

`cd unipdFisppaIdentityResearch`

Create the articles folder

`mkdir articles`

### Installing and using Ollama

Ollama (https://ollama.com/) is a service that allows the download and running of local models. In this case we will utilize a python library.

1. Install Ollama with Homebrew

`brew install ollama`

2. Start it as a background service

`brew services start ollama`

3. Download the models (will download to ~/.ollama/models)

`ollama pull gemma4:12b`
`ollama pull llama3.1:8b`
`ollama pull phi4-mini`

4. Finally install python libraries

`pip3 install -r requirements.txt`

## Run

1. First download the articles pulled from the TIPS platform and ensure it uses the proper format. It should contain atleast the following headers:

`Fulltext,Identifier,Date,Source Set,Title,URL`

The articles should be stored within this project under a the folder named `articles/`

The name of the file is used in the bodyPart column indicating where it was pulled from. ex format:

```
articles/
 - blood.csv
 - body.csv
 - brain.csv
 - digital.csv
 - dna_genes.csv
```

2. Now the main program can be run. It will first create, then populate the database. Then will start classifying articles that have not been completed yet.

use the following command to run:

`python3 main.py`

## Program Design

### Database design

We will utilize SQLite3 as a database to store article data / classifications

*Database schema*

| Column Name | SQLite Data Type | Description |
|---|---|---|
| `Id` | `INTEGER` | Primary key |
| `identifier` | `TEXT` | UUID identifying the article |
| `title` | `TEXT` | Article title |
| `url` | `TEXT` | Article URL |
| `date` | `TEXT` | Article publication date/time in ISO 8601 format |
| `fullText` | `TEXT` | Full article text |
| `source` | `TEXT` | Source or publisher of the article |
| `bodyPart` | `TEXT` | Body part where the articles were sourced by |
| `gemmaClassification` | `INTEGER` | Gemma classification result: 0, 1, or 2 |
| `llamaClassification` | `INTEGER` | Llama classification result: 0, 1, or 2 |
| `phiClassification` | `INTEGER` | Phi classification result: 0, 1, or 2 |
| `version` | `INTEGER` | Version number experiment |
