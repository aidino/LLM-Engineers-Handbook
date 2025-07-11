import os
import random
from tempfile import mkdtemp

import chromedriver_autoinstaller
from selenium import webdriver


def create_selenium_chrome_driver(use_specific_profile=True, profile_name="Profile 2", headless=True):
    """
    Tạo Chrome WebDriver với các thiết lập tối ưu để tránh lỗi
    
    Args:
        use_specific_profile (bool): Có sử dụng profile cụ thể hay không
        profile_name (str): Tên profile Chrome (mặc định "Profile 2")
        headless (bool): Chạy ở chế độ headless hay không
    
    Returns:
        webdriver.Chrome: Chrome WebDriver instance
    """
    
    # Tự động cài đặt ChromeDriver tương thích
    chromedriver_autoinstaller.install()
    
    # Tạo Chrome options với approach đã test thành công
    options = webdriver.ChromeOptions()
    
    # Core arguments (đã test thành công)
    options.add_argument("--no-sandbox") 
    options.add_argument("--disable-dev-shm-usage")
    
    # Headless mode
    if headless:
        options.add_argument("--headless=new")
    
    # Luôn dùng temporary directory để tránh xung đột
    temp_dir = mkdtemp()
    options.add_argument(f"--user-data-dir={temp_dir}")
    
    # Thêm các arguments để bypass detection
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36")
    
    # Optional: Random port để tránh xung đột (nếu cần)
    debug_port = random.randint(9000, 9999)
    options.add_argument(f"--remote-debugging-port={debug_port}")
    
    # Tạo WebDriver
    driver = webdriver.Chrome(options=options)
    print("✅ Chrome WebDriver khởi tạo thành công!")
    print(f"📁 Sử dụng temporary profile: {temp_dir}")
    
    return driver

# =================== CÁCH SỬ DỤNG ===================

if __name__ == "__main__":
    print("=== Demo Selenium Chrome WebDriver (Fixed Version) ===\n")
    
    # Test với Google
    print("1. Test với Google:")
    driver = create_selenium_chrome_driver(headless=True)
    
    driver.get("https://www.google.com")
    print(f"✅ Google - Title: {driver.title}")
    driver.quit()
    
    # Test với Medium
    print("\n2. Test với Medium:")
    driver = create_selenium_chrome_driver(headless=True)
    
    url = "https://medium.com/decodingml/a-real-time-retrieval-system-for-rag-on-social-media-data-9cc01d50a2a0"
    driver.get(url)
    print(f"✅ Medium - Title: {driver.title}")
    print(f"✅ URL: {driver.current_url}")
    
    # Lấy article content
    try:
        h1_elements = driver.find_elements("tag name", "h1")
        if h1_elements:
            print(f"✅ Article Title: {h1_elements[0].text}")
    except:
        print("⚠️  Không lấy được article title")
    
    driver.quit()
    
    print("\n🎉 Hoàn thành! Function hoạt động tốt với approach đơn giản.") 