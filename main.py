from flask import Flask, jsonify, request, render_template, send_file
import os
import traceback

from utils import preprocess_song, transcribe_song, segment_lyrics, format_lyrics

app = Flask(__name__)
UPLOAD_FOLDER = './data/uploads/'
RESULT_FOLDER = './data/results/'

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    
    try:
        # Save the uploaded file to a temporary location
        input_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(input_path)

        # Preprocess the song (e.g., convert to WAV if needed)
        preprocessed_file = preprocess_song(input_path)  # Pass the file path to preprocessing
        
        # Open the preprocessed file and pass to transcription
        with open(preprocessed_file, 'rb') as f:
            transcription = transcribe_song(f)  # Pass the open file to transcription
        
        # Extracting the transcription text from the tuple
        transcription_text = transcription[0]  # Get the transcription content
        
        # Segment the lyrics
        segments = segment_lyrics(transcription_text)
        formatted_segments = format_lyrics(segments)   # Optional: format the segments
    
        # Save the formatted segments to a file
        result_filename = 'generated_lyrics.txt'
        result_filepath = os.path.join(RESULT_FOLDER, result_filename)

        with open(result_filepath, 'w', encoding='utf-8') as f:
            f.write(formatted_segments)


        # Check if the file exists before returning the download URL
        if os.path.exists(result_filepath):
            download_url = f'/download/{result_filename}'
            return jsonify({'download_url': download_url}), 200

    except Exception as e:
        # Log the full stack trace for debugging
        error_message = str(e)
        print(f"Error occurred: {error_message}")
        print(traceback.format_exc())
        return jsonify({'error': 'An error occurred during processing.'}), 500



@app.route('/download/<filename>')
def download_file(filename):
    filepath = os.path.join(RESULT_FOLDER, filename)
    
    # Check if the file exists
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    else:
        return "File not found", 404


if __name__ == "__main__":
    app.run(debug=True)
