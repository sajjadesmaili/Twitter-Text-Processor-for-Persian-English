#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Suite for Twitter Text Processor
====================================

Comprehensive test cases to validate the functionality of the Twitter Text Processor.
Run this file to verify that all components work correctly.
"""

import unittest
from twitter_processor import TwitterTextProcessor, ProcessingConfig


class TestTwitterTextProcessor(unittest.TestCase):
    """Test cases for TwitterTextProcessor class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.processor = TwitterTextProcessor()
    
    def test_persian_normalization(self):
        """Test Persian text normalization functionality."""
        test_cases = [
            ("بچه هاي خوب", "بچه‌های خوب"),  # Fix ي and add half-space
            ("كتاب", "کتاب"),                  # Fix ك
            ("دانشگاه تهران", "دانشگاه‌تهران"), # Add half-space
            ("خانه  ي  بزرگ", "خانه‌ی بزرگ"),  # Clean up spaces and fix ي
        ]
        
        for input_text, expected in test_cases:
            with self.subTest(input_text=input_text):
                result = self.processor.normalize_persian(input_text)
                self.assertEqual(result, expected)
    
    def test_link_extraction(self):
        """Test URL extraction functionality."""
        test_cases = [
            ("Check https://example.com please", 
             ["https://example.com"], "Check  please"),
            ("Visit www.test.com and http://another.site", 
             ["www.test.com", "http://another.site"], "Visit  and"),
            ("No links here", [], "No links here"),
            ("Multiple https://site1.com and https://site2.ir", 
             ["https://site1.com", "https://site2.ir"], "Multiple  and"),
        ]
        
        for input_text, expected_links, expected_text in test_cases:
            with self.subTest(input_text=input_text):
                links, clean_text = self.processor.extract_links(input_text)
                self.assertEqual(links, expected_links)
                # Clean up extra spaces for comparison
                clean_text = ' '.join(clean_text.split())
                expected_text = ' '.join(expected_text.split())
                self.assertEqual(clean_text, expected_text)
    
    def test_hashtag_extraction(self):
        """Test hashtag extraction and classification."""
        test_cases = [
            ("#فناوری #technology test", 
             ["#فناوری"], ["#technology"], "test"),
            ("#AI #هوش_مصنوعی #python", 
             ["#هوش_مصنوعی"], ["#AI", "#python"], ""),
            ("No hashtags here", [], [], "No hashtags here"),
            ("#test123 #تست_فارسی", 
             ["#تست_فارسی"], ["#test123"], ""),
        ]
        
        for input_text, expected_fa, expected_en, expected_text in test_cases:
            with self.subTest(input_text=input_text):
                hashtags_fa, hashtags_en, clean_text = self.processor.extract_hashtags(input_text)
                self.assertEqual(hashtags_fa, expected_fa)
                self.assertEqual(hashtags_en, expected_en)
                self.assertEqual(clean_text.strip(), expected_text)
    
    def test_mention_extraction(self):
        """Test mention extraction functionality."""
        test_cases = [
            ("Hello @username and @test_user", 
             ["@username", "@test_user"], "Hello  and"),
            ("No mentions", [], "No mentions"),
            ("@single_mention only", ["@single_mention"], "only"),
        ]
        
        for input_text, expected_mentions, expected_text in test_cases:
            with self.subTest(input_text=input_text):
                mentions, clean_text = self.processor.extract_mentions(input_text)
                self.assertEqual(mentions, expected_mentions)
                # Clean up extra spaces for comparison
                clean_text = ' '.join(clean_text.split())
                expected_text = ' '.join(expected_text.split())
                self.assertEqual(clean_text, expected_text)
    
    def test_emoji_extraction(self):
        """Test emoji extraction functionality."""
        test_cases = [
            ("Happy 😊 and excited 🚀", ["😊", "🚀"], "Happy  and excited"),
            ("No emojis here", [], "No emojis here"),
            ("Only emojis: 😊🚀❤️", ["😊", "🚀", "❤️"], "Only emojis:"),
        ]
        
        for input_text, expected_emojis, expected_text in test_cases:
            with self.subTest(input_text=input_text):
                emojis, clean_text = self.processor.extract_emojis(input_text)
                self.assertEqual(emojis, expected_emojis)
                # Clean up extra spaces for comparison
                clean_text = ' '.join(clean_text.split())
                expected_text = ' '.join(expected_text.split())
                self.assertEqual(clean_text, expected_text)
    
    def test_language_detection(self):
        """Test language detection functionality."""
        test_cases = [
            ("سلام دوستان عزیز", 3, 0, 100.0, "fa"),
            ("Hello dear friends", 0, 3, 0.0, "en"),
            ("سلام hello دوستان", 2, 1, 66.7, "fa"),  # 2/3 = 66.7%
            ("", 0, 0, 0.0, "unknown"),
        ]
        
        for input_text, expected_fa, expected_en, expected_percent, expected_class in test_cases:
            with self.subTest(input_text=input_text):
                fa_count, en_count, percent_fa, lang_class = self.processor.detect_language(input_text)
                self.assertEqual(fa_count, expected_fa)
                self.assertEqual(en_count, expected_en)
                if expected_percent > 0:
                    self.assertAlmostEqual(percent_fa, expected_percent, places=1)
                else:
                    self.assertEqual(percent_fa, expected_percent)
                self.assertEqual(lang_class, expected_class)
    
    def test_complete_processing(self):
        """Test complete tweet processing pipeline."""
        sample_tweet = "سلام @user! Check https://test.com #فناوری #tech 😊"
        
        result = self.processor.process_tweet(sample_tweet)
        
        # Verify all expected keys exist
        expected_keys = [
            'clean_text', 'links', 'hashtags_fa', 'hashtags_en', 
            'mentions', 'emojis', 'fa_word_count', 'en_word_count', 
            'percent_fa', 'lang_class'
        ]
        
        for key in expected_keys:
            self.assertIn(key, result)
        
        # Verify specific extractions
        self.assertEqual(result['links'], ['https://test.com'])
        self.assertEqual(result['hashtags_fa'], ['#فناوری'])
        self.assertEqual(result['hashtags_en'], ['#tech'])
        self.assertEqual(result['mentions'], ['@user'])
        self.assertEqual(result['emojis'], ['😊'])
        self.assertEqual(result['lang_class'], 'fa')  # Should be Persian dominant
    
    def test_configuration_options(self):
        """Test different configuration options."""
        # Test with disabled features
        config = ProcessingConfig(
            normalize_persian=True,
            extract_links=False,
            extract_hashtags=False,
            extract_mentions=False,
            extract_emojis=False,
            detect_language=False
        )
        
        processor = TwitterTextProcessor(config)
        result = processor.process_tweet("Test @user #hashtag 😊 https://test.com")
        
        # Should have empty lists for disabled features
        self.assertEqual(result['links'], [])
        self.assertEqual(result['hashtags_fa'], [])
        self.assertEqual(result['hashtags_en'], [])
        self.assertEqual(result['mentions'], [])
        self.assertEqual(result['emojis'], [])
        self.assertEqual(result['fa_word_count'], 0)
        self.assertEqual(result['en_word_count'], 0)
    
    def test_batch_processing(self):
        """Test batch processing functionality."""
        tweets = [
            "First tweet #test",
            "دومین توییت #تست",
            "Third mixed tweet"
        ]
        
        results = self.processor.process_tweets_batch(tweets)
        
        self.assertEqual(len(results), 3)
        
        # Verify each result has all required keys
        for result in results:
            self.assertIn('clean_text', result)
            self.assertIn('lang_class', result)
    
    def test_edge_cases(self):
        """Test edge cases and error handling."""
        edge_cases = [
            "",           # Empty string
            "   ",        # Only whitespace
            "😊😊😊",      # Only emojis
            "123 456",    # Only numbers
            "\n\t\r",     # Only whitespace characters
        ]
        
        for edge_case in edge_cases:
            with self.subTest(edge_case=repr(edge_case)):
                # Should not raise an exception
                result = self.processor.process_tweet(edge_case)
                self.assertIsInstance(result, dict)
                self.assertIn('clean_text', result)


