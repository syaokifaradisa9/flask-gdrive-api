import os
import io
import numpy as np
import mimetypes
from PIL import Image
from dotenv import load_dotenv
import sys, fitz
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from flask import Flask, jsonify, request, send_file, Response

app = Flask(__name__)

def get_gdrive_service():
    load_dotenv()
    
    creds = None
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    refresh_token = os.getenv("REFRESH_TOKEN")
    
    creds = Credentials.from_authorized_user_info(info={
        'client_id': client_id, 
        'client_secret': client_secret, 
        'refresh_token': refresh_token
    })
    
    return build('drive', 'v3', credentials = creds)

@app.route('/')
def index():
    return 'Flask Google Drive API | Created by Muhammad Syaoki Faradisa'

@app.route('/create-folder', methods=['POST'])
def create_folder():
    try:
        # folder_name parameter as new folder name in google drive
        folder_name = request.form.get('folder_name', '')
        if not folder_name:
            return jsonify({"message" : "folder_name parameter doesn't exist!!"})
            
        # parent_id parameter as new folder location in googel drive
        parent_id = request.form.get('parent_id', os.getenv("DEFAULT_PARENT_FOLDER_ID"))

        # Searching for folder
        query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed = false and '{parent_id}' in parents"
        response = get_gdrive_service().files().list(q=query, fields='files(id, name)').execute()
        folders = response.get('files', [])

        # check the folder, is already exists in the parent id?
        if len(folders) > 0:
            return jsonify({'error': f"A folder with name '{folder_name}' already exists in the parent folder."})

        # Metadata Folder
        file_metadata = {
            'name': folder_name, 
            'mimeType': 'application/vnd.google-apps.folder', 
            'parents': [parent_id]
        }
        
        # Creating folder
        folder = get_gdrive_service().files().create(
            body=file_metadata, 
            fields='id'
        ).execute()
        
        # Return response
        return jsonify({
            'success': True,
            'folderId': folder.get("id"),
            'message': f"Folder with name {folder_name} has been created!"
        })
    except HttpError as error:
        return jsonify({'success': False, 'error': f'An error occurred: {error}'})

@app.route('/search-folder', methods=['GET'])
def find_folder():
    try:
        # folder_name parameter as the name of the folder you want to search
        folder_name = request.args.get('folder_name', '')
        if not folder_name:
            return jsonify({"message": "folder_name parameter doesn't exist!!"})
        
        # parent_id parameter to search for folder in a specified parent folder
        parent_id = request.args.get('parent_id', os.getenv("DEFAULT_PARENT_FOLDER_ID"))

        # Query for search folder
        query = "mimeType='application/vnd.google-apps.folder' and trashed = false and name = '{}' and parents in '{}'".format(folder_name, parent_id)
        response = get_gdrive_service().files().list(q=query, fields='files(id, name)').execute()
        folders = response.get('files', [])
        
        # Return response
        if not folders:
            return jsonify({'success': False, 'message': 'No folder found with name {} in parent folder {}'.format(folder_name, parent_id)})
        else:
            return jsonify({'success': True, 'folders': folders})
    except HttpError as error:
        return jsonify({'error': f'An error occurred: {error}'})

@app.route('/rename-folder', methods=['POST'])
def rename_folder():
    try:
        # parent_id paramater as which folder you want to rename
        folder_id = request.form.get('folder_id', os.getenv("DEFAULT_PARENT_FOLDER_ID"))
        if not folder_id:
            return jsonify({"message" : "folder_id parameter doesn't exist!!"})
        
        # new_folder_name parameter as new folder name you want to rename
        new_folder_name = request.form.get('new_folder_name', '')
        if not new_folder_name:
            return jsonify({"message" : "new_folder_name parameter doesn't exist!!"})
        
        # Get folder metadata
        folder_metadata = get_gdrive_service().files().get(
            fileId=folder_id, 
            fields='name'
        ).execute()

        # Change folder name
        folder_metadata['name'] = new_folder_name
        get_gdrive_service().files().update(
            fileId=folder_id, 
            body=folder_metadata, 
            fields='id'
        ).execute()
        
        # Return response
        return jsonify({
            'success': True,
            'message': f"Folder with id {folder_id} has been renamed to {new_folder_name}!"
        })
    except HttpError as error:
        return jsonify({'error': f'An error occurred: {error}'})

