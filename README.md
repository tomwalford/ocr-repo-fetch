# OCR Repository - Candidate Work Downloader

This is a web scraper built using Selenium, designed to automatically fetch all candidate work from a given centre so that you don't have to download and extract everything individually.

Getting work from OCR Repository can be a painful experience because of the wait times as the Server prepares your download, so this script is designed to be set and forget.

The script takes a really long time to run (upwards of an hour if you are getting work for 15 candidates who all have lengthy videos) so be patient and go get a cup of tea.

## Setup

### Download the script to your machine

If you have git CLI installed then you just need to run:

`git clone https://github.com/thebillington/ocr-repo-fetch`

### Install required libraries

The script only requires selenium beyond the standard python libraries:

`python3 -m pip install selenium`

### Download a Selenium driver for your Browser (preferably Chrome)

Find Chrome drivers here: https://chromedriver.chromium.org/downloads

### Updating the `ini` file

You will need to make a copy of the `env.example.ini` file and save it as `env.ini`. Note that this is excluded from the repository to preserve privacy of fields.

### Alleviating timeouts

For very large ZIP files (1GB+) it may take upwards of the default 5 minute timeout for the download to commence.

This causes an issue which has been fixed on line 28: `driver.set_page_load_timeout(1800)`.

If you are still experiencing timeouts with a 30 minute timeout (1800 seconds) then just increase this value as required.

## Notes

If you have more than one panel this script won't work, as it will automatically choose the first when the panel selection dropdown loads. If this is the case for you then ping me an email on `billy.rebecchi@googlemail.com` and we will get it working.