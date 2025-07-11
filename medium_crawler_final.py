#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Import function đã fix
from selenium_final_solution import create_selenium_chrome_driver


def crawl_medium_article(url, headless=True):
    """
    Crawl Medium article và extract thông tin chi tiết
    
    Args:
        url (str): URL của Medium article
        headless (bool): Chạy headless hay không
    
    Returns:
        dict: Thông tin article đã extract
    """
    
    print(f"🎯 Crawling Medium article: {url}")
    
    # Khởi tạo WebDriver với function đã fix
    driver = create_selenium_chrome_driver(headless=headless)
    
    article_data = {}
    
    try:
        # Navigate đến URL
        driver.get(url)
        time.sleep(3)  # Chờ page load
        
        # Basic info
        article_data['url'] = driver.current_url
        article_data['page_title'] = driver.title
        
        print(f"✅ Page loaded: {article_data['page_title']}")
        
        # Extract article title
        title_selectors = [
            'h1[data-testid="storyTitle"]',
            'h1.pw-post-title',
            'h1',
            '[data-testid="storyTitle"]'
        ]
        
        article_title = None
        for selector in title_selectors:
            try:
                element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                article_title = element.text.strip()
                if article_title:
                    break
            except:
                continue
        
        article_data['title'] = article_title
        print(f"✅ Article Title: {article_title}")
        
        # Extract author
        author_selectors = [
            '[data-testid="authorName"] a',
            '[data-testid="authorName"]',
            '.author-name a',
            'a[rel="author"]'
        ]
        
        author = None
        for selector in author_selectors:
            try:
                element = driver.find_element(By.CSS_SELECTOR, selector)
                author = element.text.strip()
                if author:
                    break
            except:
                continue
        
        article_data['author'] = author
        print(f"✅ Author: {author}")
        
        # Extract publish date
        date_selectors = [
            '[data-testid="storyPublishDate"]',
            'time',
            '.published-date'
        ]
        
        pub_date = None
        for selector in date_selectors:
            try:
                element = driver.find_element(By.CSS_SELECTOR, selector)
                pub_date = element.text.strip() or element.get_attribute('datetime')
                if pub_date:
                    break
            except:
                continue
        
        article_data['publish_date'] = pub_date
        print(f"✅ Publish Date: {pub_date}")
        
        # Extract subtitle/description
        subtitle_selectors = [
            '[data-testid="storySubtitle"]',
            '.subtitle',
            'h2.graf--subtitle'
        ]
        
        subtitle = None
        for selector in subtitle_selectors:
            try:
                element = driver.find_element(By.CSS_SELECTOR, selector)
                subtitle = element.text.strip()
                if subtitle:
                    break
            except:
                continue
        
        article_data['subtitle'] = subtitle
        if subtitle:
            print(f"✅ Subtitle: {subtitle[:100]}...")
        
        # Extract content paragraphs
        content_selectors = [
            '[data-selectable-paragraph="true"]',
            '.graf--p',
            'p'
        ]
        
        content_paragraphs = []
        for selector in content_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for elem in elements:
                    text = elem.text.strip()
                    if text and len(text) > 30:  # Lọc paragraph có nghĩa
                        content_paragraphs.append(text)
                
                if content_paragraphs:
                    break
            except:
                continue
        
        article_data['content_paragraphs'] = content_paragraphs
        article_data['content_length'] = len('\n'.join(content_paragraphs))
        
        print(f"✅ Extracted {len(content_paragraphs)} paragraphs")
        print(f"✅ Total content length: {article_data['content_length']:,} characters")
        
        # Extract tags (if available)
        tag_selectors = [
            '[data-testid="storyTags"] a',
            '.tags a',
            '.tag'
        ]
        
        tags = []
        for selector in tag_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for elem in elements:
                    tag = elem.text.strip()
                    if tag and tag not in tags:
                        tags.append(tag)
                
                if tags:
                    break
            except:
                continue
        
        article_data['tags'] = tags
        if tags:
            print(f"✅ Tags: {', '.join(tags)}")
        
        # Extract reading time
        try:
            reading_time_elem = driver.find_element(By.CSS_SELECTOR, '[data-testid="storyReadTime"]')
            article_data['reading_time'] = reading_time_elem.text.strip()
            print(f"✅ Reading Time: {article_data['reading_time']}")
        except:
            article_data['reading_time'] = None
        
        # Get full content preview
        if content_paragraphs:
            full_content = '\n\n'.join(content_paragraphs[:5])  # First 5 paragraphs
            print(f"\n📝 Content Preview:")
            print("=" * 50)
            print(full_content[:800] + "..." if len(full_content) > 800 else full_content)
            print("=" * 50)
        
        article_data['success'] = True
        article_data['error'] = None
        
    except Exception as e:
        print(f"❌ Error crawling article: {e}")
        article_data['success'] = False
        article_data['error'] = str(e)
        
    finally:
        driver.quit()
        print("✅ Driver closed")
    
    return article_data

def main():
    """Main function để test crawling"""
    
    print("🕷️  Medium Article Crawler - Final Version")
    print("=" * 60)
    
    # URL cần crawl
    url = "https://medium.com/decodingml/a-real-time-retrieval-system-for-rag-on-social-media-data-9cc01d50a2a0"
    
    # Crawl article
    result = crawl_medium_article(url, headless=True)
    
    # Print summary
    print("\n📊 CRAWLING SUMMARY:")
    print("=" * 60)
    print(f"✅ Success: {result.get('success', False)}")
    print(f"📰 Title: {result.get('title', 'N/A')}")
    print(f"👤 Author: {result.get('author', 'N/A')}")
    print(f"📅 Date: {result.get('publish_date', 'N/A')}")
    print(f"⏱️  Reading Time: {result.get('reading_time', 'N/A')}")
    print(f"📝 Content Length: {result.get('content_length', 0):,} characters")
    print(f"📄 Paragraphs: {len(result.get('content_paragraphs', []))}")
    print(f"🏷️  Tags: {len(result.get('tags', []))}")
    
    if result.get('error'):
        print(f"❌ Error: {result['error']}")
    
    print("=" * 60)
    
    return result

if __name__ == "__main__":
    result = main()
    
    # Có thể save result to JSON nếu cần
    if result.get('success'):
        print("\n💾 Bạn có thể save result này to JSON hoặc database.")
        print("🎉 Crawling completed successfully!")
    else:
        print("\n❌ Crawling failed. Please check the error above.") 