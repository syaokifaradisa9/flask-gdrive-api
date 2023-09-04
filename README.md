# Flask Google Drive API

**Flask Google Drive API** is a Python-based web application that allows you to interact with Google Drive's API to perform various actions like creating folders, uploading files, searching for folders, and more. It provides a simple and user-friendly interface to manage your Google Drive files and folders programmatically.

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Endpoints](#endpoints)
- [Dependencies](#dependencies)
- [Contributing](#contributing)

## Features

- **Create Folders:** Easily create new folders in your Google Drive.
- **Search Folders:** Search for specific folders by name within a specified parent folder.
- **Rename Folders:** Rename existing folders in your Google Drive.
- **Upload Files:** Upload files (images, documents, etc.) to your Google Drive.
- **Download Files:** Download files from your Google Drive, including converting documents to images.
- **Delete Files:** Delete files from your Google Drive.

## Getting Started

Follow these instructions to set up and run the Flask Google Drive API project on your local machine.

### Prerequisites

- Python 3.7+
- Google Cloud Platform (GCP) API Credentials (OAuth 2.0)
- Flask, Pillow, python-dotenv, google-api-python-client, pymupdf, numpy (Install dependencies via `pip install -r requirements.txt`)

### Configuration

1. Clone this repository:
    ```
    git clone https://github.com/syaokifaradisa9/flask-gdrive-api.git
    ```
2. Create a `.env` file in the project root directory with the following content, replacing the placeholders with your GCP API credentials:
    ```
    CLIENT_ID='your-client-id'
    CLIENT_SECRET='your-client-secret'
    REFRESH_TOKEN='your-refresh-token'
    DEFAULT_PARENT_FOLDER_ID='your-default-parent-folder-id'
    ```
3. Install the project dependencies:
    ```
    pip install -r requirements.txt
    ```
4. Uncomment the following lines in app.py if you want to run the application in different modes:
    - To run the application locally with debugging enabled:
        ```
        if __name__ == '__main__':
            app.run(debug=True)
        ```
    
    - To run the application in production mode:
        ```
        application = app
        ```
5. Run the Flask application:
    ```
    python app.py
    ```
6. Access the application in your web browser at `http://localhost:5000`.

## Usage

- Visit the web application's homepage to get started.
- Use the provided endpoints to create, search, rename, upload, download, and delete folders and files in your Google Drive.
- Ensure that you have the required permissions and authentication set up in your Google Cloud Platform (GCP) project.

## Endpoints

- **GET `/`**: Homepage of the application.
- **POST `/create-folder`**: Create a new folder in Google Drive.
  - **Request Parameters**:
    - `folder_name` (string): Name of the new folder.
    - `parent_id` (string, optional): ID of the parent folder. If not provided, it will use the default parent folder.
  - **Response**:
    - `success` (boolean): Indicates whether the operation was successful.
    - `folderId` (string): ID of the newly created folder.
    - `message` (string): Confirmation message.
- **GET `/search-folder`**: Search for a folder by name within a specified parent folder.
  - **Request Parameters**:
    - `folder_name` (string): Name of the folder to search for.
    - `parent_id` (string, optional): ID of the parent folder to search within. If not provided, it will use the default parent folder.
  - **Response**:
    - `success` (boolean): Indicates whether the folder was found.
    - `folders` (array of objects): List of matching folders.
- **POST `/rename-folder`**: Rename an existing folder.
  - **Request Parameters**:
    - `folder_id` (string): ID of the folder to rename.
    - `new_folder_name` (string): New name for the folder.
  - **Response**:
    - `success` (boolean): Indicates whether the operation was successful.
    - `message` (string): Confirmation message.
- **POST `/upload-file`**: Upload a file to Google Drive.
  - **Request Parameters**:
    - `file_name` (string): Name of the file to upload.
    - `parent_id` (string, optional): ID of the folder where the file will be uploaded. If not provided, it will use the default parent folder.
  - **Request Data**:
    - `file` (file): The file to upload.
  - **Response**:
    - `success` (boolean): Indicates whether the operation was successful.
    - `fileId` (string): ID of the newly uploaded file.
    - `message` (string): Confirmation message.
- **GET `/get-file`**: Download a file from Google Drive.
  - **Request Parameters**:
    - `file_id` (string): ID of the file to download.
  - **Response**: The file is downloaded as a response.
- **GET `/download-file-as-image`**: Download a document as an image (e.g., PDF to PNG).
  - **Request Parameters**:
    - `file_id` (string): ID of the file to download as an image.
  - **Response**: The image is downloaded as a response.
- **POST `/delete-file`**: Delete a file from Google Drive.
  - **Request Parameters**:
    - `file_id` (string): ID of the file to delete.
  - **Response**:
    - `success` (boolean): Indicates whether the operation was successful.
    - `message` (string): Confirmation message.

## Dependencies

- numpy
- Pillow
- python-dotenv
- google-api-python-client
- pymupdf
- flask

For a complete list of dependencies and their versions, please refer to the `requirements.txt` file or you can run command
```
pip install -r requirements.txt
```

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these guidelines:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with clear, concise commit messages.
4. Push your changes to your fork.
5. Create a pull request with a detailed description of your changes.

---

**Flask Google Drive API** is developed and maintained by [Muhammad Syaoki Faradisa](https://github.com/syaokifaradisa9).

Enjoy managing your Google Drive programmatically with Flask Google Drive API!
