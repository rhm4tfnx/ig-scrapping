import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

class Mamat():


    def __init__(self,username,password,target):
        self.username = username
        self.password = password
        self.target = target
        # self.total = total
        PATH = 'C:\Program Files (x86)/chromedriver'
        self.driver = webdriver.Chrome(PATH)
        self.timeout = 10


    def login(self):
        driver = self.driver
        driver.get('https://www.instagram.com/accounts/login')
        x = self.timeout
        userElement = WebDriverWait(driver,x).until(
            EC.presence_of_element_located((
                By.NAME, 'username')))
        userElement.send_keys(self.username)

        passElement = WebDriverWait(driver,x).until(
            EC.presence_of_element_located((
                By.NAME, 'password')))
        passElement.send_keys(self.password)

        login = WebDriverWait(driver,x).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[3]/button')))
        try:
            login.click()
            time.sleep(5)
            print(f'Log in Succes {self.username}')
        except Exception as er:
            print(f'Login Error with {self.username}')
        

    def imagePosts(self):
        self.login()
        driver = self.driver
        driver.get('https://www.instagram.com/'+self.target)
        time.sleep(3)
        strpost = WebDriverWait(driver,self.timeout).until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/main/div/header/section/ul/li[1]'))).text
        self.countPost = int(strpost.replace(',','').split(' ')[0])
        if self.countPost >= 1:
            print('found post :',self.countPost,self.target,'trying to scrapping ...')
            for _ in range(self.countPost // 7):
                ActionChains(driver).send_keys(Keys.END).perform()
                time.sleep(3)
            linkpost = driver.find_elements_by_xpath("//a[contains(@href,'/p/')]")
            listpost = []
            link = []
            for i in linkpost:
                if i.get_attribute('href'):
                    listpost.append(i.get_attribute('href'))
                else:
                    continue
            print('Succes get {} post'.format(len(listpost)))
            print('get image ..') 
            for i in listpost:
                driver.get(i)
                try:
                    image = WebDriverWait(driver,self.timeout).until(EC.presence_of_element_located((By.CLASS_NAME,'FFVAD'))).get_attribute('src')
                    link.append(image)
                except Exception:
                    print('')
                # try:
                #     video = WebDriverWait(driver,self.timeout).until(EC.presence_of_element_located((By.CLASS_NAME, 'tWeCl'))).get_attribute('src')
                #     link.append(video)
                # except Exception:
                #     print('')
                # caption = WebDriverWait(driver,self.timeout).until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/main/div/div[1]/article/div/div[2]/div/div[2]/div[1]/ul/div/li/div/div/div[2]/span'))).text
                # link.append(caption)
            print('Succes get {} image'.format(len(link)))
            try:
                os.mkdir(os.path.join(os.getcwd(),'ImageResult'))
                print('Creating Directory ..')
            except Exception:
                print('Directory ImageResult already exists')
            links = list(set(link))
            count = 1
            for url in links:
                r = requests.get(url)
                with open('ImageResult/pict'+str(count)+'.jpg','wb') as file:
                    file.write(r.content)
                count += 1
            #create folder
            print('File Succesfuly save')
        else:
            print('total post -> ',self.countPost)
            print('Users Havent post')

    # def main(self):
    #     input_username = input('[REQUIRED] Enter your username account : ')
    #     input_password = input('[REQUIRED] Enter Your password account : ')
    #     who = input('Enter username account for scrapping : ')
    #     self.im
def main():
    print('{LOGIN!}')
    # input('[REQUIRED] Enter your username account :')
    user_ig = 'yourusername'
    # input('[REQUIRED] Enter your password account :')
    pass_ig = 'yourpassword'
    # ig account to scrapping
    who = input('Enter username account for scrapping :')
    user = Mamat(user_ig,pass_ig,who)    
    user.imagePosts()

if __name__ == '__main__':
    main()
