# Selenium_Papago
<img width="500" src="https://raw.githubusercontent.com/scottgigante/NaverTTS/master/papago.svg?sanitize=true" style="max-width:100%;">
A Python-Selenium Script to translate text from a textfile using Naver Papago


### Prerequisites
Requires ChromeDriver and Selenium Package.<br>
- Download the ChromeDriver for your Chrome version: https://chromedriver.chromium.org/<br>
- Install Selenium using pip <pre>$ pip install selenium</pre>

### Usage
- Initialize source-language and target-language according to keys in the dictionary

|Language Code|	Keys|
|----|----|
|auto| Detect Language|
|ko|	Korean|
|en|	English|
|ja|	Japanese|
|zh-CN|	Chinese Simplified|
|zh-TW|	Chinese Traditional|
|es|	Spanish|
|fr|	French|
|de|	German|
|ru|	Russian|
|pt|	Portuguese|	
|it|	Italian|
|vi|	Vietnamese|
|th|	Thai|
|id|	Indonesian|	
|hi|	Hindi|

- Assign the filepath of Chrome Driver  to <i>chromedriver_filepath</i> 
- Assign the filepath of Source textfile to <i>source_filepath</i>
- Assign the Directory for Output textfile to <i>output_dir</i>
