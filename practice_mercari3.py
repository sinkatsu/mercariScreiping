from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
from selenium.common.exceptions import NoSuchElementException
import random
import time

options = webdriver.chrome.options.Options()
profile_path = r"C:\Users\watas\AppData\Local\Google\Chrome\User Data\mercari"
# profile_directory= "Profile 1"
# profile_path = "C:\\Users\\watas\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
options.add_argument('--user-data-dir=' + profile_path)
# options.add_argument('--profile-directory' + profile_directory)
CHROMEDRIVER = "C:\data\chromedriver_win32\chromedriver.exe"

# ドライバー指定でChromeブラウザを開く
browser = webdriver.Chrome(CHROMEDRIVER,options=options)
# browser = webdriver.Chrome(ChromeDriverManager().install())
browser.get('https://google.com')

# browser.get('https://www.google.com/')


def main():
    #画面遷移系
    url = "https://www.mercari.com/jp/mypage/listings"
    browser.get(url)
    url = "https://jp.mercari.com/mypage/listings/in_progress"
    browser.get(url)
    time.sleep(3)
    
    try:
        #もっと見るボタンがあれば押下
        element_btn = browser.find_element_by_css_selector('#inTransaction > div > mer-button > button')
        element_btn.click()
        time.sleep(2)

    except NoSuchElementException:
        print("要素がありませんでした...")

    else:
        print(element_btn.text)
    
    #出品した商品の全ての商品データを抽出
    #aタグを探す
    posts=browser.find_elements_by_css_selector('a[data-location="listed_item_list:in_progress:item"]')
    browser.implicitly_wait(2)
    goods_urls = []
    address_list= []
    
    for j in range(len(posts)):
        goods_urls.append(posts[j].get_attribute("href"))
        print(goods_urls)
        print(j)
        
    time.sleep(3)
    
    for i in range(len(goods_urls)):
        #垢バン対策
        s=random.uniform(2, 5)
        time.sleep(s)
        #商品名、値段、状態情報取得
        #商品詳細url取得
        goods_url=goods_urls[i]
        print(goods_url)
        goods_detail_url=goods_url.replace('transaction','item')
        #詳細ページに遷移
        browser.get(goods_url)
        browser.implicitly_wait(5)
        
        #「発送をしてください」の文章を取得する
        # status_text=browser.find_element_by_xpath('/html/body/div/div[1]/div/div/div/div/main/div/div[2]/mer-information-bubble/mer-text[1]')
        status_text=browser.find_element_by_xpath('/html/body/div/div/div/main/div/div[2]/mer-information-bubble/mer-text[1]')
        

        if status_text.text == "発送をしてください":
            
            addresss=browser.find_elements_by_xpath('/html/body/div[1]/div[1]/div/div/div/div/main/div/div[1]/div/div/div[3]/mer-display-row/span[2]/div')
            address=addresss[0].text
            print(addresss[0].text)
            browser.implicitly_wait(3)
            time.sleep(3)
            
            #商品ページに遷移
            browser.get(goods_detail_url)
            #商品名取得
            title=browser.find_element_by_xpath('//*[@id="item-info"]/section[1]/div/div/div/h1').text
            print(title)
            
            a=["●"+title+"\n"+address]
            address_list.append(a)
            browser.back()
        else:
            print("住所なし")
            
        #商品一覧ページに戻る
        browser.back()
        print(i)
        browser.implicitly_wait(2)
    
    print(address_list)
    
    #テキストデータ生成
    with open("customer_data.txt","w") as o:
        for row in address_list:
            o.write(",".join(map(str, row)) + "\n") 
    
    #chromeを閉じる
    browser.quit()
    return print("Finish!")

main()