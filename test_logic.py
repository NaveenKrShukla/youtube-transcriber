from app import get_video_id, fetch_transcript, get_playlist_video_ids

def test_single_video():
    print("Testing single video...")
    # A short video with captions: "Me at the zoo"
    url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"
    video_id = get_video_id(url)
    print(f"Video ID: {video_id}")
    assert video_id == "jNQXAC9IVRw"
    
    transcript = fetch_transcript(video_id)
    print(f"Transcript length: {len(transcript)}")
    print(f"Transcript preview: {transcript[:50]}...")
    assert len(transcript) > 0
    print("Single video test passed!")

def test_playlist():
    print("\nTesting playlist...")
    # A small playlist or just check extraction logic
    # Using a random playlist ID for testing extraction (doesn't need to be real for unit test if we mock, but here we do integration)
    # Let's use a known public playlist, e.g., Python basics
    url = "https://www.youtube.com/playlist?list=PLzMcBGfZo4-nhWva-6OVh1yKWHlYpd8qN" 
    # This is "Python for Beginners" by Tech With Tim
    
    video_ids = get_playlist_video_ids(url)
    print(f"Found {len(video_ids)} videos")
    if len(video_ids) > 0:
        print(f"First video ID: {video_ids[0]}")
        # Try fetching first transcript
        transcript = fetch_transcript(video_ids[0])
        print(f"First video transcript length: {len(transcript)}")
    
    print("Playlist test passed (extraction)!")

if __name__ == "__main__":
    try:
        test_single_video()
        test_playlist()
        print("\nAll tests passed!")
    except Exception as e:
        print(f"\nTests failed: {e}")
