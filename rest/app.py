import io
import os
import shutil
import subprocess
import time
import uuid

from flask import Flask, request, jsonify, send_file
import yaml
# from flask_migrate import Migrate

app = Flask(__name__)

from flask_cors import CORS, cross_origin

CORS(app)  # This will enable CORS for all routes

def load_config():
    try:
        with open('./config.yaml', 'r') as stream:
            config = yaml.safe_load(stream)
            return config
    except FileNotFoundError:
        raise Exception("config.yaml not found. Please create the file.")


# config = load_config()
#
# # Set up your database connection using the loaded configuration
# app.config[
#     'SQLALCHEMY_DATABASE_URI'] = f"postgresql://{config['db']['user']}:{config['db']['password']}@{config['db']['host']}:{config['db']['port']}/{config['db']['dbname']}"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#
# # Initialize SQLAlchemy
# from flask_sqlalchemy import SQLAlchemy
#
# db = SQLAlchemy(app)
#
# migrate = Migrate(app, db)


@cross_origin()
@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        # Get the uploaded files
        uploaded_files = request.files.getlist('images')
        session_id = request.form.get('sessionId')

        if session_id is None:
            session_id = 'session_' + time.strftime('%Y%m%d%H%M%S')

        data_folder = session_id
        data_path = '../data/' + data_folder + '/images'

        # Save the uploaded files (you can customize this logic)
        #  if data_path is not created, create it
        if not os.path.exists(data_path):
            os.makedirs(data_path)

        count = 1
        for file in uploaded_files:
            prefix = "00"
            if count < 10:
                prefix += "0"

            file_name = prefix + str(count) + '.jpg'
            with open(os.path.join(data_path, file_name), 'wb') as f:
                f.write(file.read())  # Corrected here

            count += 1

        return jsonify({"message": "Image(s) uploaded successfully", "sessionId": session_id}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@cross_origin()
@app.route('/processing/<session_id>', methods=['POST'])
def process_image(session_id):
    try:
        # Copy template config.yaml file to the session folder
        target_path = '../data/' + session_id + '/config.yaml'
        original_config_file = '../data/berlin/config.yaml'
        shutil.copyfile(original_config_file, target_path)

        # Run all the steps

        run_all_command = "../bin/opensfm_run_all ../data/" + session_id
        result = subprocess.run(run_all_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Check if the command was successful
        if result.returncode == 0:
            print("Run all successfully\n")
        else:
            print("Run all command failed")
            print(run_all_command)
            return jsonify({"error": "An error occured: " + result.stderr.decode()}), 500

        distort_command = "../bin/opensfm undistort ../data/" + session_id
        result = subprocess.run(distort_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Check if the command was successful
        if result.returncode == 0:
            print("Run distort successfully\n")
        else:
            print("Run distort failed")
            print(distort_command)
            return jsonify({"error": "An error occured: " + result.stderr.decode()}), 500

        depthmaps_command = "../bin/opensfm compute_depthmaps ../data/" + session_id
        result = subprocess.run(depthmaps_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Check if the command was successful
        if result.returncode == 0:
            print("Run depthmaps successfully\n")
        else:
            print("Run depthmaps failed")
            print(depthmaps_command)
            return jsonify({"error": "An error occured: " + result.stderr.decode()}), 500

        return jsonify({"ply_url": f"http://127.0.0.1:5000/ply/{session_id}?download=false"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@cross_origin()
@app.route('/ply/<session_id>', methods=['GET'])
def download_ply_file(session_id):
    try:
        file_path = '../data/' + session_id + '/undistorted/depthmaps/merged.ply'
        download = request.args.get('download', default='true', type=str)

        if download.lower() == 'true':
            # For demonstration, we'll serve it directly from memory
            return send_file(
                file_path,
                mimetype='application/octet-stream',
                as_attachment=True,
                download_name="result.ply",
            )
        else:
            with open(file_path, 'r') as file:
                data = file.read()
            return data
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
