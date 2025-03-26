"""
Command-line interface for the YouTube Summary tool.
"""

import os
import fire
from typing import Optional
from dotenv import load_dotenv

from youtube_summary.transcript import get_transcript_text
from youtube_summary.summarizer import summarize_text


def summarize(
    url: str,
    provider: Optional[str] = None,
    model: Optional[str] = None,
    max_length: Optional[int] = None,
    languages: Optional[str] = None,
    output_file: Optional[str] = None
) -> str:
    """
    Fetch a YouTube video transcript and summarize it.
    
    Args:
        url: YouTube video URL or video ID
        provider: LLM provider to use ('ollama', 'openai', 'anthropic')
        model: Model name to use with the provider
        max_length: Maximum word count for the summary
        languages: Comma-separated list of language codes to try (e.g., 'en,fr,es')
        output_file: Optional file path to save the summary
        
    Returns:
        The summarized transcript
    """
    # Load environment variables
    load_dotenv()
    
    print(f"Fetching transcript for: {url}")
    
    # Parse languages
    langs = ['en']
    if languages:
        langs = languages.split(',')
    
    # Get transcript
    transcript = get_transcript_text(url, languages=langs)
    print(f"Transcript fetched successfully ({len(transcript)} characters)")
    
    # Summarize transcript
    print(f"Summarizing transcript using {provider or os.getenv('SUMMARY_PROVIDER', 'ollama')} provider...")
    kwargs = {}
    if model:
        kwargs['model_name'] = model
    
    summary = summarize_text(transcript, provider_name=provider, max_length=max_length, **kwargs)
    
    # Save to file if requested
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(summary)
        print(f"Summary saved to {output_file}")
    
    return summary


def transcript(
    url: str,
    languages: Optional[str] = None,
    output_file: Optional[str] = None
) -> str:
    """
    Fetch a YouTube video transcript without summarizing.
    
    Args:
        url: YouTube video URL or video ID
        languages: Comma-separated list of language codes to try (e.g., 'en,fr,es')
        output_file: Optional file path to save the transcript
        
    Returns:
        The transcript text
    """
    # Load environment variables
    load_dotenv()
    
    print(f"Fetching transcript for: {url}")
    
    # Parse languages
    langs = ['en']
    if languages:
        langs = languages.split(',')
    
    # Get transcript
    transcript = get_transcript_text(url, languages=langs)
    print(f"Transcript fetched successfully ({len(transcript)} characters)")
    
    # Save to file if requested
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(transcript)
        print(f"Transcript saved to {output_file}")
    
    return transcript


def main():
    """Entry point for the CLI."""
    fire.Fire({
        'summarize': summarize,
        'transcript': transcript
    })


if __name__ == "__main__":
    main()
