from youtube_transcript_api import YouTubeTranscriptApi
import inspect

print(f"Type of YouTubeTranscriptApi: {type(YouTubeTranscriptApi)}")
print(f"Dir of YouTubeTranscriptApi: {dir(YouTubeTranscriptApi)}")

try:
    print("Attempting to call get_transcript...")
    # Test with the video ID from the error
    YouTubeTranscriptApi.get_transcript("U67mQO16xaE")
    print("Success!")
except AttributeError as e:
    print(f"AttributeError caught: {e}")
except Exception as e:
    print(f"Other error caught: {e}")
