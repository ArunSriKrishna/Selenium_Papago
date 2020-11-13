from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from sys import exit
from time import sleep, time
from datetime import datetime

now = datetime.now()
dt_string = now.strftime("%H_%M_%S")

file_source = open("/home/arunkrishna/Downloads/rath-trans.txt")
file_output = open(f"/home/arunkrishna/Documents/output_{dt_string}.txt", "a")
chromedriver = "/home/arunkrishna/Downloads/chromedriver"

source_language = "English"
target_language = "Japanese"

language_code = {
    "Detect Language": "auto",
    "Korean": "ko",
    "English": "en",
    "Japanese": "ja",
    "Chinese Simplified": "zh-CN",
    "Chinese Traditional": "zh-TW",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Russian": "ru",
    "Portuguese": "pt",
    "Italian": "it",
    "Vietnamese": "vi",
    "Thai": "th",
    "Indonesian": "id",
    "Hindi": "hi"
}

webElements = {
    "input-textbox": ["id", "txtSource"],
    "output-textbox": ["id", "txtTarget"],
    "translate-btn": ["id", "btnTranslate"]
}

def find_webelement(element):
    webElement = driver.find_element(element[0], element[1])
    return webElement

driver = webdriver.Chrome(chromedriver)
driver.get(f"https://papago.naver.com/?sk={language_code[source_language]}&tk={language_code[target_language]}")
try:
    wait = WebDriverWait(driver, timeout=15)
    wait.until(ec.visibility_of_element_located(webElements["translate-btn"]))
except:
    exit("Webpage Timed out!")

start_time = time()
input_textbox = find_webelement(webElements["input-textbox"])
output_textbox = find_webelement(webElements["output-textbox"])
translate_button = find_webelement(webElements["translate-btn"])
source_read = file_source.readlines()
source_text = ''.join(source_read)

last_index = len(source_text) - 1
curr_index = 0
batch_count = 0

while curr_index <= last_index-1:
    source = ''

    if (last_index - curr_index) >= 4999:
        source = source_text[curr_index: curr_index + 5000]
    else:
        source = source_text[curr_index: last_index-curr_index+1]
        print(f"Batch has less than 5000 Characters!")

    i = len(source) - 1
    while i > 1:
        if source[i] == '\n':
            source = source[0: i]
            break
        i = i - 1
    print("\nBatch Character Count: " + str(len(source)))

    script = "var ele = " + repr(source) + ";" + "\n document.getElementById('txtSource').value=ele;"
    driver.execute_script(script)
    input_textbox.send_keys(" ")

    translated = "null"
    base_time = 0

    while translated == "null" or translated == "..." or translated == "":
        base_time += 1
        sleep(0.01)
        translated = output_textbox.text

        if "Unable to connect to network." in translated[0:30]:
            exit("Oops! Try checking your network")

        if base_time == 500:
            translate_button.click()

        if base_time == 1500:
            exit("Oops! Try checking the source-text or your network")

    timeout = 0
    change_count = 0
    timed_out = []

    while 1:
        sleep(0.1)
        timeout += 1
        translated_curr = output_textbox.text
        if translated_curr != translated:
            translated = translated_curr
            change_count += 1
        else:
            if timeout > 100:
                timed_out.append(batch_count + 1)
                print("Timed out!")
                break
            if change_count >= 3:
                print("Changes caught!")
                break

    translated = output_textbox.text
    file_output.write(translated)
    batch_count += 1
    curr_index += len(source)
    progress = round((curr_index / last_index) * 100, 2)
    print(f"Batch count {batch_count}: ({curr_index}/{last_index})\nCharacters Processed: {curr_index} Progress <{progress}%>")

print(f"\nCompleted in {round(time() - start_time, 2)} second(s)!\nTotal Characters Processed: {curr_index}")
print("Timedout Batch(s) -->",timed_out)
