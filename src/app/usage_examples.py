#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Twitter Text Processor - Usage Examples
=====================================

This file demonstrates various usage scenarios for the Twitter Text Processor
with real-world examples and different configuration options.
"""

from twitter_processor import TwitterTextProcessor, ProcessingConfig


def example_1_basic_usage():
    """Example 1: Basic usage with default configuration."""
    print("="*60)
    print("EXAMPLE 1: Basic Usage")
    print("="*60)
    
    # Sample tweets with mixed Persian-English content
    sample_tweets = [
        "سلام دوستان! امروز یک روز فوق‌العاده بود 😊 #روز_خوب",
        "Check out this amazing link: https://github.com/example #coding #python",
        "امروز در کنفرانس @TechConf شرکت کردم 🚀 https://techconf.ir #فناوری #AI",
        "Mixed content: hello سلام world دنیا! #test #تست 😎"
    ]
    
    # Create processor with default settings
    processor = TwitterTextProcessor()
    
    for i, tweet in enumerate(sample_tweets, 1):
        print(f"\n--- Tweet {i} ---")
        print(f"Original: {tweet}")
        
        result = processor.process_tweet(tweet)
        
        print(f"Clean Text: {result['clean_text']}")
        print(f"Language: {result['lang_class']} ({result['percent_fa']:.1f}% Persian)")
        print(f"Persian Hashtags: {result['hashtags_fa']}")
        print(f"English Hashtags: {result['hashtags_en']}")
        print(f"Links: {result['links']}")
        print(f"Mentions: {result['mentions']}")
        print(f"Emojis: {result['emojis']}")


def example_2_custom_configuration():
    """Example 2: Custom configuration for specific use cases."""
    print("\n" + "="*60)
    print("EXAMPLE 2: Custom Configuration")
    print("="*60)
    
    # Create different configurations for different scenarios
    
    # Configuration 1: Only text cleaning and language detection
    clean_only_config = ProcessingConfig(
        normalize_persian=True,
        extract_links=False,
        extract_hashtags=False,
        extract_mentions=False,
        extract_emojis=False,
        detect_language=True,
        lang_threshold=50.0
    )
    
    # Configuration 2: Full feature extraction, no language detection
    feature_only_config = ProcessingConfig(
        normalize_persian=True,
        extract_links=True,
        extract_hashtags=True,
        extract_mentions=True,
        extract_emojis=True,
        detect_language=False,
        lang_threshold=50.0
    )
    
    # Configuration 3: High Persian threshold for stricter classification
    strict_persian_config = ProcessingConfig(
        normalize_persian=True,
        extract_links=True,
        extract_hashtags=True,
        extract_mentions=True,
        extract_emojis=True,
        detect_language=True,
        lang_threshold=75.0  # 75% threshold for Persian classification
    )
    
    sample_text = "سلام friends! امروز coding کردم 😊 https://example.com #فناوری #tech @username"
    
    processors = [
        ("Clean Only", TwitterTextProcessor(clean_only_config)),
        ("Features Only", TwitterTextProcessor(feature_only_config)),
        ("Strict Persian (75%)", TwitterTextProcessor(strict_persian_config))
    ]
    
    print(f"Sample text: {sample_text}")
    
    for name, processor in processors:
        print(f"\n--- {name} Configuration ---")
        result = processor.process_tweet(sample_text)
        
        print(f"Clean Text: '{result['clean_text']}'")
        print(f"Language Classification: {result['lang_class']}")
        print(f"Persian %: {result['percent_fa']:.1f}%")
        print(f"Hashtags FA: {result['hashtags_fa']}")
        print(f"Hashtags EN: {result['hashtags_en']}")


def example_3_persian_normalization():
    """Example 3: Demonstrate Persian text normalization features."""
    print("\n" + "="*60)
    print("EXAMPLE 3: Persian Text Normalization")
    print("="*60)
    
    # Texts with common Persian issues
    problematic_texts = [
        "بچه هاي خوب",              # Wrong 'ي' and missing half-space
        "كتاب هاي جديد",            # Wrong 'ك' and 'ي'
        "خانه  ي    بزرگ",          # Extra spaces around 'ي'
        "دانشگاه تهران",             # Missing half-space before suffix
        "می رود به مدرسه",         # Wrong spacing
        "انگلیسي صحبت مي كند"      # Multiple issues
    ]
    
    processor = TwitterTextProcessor()
    
    for text in problematic_texts:
        result = processor.process_tweet(text)
        print(f"Before: '{text}'")
        print(f"After:  '{result['clean_text']}'")
        print()


def example_4_language_detection_analysis():
    """Example 4: Analyze language detection with different thresholds."""
    print("\n" + "="*60)
    print("EXAMPLE 4: Language Detection Analysis")
    print("="*60)
    
    # Test texts with varying Persian/English ratios
    test_texts = [
        "سلام دوستان عزیز",                    # 100% Persian
        "Hello dear friends",                   # 100% English
        "سلام hello دوستان friends",           # 50% Persian
        "Today امروز is یک روز good day",      # Mixed
        "Programming در Python خیلی fun است", # Technical mixed
        "AI و machine learning در Iran"        # Technical terms
    ]
    
    thresholds = [30.0, 50.0, 70.0]
    
    for text in test_texts:
        print(f"\nText: '{text}'")
        print("Threshold | Persian% | Classification | FA_Words | EN_Words")
        print("-" * 65)
        
        for threshold in thresholds:
            config = ProcessingConfig(lang_threshold=threshold)
            processor = TwitterTextProcessor(config)
            result = processor.process_tweet(text)
            
            print(f"   {threshold:4.1f}%  |  {result['percent_fa']:6.1f}%  |      {result['lang_class']:2s}       |    {result['fa_word_count']:2d}    |    {result['en_word_count']:2d}")


def example_5_batch_processing():
    """Example 5: Process multiple tweets efficiently."""
    print("\n" + "="*60)
    print("EXAMPLE 5: Batch Processing")
    print("="*60)
    
    # Simulate a dataset of tweets
    tweet_dataset = [
        "صبح بخیر! امروز هوا عالیه ☀️ #صبح_بخیر",
        "Good morning everyone! Beautiful weather today ☀️ #morning",
        "کار جدیدم رو شروع کردم 🎉 خیلی excited هستم! #job #career",
        "Learning Python programming 🐍 #coding #python #learning",
        "دیشب فیلم دیدم https://imdb.com/movie123 #movie #cinema",
        "Weekend plans: coding + coffee ☕ #weekend #coding",
        "امتحانات تموم شد! 🎓 Time to celebrate #graduation #university",
        "New blog post published: https://myblog.com/post1 #blogging #tech",
        "شب یلدا مبارک! 🌙 Happy Yalda night everyone #یلدا #winter",
        "AI revolution is here 🤖 هوش مصنوعی everywhere #AI #tech #فناوری"
    ]
    
    processor = TwitterTextProcessor()
    
    # Process all tweets in batch
    results = processor.process_tweets_batch(tweet_dataset)
    
    # Analyze the results
    print(f"Processed {len(results)} tweets:")
    print("\nLanguage Distribution:")
    
    lang_counts = {'fa': 0, 'en': 0, 'unknown': 0}
    for result in results:
        lang_counts[result['lang_class']] += 1
    
    for lang, count in lang_counts.items():
        percentage = (count / len(results)) * 100
        print(f"  {lang.upper()}: {count} tweets ({percentage:.1f}%)")
    
    print(f"\nTotal hashtags extracted:")
    all_hashtags_fa = []
    all_hashtags_en = []
    all_links = []
    all_mentions = []
    
    for result in results:
        all_hashtags_fa.extend(result['hashtags_fa'])
        all_hashtags_en.extend(result['hashtags_en'])
        all_links.extend(result['links'])
        all_mentions.extend(result['mentions'])
    
    print(f"  Persian hashtags: {len(all_hashtags_fa)} - {set(all_hashtags_fa)}")
    print(f"  English hashtags: {len(all_hashtags_en)} - {set(all_hashtags_en)}")
    print(f"  Links: {len(all_links)}")
    print(f"  Mentions: {len(all_mentions)}")


def example_6_feature_specific_processing():
    """Example 6: Using individual processing functions."""
    print("\n" + "="*60)
    print("EXAMPLE 6: Feature-Specific Processing")
    print("="*60)
    
    # Create processor
    processor = TwitterTextProcessor()
    
    sample_text = "سلام @username! Check: https://test.com #فناوری #tech 😊🚀"
    print(f"Original text: {sample_text}")
    
    # Step-by-step processing demonstration
    current_text = sample_text
    
    # Step 1: Persian normalization
    normalized_text = processor.normalize_persian(current_text)
    print(f"\n1. After normalization: '{normalized_text}'")
    current_text = normalized_text
    
    # Step 2: Link extraction
    links, current_text = processor.extract_links(current_text)
    print(f"2. Links extracted: {links}")
    print(f"   Text after link removal: '{current_text}'")
    
    # Step 3: Hashtag extraction
    hashtags_fa, hashtags_en, current_text = processor.extract_hashtags(current_text)
    print(f"3. Persian hashtags: {hashtags_fa}")
    print(f"   English hashtags: {hashtags_en}")
    print(f"   Text after hashtag removal: '{current_text}'")
    
    # Step 4: Mention extraction
    mentions, current_text = processor.extract_mentions(current_text)
    print(f"4. Mentions extracted: {mentions}")
    print(f"   Text after mention removal: '{current_text}'")
    
    # Step 5: Emoji extraction
    emojis, current_text = processor.extract_emojis(current_text)
    print(f"5. Emojis extracted: {emojis}")
    print(f"   Text after emoji removal: '{current_text}'")
    
    # Step 6: Language detection
    fa_count, en_count, percent_fa, lang_class = processor.detect_language(current_text)
    print(f"6. Language analysis:")
    print(f"   Persian words: {fa_count}")
    print(f"   English words: {en_count}")
    print(f"   Persian percentage: {percent_fa:.1f}%")
    print(f"   Classification: {lang_class}")
    
    print(f"\nFinal clean text: '{current_text}'")


def example_7_edge_cases():
    """Example 7: Handle edge cases and problematic inputs."""
    print("\n" + "="*60)
    print("EXAMPLE 7: Edge Cases and Error Handling")
    print("="*60)
    
    edge_cases = [
        "",                          # Empty string
        "   ",                      # Only whitespace
        "😊😊😊",                    # Only emojis
        "##",                       # Invalid hashtags
        "https://",                 # Incomplete URL
        "@",                        # Invalid mention
        "123 456 789",             # Only numbers
        "!@#$%^&*()",              # Only symbols
        "   سلام   دنیا   ",        # Extra whitespace
        "text\nwith\nnewlines",    # Newlines
    ]
    
    processor = TwitterTextProcessor()
    
    for i, text in enumerate(edge_cases, 1):
        print(f"\nEdge case {i}: '{repr(text)}'")
        try:
            result = processor.process_tweet(text)
            print(f"  Clean text: '{result['clean_text']}'")
            print(f"  Language: {result['lang_class']}")
            print(f"  Word counts: FA={result['fa_word_count']}, EN={result['en_word_count']}")
        except Exception as e:
            print(f"  Error: {str(e)}")


def example_8_performance_comparison():
    """Example 8: Compare processing with different configurations."""
    print("\n" + "="*60)
    print("EXAMPLE 8: Performance Comparison")
    print("="*60)
    
    import time
    
    # Create test dataset
    test_tweets = [
        f"توییت شماره {i} با محتوای فارسی و English #test{i} @user{i} 😊 https://example{i}.com"
        for i in range(100)
    ]
    
    configurations = [
        ("Full Processing", ProcessingConfig()),
        ("Minimal Processing", ProcessingConfig(
            normalize_persian=True,
            extract_links=False,
            extract_hashtags=False,
            extract_mentions=False,
            extract_emojis=False,
            detect_language=False
        )),
        ("No Normalization", ProcessingConfig(
            normalize_persian=False,
            extract_links=True,
            extract_hashtags=True,
            extract_mentions=True,
            extract_emojis=True,
            detect_language=True
        ))
    ]
    
    print(f"Processing {len(test_tweets)} tweets with different configurations:")
    print()
    
    for config_name, config in configurations:
        processor = TwitterTextProcessor(config)
        
        start_time = time.time()
        results = processor.process_tweets_batch(test_tweets)
        end_time = time.time()
        
        processing_time = end_time - start_time
        tweets_per_second = len(test_tweets) / processing_time
        
        print(f"{config_name}:")
        print(f"  Time: {processing_time:.4f} seconds")
        print(f"  Speed: {tweets_per_second:.1f} tweets/second")
        print()


def main():
    """Run all examples."""
    print("Twitter Text Processor - Comprehensive Examples")
    print("=" * 60)
    
    example_1_basic_usage()
    example_2_custom_configuration()
    example_3_persian_normalization()
    example_4_language_detection_analysis()
    example_5_batch_processing()
    example_6_feature_specific_processing()
    example_7_edge_cases()
    example_8_performance_comparison()
    
    print("\n" + "="*60)
    print("All examples completed successfully!")
    print("="*60)


if __name__ == "__main__":
    main()