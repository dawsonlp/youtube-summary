from youtube_transcript_api import YouTubeTranscriptApi

# Example video ID from the URL you provided
video_id = "TdAAUoJ065o"

try:
    # Get the transcript
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    
    # Print the transcript
    for line in transcript:
        print(f"{line['start']}-{line['start'] + line['duration']}: {line['text']}")
    
    # Alternatively, get the transcript as a single string
    transcript_text = ' '.join([line['text'] for line in transcript])
    print("\nFull transcript as a single string:")
    print(transcript_text)
    
except Exception as e:
    print(f"An error occurred: {e}")
