Google Calendar and Drive Integration

This Python script allows you to interact with the Google Calendar and Google Drive APIs. It performs various tasks such as creating folders, renaming them, and managing events in Google Calendar.
Prerequisites

Before you can use this script, you need to set up the following prerequisites:

Google API Credentials:
---------------

To use the Google Calendar and Google Drive APIs, you need to create and download API credentials in the form of a JSON file. Here's how to do it:
    - Go to the Google API Console.
    - Create a new project or select an existing project.
    - In the project, go to the "APIs & Services" > "Library" section.
    - Search for "Google Calendar API" and "Google Drive API" and enable them for your project.
    - After enabling the APIs, go to the "APIs & Services" > "Credentials" section.
    - Click on "Create credentials" and select "OAuth client ID."
    - Choose "Desktop app" as the application type.
    - Give it a name, and then click "Create."
    - In the newly created OAuth 2.0 Client ID, click "Download" to download the JSON file that contains your API credentials.
    - Place this JSON file in the same directory as your Python script, and name it credentials.json. Make sure it's named exactly as specified to ensure the script can locate and use it.

Python Dependencies:
---------------
Ensure you have the required Python libraries installed. You can install them using pip:
    
```python
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

Folder ID:
---------------

You need to specify the parent folder ID in which the script will create subfolders on Google Drive. To find the ID of the parent folder, you can use the following code snippet:
```python
def get_folder_id_by_name(folder_name):
    results = drive_service.files().list(q=f"name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder'").execute()
    files = results.get('files', [])
    if files:
        return files[0]['id']
    else:
        return None

folder_name = "Mein Ordner"
folder_id = get_folder_id_by_name(folder_name)

if folder_id:
    print(f"The Folder '{folder_name}' has the ID: {folder_id}")
else:
    print(f"Der Ordner '{folder_name}' was not found.")
```
Replace "Mein Ordner" with the name of your desired parent folder. When you run this code, it will print the ID of the folder if found
This snippet has to be implemented in main.py after you have connected to the Google API Services

Usage:
---------------

Run the script:
```python
python main.py
```
The script will check for the existence of the token.json file, which stores your access and refresh tokens for Google APIs. If it doesn't exist or is no longer valid, it will initiate the authorization flow to generate a new one.

It fetches a list of subfolders in your Google Drive that are children of the specified parent folder.

It also retrieves a list of upcoming events from your Google Calendar.

The script then compares the list of folders and events and performs various operations:
It creates a folder for each event if it doesn't already exist in Google Drive.
It renames folders to [Veraltet] if they don't match any events.
If [Veraltet] folders already exist, it appends a number to them to create unique names.

The script runs in an infinite loop, checking for changes and updating folders as necessary.

Google API Scopes

The script uses the following Google API scopes:

    https://www.googleapis.com/auth/calendar.readonly for Google Calendar access.
    https://www.googleapis.com/auth/drive for Google Drive access.

License
---------------


This project is licensed under the MIT License - see the LICENSE file for details.
Acknowledgments
This script is based on the Google API Python Quickstart tutorial.
The Google API libraries are used for accessing Google Calendar and Drive.
