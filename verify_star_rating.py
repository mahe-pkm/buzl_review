import time
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run_test():
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    # Initialize Chrome driver
    driver = webdriver.Chrome(options=chrome_options)
    
    # URL to load
    url = "https://localhost:7894/397"
    
    # Test cases
    test_cases = [
        {
            "name": "Excellent",
            "text": "I had a wonderful experience! The teaching staff was excellent and very friendly. Highly recommended!",
            "expected": "Excellent (5/5)"
        },
        {
            "name": "Good",
            "text": "The classroom was good. Faculty was helpful.",
            "expected": "Good (4/5)"
        },
        {
            "name": "Average",
            "text": "The experience was average. Ok quality, but normal outcomes.",
            "expected": "Average (3/5)"
        },
        {
            "name": "Poor",
            "text": "The faculty here were quite disappointing. I had higher expectations, but the teaching staff did not meet them. Would not recommend based on my experience.",
            "expected": "Poor (2/5)"
        },
        {
            "name": "Poor (worst)",
            "text": "horrible quality and unhelpful staff. worst ever!",
            "expected": "Poor (2/5)"
        }
    ]
    
    results = []
    success = True
    
    try:
        print(f"Loading URL: {url}")
        driver.get(url)
        time.sleep(3)  # Wait for page/JS to load completely
        
        # Make the draft section visible so selenium can interact with the textarea
        driver.execute_script("document.getElementById('draft-section').style.display = 'block';")
        time.sleep(1)
        
        # Locate the textarea
        textarea = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "draft-textarea"))
        )
        
        for case in test_cases:
            print(f"\nRunning test case: {case['name']}")
            print(f"Input text: '{case['text']}'")
            
            # Clear textarea using backspaces or clear()
            # Sometimes clear() doesn't fire event correctly in all drivers, let's do clear then check.
            textarea.clear()
            textarea.send_keys(case['text'])
            
            # Wait for some time to let dynamic updates happen
            time.sleep(1)
            
            # Retrieve output text
            star_text_element = driver.find_element(By.ID, "draft-star-text")
            actual_text = star_text_element.text
            
            print(f"Expected: '{case['expected']}'")
            print(f"Actual: '{actual_text}'")
            
            matched = (actual_text == case['expected'])
            results.append({
                "name": case["name"],
                "input": case["text"],
                "expected": case["expected"],
                "actual": actual_text,
                "passed": matched
            })
            
            if not matched:
                success = False
                
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        success = False
    finally:
        driver.quit()
        
    print("\n" + "="*40)
    print("TEST RESULTS SUMMARY")
    print("="*40)
    for res in results:
        status = "PASSED" if res["passed"] else "FAILED"
        print(f"[{status}] {res['name']}:")
        print(f"  Expected: {res['expected']}")
        print(f"  Actual:   {res['actual']}")
    
    return success

if __name__ == "__main__":
    ok = run_test()
    sys.exit(0 if ok else 1)
