from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
chrome_options = Options()
chrome_options.add_argument("--headless") # run chrome browser without GUI 
import numpy as np

def get_hp(s):
    your_hp = ''
    for i in s:
        if i != '%':
            your_hp += i
        else:
            break
            
    return int(your_hp)

#driver = webdriver.Chrome(executable_path="/mnt/c/Users/wee_j/Documents/Python Notebooks/chromedriver/chromedriver.exe", options=chrome_options)
#driver.close()
#driver.quit()
driver = webdriver.Chrome(executable_path="chromedriver.exe", options=chrome_options)
driver.get('https://www.tppcrpg.net/login.php') # URL destination 
time.sleep(2)

driver.find_element_by_name("LoginID").send_keys('user') # enter your username
driver.find_element_by_name("NewPass").send_keys('password') # enter your password
driver.find_element_by_xpath("//input[@type='submit']").click()
time.sleep(2)

while 1:

    driver.find_element_by_link_text("Trainer Battle").click()
    time.sleep(2)
#99561np.random.choice(["2719620", "3387834"])
    driver.find_element_by_name("Trainer").send_keys("3395547") # Change the trainer ID you want to battle with 
    driver.find_element_by_xpath("//input[@type='submit']").click()
    time.sleep(2)

    driver.find_element_by_xpath("//span[@class='Trainer1']//input[@type='button']").click()
    time.sleep(2)

    while 1:
        
        time.sleep(2)

        print(driver.find_element_by_xpath(r"//ul[@id='battleText']").text)
        
        your_roster = []
        i = 1
        while i!= 0:
            try:
                path = "//*[@id='Trainer1_Pokemon']/ul/li["+str(i)+"]/div/div"
                your_roster.append(get_hp(driver.find_element_by_xpath(path).get_attribute('style').split()[1]))
                i += 1
            except:
                i = 0
                
        opp_roster = []
        i = 1
        while i!= 0:
            try:
                path = "//*[@id='Trainer2_Pokemon']/ul/li["+str(i)+"]/div/div"
                opp_roster.append(get_hp(driver.find_element_by_xpath(path).get_attribute('style').split()[1]))
                i += 1
            except:
                i = 0

        player = driver.find_element_by_xpath("//div[@id='Trainer1_Active']//div[@class='innerContent']//div[@class='hpBar']").get_attribute('title')
        opponent = driver.find_element_by_xpath("//div[@id='Trainer2_Active']//div[@class='innerContent']//div[@class='hpBar']").get_attribute('title')
        your_hp = get_hp(player) 
        opp_hp = get_hp(opponent) 
        time.sleep(2)

        #print("Your HP: %d, Opponent HP: %d"%(your_hp,opp_hp))
        #print("Your Pokemon: ", your_roster)
        #print("Opponent Pokemon: ", opp_roster)
                
        if np.all(np.array(opp_roster) == 0) == True: # Opponent lost.
            print("Battle Won!")
            driver.find_element_by_link_text('Restart Battle').click()
            print("Restarting New Battle...\n")
        elif np.all(np.array(your_roster) == 0) == True: # You lost.
            print("Battle Lost!")
            driver.find_element_by_link_text('Restart Battle').click()
            print("Restarting New Battle...\n")
        else:
            if your_hp > 0 and opp_hp == 0:
                cnt = 0
                while 1:
                    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, r'//*[@class="submit"]')))
                    try:
                        driver.find_element_by_class_name("submit").click()
                        break
                    except:
                        cnt += 1
                        if cnt == 5:
                            break
                if cnt == 5:
                    break

            elif your_hp > 0 and opp_hp > 0:
                cnt = 0
                while 1:
                    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, r'//*[@class="submit"]')))
                    try:
                        driver.find_element_by_class_name("submit").click()
                        break
                    except:
                        cnt += 1
                        if cnt == 5:
                            break
                if cnt == 5:
                    break


            else:
                if len(np.where(np.array(your_roster)>0)) > 0:
                    next_candidate = str(np.min(np.where(np.array(your_roster)>0)))
                    cnt = 0
                    while 1:
                        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//a[@slot='+str(next_candidate)+']')))
                        try:
                            driver.find_element_by_xpath(u'//a[@slot='+str(next_candidate)+']').click()
                            break
                        except:
                            cnt += 1
                            if cnt == 5:
                                break
                    if cnt == 5:
                        break
else:
    driver.close()
    driver.quit()   