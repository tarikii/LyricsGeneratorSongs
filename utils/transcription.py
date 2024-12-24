import whisper
import json

def transcribe_song(file):
    try:
        model = whisper.load_model("base")
        file_contents = file.read()
        
        # Save the file contents to a temporary file
        temp_filename = "temp_audio.wav"
        with open(temp_filename, 'wb') as f:
            f.write(file_contents)

        # Transcribe the audio file using Whisper
        result = model.transcribe(temp_filename)
        transcription_text = result['text']
        
        # Return as JSON format (if required by segment_lyrics)
        return json.dumps({'transcription': transcription_text}), 1  # Return the transcription as JSON
    except Exception as e:
        print(f"Error in transcription: {e}")
        raise