@app.route('/upload-file', methods=['POST'])
def upload_file():
    folder_name = "files/uploads_to_drive"
    
    try:
        # name_file parameter as the name of the file you want to save
        file_name = request.form.get('file_name', '')
        if not file_name:
            return jsonify({"message" : "file_name parameter doesn't exist!!"})
            
        # parent_id parameter as the location where the file will be placed
        parent_id = request.form.get('parent_id', os.getenv("DEFAULT_PARENT_FOLDER_ID"))
        
        # file parameter as the file you want to upload, it can be image, document, or other.
        file = request.files.get('file', None)
        if not file:
            return jsonify({"message" : "file parameter doesn't exist!!"})
        
        # Make uploads folder in flask project
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        file.save(os.path.join(folder_name, file.filename))

        # Create media file upload
        media = MediaFileUpload(f"{folder_name}/{file.filename}", resumable=True)
        
        # Upload File from local flask to google drive
        file_metadata = {'name': file_name, 'parents': [parent_id]}
        uploaded_file = get_gdrive_service().files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        
        # Return response back
        return jsonify({
            'success': True,
            'fileId': uploaded_file.get("id"),
            'message': f"File with name {file_name} has been uploaded!",
        })
    except HttpError as error:
        return jsonify({'error': f'An error occurred: {error}'})
        
@app.route('/get-file', methods=['GET'])
def get_file():
    folder_name = "files/download_from_drive"
    
    try:
        # file_id parameter as id file you want to download
        file_id = request.args.get('file_id', '')
        if not file_id:
            return jsonify({"message" : "file_id parameter doesn't exist!!"})
        
        # Get file from Google Drive
        file = get_gdrive_service().files().get(fileId=file_id).execute()

        # Get the file content
        content = get_gdrive_service().files().get_media(fileId=file_id).execute()

        # Create the folder if it doesn't exist in flask
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
    
        # Determine the file extension if doesn't exist
        file_extension = mimetypes.guess_extension(file['mimeType'])
        file_name = file_id
        if file_extension not in file_name:
            file_name = f"{file_name}{file_extension}"
    
        # Define the file path
        file_path = os.path.join(folder_name, file_name)
        
        # Write the file content to the target path
        with io.BytesIO(content) as fh:
            with open(file_path, 'wb') as f:
                fh.seek(0)
                f.write(fh.read())
        
        # Determine the file extension for download if doesn't exist
        download_file_name = file['name']
        if file_extension not in download_file_name:
            download_file_name = f"{download_file_name}{file_extension}"
            
        # Send the file as a download response
        return send_file(file_path, download_name = download_file_name)
    except HttpError as error:
        return jsonify({'error': f'An error occurred: {error}'})

@app.route('/download-file-as-image', methods=['GET'])
def download_file_as_image():
    folder_name = "files/file_as_image"
    try:
        # file_id parameter as id file you want to download
        file_id = request.args.get('file_id', '')
        if not file_id:
            return jsonify({"message" : "file_id parameter doesn't exist!!"})
        
        # Get file from Google Drive
        file = get_gdrive_service().files().get(fileId=file_id).execute()

        # Get the file content
        content = get_gdrive_service().files().get_media(fileId=file_id).execute()

        # Create the target folder if it doesn't exist
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
    
        # Determine the file extension if it doesn't exist
        file_extension = mimetypes.guess_extension(file['mimeType'])
        file_name = file_id
        if file_extension not in file_name:
            file_name = f"{file_name}{file_extension}"
    
        # Define the file path in local flask project
        file_path = os.path.join(folder_name, file_name)
        
        # Write the file content to the target path
        with io.BytesIO(content) as fh:
            with open(file_path, 'wb') as f:
                fh.seek(0)
                f.write(fh.read())
            
        # Open the document and convert pages to images
        doc = fitz.open(file_path)
        image_file_paths = []
        dpi_factor = 125 / 72
        for page in doc: 
            image_file_path = os.path.join(folder_name, f"{file_name}_{page.number}.png")
            pix = page.get_pixmap(matrix=fitz.Matrix(dpi_factor, dpi_factor))
            pix.save(image_file_path)
            image_file_paths.append(image_file_path)
        
        # Prepare the combined image
        download_file_name = f"{file['name']}.png"
        image_combine_path = f"{folder_name}/{file_id}.png"
        images = [Image.open(i) for i in image_file_paths]
        min_shape = sorted( [(np.sum(i.size), i.size ) for i in images])[0][1]
        imgs_comb = np.hstack([i.resize(min_shape) for i in images])
        imgs_comb = np.vstack([i.resize(min_shape) for i in images])
        imgs_comb = Image.fromarray(imgs_comb)
        
        # Save the combined image
        imgs_comb.save(image_combine_path)
        
        # Send the combined image as a download response
        return send_file(image_combine_path, download_name = download_file_name)
    except HttpError as error:
        return jsonify({'error': f'An error occurred: {error}'})

@app.route('/delete-file', methods=['POST'])
def delete_file():
    try:
        # file_id parameter as the file want you to delete
        file_id = request.form.get('file_id', '')
        if not file_id:
            return jsonify({"message" : "file_id parameter doesn't exist!!"})

        # Delete the file from Google Drive
        get_gdrive_service().files().delete(fileId=file_id).execute()

        # Send response back
        return jsonify({
            'success': True,
            'message': f"File with ID {file_id} has been deleted!"
        })
    except HttpError as error:
        return jsonify({'error': f'An error occurred: {error}'})

# Uncomment if you want run into local
# if __name__ == '__main__':
#     app.run(debug = True)
    
# Uncomment if you want run into production
# application = app