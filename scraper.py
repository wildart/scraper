import sys
import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

maxpages = 1000

url = sys.argv[1]
outfile = sys.argv[2] + '.json'
if len(sys.argv) > 3:
    maxpages = int(sys.argv[3])

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome('bin/chromedriver', 0, options)
driver.get(url)

jscript = """{
var cp = document.getElementById('ContentPane');
var sec = cp.getElementsByTagName('section');
return sec.item(sec.length-1).querySelectorAll('td.PadLeft10');
}
"""
results = []
pages = 1
while True:
    tds = driver.execute_script(jscript)

    for td in tds:
        result = td.text.split("\n")
        result = result[:-1]
        children = driver.execute_script('return arguments[0].children;', td)
        for ch in children:
            if ch.tag_name == 'a':
                result.append(ch.get_attribute('href'))
                break
        results.append(list(result))

    content = driver.find_element_by_id('ContentPane')

    # enter next page
    pagenumber = driver.find_element_by_class_name('DataFormTextBox')
    pages += 1
    pagenumber.send_keys('{0}\n'.format(pages))

    print('Loading page #{0}'.format(pages))
    WebDriverWait(driver, 10).until(EC.staleness_of(content))
    while True:
        try:
            content = driver.find_element_by_id('ContentPane')
            print('\nLoaded page #{0}\n'.format(pages))
            break
        except:
            WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located(By.ID, 'ContentPane'))
            print('.')

    if pages >= maxpages:
        break

driver.quit()

with open(outfile, 'w') as io:
    json.dump(results, io)
