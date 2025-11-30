from youtube_transcript_api import YouTubeTranscriptApi
import inspect

print("Checking YouTubeTranscriptApi methods and signature...")
try:
    # Check __init__ signature
    print(f"__init__ signature: {inspect.signature(YouTubeTranscriptApi.__init__)}")
except Exception as e:
    print(f"Could not get __init__ signature: {e}")

try:
    # Check fetch signature
    print(f"fetch signature: {inspect.signature(YouTubeTranscriptApi.fetch)}")
except Exception as e:
    print(f"Could not get fetch signature: {e}")

# Check if there's a specific method for cookies or if it's in the constructor
print(f"Dir of class: {dir(YouTubeTranscriptApi)}")
