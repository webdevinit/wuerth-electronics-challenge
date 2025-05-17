import requests
import html2text
from urllib.parse import urlparse
import os

def scrape_to_markdown(url):
    # Headers to help avoid cookie banners
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'DNT': '1',  # Do Not Track
        'Cookie': '',  # Empty cookie
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Convert HTML to markdown
        converter = html2text.HTML2Text()
        converter.ignore_links = False
        converter.ignore_images = False
        converter.body_width = 0  # Don't wrap text
        
        markdown_content = converter.handle(response.text)
        return markdown_content
        
    except requests.RequestException as e:
        return f"Error scraping {url}: {str(e)}"

def save_to_markdown(url, content, output_dir="scraped_content"):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Create filename from URL
    domain = urlparse(url).netloc
    filename = f"{domain}.md"
    filepath = os.path.join(output_dir, filename)
    
    # Write content to file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"# Content from {url}\n\n")
        f.write(content)
    
    return filepath

if __name__ == "__main__":
    test_url = "https://www.mouser.de/ProductDetail/Vishay-Vitramon/HV2220Y103KXHATHV?qs=FphPqe%252Bob2iFgQ66zqiYBw%3D%3D&srsltid=AfmBOooekcSyTUuyyGI81Nlr596Vv-UHXuW996YwtWRPTF3eGG_vNWZ5"
    content = scrape_to_markdown(test_url)
    
    # Save the content to a markdown file
    output_path = save_to_markdown(test_url, content)
    print(f"Content saved to: {output_path}")