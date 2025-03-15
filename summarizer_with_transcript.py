import os
import requests
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
from dotenv import load_dotenv

# Loading environment variables from `.env` file
load_dotenv()

# Load API keys from environment variables
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')  # Adjust model name as per documentation

def get_video_id(url):
    """Extract video ID from YouTube URL."""
    if 'youtube.com/watch?v=' in url:
        return url.split('v=')[1].split('&')[0]
    elif 'youtu.be/' in url:
        return url.split('youtu.be/')[1].split('?')[0]
    else:
        raise ValueError("Invalid YouTube URL")

def get_transcription(video_id):
    """Fetch transcription if available."""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        return ' '.join([item['text'] for item in transcript])
    except Exception as e:
        print(f"Transcription not available: {e}")
        return None

def summarize_transcription(text):
    """Summarize transcription using Gemini API."""
    task_prompt = """Analyze the text, understand it and create a comprehensize and detailed summary.
I expect you to give a brief summary first, then divide the text into sections, and explain each section.
At the end, provide key insights and quotations from the text and put them in different sections as well."""
    prompt = task_prompt + f': {text}'
    response = model.generate_content(prompt)
    return response.text

def get_comments(video_id, max_comments=100):
    """Fetch up to max_comments from YouTube API."""
    comments = []
    next_page_token = ''
    url_base = f'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={video_id}&key={YOUTUBE_API_KEY}&maxResults=100'
    while len(comments) < max_comments:
        url = f"{url_base}&pageToken={next_page_token}"
        response = requests.get(url).json()
        if 'items' not in response:
            break
        for item in response['items']:
            comments.append(item['snippet']['topLevelComment']['snippet']['textDisplay'])
            if len(comments) >= max_comments:
                break
        next_page_token = response.get('nextPageToken', '')
        if not next_page_token:
            break
    return comments[:max_comments]

def analyze_comments(comments):
    """Analyze comments using Gemini API."""
    comments_text = '\n'.join(comments)
    prompt = (
        f"Analyze these YouTube comments:\n{comments_text}\n\n"
        "Provide a summary of what most people are saying and list any insightful or thoughtful comments."
    )
    response = model.generate_content(prompt)
    return response.text

def main(video_url):
    """Main function to process the YouTube video."""
    try:
        # Extract video ID
        video_id = get_video_id(video_url)
        
        # Get and summarize transcription
        transcription = get_transcription(video_id)
        if transcription:
            print("\nTranscription Summary:")
            summary = summarize_transcription(transcription)
            print(summary)
        else:
            print("No transcription available. Speech-to-Text not implemented in this version.")

        # Fetch and analyze comments
        comments = get_comments(video_id)
        if comments:
            print("\nComments Analysis:")
            analysis = analyze_comments(comments)
            print(analysis)
        else:
            print("No comments found.")
            
    except Exception as e:
        print(f"Error: {e}")

# Example usage
if __name__ == "__main__":
    video_url = input("Enter YouTube video URL: ")
    main(video_url)
