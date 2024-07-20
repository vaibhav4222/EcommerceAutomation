import pytest
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="class")
def setup(request):
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.maximize_window()
    driver.implicitly_wait(10)
    driver.get("https://www.demoblaze.com/")

    request.cls.driver = driver
    yield
    driver.quit()


@pytest.mark.usefixtures("setup")
class TestECommerce:

    def read_credentials(self):
        df = pd.read_excel('C:/Users/Prashant Kubal/Desktop/Credentials.xlsx', sheet_name='LoginData')
        return df

    def read_payment_details(self):
        df = pd.read_excel('C:/Users/Prashant Kubal/Desktop/Credentials.xlsx', sheet_name='PaymentDetails')
        return df

    def handle_alert(self):
        try:
            alert = self.driver.switch_to.alert
            alert.accept()  # Accept the alert if present
        except:
            pass  # Ignore if no alert present

    def test_signup_negative(self):
        driver = self.driver
        credentials = self.read_credentials()
        signup_username = credentials.iloc[0, 0]

        driver.find_element(By.XPATH, "(//a[normalize-space()='Sign up'])[1]").click()
        time.sleep(1)
        username_field = driver.find_element(By.XPATH, "//input[@id='sign-username']")
        username_field.send_keys(signup_username)

        time.sleep(1)
        driver.find_element(By.XPATH, "//button[normalize-space()='Sign up']").click()
        time.sleep(1)

        self.handle_alert()

        # Clear the username field after handling the alert
        username_field.clear()
        time.sleep(1)

    def test_signup_positive(self):
        driver = self.driver
        credentials = self.read_credentials()
        signup_username = credentials.iloc[0, 0]
        signup_password = credentials.iloc[0, 1]

        driver.find_element(By.XPATH, "//input[@id='sign-username']").send_keys(signup_username)
        time.sleep(1)
        driver.find_element(By.XPATH, "//input[@id='sign-password']").send_keys(signup_password)
        time.sleep(1)
        driver.find_element(By.XPATH, "//button[normalize-space()='Sign up']").click()
        time.sleep(1)

        self.handle_alert()

    def test_login_negative(self):
        driver = self.driver
        credentials = self.read_credentials()
        for index, row in credentials.iterrows():
            driver.find_element(By.XPATH, "(//a[normalize-space()='Log in'])[1]").click()
            time.sleep(2)
            username_field = driver.find_element(By.XPATH, "//input[@id='loginusername']")
            username_field.send_keys(row[0])
            driver.find_element(By.XPATH, "//button[normalize-space()='Log in']").click()
            time.sleep(2)
            self.handle_alert()

            # Clear the username field after handling the alert
            username_field.clear()
            time.sleep(2)

    def test_login_positive(self):
        driver = self.driver
        credentials = self.read_credentials()
        for index, row in credentials.iterrows():
            driver.find_element(By.XPATH, "//input[@id='loginusername']").send_keys(row[0])
            driver.find_element(By.XPATH, "//input[@id='loginpassword']").send_keys(row[1])
            driver.find_element(By.XPATH, "//button[normalize-space()='Log in']").click()
            time.sleep(3)

    def test_product_browsing(self):
        driver = self.driver
        # driver.find_element(By.XPATH, "(//a[@class='nav-link'])[1]").click()
        # time.sleep(2)

        # Scroll page
        element = self.driver.find_element(By.XPATH, "(//button[normalize-space()='Next'])[1]")
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        time.sleep(2)

    def test_navigate_to_last_page(self):
        driver = self.driver
        driver.find_element(By.XPATH, "(//button[normalize-space()='Next'])[1]").click()  # Corrected XPath here
        time.sleep(2)
        # Scroll to a specific vertical position using JavaScript
        scroll_height = 600  # Adjust this value based on your requirement
        script = f"window.scrollTo(0, {scroll_height});"
        driver.execute_script(script)
        time.sleep(2)

    def test_select_last_product(self):
        driver = self.driver
        driver.find_element(By.XPATH, "(//a[normalize-space()='MacBook Pro'])[1]").click()  # Corrected XPath here
        time.sleep(2)

    def test_add_product_to_cart(self):
        driver = self.driver
        driver.find_element(By.XPATH, "(//a[normalize-space()='Add to cart'])[1]").click()
        time.sleep(2)
        self.handle_alert()
    def test_checkout_process_negative(self):
        driver = self.driver
        payment_details = self.read_payment_details().iloc[0]

        driver.find_element(By.XPATH, "//a[normalize-space()='Cart']").click()
        time.sleep(2)
        driver.find_element(By.XPATH, "//button[normalize-space()='Place Order']").click()
        time.sleep(2)

        driver.find_element(By.XPATH, "//button[normalize-space()='Purchase']").click()
        time.sleep(2)
        self.handle_alert()
        time.sleep(1)

    def test_checkout_process_positive(self):
        driver = self.driver
        payment_details = self.read_payment_details().iloc[0]

        driver.find_element(By.ID, 'name').send_keys(str(payment_details['Name']))
        time.sleep(1)
        driver.find_element(By.ID, 'country').send_keys(str(payment_details['Country']))
        time.sleep(1)
        driver.find_element(By.ID, 'city').send_keys(str(payment_details['City']))
        time.sleep(1)
        driver.find_element(By.ID, 'card').send_keys(str(payment_details['Credit Card']))
        time.sleep(1)
        driver.find_element(By.ID, 'month').send_keys(str(payment_details['Month']))
        time.sleep(1)
        driver.find_element(By.ID, 'year').send_keys(str(payment_details['Year']))
        time.sleep(1)

        driver.find_element(By.XPATH, "//button[normalize-space()='Purchase']").click()
        time.sleep(2)

        driver.find_element(By.XPATH, "//button[normalize-space()='Purchase']").click()
        time.sleep(2)

        driver.find_element(By.XPATH, "//button[normalize-space()='OK']").click()
        time.sleep(2)

    def test_Logout(self):
            driver = self.driver
            driver.find_element(By.XPATH, "(// a[normalize-space() = 'Log out'])[1]").click()
            time.sleep(2)


    # if __name__ == "__main__":
    #     pytest.main()
