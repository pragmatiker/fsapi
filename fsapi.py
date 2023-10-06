#!/usr/bin/env python3
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Define the base directory
BASE_DIRECTORY = '/home/therty'

@app.route('/get_filenames', methods=['GET'])
def get_filenames():
    # Get the directory name from the request parameter 'directory'
    directory_name = request.args.get('directory')

    if directory_name is None:
        return jsonify({"error": "Directory parameter is missing"}), 400

    # Check if the provided directory contains path separators ('/' or '\')
    if '/' in directory_name or '\\' in directory_name:
        return jsonify({"error": "Subdirectories are not allowed"}), 400

    # Construct the full path by joining the base directory and the requested directory name
    directory_path = os.path.normpath(os.path.join(BASE_DIRECTORY, directory_name))

    # Check if the specified directory is within the allowed base directory
    if not directory_path.startswith(os.path.abspath(BASE_DIRECTORY)):
        return jsonify({"error": "Access to this directory is not allowed"}), 403

    # Check if the specified directory exists
    if not os.path.exists(directory_path):
        return jsonify({"error": "Directory not found"}), 404

    # List files in the specified directory
    filenames = os.listdir(directory_path)

    return jsonify({"filenames": filenames})

if __name__ == '__main__':
    app.run(debug=True)