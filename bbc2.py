from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from urllib.request import urlopen
from bs4 import BeautifulSoup

BBCUrl="http://bbcsfx.acropolis.org.uk"
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument("--headless")


def WaitWebLoaded(driver):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".progress.wclear")))
    return None

def GetBBCSoundCatList(url):
    driver=webdriver.Chrome(chrome_options=options)
    driver.get(url)
    WaitWebLoaded(driver)
    #print(element)
    soup=BeautifulSoup(driver.page_source,'html.parser')
    cats=soup.find_all('option')
    #print(cats)
    catlist=[]
    for cat in cats:
        cat_modified=cat.string.lower().replace(' ','+')
        cat_modified2=cat_modified.replace('/','%2F')
        cat_modified3=cat_modified2.replace('&','%26')
        catlist.append(cat_modified3)
    catlist=catlist[1:]
    #print("OK")
    return catlist

#print(GetBBCSoundCatList(BBCUrl))
#print(download)
#print(soup.prettify())


def GetCatUrl(cat):
    CatUrl=BBCUrl+'/?cat='+cat
    return CatUrl

def SaveWavToDir(BBCWavName,output_dir,output_name):
    BBCWavSource = "http://bbcsfx.acropolis.org.uk/assets/"
    WavSouce=BBCWavSource+BBCWavName
    #print(WavSouce)
    r = urlopen(WavSouce)
    #print(r.getcode())
    wav = r.read()
    wav_name = output_dir + "/" + output_name+".wav"
    #print(wav_name)
    r.close()
    #print("OK2")
    output = open(wav_name, "wb")
    output.write(wav)
    output.close()
    #print("OK3")



def SearchCatUrlListForPages(CatList):
    for Cat in CatList:
        dir_name=Cat.replace('+','_')        
        print(dir_name)
        os.mkdir(dir_name)
        CatUrl=GetCatUrl(Cat)
        driver = webdriver.Chrome(chrome_options=options)
        driver.get(CatUrl)
        WaitWebLoaded(driver)
        cnt = 0
        while True:

            WaitWebLoaded(driver)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            WavLocations = soup.find_all("a", string="Download")

            for WavLocation in WavLocations:
                cnt += 1
                #print(WavLocation)
                BBCWavSource = WavLocation.get('href').split('/')[-1]
                WavData = WavLocation.get("aria-label")
                WavName = dir_name+"_"+str(cnt)
                SaveWavToDir(BBCWavSource,dir_name,WavName)
                print(f"cnt:{cnt}")

                print(WavData+" done ")

            IsEnd = True if soup.find('a', class_='paginate_button next disabled') != None else False
            print(IsEnd)
            if IsEnd:
                cnt=0
                print(f"~~~~~~~~~~~~{dir_name}  done!~~~~~~~~~~~~~")
                driver.quit()
                break

            driver.find_element_by_link_text('Next').click()


if __name__ == "__main__":
    catlist=GetBBCSoundCatList(BBCUrl)
    SearchCatUrlListForPages(catlist)




