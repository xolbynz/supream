from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
# 크롬 옵션 설정 (필요에 따라 headless 등 추가 가능)
chrome_options = Options()
# chrome_options.add_argument("--headless")  # 브라우저 창을 띄우지 않으려면 주석 해제

# 크롬 드라이버 서비스 경로 설정 (chromedriver가 PATH에 있으면 생략 가능)
service = Service()  # chromedriver 경로를 지정하려면 Service('/path/to/chromedriver')

# 크롬 브라우저 열기
driver = webdriver.Chrome(service=service, options=chrome_options)

# Supreme 신상품 페이지 열기
driver.get("https://shop.supreme.com/collections/new")

# 상품 리스트가 로드될 때까지 대기
wait = WebDriverWait(driver, 10)
product_ul = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "#MainContent > div > div > ul[data-testid='product-list']"))
)

# 상품 리스트의 각 li 요소 추출
product_items = product_ul.find_elements(By.TAG_NAME, "li")

for item in product_items:
    try:
        # 상품명
        name = item.find_element(By.CSS_SELECTOR, "span.sc-2s21k7-0").text
    except:
        name = ""
    try:
        # 가격
        price = item.find_element(By.CSS_SELECTOR, "span[aria-label='product price']").text
    except:
        price = ""
    try:
        # 이미지 URL 및 alt
        img_elem = item.find_element(By.TAG_NAME, "img")
        img = img_elem.get_attribute("src")
        img_alt = img_elem.get_attribute("alt")
    except:
        img = ""
        img_alt = ""
    try:
        # 상품 상세 링크
        link = item.find_element(By.CSS_SELECTOR, "a[data-testid='react-router-link']").get_attribute("href")
    except:
        link = ""
    try:
        # 품절 여부
        soldout = item.find_element(By.CSS_SELECTOR, "p[data-testid='sold-out-product-message']").text
    except:
        soldout = ""
    # item의 전체 text 추출
    try:
        item_text = item.text
    except:
        item_text = ""
    while True:
        if "Micro Dwon Half Zip" in img_alt and "Silver"  in img_alt:
            # Brushed Stripe Sweater 상품을 클릭해서 상세 페이지로 이동
            try:
                link_elem = item.find_element(By.CSS_SELECTOR, "a[data-testid='react-router-link']")
                driver.execute_script("arguments[0].click();", link_elem)
                print("Micro Dwon Half Zip 상세 페이지로 이동했습니다.")

                # 상세 페이지가 로드될 때까지 대기 (add-to-cart-button 등장까지)
                wait = WebDriverWait(driver, 60)
                add_to_cart_btn = wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='add-to-cart-button']"))
                )
                time.sleep(0.5)
                # add-to-cart-button 클릭
                # 사이즈 드롭다운에서 Medium 선택
                try:
                    size_select = driver.find_element(By.CSS_SELECTOR, "select[data-testid='size-dropdown']")
                    for option in size_select.find_elements(By.TAG_NAME, "option"):
                        if option.text.strip().lower() == "medium":
                            option.click()
                            print("사이즈 Medium 선택 완료")
                            break
                except Exception as e:
                    print("사이즈 선택 중 오류:", e)

                add_to_cart_btn.click()
                print("add to cart 버튼을 클릭했습니다.")

                # checkout now 버튼이 나타날 때까지 대기
                try:
                    # mini-cart가 뜰 때까지 대기
                    mini_cart_checkout_btn = WebDriverWait(driver, 60).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-testid='mini-cart-checkout-link']"))
                    )
                    # checkout now 클릭
                    mini_cart_checkout_btn.click()
                    print("checkout now 버튼을 클릭했습니다.")

                    # --- Checkout 폼 자동 입력 ---
                    # 이메일 등 정보 입력
                    try:
                        # 이메일
                        email_input = WebDriverWait(driver, 100000).until(
                            EC.presence_of_element_located((By.ID, "email"))
                        )
                        email_input.clear()
                        email_input.send_keys("rnjs5162@gmail.com")

                        # Last name
                        last_name_input = driver.find_element(By.ID, "TextField0")
                        last_name_input.clear()
                        last_name_input.send_keys("")

                        # First name
                        first_name_input = driver.find_element(By.ID, "TextField1")
                        first_name_input.clear()
                        first_name_input.send_keys("")

                        # Postal code
                        postal_code_input = driver.find_element(By.ID, "TextField2")
                        postal_code_input.clear()
                        postal_code_input.send_keys("")

                        # Country/Region
                        country_select = driver.find_element(By.ID, "Select0")
                        for option in country_select.find_elements(By.TAG_NAME, "option"):
                            if option.get_attribute("value") == "KR":
                                option.click()
                                break

                        # Province
                        province_select = driver.find_element(By.ID, "Select1")
                        for option in province_select.find_elements(By.TAG_NAME, "option"):
                            if "gwangju city" in option.text or "광주" in option.text:
                                option.click()
                                break

                        # City
                        city_input = driver.find_element(By.ID, "TextField3")
                        city_input.clear()
                        city_input.send_keys("")

                        # Address1
                        address1_input = driver.find_element(By.ID, "TextField4")
                        address1_input.clear()
                        address1_input.send_keys("")

                        # Address2 (optional)
                        try:
                            address2_input = driver.find_element(By.ID, "TextField5")
                            address2_input.clear()
                            address2_input.send_keys("")
                        except Exception:
                            pass

                        # Phone
                        phone_input = driver.find_element(By.ID, "TextField6")
                        phone_input.clear()
                        phone_input.send_keys("")

                        # "More Payment Options" 클릭 후 카카오페이 선택
                        try:
                            # "More Payment Options" 라디오 버튼 클릭
                            more_payment_radio = driver.find_element(By.ID, "basic-More Payment Options")
                            driver.execute_script("arguments[0].click();", more_payment_radio)
                            print('"More Payment Options" 라디오 버튼을 클릭했습니다.')
                            # "Kakao" 라디오 버튼을 찾아 클릭 (카카오페이 결제 방식 선택)
                            try:
                                # "Kakao" 라디오 버튼은 id="choice-81"로 추정됨
                                kakao_radio = driver.find_element(By.ID, "choice-81")
                                driver.execute_script("arguments[0].click();", kakao_radio)
                                print('"Kakao" 라디오 버튼을 클릭했습니다.')

                            except Exception as e:
                                print('"Kakao" 라디오 버튼 클릭 중 오류:', e)

                            print("카카오페이 버튼을 클릭했습니다.")
                        except Exception as e:
                            print("카카오페이 결제 선택 중 오류:", e)
                        except Exception:
                            pass

                        # Date of Birth (YYYY-MM-DD)
                        try:
                            dob_input = driver.find_element(By.ID, "PaymentAdditionalField-Cards-PersonalCardDateOfBirth")
                            dob_input.clear()
                            dob_input.send_keys("")
                        except Exception:
                            pass

                        # PIN CODE first two digits
                        try:
                            pin_input = driver.find_element(By.ID, "PaymentAdditionalField-Cards-PersonalCardPinCodeFirstTwoDigits")
                            pin_input.clear()
                            pin_input.send_keys("")
                        except Exception:
                            pass

                        # 약관 동의 체크박스들 모두 체크
                        checkbox_ids = [
                            "custom-checkbox-0", "custom-checkbox-1", "custom-checkbox-2",
                            "custom-checkbox-3", "custom-checkbox-4", "custom-checkbox-5", "accept-tos"
                        ]
                        for cid in checkbox_ids:
                            try:
                                cb = driver.find_element(By.ID, cid)
                                if not cb.is_selected():
                                    cb.click()
                            except Exception:
                                pass

                        print("체크아웃 폼 자동 입력 완료")
                    except Exception as e:
                        print("체크아웃 폼 자동입력 중 오류:", e)
                        # TextField8도 개인통관번호 입력
                        try:
                            # TextField7이 나타날 때까지 대기
                            time.sleep(5)
                            tf8_input = WebDriverWait(driver, 30).until(
                                EC.presence_of_element_located((By.ID, "TextField7"))
                            )
                            tf8_input.clear()
                            tf8_input.send_keys("")  # 실제 개인통관번호로 대체 필요
                            print("TextField7 입력 완료")
                        except Exception:
                            pass

                    # "process payment" 버튼 클릭
                        try:
                            pay_button = driver.find_element(By.ID, "checkout-pay-button")
                            driver.execute_script("arguments[0].click();", pay_button)
                            print('"process payment" 버튼을 클릭했습니다.')
                        except Exception as e:
                            print('"process payment" 버튼 클릭 중 오류:', e)
               
    
                except Exception as e:
                    print("checkout now 클릭 중 오류 발생:", e)

                break  # 하나만 클릭하고 루프 종료
            except Exception as e:
                print("클릭 중 오류 발생:", e)
        else:
            print("상품이 아닙니다.")
            driver.refresh()
