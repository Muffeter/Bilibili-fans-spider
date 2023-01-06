from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import csv

def initDriver(url):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    actions = ActionChains(driver)
    driver.get(url)
    driver.get(url)
    driver.implicitly_wait(10)
    return driver, actions

def getPageNum(driver):
    text = driver.find_element("xpath", '//ul[@class="be-pager"]/span[@class="be-pager-total"]').get_attribute("textContent").split(' ')
    return text[1]

def goNextPage(driver, actions):
    bottom = driver.find_element("xpath", '//li[@class="be-pager-next"]/a')
    actions.click(bottom)
    actions.perform()
    actions.reset_actions()

def getCard(li, actions):
    cover = li.find_element("xpath", './/a[@class="cover"]')
    actions.move_to_element(cover)
    actions.perform()
    actions.reset_actions()

def writeData(driver):
    #get card list
    cardList = driver.find_elements("xpath", '//div[@id="id-card"]')
    for card in cardList:
        up_name = card.find_element("xpath", './/img[@class="idc-avatar"]').get_attribute("alt")
        up_fansNum = card.find_elements('css selector','span.idc-meta-item')[1].get_attribute("textContent")
        print(f'name:{up_name}, {up_fansNum}')
        #write info into csv file
        with open('.\\date.csv', mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([up_name, up_fansNum])

def spawn(driver, actions):
    #get card list
    ulList = driver.find_elements("xpath", '//ul[@class="relation-list"]/li')
    #spawn card
    for li in ulList:
        getCard(li, actions)
        time.sleep(2)
    
def spawnCards(page, driver, actions):
    #遍历所有页
    for i in range(1,int(page) + 1):
        print(f"get data in page {i}\n")
        spawn(driver, actions)
        if (i != int(page)):
            #翻页
            goNextPage(driver, actions)
            time.sleep(6) 

def main():
    #init driver
    uid = input("bilibili uid:")
    url = "https://space.bilibili.com/" + uid + "/fans/fans"
    driver, actions = initDriver(url)
    page = getPageNum(driver)

    #生成card信息(ajax)
    spawnCards(page, driver, actions)
    writeData(driver)

    driver.quit()

if __name__ == "__main__":
    main()