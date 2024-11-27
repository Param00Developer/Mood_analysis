# Mood_Analysis

## Description
Mood_Analysis is a Python-based project that analyzes mood scores based on activities and hours of sleep. The analysis is performed using aggregated data from various collections such as:

- **Mood**: Tracks mood scores.
- **Sleep**: Logs sleep hours.
- **Activity**: Records activities performed.
- **User**: Stores user data.

By correlating these factors, the project aims to provide insights into how sleep and activities affect overall mood.

## Libraries Used
The project relies on the following libraries:
- **Pymongo**: To interact with MongoDB for storing and retrieving data.
- **Pydantic**: For data validation and modeling.

## Setup Instructions
To set up the project locally, follow these steps:

### 1. Clone the repository
  First, clone the project repository to your local machine using Git:
  
  ```bash
  git clone https://github.com/Param00Developer/Mood_analysis
```
### 2. Navigate to the project directory
  Go to the directory where the project is located:
```bash
    >>cd Mood_Analysis
```
### 3. Install dependencies
  Install the required dependencies using pip:
```
    pip install -r requirements.txt
```
### 4. Set up environment variables
  You'll need to configure the environment variables for your project:
```
  Copy .env.example to .env:
  >>cp .env.example .env
```
  Open .env in a text editor and fill in the necessary values, such as database connection details for MongoDB.
### 5. Ensure MongoDB is running
  Make sure your MongoDB instance is up and running, and is accessible based on the configuration you provided in the .env file.
### 6. Run the application
   Finally, run the project using the following command:
```
  >>python main.py
```

## Usage
Once the project is running, it will start analyzing mood based on the aggregated data from the collections (Mood, Sleep, Activity, User). The output will provide insights into the relationship between mood, sleep, and activities through a Json file called as "output.json" which will be created inside the root folder.
