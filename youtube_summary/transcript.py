"""
Module for extracting transcripts from YouTube videos.
"""

import re
from typing import Dict, List, Optional, Union
from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(url: str) -> str:
    """
    Extract the video ID from a YouTube URL.
    
    Args:
        url: The YouTube URL to extract the ID from
        
    Returns:
        The extracted video ID
        
    Raises:
        ValueError: If the URL is not a valid YouTube URL
    """
    # Match patterns like:
    # - https://www.youtube.com/watch?v=VIDEO_ID
    # - https://youtu.be/VIDEO_ID
    # - https://youtube.com/watch?v=VIDEO_ID
    # - https://www.youtube.com/watch?v=VIDEO_ID&feature=share
    patterns = [
        r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/|youtube\.com/v/|youtube\.com/\?v=)([^&\n?#]+)',
        r'youtube\.com/shorts/([^&\n?#]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    raise ValueError(f"Could not extract video ID from URL: {url}")


def get_transcript(video_id_or_url: str, languages: List[str] = ['en']) -> List[Dict[str, Union[str, float]]]:
    """
    Get the transcript for a YouTube video.
    
    Args:
        video_id_or_url: Either a YouTube video ID or URL
        languages: List of language codes to try, in order of preference
        
    Returns:
        A list of transcript segments, each containing 'text', 'start', and 'duration' keys
        
    Raises:
        ValueError: If the transcript could not be retrieved
    """
    # Check if it's a URL or a video ID
    if 'youtube.com' in video_id_or_url or 'youtu.be' in video_id_or_url:
        video_id = extract_video_id(video_id_or_url)
    else:
        video_id = video_id_or_url
    
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
        return transcript
    except Exception as e:
        raise ValueError(f"Could not retrieve transcript: {str(e)}")


def get_transcript_text(video_id_or_url: str, languages: List[str] = ['en']) -> str:
    """
    Get the transcript for a YouTube video as a single string.
    
    Args:
        video_id_or_url: Either a YouTube video ID or URL
        languages: List of language codes to try, in order of preference
        
    Returns:
        The transcript as a single string
        
    Raises:
        ValueError: If the transcript could not be retrieved
    """
    transcript_segments = get_transcript(video_id_or_url, languages)
    return ' '.join([segment['text'] for segment in transcript_segments])
