from SelScrape import SelScrape
import time as t


Scrape=SelScrape("Driver\chromedriver.exe")

Scrape.Open()
Scrape.NavTo("https://www.google.com")

CookieButton=Scrape.Get_Element_By_xpath("//*[@id=\"L2AGLb\"]/div")
CookieButton.click()
searchbar=Scrape.Get_Element_By_xpath("/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input")
Scrape.WriteToElement(searchbar,"Youtube")
t.sleep(100)


