# Twitter Text Processor for Persian/English

A comprehensive Python library for processing Twitter texts with special support for Persian (Farsi) language characteristics. This processor handles text normalization, feature extraction, and language detection with modular, configurable components.

## Features

### 🔧 **Modular Processing Steps**
- **Persian Normalization**: Fix half-spaces and convert Arabic characters to Persian
- **Link Extraction**: Extract and remove URLs from text
- **Hashtag Processing**: Separate Persian and English hashtags
- **Mention Extraction**: Extract @username references
- **Emoji Handling**: Extract and categorize emojis
- **Language Detection**: Classify text as Persian or English based on configurable thresholds

### 🎯 **Key Advantages**
- **Configurable**: Enable/disable any processing step
- **Persian-aware**: Proper handling of Persian text characteristics
- **Performance-optimized**: Pre-compiled regex patterns
- **Comprehensive**: Handles mixed Persian-English content
- **Well-documented**: Extensive comments and type hints

## Installation

```bash
# Clone or download the processor
# No additional dependencies required - uses only Python standard library
```

## Quick Start

```python
from twitter_processor import TwitterTextProcessor

# Create processor with default settings
processor = TwitterTextProcessor()

# Process a tweet
tweet = "سلام! Check this: https://example.com #فناوری #tech @user 😊"
result = processor.process_tweet(tweet)

print(result['clean_text'])  # Clean text without links/hashtags/mentions/emojis
print(result['hashtags_fa']) # Persian hashtags: ['#فناوری']
print(result['hashtags_en']) # English hashtags: ['#tech']
print(result['lang_class'])  # Language classification: 'fa' or 'en'
```

## Configuration

### ProcessingConfig Class

Control which processing steps are enabled:

```python
from twitter_processor import TwitterTextProcessor, ProcessingConfig

# Custom configuration
config = ProcessingConfig(
    normalize_persian=True,   # Fix Persian text issues
    extract_links=True,       # Remove and extract URLs
    extract_hashtags=True,    # Process hashtags
    extract_mentions=False,   # Skip mention extraction
    extract_emojis=True,      # Handle emojis
    detect_language=True,     # Language detection
    lang_threshold=60.0       # Persian threshold (60%)
)

processor = TwitterTextProcessor(config)
```

### Configuration Options

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `normalize_persian` | bool | True | Enable Persian text normalization |
| `extract_links` | bool | True | Extract and remove URLs |
| `extract_hashtags` | bool | True | Extract and classify hashtags |
| `extract_mentions` | bool | True | Extract @username mentions |
| `extract_emojis` | bool | True | Extract emoji characters |
| `detect_language` | bool | True | Perform language detection |
| `lang_threshold` | float | 50.0 | Persian percentage threshold for classification |

## Processing Steps

### 1. Persian Normalization
```python
# Fixes common Persian text issues:
# - Converts Arabic ي and ك to Persian ی and ک
# - Normalizes half-spaces (‌) for proper word separation
# - Adds half-spaces before common suffixes

text = "بچه هاي خوب"  # Before
text = "بچه‌های خوب"  # After normalization
```

### 2. Link Extraction
```python
# Extracts various URL formats:
links = [
    "https://example.com",
    "http://test.ir", 
    "www.site.com",
    "domain.com/path"
]
```

### 3. Hashtag Classification
```python
# Separates hashtags by language:
hashtags_fa = ["#فناوری", "#ایران"]      # Persian hashtags
hashtags_en = ["#technology", "#AI"]      # English hashtags

# Classification based on character analysis
```

### 4. Mention Extraction
```python
# Extracts all @username patterns:
mentions = ["@username", "@test_user"]
```

### 5. Emoji Processing
```python
# Extracts Unicode emojis:
emojis = ["😊", "🚀", "❤️"]

# Handles various emoji ranges including:
# - Emoticons, symbols, pictographs
# - Transport and map symbols  
# - Flags and enclosed characters
```

