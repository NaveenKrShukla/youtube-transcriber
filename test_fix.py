from app import fetch_transcript
import sys

video_id = "U67mQO16xaE"

print(f"Testing fetch_transcript with video ID: {video_id}")
try:
    transcript = fetch_transcript(video_id)
    if "[Error fetching transcript" in transcript:
        print("FAILED: Error returned from fetch_transcript")
        print(transcript)
        sys.exit(1)
    else:
        print("SUCCESS: Transcript fetched successfully")
        print(f"Transcript length: {len(transcript)}")
        print(f"First 100 chars: {transcript[:100]}")
except Exception as e:
    print(f"FAILED: Exception raised: {e}")
    sys.exit(1)
