
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


driver=[]


class SelScrape:
    def  __init__(self,Dexecutable_path):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(executable_path=Dexecutable_path, options=options)
        driver.close()
        self.executable_path=Dexecutable_path
        self.driver=driver
    def Get_Element_By_Tag(self,tag):
        return self.driver.find_element_by_tag_name(tag)
    def Get_Element_By_Tag(self,tag,attrib,attribvalue):
        return self.driver.find_element_by_xpath(f"//{tag}[@{attrib}=\"{attribvalue}\"")
    def Get_Text_By_Tag(self,tag):
        return self.driver.find_element_by_tag_name(tag).text
    def Get_Text_By_Tag(self,tag,attrib,attribvalue):
        return self.driver.find_element_by_xpath(f"//{tag}[@{attrib}=\"{attribvalue}\"").text
    def Get_Elements_By_Tag(self,tag):
        return self.driver.find_elements_by_tag_name(tag)
    def Get_Elements_By_Tag(self,tag,attrib,attribvalue):
        return self.driver.find_elements_by_xpath(f"//{tag}[@{attrib}=\"{attribvalue}\"")
    def Get_Element_By_xpath(self,xpath):
        return self.driver.find_element_by_xpath(xpath)
    def Get_Elements_By_xpath(self,xpath):
        return self.driver.find_elements_by_xpath(xpath)
    def GetURl(self):
        return self.driver.current_url
    def Open(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(executable_path=self.executable_path, options=options)
    def Close(self):
        self.driver.close() 
    def ScrollToElementXPATH(self,xpath):
        element = self.driver.find_element_by_xpath(xpath)  
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
    def ScrollToElementTag(self,tag):
        element = self.driver.find_element_by_tag_name(tag)  
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
    def ScrollToElementTag(self,tag,attrib,attribvalue):
        element = self.driver.find_element_by_xpath(f"//{tag}[@{attrib}=\"{attribvalue}\"")  
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
    def WriteToElement(self,element,text):
        element.send_keys(text)
    def WriteToElementXPATH(self,xpath,text):
        self.driver.find_element_by_xpath(xpath).send_keys(text) 
    def NavTo(self,url):
        self.driver.get(url)
    def GetWindowsHandles(self):
        return self.driver.window_handles
    def WSwitchTo(self,window):
        self.driver.switch_to.window(window)
    def IFrameSwitch(self,frame):
        self.driver.switch_to.frame(frame)
    def WaitElement(self,tick,xpath):
        return WebDriverWait(self.driver, tick).until(EC.presence_of_element_located((By.XPATH, xpath)))
    def WaitElementTag(self,tick,tagname):
        return WebDriverWait(self.driver, tick).until(EC.presence_of_element_located((By.TAG_NAME, tagname)))
    def WaitElementTag(self,tick,tagname,attrib,attribvalue):
        return WebDriverWait(self.driver, tick).until(EC.presence_of_element_located((By.XPATH, f"//{tagname}[@{attrib}=\"{attribvalue}\"")))


    


        

