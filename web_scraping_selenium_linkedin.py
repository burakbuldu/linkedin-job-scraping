# Libraries
import time
import pandas as pd    
# ------------- # 
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# Driver path
path = '/Users/Lenovo/Downloads/chromedriver.exe'
driver = webdriver.Chrome(path)  

# Maximize Window
driver.maximize_window() 
driver.minimize_window()  
driver.maximize_window()  
driver.switch_to.window(driver.current_window_handle)
driver.implicitly_wait(10)

# Enter to the site
driver.get('https://www.linkedin.com/login');
time.sleep(0.5)


user_name = "..........." # mail or telephone
password = "..........." # password
driver.find_element_by_xpath('//*[@id="username"]').send_keys(user_name)
driver.find_element_by_xpath('//*[@id="password"]').send_keys(password)
time.sleep(0.5)

# Login button
driver.find_element_by_xpath('//*[@id="organic-div"]/form/div[3]/button').click()
driver.implicitly_wait(30)

# Jobs page
driver.find_element_by_xpath('//*[@id="ember19"]').click()
time.sleep(0.5)
# Go to search results directly
driver.get("https://www.linkedin.com/jobs/search/?geoId=102105699&keywords=Data%20Analytics&location=T%C3%BCrkiye")
time.sleep(0.5)

# Get all links for these offers
links = []
# Navigate all pages

allpagesnums = driver.find_elements(By.CSS_SELECTOR, '.artdeco-pagination__indicator')

lastpagenum = int(allpagesnums[len(allpagesnums)-1].text)

print('Links are being collected now. There are '+str(lastpagenum)+' pages of links.')
try: 
    for page in range(2,lastpagenum):
        time.sleep(0.5)
        jobs_block = driver.find_element_by_class_name('jobs-search-results__list')
        jobs_list= jobs_block.find_elements(By.CSS_SELECTOR, '.jobs-search-results__list-item')
    
        for job in jobs_list:
            all_links = job.find_elements_by_tag_name('a')
            for a in all_links:
                if str(a.get_attribute('href')).startswith("https://www.linkedin.com/jobs/view") and a.get_attribute('href') not in links: 
                    links.append(a.get_attribute('href'))
                else:
                    pass
            # scroll down for each job element
            driver.execute_script("arguments[0].scrollIntoView();", job)
        
        print(f'Collecting the links in the page: {page-1}')
        # go to next page:
        driver.find_element_by_xpath(f"//button[@aria-label='{page}. Sayfa']").click()
        time.sleep(0.5)
except:
    pass
print('Found ' + str(len(links)) + ' links for job offers')

# Create empty lists to store information
job_titles = []
company_names = []
company_locations = []
work_methods = []
post_dates = []
work_times = [] 
job_desc = []

i = 0
j = 1

# Visit each link one by one to scrape the information
print('Visiting the links and collecting information just started.')
for i in range(len(links)):
    try:
        driver.get(links[i])
        i=i+1
        time.sleep(0.5)
        # Click See more.
        driver.find_element_by_class_name("artdeco-card__actions").click()
        time.sleep(0.5)
    except:
        pass
    
    # Find the general information of the job offers
    contents = driver.find_elements_by_class_name('p5')
    for content in contents:
        try:
            job_titles.append(content.find_element_by_tag_name("h1").text)
            company_names.append(content.find_element_by_class_name("jobs-unified-top-card__company-name").text)
            company_locations.append(content.find_element_by_class_name("jobs-unified-top-card__bullet").text)
            work_methods.append(content.find_element_by_class_name("jobs-unified-top-card__workplace-type").text)
            post_dates.append(content.find_element_by_class_name("jobs-unified-top-card__posted-date").text)
            work_times.append(content.find_element_by_class_name("jobs-unified-top-card__job-insight").text)
            print(f'Scraping the Job Offer {j} DONE.')
            j+= 1
        except:
            pass
        time.sleep(0.5)
        
        # Scraping the job description
    job_description = driver.find_elements_by_class_name('jobs-description__content')
    for description in job_description:
        job_text = description.find_element_by_class_name("jobs-box__html-content").text
        job_text = job_text.replace(",", " ")
        job_text = job_text.replace("\n", " ")
        job_desc.append(job_text)
        print(f'Scraping the Job Offer {j}')
        time.sleep(0.5)  
            
# Creating the dataframe 
df = pd.DataFrame(list(zip(job_titles,company_names,
                    company_locations,work_methods,
                    post_dates,work_times,job_desc)),
                    columns =['job_title', 'company_name',
                           'company_location','work_method',
                           'post_date','work_time','job_desc'])

# Storing the data to csv file
df.to_csv('job_offers.csv', index=False)
