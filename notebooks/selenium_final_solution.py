import os
import platform
import random
import time
from tempfile import mkdtemp

import chromedriver_autoinstaller
from selenium import webdriver


def get_os_specific_config(target_os=None):
    """
    Lấy cấu hình User-Agent và options phù hợp cho từng OS
    
    Args:
        target_os (str): 'linux', 'darwin', 'windows' hoặc None để auto-detect
    
    Returns:
        dict: Cấu hình cho OS được chọn
    
    Note:
        Linux config thường hoạt động tốt hơn với các trang web có cơ chế chống bot
        vì Linux User-Agent ít bị nghi ngờ hơn trong môi trường server/automation
    """
    if target_os is None:
        target_os = platform.system().lower()
    
    configs = {
        'linux': {
            'user_agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
            'extra_args': [
                '--disable-dev-shm-usage',
                '--no-sandbox',
            ]
        },
        'darwin': {
            'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
            'extra_args': [
                '--disable-dev-shm-usage',
                '--no-sandbox',
            ]
        },
        'windows': {
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
            'extra_args': [
                '--disable-dev-shm-usage',
                '--no-sandbox',
            ]
        }
    }
    
    return configs.get(target_os, configs['linux'])


def create_selenium_chrome_driver(use_specific_profile=True, profile_name="Profile 2", headless=True, target_os=None):
    """
    Tạo Chrome WebDriver với các thiết lập tối ưu để tránh lỗi
    
    Args:
        use_specific_profile (bool): Có sử dụng profile cụ thể hay không
        profile_name (str): Tên profile Chrome (mặc định "Profile 2")
        headless (bool): Chạy ở chế độ headless hay không
        target_os (str): 'linux', 'darwin', 'windows' hoặc None để auto-detect
    
    Returns:
        webdriver.Chrome: Chrome WebDriver instance
    """
    
    # Lấy cấu hình cho OS hiện tại hoặc OS được chọn
    current_os = platform.system().lower()
    os_config = get_os_specific_config(target_os)
    
    print(f"🖥️  Detected OS: {current_os}")
    if target_os and target_os != current_os:
        print(f"🔄 Using config for: {target_os}")
    else:
        print(f"🔄 Using config for: {current_os}")
    
    # Tự động cài đặt ChromeDriver tương thích
    chromedriver_autoinstaller.install()
    
    # Tạo Chrome options với approach đã test thành công
    options = webdriver.ChromeOptions()
    
    # Core arguments từ OS config
    for arg in os_config['extra_args']:
        options.add_argument(arg)
    
    # Headless mode
    if headless:
        options.add_argument("--headless=new")
    
    # Luôn dùng temporary directory để tránh xung đột
    temp_dir = mkdtemp()
    options.add_argument(f"--user-data-dir={temp_dir}")
    
    # Thêm các arguments để bypass detection với User-Agent phù hợp OS
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(f"--user-agent={os_config['user_agent']}")
    
    # Thêm các arguments để sửa lỗi kết nối
    options.add_argument("--disable-web-security")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--ignore-ssl-errors")
    options.add_argument("--ignore-certificate-errors-spki-list")
    options.add_argument("--disable-features=VizDisplayCompositor")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-first-run")
    options.add_argument("--disable-default-apps")
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-backgrounding-occluded-windows")
    options.add_argument("--disable-renderer-backgrounding")
    
    # Không sử dụng random port để tránh xung đột
    # debug_port = random.randint(9000, 9999)
    # options.add_argument(f"--remote-debugging-port={debug_port}")
    
    # Tạo WebDriver với timeout
    driver = webdriver.Chrome(options=options)
    
    # Thiết lập timeout để tránh lỗi kết nối
    driver.set_page_load_timeout(30)
    driver.implicitly_wait(10)
    
    print("✅ Chrome WebDriver khởi tạo thành công!")
    print(f"📁 Sử dụng temporary profile: {temp_dir}")
    print(f"🌐 User-Agent: {os_config['user_agent'][:50]}...")
    
    return driver


def test_url(url, description, headless=True, target_os=None):
    """
    Hàm tiện ích để test một URL
    
    Args:
        url (str): URL cần test
        description (str): Mô tả test case
        headless (bool): Chạy ở chế độ headless hay không
        target_os (str): 'linux', 'darwin', 'windows' hoặc None để auto-detect
    
    Returns:
        bool: True nếu thành công, False nếu lỗi
    """
    print(f"\n🔍 Test với {description}:")
    driver = create_selenium_chrome_driver(headless=headless, target_os=target_os)
    
    try:
        driver.get(url)
        print(f"✅ {description} - Title: {driver.title}")
        
        # Thêm một số kiểm tra cơ bản
        if driver.current_url:
            print(f"✅ URL hiện tại: {driver.current_url}")
        
        # Kiểm tra có content không
        body = driver.find_element("tag name", "body")
        if body and len(body.text) > 0:
            print(f"✅ Trang có nội dung (độ dài: {len(body.text)} ký tự)")
        
        driver.quit()
        return True
        
    except Exception as e:
        print(f"❌ Lỗi khi truy cập {description}: {str(e)[:100]}...")
        driver.quit()
        return False