### 6. Language Detection
```python
# Word-level language analysis:
result = {
    'fa_word_count': 5,      # Persian words count
    'en_word_count': 2,      # English words count  
    'percent_fa': 71.4,      # Persian percentage
    'lang_class': 'fa'       # Final classification
}

# Classification based on configurable threshold
```

## Output Format

The `process_tweet()` method returns a dictionary with these columns:

```python
{
    'clean_text': str,        # Cleaned text without extracted elements
    'links': List[str],       # Extracted URLs
    'hashtags_fa': List[str], # Persian hashtags
    'hashtags_en': List[str], # English hashtags  
    'mentions': List[str],    # @username mentions
    'emojis': List[str],      # Extracted emojis
    'fa_word_count': int,     # Persian word count
    'en_word_count': int,     # English word count
    'percent_fa': float,      # Persian percentage (0-100)
    'lang_class': str         # 'fa', 'en', or 'unknown'
}
```

## Batch Processing

Process multiple tweets efficiently:

```python
tweets = [
    "First tweet with #hashtag",
    "دومین توییت با #هشتگ", 
    "Third mixed tweet #فارسی #english"
]

results = processor.process_tweets_batch(tweets)

for i, result in enumerate(results):
    print(f"Tweet {i+1}: {result['lang_class']}")
```

## Advanced Usage Examples

### Custom Language Threshold
```python
# Stricter Persian classification (70% threshold)
config = ProcessingConfig(lang_threshold=70.0)
processor = TwitterTextProcessor(config)

# More lenient classification (30% threshold)  
config = ProcessingConfig(lang_threshold=30.0)
processor = TwitterTextProcessor(config)
```

### Disable Specific Features
```python
# Only text cleaning, no feature extraction
config = ProcessingConfig(
    normalize_persian=True,
    extract_links=False,
    extract_hashtags=False,
    extract_mentions=False,
    extract_emojis=False,
    detect_language=False
)

processor = TwitterTextProcessor(config)
result = processor.process_tweet(tweet)
# Only 'clean_text' will contain processed content
```

### Feature-Specific Processing
```python
# Only hashtag and language processing
config = ProcessingConfig(
    normalize_persian=True,
    extract_links=False,
    extract_hashtags=True,  # Only hashtags
    extract_mentions=False,
    extract_emojis=False,
    detect_language=True    # And language detection
)
```

## Performance Notes

- **Regex Compilation**: Patterns are pre-compiled for better performance
- **Memory Efficient**: Processes text in-place where possible
- **Batch Processing**: Optimized for processing large tweet datasets
- **No External Dependencies**: Uses only Python standard library

## Error Handling

The processor handles various edge cases:

- Empty or whitespace-only texts
- Texts with only special characters
- Mixed RTL/LTR content
- Malformed URLs or hashtags
- Unicode normalization issues

## Persian Language Support

### Half-space Handling
```python
# Automatic half-space normalization:
"کتاب های جدید" → "کتاب‌های جدید"
"می رود" → "می‌رود"
```

### Arabic Character Conversion
```python
# Arabic to Persian character mapping:
"بچه هاي خوب" → "بچه‌های خوب"  # ي → ی
"كتاب" → "کتاب"                # ك → ک  
```

### Language Detection Algorithm
1. **Word-level Analysis**: Each word is classified individually
2. **Character Counting**: Persian vs English character ratios
3. **Threshold Application**: Configurable classification threshold
4. **Fallback Handling**: 'unknown' for ambiguous cases

## Testing

Run the built-in test example:

```python
python twitter_processor.py
```

This will process a sample tweet and display all extraction results.

## Contributing

Feel free to contribute by:
- Adding more Persian text normalization rules
- Improving emoji detection patterns  
- Enhancing language detection accuracy
- Adding support for other languages
- Optimizing performance

## License

This project is open source. Feel free to use and modify according to your needs.

## Changelog

### Version 1.0.0
- Initial release with full Persian/English support
- Modular processing architecture
- Comprehensive text normalization
- Configurable processing steps
- Batch processing capabilities

---

**Keywords**: Persian NLP, Farsi text processing, Twitter analysis, social media mining, text normalization, hashtag extraction, language detection