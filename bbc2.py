from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
from urllib.request import Request,urlopen
from bs4 import BeautifulSoup
BBCUrl="http://bbcsfx.acropolis.org.uk"
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument("--headless")

def WaitWebLoaded(driver):
    IsPageLoaded=False
    while not IsPageLoaded:
        try:
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".progress.wclear")))
            IsPageLoaded=True
        except:
            driver.refresh()
            print("Loading current page again")
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


#url='http://bbcsfx.acropolis.org.uk'
def GetCatUrl(cat):
    CatUrl=BBCUrl+'/?cat='+cat
    return CatUrl

def SaveWavToDir(BBCWavName,output_dir,output_name):
    BBCWavSource = "http://bbcsfx.acropolis.org.uk/assets/"
    WavSouce=BBCWavSource+BBCWavName
    #print(WavSouce)
    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    req = Request(WavSouce, headers=headers)
    IsDone=False
    while not IsDone:
        try:
            r = urlopen(req)
            wav = r.read()
            print(r.getcode())
            IsDone=True
        except:
            time.sleep(5)
            print("-------reload file---------")

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
    #
    catlist1=catlist[135:]
    #print(catlist[98:])
    SearchCatUrlListForPages(catlist1)

#SearchCatUrlListForPages(["http://bbcsfx.acropolis.org.uk/?cat=abbeys"])


