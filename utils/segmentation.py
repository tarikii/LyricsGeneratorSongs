import json

def segment_lyrics(transcription_text):
    try:
        # Parse the JSON string to extract the transcription text
        transcription_json = json.loads(transcription_text)
        transcription = transcription_json.get('transcription', '')

        # Split the transcription into individual words
        words = transcription.split()

        # Create the final segmented lyrics
        segmented_lyrics = []
        current_line = []

        # Iterate through the words and group them into 4-word lines
        for i, word in enumerate(words):
            current_line.append(word)

            # When we have 4 words, we add them as a new line and reset
            if len(current_line) == 4:
                segmented_lyrics.append(" ".join(current_line))
                current_line = []  # Reset for next line

            # Add two blank lines after every 4 lines (16 words)
            if (i + 1) % 16 == 0 and (i + 1) != len(words):
                segmented_lyrics.append("")  # First blank line
                segmented_lyrics.append("")  # Second blank line

        # Append any remaining words in the current line if there are any
        if current_line:
            segmented_lyrics.append(" ".join(current_line))

        return "\n".join(segmented_lyrics)  # Join all segments with newlines

    except Exception as e:
        print(f"Error in segmentation: {e}")
        raise
