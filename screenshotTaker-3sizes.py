# takes screenshots of webpages in 3 sizes, ready to be put into a Photoshop mockup
#    desktop
#    ipad/tablet
#    phone
# Sites to take screenshots of are in sites.txt

# TODO: run headless ... for now is fun watching it
# TODO: use f-strings instead of old-school string formatting

from selenium import webdriver
from datetime import datetime
import os, time, traceback

subDir = 'screenshots-3sizes'                           #create a directory to save in
os.makedirs(subDir, exist_ok=True)              

dateStamp = datetime.today().strftime('%Y-%m-%d')

with webdriver.Firefox() as driver:                      #this method auto-closes the browser when done
    with open("sites.txt") as f:
        sites = f.read().splitlines()                   # splitlines() method splits the string at line breaks and returns a list of lines in the string

    for site in sites:
        siteReadable = site.lower()                     # list of sites/pages provided are often not human friendly for reading
        url = 'http://' + siteReadable                  # TODO: watch for issues with https vs http???
        print('getting ' + url)  

        desktop = {'output': subDir + '/' + str(siteReadable) + '-desktop.png',
                    'width': 2200,
                    'height': 1800}
        tablet = {'output': subDir + '/' + str(siteReadable) + '-tablet.png',
                    'width': 1200,
                    'height': 1400}
        phone = {'output': subDir + '/' + str(siteReadable) + '-phone.png',
                    'width': 680,
                    'height': 1200}
            
        try:  
            # do the desktop version
            driver.set_window_size(desktop['width'], desktop['height'])
            driver.get(url);
            time.sleep(2)                                           # helps let all images render and page settle down
            driver.save_screenshot(desktop['output'])

            # do the tablet version
            driver.set_window_size(tablet['width'], tablet['height'])
            driver.get(url);
            time.sleep(2)                                           # helps let all images render and page settle down
            driver.save_screenshot(tablet['output'])

            # do the phone version
            driver.set_window_size(phone['width'], phone['height'])
            driver.get(url);
            time.sleep(2)                                            # helps let all images render and page settle down
            driver.save_screenshot(phone['output'])

            time.sleep(2)
        
        # TODO: better error handling ... raise for status ... log the type of error (ex, 404)
        except:
            print('there was a problem at: %s ' % (siteReadable))      
            errorFile = open('errorInfo.txt', 'a')
            errorFile.write('error on %s at %s ' % (dateStamp, siteReadable) + '\n')
            errorFile.write(traceback.format_exc())
            errorFile.close()
            continue
        
print('done processing')