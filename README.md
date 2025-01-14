# Web Content Scraper

A Python tool for scraping and cleaning HTML content from webpages. It supports extracting elements by class, ID, or tag and displays structured results.

## Features

- Validates and checks URL accessibility.  
- Extracts content by class, ID, or tag.  
- Cleans HTML, preserving essential structures like blockquotes.  
- Handles errors gracefully (timeouts, invalid inputs, etc.).

## Installation

1. Clone the repository:  
   ```bash
   git clone https://github.com/yourusername/web-content-scraper.git
   cd web-scraping
   ```  
2. Install dependencies:  
   ```bash
   pip install requests
   ```

## Usage

1. Run the script:  
   ```bash
   python web-scraping.py
   ```  
2. Follow the prompts:  
   - Enter a valid URL.  
   - Choose the type of element (class, ID, or tag).  
   - Enter the selector value.  
3. View the cleaned content in the console.

## Example Output
For a `div` with a class:  
```plaintext
1. [How to create Tags / Categories for different Topics]
2. [Re: How to create Tags / Categories for different Topics]
```

## Edge Case Example
This scraper can extract content from websites that return a 404 status code. For example:  

1. **Example 1**: https://www.phpbb.com/community/viewtopic.php?f=46&t=2159437
   - The scraper processes the HTML and extracts content from specified elements.  

2. **Example 2**: https://forum.vbulletin.com/forum/vbulletin-3-8/vbulletin-3-8-questions-problems-an
   - Status Code: 404  
   - Despite the error code, the tool scrapes available HTML content.
