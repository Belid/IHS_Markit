import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


class ChromeIhs:

    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_experimental_option("detach", True)
        self.chrome_options.add_experimental_option("prefs", {"download.default_directory": "C:\\Temp\\test_bomcheck"})
        opt = Options()
        opt.add_experimental_option('debuggerAddress', 'localhost:9100')
        self.driver = webdriver.Chrome(executable_path="C:\\bomcheck\\chromedriver.exe", chrome_options=opt)
        self.part_number_list = []
        self.table_list = []
        self.table3_list = []
        self.table4_list = []

    def get_ihs_table_list(self, ordering_text):
        part_start_with = self.driver.find_element(By.XPATH, "/html/body/app/div[1]/bom-header/div/div/div[2]/simplesearch/div/div/div[2]/input")
        part_start_with.send_keys(Keys.CONTROL + 'a', Keys.BACKSPACE)
        part_start_with.send_keys(ordering_text)
        self.driver.find_element(By.XPATH, "/html/body/app/div[1]/bom-header/div/div/div[2]/simplesearch/div/div/span/button/svg-symbol").click()
        time.sleep(3)       # first sleep
        table = self.driver.find_element(By.XPATH, "/html/body/app/div[1]/main-content/div/div/div/part-search/div/part-search-results/div/div/cap-grid-ng/cap-grid-wrapper/ag-grid-angular/div/div[2]/div[2]/div[3]/div[1]")
        self.table_list = list(table.text.splitlines())
        print(self.table_list)
        if len(self.table_list) == 0:
            try:
                self.driver.find_element(By.XPATH, "/html/body/app/modal-placeholder/modal-view/div/div/div/fuzzy-search-modal/modal-header/div/div/button").click()

            except:
                self.refresh(ordering_text)

        return self.table_list

    def download_pdf_ihs(self, current_row):
        print(current_row)
        self.driver.find_element(By.XPATH, "/html/body/app/div[1]/main-content/div/div/div/part-search/div/part-search-results/div/div/cap-grid-ng/cap-grid-wrapper/ag-grid-angular/div/div[2]/div[2]/div[3]/div[1]/div[{}]/div[2]/div/a[2]".format(current_row)).click()
        time.sleep(3)
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def get_status_value(self, current_row):
        if len(self.table_list) < 6:
            self.driver.find_element(By.NAME, "eurohs").click()
            time.sleep(3)
        elif len(self.table_list) > 5:
            self.driver.find_element(By.XPATH, "/html/body/app/div[1]/main-content/div/div/div/part-search/div/part-search-results/div/div/cap-grid-ng/cap-grid-wrapper/ag-grid-angular/div/div[2]/div[2]/div[3]/div[1]/div[{}]/div[2]/div/a[1]".format(current_row)).click()
            time.sleep(2)
            self.driver.find_element(By.XPATH, "/html/body/app/modal-placeholder/modal-view/div/div/div/part-details/modal-window/div[2]/div/div/menu-item-panel/div/ul/li[4]/single-item/div/a/span[1]").click()
            time.sleep(2)
            self.driver.find_element(By.XPATH, "/html/body/app/modal-placeholder/modal-view/div/div/div/part-details/modal-window/div[2]/div/div/menu-item-panel/div/ul/li[4]/ul/li[2]/single-item/div/a/span[1]").click()
            time.sleep(1)
        table1 = self.driver.find_element(By.XPATH, "/html/body/app/modal-placeholder/modal-view/div/div/div/part-details/modal-window/div[2]/div/div/div/grid-panel/cap-grid-ng-wrapper/cap-grid-ng/cap-grid-wrapper/ag-grid-angular/div/div[2]/div[2]/div[3]/div[2]/div/div/div[1]")
        table1_list = list(table1.text.splitlines())
        table2 = self.driver.find_element(By.XPATH, "/html/body/app/modal-placeholder/modal-view/div/div/div/part-details/modal-window/div[2]/div/div/div/grid-panel/cap-grid-ng-wrapper/cap-grid-ng/cap-grid-wrapper/ag-grid-angular/div/div[2]/div[2]/div[3]/div[2]/div/div/div[2]")
        table2_list = list(table2.text.splitlines())
        table3 = self.driver.find_element(By.XPATH, "/html/body/app/modal-placeholder/modal-view/div/div/div/part-details/modal-window/div[2]/div/div/div/grid-panel/cap-grid-ng-wrapper/cap-grid-ng/cap-grid-wrapper/ag-grid-angular/div/div[2]/div[2]/div[3]/div[2]/div/div/div[3]")
        self.table3_list = list(table3.text.splitlines())
        table4 = self.driver.find_element(By.XPATH, "/html/body/app/modal-placeholder/modal-view/div/div/div/part-details/modal-window/div[2]/div/div/div/grid-panel/cap-grid-ng-wrapper/cap-grid-ng/cap-grid-wrapper/ag-grid-angular/div/div[2]/div[2]/div[3]/div[2]/div/div/div[4]")
        self.table4_list = list(table4.text.splitlines())
        print(table1_list)
        print(table2_list)
        print(self.table3_list)
        print(self.table4_list)
        self.check_date()           # return the year
        status = "none"
        if table2_list[0] == "EU RoHS Version" and table2_list[1] == "RoHS 2 (2015/863/EU)":
            status = "C"
        self.driver.find_element(By.XPATH, "/html/body/app/modal-placeholder/modal-view/div/div/div/part-details/modal-window/div[2]/div/part-details-toolbar/div/toolbar/div/div[1]/toolbar-list[2]/div/div/button/span").click()
        self.driver.find_element(By.XPATH, "/html/body/app/modal-placeholder/modal-view/div/div/div/part-details/modal-window/div[2]/div/part-details-toolbar/div/toolbar/div/div[1]/toolbar-list[2]/div/div/div/ul/toolbar-list-item[6]").click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, "/html/body/app/modal-placeholder/modal-view[2]/div/div/div/part-details-print-preview/div[1]/div/div/div/div/div[1]/div[3]/button[1]").click()

        return status

    def check_date(self):
        year = 1999
        if self.table4_list[0] == 'Last Verified Date':
            year = self.table4_list[1]
            year = int(year[6:])
            print(year)
        return year

    def eu_rohs_exemptions(self):
        if self.table3_list[0] == "EU RoHS Exemptions":
            result = self.table3_list[1]
        else:
            result = ""
        return result

    def download_print(self):
        self.driver.find_element(By.XPATH, "/html/body/app/modal-placeholder/modal-view[2]/div/div/div/part-details-print-preview/modal-header/div/div/button").click()
        self.driver.find_element(By.XPATH, "/html/body/app/modal-placeholder/modal-view/div/div/div/part-details/modal-window/div[1]/h3/div[2]").click()

    def error(self):
        self.driver.find_element(By.XPATH, "/html/body/app/modal-placeholder/modal-view/div/div/div/fuzzy-search-modal/div[2]/button[2]").click()
        print("x click")
        time.sleep(3)

    def refresh(self, ordering_text):
        self.driver.get("https://4donline.ihs.com/parts-intelligence/#/search/parts?keyword={}&type=startswith&ignore=true".format(ordering_text))
        time.sleep(2)


def main():
    pass
    # Chrome_IHS()


if __name__ == "__main__":
    main()
    # chrome = Chrome()
