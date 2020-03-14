from selenium import webdriver

driver = webdriver.Chrome()

driver.get("https://google.com")

title = driver.title
print(title)

driver.close()