def test_medium_with_all_os():
    """
    Test Medium với tất cả các OS config để tìm cái nào hoạt động tốt nhất
    """
    print("\n🔄 Test Medium với tất cả OS configs:")
    
    medium_url = "https://medium.com"
    os_list = ['linux', 'darwin', 'windows']
    
    for os_name in os_list:
        print(f"\n🔍 Test Medium với {os_name} config:")
        driver = create_selenium_chrome_driver(headless=True, target_os=os_name)
        
        try:
            driver.get(medium_url)
            print(f"✅ Medium ({os_name}) - Title: {driver.title}")
            driver.quit()
            return os_name  # Trả về OS config đầu tiên hoạt động
        except Exception as e:
            print(f"❌ Lỗi với {os_name} config: {str(e)[:100]}...")
            driver.quit()
    
    print("❌ Không có OS config nào hoạt động với Medium")
    return None


# =================== CÁCH SỬ DỤNG ===================

if __name__ == "__main__":
    print("=== Demo Selenium Chrome WebDriver (Multi-OS Support) ===\n")
    
    # Danh sách các trang web để test
    test_sites = [
        ("https://www.google.com", "Google"),
        ("https://en.wikipedia.org/wiki/Machine_learning", "Wikipedia"),
        ("https://github.com", "GitHub"),
        ("https://stackoverflow.com", "Stack Overflow"),
    ]
    
    # Test các trang web chính với OS hiện tại
    print("🔄 Test với cấu hình OS hiện tại:")
    successful_tests = 0
    total_tests = len(test_sites)
    
    for url, description in test_sites:
        if test_url(url, description, headless=True):
            successful_tests += 1
    
    print(f"\n📊 Kết quả với OS hiện tại: {successful_tests}/{total_tests} tests thành công")
    
    # Test riêng với Medium để tìm OS config tốt nhất
    print("\n" + "="*60)
    print("🔍 Test đặc biệt với Medium để tìm OS config tốt nhất:")
    
    # Test Medium với tất cả OS configs
    working_os = test_medium_with_all_os()
    
    if working_os:
        print(f"\n🎉 Tìm thấy OS config hoạt động: {working_os}")
        print(f"🔄 Test thêm với article URL...")
        
        article_url = "https://medium.com/decodingml/a-real-time-retrieval-system-for-rag-on-social-media-data-9cc01d50a2a0"
        driver = create_selenium_chrome_driver(headless=True, target_os=working_os)
        
        try:
            driver.get(article_url)
            print(f"✅ Medium Article ({working_os}) - Title: {driver.title}")
            
            # Thử lấy article content
            try:
                h1_elements = driver.find_elements("tag name", "h1")
                if h1_elements:
                    print(f"✅ Article Title: {h1_elements[0].text}")
            except Exception as e:
                print(f"⚠️  Không lấy được article title: {e}")
                
        except Exception as e:
            print(f"❌ Article URL vẫn lỗi: {str(e)[:100]}...")
        
        driver.quit()
    else:
        print("❌ Không tìm thấy OS config nào hoạt động với Medium")
        print("💡 Có thể do cơ chế chống bot mạnh hoặc cấu hình mạng")
    
    print("\n" + "="*60)
    print("🎉 Hoàn thành! Selenium WebDriver với multi-OS support.")
    print("📝 Lưu ý:")
    print("   - Code tự động detect OS và sử dụng config phù hợp")
    print("   - Có thể force sử dụng config của OS khác bằng target_os")
    print("   - Linux config có thể hoạt động tốt hơn với một số trang web")
    print("\n🛠️  Cách sử dụng:")
    print("   # Tự động detect OS:")
    print("   driver = create_selenium_chrome_driver(headless=True)")
    print("   ")
    print("   # Force sử dụng Linux config:")
    print("   driver = create_selenium_chrome_driver(headless=True, target_os='linux')")
    print("   ")
    print("   # Force sử dụng Windows config:")
    print("   driver = create_selenium_chrome_driver(headless=True, target_os='windows')")
    print("   ")
    print("   driver.get('https://example.com')")
    print("   # Làm việc với driver...")
    print("   driver.quit()") 