class TestProcessingConfig(unittest.TestCase):
    """Test cases for ProcessingConfig class."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = ProcessingConfig()
        
        self.assertTrue(config.normalize_persian)
        self.assertTrue(config.extract_links)
        self.assertTrue(config.extract_hashtags)
        self.assertTrue(config.extract_mentions)
        self.assertTrue(config.extract_emojis)
        self.assertTrue(config.detect_language)
        self.assertEqual(config.lang_threshold, 50.0)
    
    def test_custom_config(self):
        """Test custom configuration values."""
        config = ProcessingConfig(
            normalize_persian=False,
            extract_links=False,
            lang_threshold=75.0
        )
        
        self.assertFalse(config.normalize_persian)
        self.assertFalse(config.extract_links)
        self.assertTrue(config.extract_hashtags)  # Should remain default
        self.assertEqual(config.lang_threshold, 75.0)


class TestLanguageThreshold(unittest.TestCase):
    """Test language classification with different thresholds."""
    
    def test_threshold_variations(self):
        """Test language classification with different thresholds."""
        # Text with 60% Persian words
        mixed_text = "سلام hello دوستان friend جان"  # 3 Persian, 2 English = 60% Persian
        
        test_cases = [
            (30.0, 'fa'),  # Low threshold - should classify as Persian
            (50.0, 'fa'),  # Medium threshold - should classify as Persian  
            (70.0, 'en'),  # High threshold - should classify as English
            (90.0, 'en'),  # Very high threshold - should classify as English
        ]
        
        for threshold, expected_class in test_cases:
            with self.subTest(threshold=threshold):
                config = ProcessingConfig(lang_threshold=threshold)
                processor = TwitterTextProcessor(config)
                result = processor.process_tweet(mixed_text)
                self.assertEqual(result['lang_class'], expected_class)


def run_integration_test():
    """Run integration test with realistic data."""
    print("Running Integration Test...")
    print("-" * 40)
    
    # Realistic tweet examples
    real_tweets = [
        "صبح بخیر دوستان! امروز روز خوبی خواهد بود ☀️ #صبح_بخیر #انگیزشی",
        "Just published my new blog post about #MachineLearning https://myblog.com/ml-post 🤖 #AI #DataScience",
        "کنفرانس فناوری امروز عالی بود! Met great people @techconf #TechConf2024 🚀",
        "Working on a new #Python project 🐍 خیلی exciting است! #coding #development",
        "شب یلدا مبارک to all my friends! 🌙❄️ #یلدا #WinterSolstice #celebration"
    ]
    
    processor = TwitterTextProcessor()
    results = processor.process_tweets_batch(real_tweets)
    
    print(f"Processed {len(results)} tweets:")
    
    for i, (tweet, result) in enumerate(zip(real_tweets, results), 1):
        print(f"\nTweet {i}:")
        print(f"Original: {tweet}")
        print(f"Clean: {result['clean_text']}")
        print(f"Language: {result['lang_class']} ({result['percent_fa']:.1f}% Persian)")
        print(f"Features: Links={len(result['links'])}, "
              f"Hashtags={len(result['hashtags_fa']) + len(result['hashtags_en'])}, "
              f"Mentions={len(result['mentions'])}, Emojis={len(result['emojis'])}")
    
    print("\nIntegration test completed successfully! ✅")


if __name__ == '__main__':
    print("Twitter Text Processor - Test Suite")
    print("=" * 50)
    
    # Run unit tests
    print("Running Unit Tests...")
    unittest.main(verbosity=2, exit=False)
    
    print("\n" + "=" * 50)
    
    # Run integration test
    run_integration_test()