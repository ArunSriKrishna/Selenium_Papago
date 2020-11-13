from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from sys import exit
from time import sleep, time
from datetime import datetime

now = datetime.now()
dt_string = now.strftime("%H_%M_%S")

# Change the following parameters
#-------------------------------
source_filepath = ""
chromedriver_filepath = ""
output_dir = ""

source_language = "English"
target_language = "Japanese"
#-------------------------------

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

# Dictionary for WebElements
webElements = {
    "input-textbox": ["id", "txtSource"],
    "output-textbox": ["id", "txtTarget"],
    "translate-btn": ["id", "btnTranslate"]
}

# Open input and output files
file_source = open(f"{source_filepath}")
file_output = open(f"{output_dir}/output_{dt_string}.txt", "a")

# Finds the elements using Dictionary
def find_webelement(element):
    webElement = driver.find_element(element[0], element[1])
    return webElement

# Uses ChromeWebDriver
driver = webdriver.Chrome(chromedriver_filepath)
driver.get(f"https://papago.naver.com/?sk={language_code[source_language]}&tk={language_code[target_language]}")
try:
    wait = WebDriverWait(driver, timeout=15)
    wait.until(ec.visibility_of_element_located(webElements["translate-btn"]))
except:
    # Waits for 15 seconds before Timeout
    exit("Webpage Timed out!")

# To find Execution time
start_time = time()

input_textbox = find_webelement(webElements["input-textbox"])
output_textbox = find_webelement(webElements["output-textbox"])
translate_button = find_webelement(webElements["translate-btn"])

# Reads source textfile and converts it to string
source_read = file_source.readlines()
source_text = ''.join(source_read)

last_index = len(source_text) - 1
curr_index = 0
batch_count = 0

# Loop until all characters are processed
while curr_index <= last_index-1:
    source = ''

    # Considers in batches of 5000 characters
    if (last_index - curr_index) >= 4999:
        source = source_text[curr_index: curr_index + 5000]
    else:
        # If a Batch has less than 5000 characters
        source = source_text[curr_index: last_index-curr_index+1]
        print(f"Batch has less than 5000 Characters!")

    # Finds the last linebreak in the batch and substring of the batch till the last linebreak is considered as input
    # To avoid cases where only parts of the line are translated
    i = len(source) - 1
    while i > 1:
        if source[i] == '\n':
            source = source[0: i]
            break
        i = i - 1
    print("\nBatch Character Count: " + str(len(source)))

    # Creates a JavaScript to input the batch to the WebElement input_textbox
    script = "var ele = " + repr(source) + ";" + "\n document.getElementById('txtSource').value=ele;"
    driver.execute_script(script)
    input_textbox.send_keys(" ")

    translated = "null"
    base_time = 0

    # Captures the initial unrefined translated text from the WebElement output-textbox
    while translated == "null" or translated == "..." or translated == "":
        base_time += 1
        sleep(0.01)
        translated = output_textbox.text
        # Checks for loss of internet connection warning in the WebElement output-textbox
        if "Unable to connect to network." in translated[0:30]:
            exit("Oops! Try checking your network")
        # Clicks on Translate button if there is no output for 5 seconds
        if base_time == 500:
            sleep(0.5)
            translate_button.click()
        # Exits if there is not output from server for 15 seconds
        if base_time == 1500:
            exit("Oops! Try checking the source-text or your network")

    timeout = 0
    change_count = 0
    timed_out = []
    
    # Captures refined translated from the WebElement output-textbox, timeout if there is no change in the text within 10 seconds
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
    
    # Write the output-text to a file
    file_output.write(translated)
    
    batch_count += 1
    curr_index += len(source)
    progress = round((curr_index / last_index) * 100, 2)
    print(f"Batch count {batch_count}: ({curr_index}/{last_index})\nCharacters Processed: {curr_index} Progress <{progress}%>")

print(f"\nCompleted in {round(time() - start_time, 2)} second(s)!\nTotal Characters Processed: {curr_index}")

# Prints batch_count of the batches that timedout while capturing refined translated text
print("Timedout Batch(s) -->",timed_out)
