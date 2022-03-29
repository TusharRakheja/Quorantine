from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import argparse
import getpass
import time

PARSER = argparse.ArgumentParser()
PARSER.add_argument('-e', '--email', dest='email', type=str, default=None, help='The email address you use for Quora', required=True)
PARSER.add_argument('-u', '--username', dest='username', type=str, default=None, help='Your Quora username e.g. "-u Ethan-Hawke-3" for https://www.quora.com/profile/Ethan-Hawke-3', required=True)
PARSER.add_argument('-s', '--space', dest='spaces', nargs='*', help='Quora spaces you''re active in e.g. "-s badalgos mastermind" if you''re active in https://badalgos.quora.com and https://mastermind.quora.com. The more comprehensive your list, the more stable the script.', required=False)
ARGS = PARSER.parse_args()

password = getpass.getpass(prompt='Quora password: ', stream=None).strip()

driver = webdriver.Chrome(ChromeDriverManager().install())

lang_list = ['fr', 'es', 'hi', 'ja', 'de', 'it', 'id', 'pt', 'nl', 'da', 'fi', 'no', 'sv', 'mr', 'bn', 'ta', 'ar', 'he', 'gu', 'kn', 'ml', 'te', 'pl']

ignore_list =  ["{}.quora.com".format(lang) for lang in lang_list] + ['/following', '/answer', '/topic/', '/messages/'] + ([] if ARGS.spaces is None else ARGS.spaces)

# If you want questions with certain keywords to be ignored, add them here. Not making this a CLI arg since it can potentially be long.
keep_list = ['or', 'rude']

driver.get('https://www.quora.com')
time.sleep(5)
driver.set_window_size(1024, 600)
driver.maximize_window()
would_have_deleted = []

would_not_have_deleted = []

email_input = driver.find_element_by_id("email")
email_input.send_keys(ARGS.email)

password_input = driver.find_element_by_id("password")
password_input.send_keys(password)

time.sleep(2)

password_input.send_keys(Keys.RETURN)

time.sleep(2)

driver.get('https://www.quora.com/profile/{}/answers'.format(ARGS.username))

time.sleep(3)

SCROLL_PAUSE_TIME = 4

questions = driver.find_elements_by_css_selector('a.q-box')

print("Num questions: {}".format(len(questions)))

first_try = True

end_of_page = False

deleted_set = set()

while not end_of_page:
    if first_try:
        first_try = False
    else:
        last_height = driver.execute_script("return document.body.scrollHeight")
        for i in range(10):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            end_of_page = True
            break
        questions = driver.find_elements_by_css_selector('a.q-box')

    for question in questions:
        try:
            qtxt = question.get_attribute('href')
        except StaleElementReferenceException:
            driver.get('https://www.quora.com/profile/{}/answers'.format(ARGS.username))
            time.sleep(3)
            break

        if qtxt in deleted_set:
            continue
        if not qtxt.startswith('https://www.quora.com/'):
            continue
        if qtxt == 'https://www.quora.com/profile/{}'.format(ARGS.username) or qtxt == 'https://www.quora.com/':
            continue
        ignore = False
        for word in ignore_list:
            if word in qtxt:
                ignore = True
                break
        
        if ignore:
            continue

        do_not_delete = False
        for word in keep_list:
            if word in qtxt:
                do_not_delete = True
                would_not_have_deleted.append(qtxt)
                break
        
        if not do_not_delete:
            print("Deleting: " + qtxt)
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])
            driver.get(qtxt + "/answer/{}".format(ARGS.username))
            time.sleep(3)
            try:
                element = driver.find_element_by_xpath("//*[contains(text(), \"Don't Share\")]")
                element.click()
            except NoSuchElementException:
                pass
            try:
                element = driver.find_element_by_css_selector('div.DesktopMessagesDock___StyledFixed-sc-1bh1698-0')
                driver.execute_script("""
                var element = arguments[0];
                element.parentNode.removeChild(element);
                """, element)
            except NoSuchElementException:
                pass
            btns = driver.find_elements_by_tag_name('button')
            for i in range(11, len(btns)):
                btn = btns[i]
                btn.click()
                time.sleep(1)
                try:
                    delb = driver.find_element_by_xpath("//*[contains(text(), 'Delete answer')]")
                    delb.click()
                    time.sleep(1)
                    delb = driver.find_element_by_xpath("//*[contains(text(), 'Confirm')]")
                    delb.click()
                    time.sleep(1)
                    deleted_set.add(qtxt)
                    break

                except NoSuchElementException:
                    continue

            driver.close()
            driver.switch_to.window(driver.window_handles[0])