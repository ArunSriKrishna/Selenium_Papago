# Selenium_Papago
<img width="500" src="https://raw.githubusercontent.com/scottgigante/NaverTTS/master/papago.svg?sanitize=true" style="max-width:100%;">
A Python-Selenium Script to translate text from a textfile using Naver Papago


### Prerequisites
Requires ChromeDriver and Selenium Package.<br>
- Download the ChromeDriver for your Chrome version: https://chromedriver.chromium.org/<br>
- Install Selenium using pip <pre>$ pip install selenium</pre>

### Usage
- Assign <i>source_language</i> and <i>target_language</i> from values of Keys in the Dictionary
- Assign the filepath of Chrome Driver  to <i>chromedriver_filepath</i> 
- Assign the filepath of Source textfile to <i>source_filepath</i>
- Assign the Directory for Output textfile to <i>output_dir</i>

### language_code Dictionary
|	Keys|Language Code|
|----|----|
| Detect Language|auto|
|	Korean|ko|
|	English|en|
|	Japanese|ja|
|	Chinese Simplified|zh-CN|
|Chinese Traditional|zh-TW|	
|	Spanish|es|
|	French|fr|
|	German|de|
|	Russian|ru|
|	Portuguese|	pt|
|	Italian|it|
|	Vietnamese|vi|
|	Thai|th|
|	Indonesian|id|	
|	Hindi|hi|
