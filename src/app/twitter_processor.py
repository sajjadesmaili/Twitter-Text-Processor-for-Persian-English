#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Twitter Text Processor for Persian/English Texts
===============================================

A comprehensive text processing library for Twitter data that handles:
- Persian text normalization
- Link extraction and removal
- Hashtag extraction (Persian/English)
- Mention extraction
- Emoji extraction
- Language detection and classification

Author: Sajjad Esmaili with by AI Assistant
Version: 1.0.0
"""

import re
import unicodedata
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class ProcessingConfig:
    """Configuration class for text processing options."""
    
    normalize_persian: bool = True
    extract_links: bool = True
    extract_hashtags: bool = True
    extract_mentions: bool = True
    extract_emojis: bool = True
    detect_language: bool = True
    lang_threshold: float = 50.0  # Threshold for Persian language classification


class TwitterTextProcessor:
    """
    Main class for processing Twitter texts with Persian and English content.
    
    This processor handles various aspects of text cleaning and feature extraction
    from Twitter data, with special attention to Persian language characteristics.
    """
    
    def __init__(self, config: Optional[ProcessingConfig] = None):
        """
        Initialize the Twitter text processor.
        
        Args:
            config (ProcessingConfig, optional): Configuration for processing steps.
                                               If None, default config is used.
        """
        self.config = config or ProcessingConfig()
        
        # Compile regex patterns for better performance
        self._compile_patterns()
        
        # Persian and English character sets for language detection
        self.persian_chars = set('آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی')
        self.english_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
    
    def _compile_patterns(self):
        """Compile regex patterns for efficient text processing."""
        
        # Link patterns - comprehensive URL matching
        self.link_pattern = re.compile(
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
            r'|www\.(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
            r'|(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}(?:/\S*)?'
        )
        
        # Hashtag patterns - supports Persian and English
        self.hashtag_pattern = re.compile(r'#[\u0600-\u06FFa-zA-Z0-9_]+')
        
        # Mention pattern
        self.mention_pattern = re.compile(r'@[a-zA-Z0-9_]+')
        
        # Emoji pattern - comprehensive Unicode emoji ranges
        self.emoji_pattern = re.compile(
            r'[\U0001F600-\U0001F64F]|'  # emoticons
            r'[\U0001F300-\U0001F5FF]|'  # symbols & pictographs
            r'[\U0001F680-\U0001F6FF]|'  # transport & map symbols
            r'[\U0001F1E0-\U0001F1FF]|'  # flags (iOS)
            r'[\U00002702-\U000027B0]|'  # dingbats
            r'[\U000024C2-\U0001F251]'   # enclosed characters
        )
        
        # Persian normalization patterns
        self.arabic_to_persian = {
            'ي': 'ی',  # Arabic Yeh to Persian Yeh
            'ك': 'ک',  # Arabic Kaf to Persian Kaf
        }
        
        # Half-space normalization pattern
        self.half_space_pattern = re.compile(r'\u200C+')
    
    def normalize_persian(self, text: str) -> str:
        """
        Normalize Persian text by fixing half-spaces and converting Arabic characters.
        
        Args:
            text (str): Input text to normalize
            
        Returns:
            str: Normalized Persian text
        """
        if not self.config.normalize_persian:
            return text
        
        # Convert Arabic characters to Persian
        for arabic, persian in self.arabic_to_persian.items():
            text = text.replace(arabic, persian)
        
        # Normalize half-spaces (Zero Width Non-Joiner)
        # Replace multiple consecutive half-spaces with single half-space
        text = self.half_space_pattern.sub('\u200C', text)
        
        # Add proper half-spaces before common Persian suffixes
        persian_suffixes = ['های', 'ها', 'تان', 'تون', 'شان', 'شون', 'مان', 'مون']
        for suffix in persian_suffixes:
            # Add half-space before suffix if not already present
            pattern = f'(?<!\u200C){suffix}'
            replacement = f'\u200C{suffix}'
            text = re.sub(pattern, replacement, text)
        
        return text.strip()
    
    def extract_links(self, text: str) -> Tuple[List[str], str]:
        """
        Extract all links from text and return cleaned text.
        
        Args:
            text (str): Input text containing links
            
        Returns:
            Tuple[List[str], str]: (list of extracted links, text without links)
        """
        if not self.config.extract_links:
            return [], text
        
        links = self.link_pattern.findall(text)
        clean_text = self.link_pattern.sub('', text).strip()
        
        # Remove extra whitespaces
        clean_text = re.sub(r'\s+', ' ', clean_text)
        
        return links, clean_text
    
    def extract_hashtags(self, text: str) -> Tuple[List[str], List[str], str]:
        """
        Extract hashtags and classify them as Persian or English.
        
        Args:
            text (str): Input text containing hashtags
            
        Returns:
            Tuple[List[str], List[str], str]: (Persian hashtags, English hashtags, clean text)
        """
        if not self.config.extract_hashtags:
            return [], [], text
        
        hashtags = self.hashtag_pattern.findall(text)
        hashtags_fa = []
        hashtags_en = []
        
        for hashtag in hashtags:
            # Remove # symbol for classification
            hashtag_text = hashtag[1:]
            
            # Count Persian and English characters
            persian_count = sum(1 for char in hashtag_text if char in self.persian_chars)
            english_count = sum(1 for char in hashtag_text if char in self.english_chars)
            
            # Classify based on character count
            if persian_count > english_count:
                hashtags_fa.append(hashtag)
            else:
                hashtags_en.append(hashtag)
        
        # Remove hashtags from text
        clean_text = self.hashtag_pattern.sub('', text).strip()
        clean_text = re.sub(r'\s+', ' ', clean_text)
        
        return hashtags_fa, hashtags_en, clean_text
    
    def extract_mentions(self, text: str) -> Tuple[List[str], str]:
        """
        Extract all mentions (@username) from text.
        
        Args:
            text (str): Input text containing mentions
            
        Returns:
            Tuple[List[str], str]: (list of mentions, text without mentions)
        """
        if not self.config.extract_mentions:
            return [], text
        
        mentions = self.mention_pattern.findall(text)
        clean_text = self.mention_pattern.sub('', text).strip()
        clean_text = re.sub(r'\s+', ' ', clean_text)
        
        return mentions, clean_text
    
    def extract_emojis(self, text: str) -> Tuple[List[str], str]:
        """
        Extract all emojis from text.
        
        Args:
            text (str): Input text containing emojis
            
        Returns:
            Tuple[List[str], str]: (list of emojis, text without emojis)
        """
        if not self.config.extract_emojis:
            return [], text
        
        emojis = self.emoji_pattern.findall(text)
        clean_text = self.emoji_pattern.sub('', text).strip()
        clean_text = re.sub(r'\s+', ' ', clean_text)
        
        return emojis, clean_text
    
    def detect_language(self, text: str) -> Tuple[int, int, float, str]:
        """
        Detect language composition and classify text as Persian or English.
        
        Args:
            text (str): Input text for language detection
            
        Returns:
            Tuple[int, int, float, str]: (Persian word count, English word count, 
                                        Persian percentage, language classification)
        """
        if not self.config.detect_language:
            return 0, 0, 0.0, 'unknown'
        
        # Split text into words
        words = text.split()
        
        fa_word_count = 0
        en_word_count = 0
        
        for word in words:
            # Remove punctuation for better analysis
            clean_word = re.sub(r'[^\u0600-\u06FFa-zA-Z]', '', word)
            
            if not clean_word:
                continue
            
            # Count Persian and English characters in the word
            persian_chars_in_word = sum(1 for char in clean_word if char in self.persian_chars)
            english_chars_in_word = sum(1 for char in clean_word if char in self.english_chars)
            
            # Classify word based on dominant character type
            if persian_chars_in_word > english_chars_in_word:
                fa_word_count += 1
            elif english_chars_in_word > 0:
                en_word_count += 1
        
        total_words = fa_word_count + en_word_count
        
        if total_words == 0:
            return 0, 0, 0.0, 'unknown'
        
        percent_fa = (fa_word_count / total_words) * 100
        
        # Classify based on threshold
        lang_class = 'fa' if percent_fa >= self.config.lang_threshold else 'en'
        
        return fa_word_count, en_word_count, percent_fa, lang_class
    
    def process_tweet(self, tweet_text: str) -> Dict[str, any]:
        """
        Process a complete tweet through all enabled processing steps.
        
        Args:
            tweet_text (str): Raw tweet text
            
        Returns:
            Dict[str, any]: Dictionary containing all processed data with columns:
                          clean_text, links, hashtags_fa, hashtags_en, mentions, 
                          emojis, fa_word_count, en_word_count, percent_fa, lang_class
        """
        # Step 1: Persian normalization
        processed_text = self.normalize_persian(tweet_text)
        
        # Step 2: Extract links
        links, processed_text = self.extract_links(processed_text)
        
        # Step 3: Extract hashtags
        hashtags_fa, hashtags_en, processed_text = self.extract_hashtags(processed_text)
        
        # Step 4: Extract mentions
        mentions, processed_text = self.extract_mentions(processed_text)
        
        # Step 5: Extract emojis
        emojis, processed_text = self.extract_emojis(processed_text)
        
        # Step 6: Language detection
        fa_word_count, en_word_count, percent_fa, lang_class = self.detect_language(processed_text)
        
        # Step 7: Final cleanup
        clean_text = re.sub(r'\s+', ' ', processed_text).strip()
        
        return {
            'clean_text': clean_text,
            'links': links,
            'hashtags_fa': hashtags_fa,
            'hashtags_en': hashtags_en,
            'mentions': mentions,
            'emojis': emojis,
            'fa_word_count': fa_word_count,
            'en_word_count': en_word_count,
            'percent_fa': percent_fa,
            'lang_class': lang_class
        }
    
    def process_tweets_batch(self, tweets: List[str]) -> List[Dict[str, any]]:
        """
        Process multiple tweets in batch.
        
        Args:
            tweets (List[str]): List of raw tweet texts
            
        Returns:
            List[Dict[str, any]]: List of processed tweet data
        """
        return [self.process_tweet(tweet) for tweet in tweets]


# Example usage and testing
if __name__ == "__main__":
    # Example tweet with mixed content
    sample_tweet = """
    سلام دوستان! امروز یک روز عالی بود 😊 
    Check out this link: https://example.com 
    #فناوری #technology @sajjad_esmaili_ir 
    با half‌space مشکل داشتم ولي الان درست شده
    🚀 #AI #هوش_مصنوعی
    """
    
    # Create processor with default config
    processor = TwitterTextProcessor()
    
    # Process the tweet
    result = processor.process_tweet(sample_tweet)
    
    # Display results
    print("=== Twitter Text Processing Results ===")
    for key, value in result.items():
        print(f"{key}: {value}")
    
    # Example with custom config
    custom_config = ProcessingConfig(
        normalize_persian=True,
        extract_links=True,
        extract_hashtags=True,
        extract_mentions=False,  # Disable mention extraction
        extract_emojis=True,
        detect_language=True,
        lang_threshold=60.0  # Higher threshold for Persian classification
    )
    
    custom_processor = TwitterTextProcessor(custom_config)
    custom_result = custom_processor.process_tweet(sample_tweet)
    
    print("\n=== Custom Configuration Results ===")
    print(f"Mentions extraction disabled: {custom_result['mentions']}")
    print(f"Language classification with 60% threshold: {custom_result['lang_class']}")
