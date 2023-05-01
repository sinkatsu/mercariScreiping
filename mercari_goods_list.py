from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
import random
import time

options = webdriver.chrome.options.Options()
#久しぶりに起動する際はprofile_pathのディレクトリ内のデータを消して再び手動でログインしなおす
profile_path = r"C:\Users\watas\AppData\Local\Google\Chrome\User Data\mercari"
options.add_argument('--user-data-dir=' + profile_path)
CHROMEDRIVER = "C:\data\chromedriver_win32\chromedriver.exe"

# ドライバー指定でChromeブラウザを開く
# browser = webdriver.Chrome(CHROMEDRIVER,options=options)
browser = webdriver.Chrome(ChromeDriverManager().install(),options=options)
browser.get('https://google.com')

def main():
    #画面遷移系
    url = "https://www.mercari.com/jp/mypage/listings"
    browser.get(url)
    url = "https://jp.mercari.com/mypage/listings/completed"
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
    posts=browser.find_elements_by_css_selector('a[data-location="listed_item_list:completed:item"]')
    browser.implicitly_wait(2)
    goods_urls = []
    address_list= []
    item_ls = []
    
    for j in range(len(posts)):
        goods_urls.append(posts[j].get_attribute("href"))
        # print(goods_urls)
        print(j)
        
    time.sleep(3)
    
    for i in range(len(goods_urls)):
        #垢バン対策
        s=random.uniform(2, 4)
        time.sleep(s)
        #商品名、値段、状態情報取得
        #商品詳細url取得
        goods_url=goods_urls[i]
        print(goods_url)
        goods_detail_url=goods_url.replace('transaction','item')
        #詳細ページに遷移
        browser.get(goods_url)
        browser.implicitly_wait(3)
        time.sleep(3)
        
        #商品ページに遷移
        browser.get(goods_detail_url)
        #商品名取得
        title=browser.find_element_by_xpath('//*[@id="item-info"]/section[1]/div/div/div/h1').text
        item_price =browser.find_element_by_xpath('/html/body/div[1]/div/div[2]/main/article/div[2]/section[1]/section[1]/div/div/span[2]').text
        print(title)
        print(item_price)
            
        #リスト作成
        a=["●"+title+"\n"+item_price+"円"]
        item_ls.append(a)
        browser.back()
            
        #商品一覧ページに戻る
        browser.back()
        print(i)
        browser.implicitly_wait(2)
    
    print(item_ls)
    
    #テキストデータ生成
    with open("customer_data.txt","w") as o:
        for row in item_ls:
            o.write(",".join(map(str, row)) + "\n") 
    
    #chromeを閉じる
    browser.quit()
    return print("Finish!")

main()