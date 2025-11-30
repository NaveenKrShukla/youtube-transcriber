import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import yt_dlp
import re
import time

# Set page configuration
st.set_page_config(
    page_title="YouTube Transcriber",
    page_icon="📝",
    layout="centered"
)

# Custom CSS for styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        padding: 10px;
        font-size: 16px;
    }

    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background: linear-gradient(45deg, #FF0000, #FF5E5E);
        color: white;
        font-weight: 600;
        border: none;
        padding: 12px;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(255, 0, 0, 0.3);
    }

    .stTextArea textarea {
        font-family: 'Courier New', Courier, monospace;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
    }

    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f1f1f1;
        color: #555;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        border-top: 1px solid #ddd;
        z-index: 1000;
    }
    
    /* Dark mode adjustment for footer */
    @media (prefers-color-scheme: dark) {
        .footer {
            background-color: #0e1117;
            color: #aaa;
            border-top: 1px solid #333;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def get_video_id(url):
    """Extracts the video ID from a YouTube URL."""
    # Examples:
    # https://www.youtube.com/watch?v=VIDEO_ID
    # https://youtu.be/VIDEO_ID
    # https://www.youtube.com/embed/VIDEO_ID
    
    # Simple regex for video ID
    video_id_match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    if video_id_match:
        return video_id_match.group(1)
    return None

def get_playlist_video_ids(url):
    """Extracts all video IDs and titles from a playlist URL using yt-dlp."""
    ydl_opts = {
        'extract_flat': True,
        'quiet': True,
        'ignoreerrors': True,
    }
    
    videos = []
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            if 'entries' in info:
                for entry in info['entries']:
                    if entry and 'id' in entry:
                        videos.append({
                            'id': entry['id'],
                            'title': entry.get('title', 'Unknown Title')
                        })
        except Exception as e:
            st.error(f"Error extracting playlist: {e}")
            return []
            
    return videos

def fetch_transcript(video_id):
    """Fetches the transcript for a single video ID."""
    try:
        api = YouTubeTranscriptApi()
        transcript_list = api.fetch(video_id)
        formatter = TextFormatter()
        text_transcript = formatter.format_transcript(transcript_list)
        return text_transcript
    except Exception as e:
        # Return error message as string to be included in final output
        return f"[Error fetching transcript for video {video_id}: {str(e)}]"

def main():
    st.title("📝 YouTube Transcriber")
    st.write("Generate transcripts for YouTube videos, playlists, and live streams.")

    url = st.text_input("Enter YouTube Video or Playlist URL:", placeholder="https://www.youtube.com/watch?v=...")

    if st.button("Transcribe"):
        if not url:
            st.warning("Please enter a URL.")
            return

        progress_bar = st.progress(0)
        status_text = st.empty()
        
        full_transcript = ""
        
        # Check if it's a playlist
        if "list=" in url:
            status_text.text("Processing playlist...")
            videos = get_playlist_video_ids(url)
            
            if not videos:
                st.error("Could not find any videos in the playlist.")
                return
            
            total_videos = len(videos)
            st.info(f"Found {total_videos} videos in playlist.")
            
            for i, video in enumerate(videos):
                video_id = video['id']
                title = video['title']
                
                status_text.text(f"Transcribing video {i+1}/{total_videos}: {title}...")
                transcript = fetch_transcript(video_id)
                
                # Append to full transcript for download
                full_transcript += f"\n\n--- Video {i+1}: {title} ({video_id}) ---\n\n{transcript}"
                
                # Display in expander
                with st.expander(f"{i+1}. {title}"):
                    st.text_area("Transcript", value=transcript, height=200, key=f"transcript_{i}")
                
                progress_bar.progress((i + 1) / total_videos)
                
        else:
            # Single video
            status_text.text("Processing single video...")
            video_id = get_video_id(url)
            
            if not video_id:
                st.error("Invalid YouTube URL. Could not extract video ID.")
                return
            
            transcript = fetch_transcript(video_id)
            full_transcript = transcript
            progress_bar.progress(100)

        status_text.text("Transcription complete!")
        
        # Display Output
        st.subheader("Transcript")
        st.text_area("Copy your transcript here:", value=full_transcript, height=300)
        
        # Download Button
        st.download_button(
            label="Download Transcript (.txt)",
            data=full_transcript,
            file_name="transcript.txt",
            mime="text/plain"
        )

if __name__ == "__main__":
    main()
