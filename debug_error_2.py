from youtube_transcript_api import YouTubeTranscriptApi
import sys

with open("debug_output.txt", "w") as f:
    f.write(f"Type: {type(YouTubeTranscriptApi)}\n")
    f.write(f"Dir: {dir(YouTubeTranscriptApi)}\n")
    try:
        import youtube_transcript_api
        f.write(f"Module file: {youtube_transcript_api.__file__}\n")
    except:
        pass
