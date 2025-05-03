# Wendy the Chatbot

## Database Local Set-Up Guide
### Download Dataset
Navigate to Kaggles' dataset called [Healful: Wearable Data vs Self-Reported QoL](https://www.kaggle.com/datasets/ppedroalmir/self-reported-qol).
Download the files called '20230120-data-collector-dailyRegister.csv', '20230120-data-collector-dailyStress.csv', '20230120-data-collector-participant.csv', '20230625-processed-physical-qol.csv'.
This chatbot focuses on the user's ID wearable device, and age. It also focuses on the height, weight, number of steps, calories, and amount of sleep. To lessen the amount of data stored in the database, filter out the columns that are not mentioned.
### Create SQL Database
Create a SQL Database using the code in the create-db.sql file. Then using SQL commands or the Import Table Wizard in MyMSQL Workbench, input the database from the csv files into the database.
### Edit Main.py
Currently, the file has a link with the password to my local database. Please change the password to your password for your database.

## Installation Guide
### Local LLM set-up
1. Download [Ollama For Mac](https://ollama.com/download/mac) or [Ollama For Windows](https://ollama.com/download/windows)
2. Once the download is complete, ensure that ollama is running by have the application open
3. In a terminal or command prompt window, run the command to download the llama3.2 model
   ```bash
   ollama pull llama3.2:3b
   ```
### Python virtual environment set-up
1. Create virtual environment
   ```bash
   python -m venv myenv
   ```
2. Activate the environment
   ```bash
   # on Windows
   myenv\Scripts\activate
   ```
   ```bash
   # on macOS and Linux
   source myenv/bin/activate
   ```
3. Install Requirements
   ```bash
   pip install -r requirements.txt
   ```
### Run the Program 
Run the main.py using the PyCharm or VSCode run button or use the python command in the terminal/command prompt
