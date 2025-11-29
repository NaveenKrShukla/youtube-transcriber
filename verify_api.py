from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import sys

video_id = "U67mQO16xaE"

with open("verify_output_2.txt", "w") as f:
    try:
        api = YouTubeTranscriptApi()
        transcript_obj = api.fetch(video_id)
        
        f.write(f"Transcript object type: {type(transcript_obj)}\n")
        
        # Test to_raw_data
        try:
            raw_data = transcript_obj.to_raw_data()
            f.write(f"to_raw_data type: {type(raw_data)}\n")
            if isinstance(raw_data, list) and len(raw_data) > 0:
                f.write(f"First item in raw_data: {raw_data[0]}\n")
        except Exception as e:
            f.write(f"Error with to_raw_data: {e}\n")

        # Test TextFormatter with original object
        formatter = TextFormatter()
        try:
            f.write("Attempting TextFormatter.format_transcript(transcript_obj)...\n")
            formatted = formatter.format_transcript(transcript_obj)
            f.write(f"Formatter output (first 50 chars): {formatted[:50]}\n")
        except Exception as e:
            f.write(f"Error with TextFormatter(transcript_obj): {e}\n")
            
        # Test TextFormatter with raw_data
        if 'raw_data' in locals():
            try:
                f.write("Attempting TextFormatter.format_transcript(raw_data)...\n")
                formatted = formatter.format_transcript(raw_data)
                f.write(f"Formatter output (first 50 chars): {formatted[:50]}\n")
            except Exception as e:
                f.write(f"Error with TextFormatter(raw_data): {e}\n")

    except Exception as e:
        f.write(f"General error: {e}\n")
