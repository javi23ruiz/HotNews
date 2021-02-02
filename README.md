# CompanyTracker
The goal of the project is to retrieve scattered news of a company on the web using Google News API. The project is developed with the Flask web framework. 

## Motivation of the project.
Nowadays there are a wide range of different sources of information. If an individual is interested in a particular company, he/she has to search for a vast number of sources to get an idea of what is going on with the company. However, with this solution a user can receive a summary of the top news within seconds. Therefore, less time will be spent on googling news articles, everything will be sent to you right away by executing this application. 

## Features of the project.

1. **Mail Sender**: Module to send an email to a user with the links of the news including a summary (applying NLP techniques), source of the news, date published and an image if found in teh article. 
2. **Podcast generator**: Module to generate a .mp3 file with the audio of the summary of the news. You can listen to the audio and download it. 
3. The News are generated using **Google News API**: HTTP REST API for searching and retrieving articles all over the web. The free version is implemented in this application, therefore you can only go back in time one month. The articles are ranked by relevancy and by default the application returns 8 articles. A keyword must be specified by the user to search for that specific company.
4. **Word Cloud**: A wordcloud graph is generated with the most common words retrieved from the news articles. 
5 **Text Summarization**: The text of every article is summarized and displayed for the user
6. **Sentiment Analysis**: Once the news are retrieved, a sentiment analysis model will determine the sentiment of the headline. It can either be positive, neutral or negative. 


## Installation

**Conda (Recommended):**
```bash
# 1. Open Anaconda prompt or a command line 

# 2. Crear a new virtual environment
conda create --name MyNewEnvName

# 3. Activate the environment
conda activate MyNewEnvName

# 4. Install all the required libraries in conda
conda install --file requirements.txt
```

## SET-UP

## TESTS 
Describe and show how to run the tests with code examples.


## Contributing 
Pull requests are welcome. For major changes, please open an issue first to discuss the implementation of your new feature. 

Please make sure to update tests as appropriate

## License 

??


