from playwright.sync_api import Playwright, sync_playwright, TimeoutError
from playwright._impl._api_types import Error
import asyncio
from datetime import datetime

# https://playwright.dev/python/docs/intro/

class browser_operate():
    def __init__(self):
        # playwrightハンドラーを使用してリソースの管理を行う
        # 'chromium'を使ってMicrosoft Edgeを操作。
        # ヘッドフルモードで起動。ヘッドレスモードでは正常にタイトルが読み込めなかった
        self.playwright = sync_playwright().__enter__()
        self.browser = self.playwright.chromium.launch(headless=False)
        self.page = self.browser.new_page()

        # Emailでログインするメソッドを実行
        self.login_menoy_foward()

            
    def login_menoy_foward(self):
        # ログインの実行
        url = "https://moneyforward.com/"
        self.page.goto(url)
        print("ブラウザ 起動")
        self.page.click("a:text('ログイン')")
        self.page.click("p:text('メールアドレスでログイン')")
        self.page.fill("input[class='m3YGqu2j inputItem']","input-your-email-address")
        self.page.click("input[value='同意してログインする']")
        self.page.fill("input[class='I_c0y7tJ input-field M_ePduw4 inputItem MHLhKz7Z']","input-your-password")
        self.page.click("input[value='ログインする']")
        self.page.wait_for_selector("a[href='/sign_out']", timeout=30000)
        print("ログイン 成功")

    def input_data(self, input_data_list):
        # 支払い項目ごとに入力する関数
        # 例：input_data_list = ['2023/5/10', '⑨シルベーヌ 5個', '324', 'dn1', 'dn11', '手持ちの財布']
        self.input_date_data(input_data_list[0])

        self.input_payment_data(input_data_list[1])

        self.input_price_data(input_data_list[2])

        self.input_group_data(input_data_list[3],input_data_list[4])

        self.input_wallet_data(input_data_list[5])

        self.save_data()


    def input_date_data(self, date):
        #日付の入力　現在の日付を取得
        today = self.page.eval_on_selector("#js-cf-manual-payment-entry-updated-at-label", "el => el.textContent")

        # 入力する日と何か月差があるか 文字列をdatetimeオブジェクトに変換して計算
        date_format = "%Y/%m/%d"
        input_date = datetime.strptime(date, date_format)
        today = datetime.strptime(today, date_format)

        # 年と月の差を計算
        year_diff = input_date.year - today.year
        month_diff = year_diff*12 + input_date.month - today.month

        # カレンダーの表示、日付をクリック
        if month_diff < 0:
            target_class = "th[class='prev']"
        else:
            target_class = "th[class='next']"

        
        self.page.click("p[id='js-cf-manual-payment-entry-calendar']")
        for i in range(abs(month_diff)):
            self.page.click(target_class)

        target_date = "td.day:not(.old):not(.new):text('" + str(input_date.day) + "')"
        self.page.click(target_date)

        # チェック
        check_date = self.page.eval_on_selector("#js-cf-manual-payment-entry-updated-at-label", "el => el.textContent")
        

    def input_group_data(self, large_group, middle_group):
        # 大項目、中項目を指定する。
        # Selecterではないドロップダウンリスト。click関数を使用して値を指定する
        large_group_selector = 'a.l_c_name:text("' + large_group + '")'
        middle_group_selector = 'a.m_c_name:text("' + middle_group + '")'
        self.page.click("a#js-large-category-selected")
        self.page.click(large_group_selector)
        self.page.click("a#js-middle-category-selected")
        self.page.click(middle_group_selector)

    def input_wallet_data(self, wallet_name):
        # ドロップダウンリストから支出元を指定する。Selecterのドロップダウンリスト
        self.page.select_option("#user_asset_act_sub_account_id_hash", wallet_name)

    def input_price_data(self, price):
        # 入力欄に値を入力する
        self.page.fill("input[id='js-cf-manual-payment-entry-amount']",price)

    def input_payment_data(self, payment):
        # 入力欄に値を入力する
        self.page.fill("input[id='js-cf-manual-payment-entry-content']",payment)

    def save_data(self):
        # 保存を行う
        self.page.click("input[id='js-cf-manual-payment-entry-submit-button']")

        # 保存内容が表示されるまで待機
        self.page.wait_for_selector("input[id='js-cf-manual-payment-entry-submit-button']", timeout=30000)
        print("保存 成功")

    def browser_close(self):
        # ブラウザを閉じる
        self.browser.close()
        print("ブラウザ 終了")

#browser_operate() 
# main.browser_close()