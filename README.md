<img src="https://github.com/TusharRakheja/Quorantine/raw/main/pic.png" width="auto" height="60px" />

___

Quorantine is a Selenium script to delete all your Quora answers and give you back some of your privacy.

### Dependencies

- Python 3.8+
- `pip install selenium`
- `pip install webdriver-manager`

### Usage

```
PS> python .\quorantine.py -h
usage: quorantine.py [-h] -e EMAIL -u USERNAME [-s [SPACES [SPACES ...]]]

optional arguments:
  -h, --help            show this help message and exit
  -e EMAIL, --email EMAIL
                        The email address you use for Quora
  -u USERNAME, --username USERNAME
                        Your Quora username e.g. "-u Ethan-Hawke-3" for https://www.quora.com/profile/Ethan-Hawke-3
  -s [SPACES [SPACES ...]], --space [SPACES [SPACES ...]]
                        Quora spaces youre active in e.g. "-s badalgos mastermind" if youre active in https://badalgos.quora.com and https://mastermind.quora.com. The more comprehensive your list, the more stable the script.
```

### Considerations

- It's hard-coded to Google Chrome, but should be easy to use a different browser by changing this line: 
  - `driver = webdriver.Chrome(ChromeDriverManager().install())`

- If you want to preserve your answers to certain questions, add some keywords found in the text of those questions to the `keep_list` object. 
  - Any question which has any of the words in `keep_list` will be ignored.
  - This was not made a CLI argument since there can potentially be lots of words in the list.

- You may need to run this script several times to delete _all_ of your answers.

- I tested this script with several Quora accounts. For some of them, it unexpectedly put a CAPTCHA box on the login screen. 
  - This won't work if your account shows that behavior.
