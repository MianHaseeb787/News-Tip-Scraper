from selenium import webdriver  # Import seleniumwire
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import json
import time
import csv
import io
import gzip


jn_headers = ["sname", "Job Title", "Outlet Name", "Outlet URL", "Biography", "X url", "Linkedin url", "facebook url", "threads url", "Topics", "Country", "State", "Suburb", "Email", "Phone", "Picture Url", "Source url", "Last Article Url", "Author Url"]
with open("jndata.csv", mode="w", newline='') as jn_file:
    jn_writer = csv.writer(jn_file)
    jn_writer.writerow(jn_headers)

host_headers = ["Name", "Url", "Description", "X Url", "Linkedin url", "facebook url", "threads url", "Topics", "Country", "Email", "Phone", "logo Url", "Source Url" ]
with open("hostdata.csv", mode="w", newline='') as hs_file:
    hs_writer = csv.writer(hs_file)
    hs_writer.writerow(host_headers)

options = Options()

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), 
    options=options,
)


driver.get("https://anewstip.com/accounts/login/")
time.sleep(3)

email_input = driver.find_element(By.NAME, "email")
email_input.send_keys("mianhaseeb.ce@gmail.com")

pas_input = driver.find_element(By.NAME, "password")
pas_input.send_keys("gggg2001")

submit_button = driver.find_element(By.CLASS_NAME, "pure-button-primary")
submit_button.click()
time.sleep(5)

journalist_profiles = driver.find_element(By.CSS_SELECTOR, "li.search-by[type='journalists']")
journalist_profiles.click()

advance_search_btn  = driver.find_element(By.ID, "advanced_search_link")
advance_search_btn.click()
time.sleep(3)

dropdown = driver.find_element(By.ID, "advanced_search_field_country")


select = Select(dropdown)

country_text = "United States"
select.select_by_value(country_text)

search_btn = driver.find_element(By.ID, "search_btn")
search_btn.click()
time.sleep(5)

# PageSize_dropdown = driver.find_element(By.ID, "page_size_selector")
# select = Select(PageSize_dropdown)
# select.select_by_value("150")


state_dropdown = driver.find_element(By.CSS_SELECTOR, "select.facet-filter.SumoUnder[data-filter='state']")
state_select = Select(state_dropdown)

city_dropdown = driver.find_element(By.CSS_SELECTOR, "select.facet-filter.SumoUnder[data-filter='city']")
city_select = Select(city_dropdown)

time.sleep(2)


for j in range(len(state_select.options)):

    state_dropdown = driver.find_element(By.CSS_SELECTOR, "select.facet-filter.SumoUnder[data-filter='state']")
    state_select = Select(state_dropdown)
    option = state_select.options[j]
    state_text = option.text
    print(f"state : {state_text}")
    state_select.select_by_visible_text(option.text)

    
    time.sleep(3)

    city_dropdown = driver.find_element(By.CSS_SELECTOR, "select.facet-filter.SumoUnder[data-filter='city']")
    city_select = Select(city_dropdown)
    # Iterate over each option in the dropdown
    for i in range(len(city_select.options)):

        city_dropdown = driver.find_element(By.CSS_SELECTOR, "select.facet-filter.SumoUnder[data-filter='city']")
        city_select = Select(city_dropdown)
        option = city_select.options[i]
        city_select.select_by_visible_text(option.text)
    
        time.sleep(2)

        records = driver.find_elements(By.CLASS_NAME, "search-item")
        for record in records:
            name = record.find_element(By.CSS_SELECTOR, "span.info-name > a")
            name.click()

            # Switch to the new tab
            driver.switch_to.window(driver.window_handles[-1])

            news_articles_btn = driver.find_element(By.CSS_SELECTOR, 'a.action-link[content-id="author_articles"]')
            news_articles_btn.click()
            # time.sleep(1)

            # scrape jn profile page
            try:
                name = driver.find_element(By.CLASS_NAME, "info-name").text
            except:
                name = ''

            try:
                job_title = driver.find_element(By.CSS_SELECTOR, '.info-title > a').text
            except:
                job_title = ''

            try:
                outlet_name = driver.find_element(By.CSS_SELECTOR, '.info-outlet-name > a').text
            except:
                outlet_name = ''

            try:
                outlet_url = driver.find_element(By.CSS_SELECTOR, '.info-outlet-name > a').get_attribute('href')
            except:
                outlet_url = ''

            try:
                biography = driver.find_element(By.XPATH, f'(//div[@class="profile"])[{i+1}]//div[@class="biography"]').text
            except:
                biography = ''

            try:
                x_url = driver.find_element(By.XPATH, f'(//div[@class="profile"])[{i+1}]//div[@class="contact-info-item"]/i[@class="icon-twitter"]/following-sibling::a').get_attribute('href')
            except:
                x_url = ''

            try:
                linkedin_url = driver.find_element(By.XPATH, f'(//div[@class="profile"])[{i+1}]//div[@class="contact-info-item"]/i[@class="icon-linkedin-empty"]/following-sibling::a').get_attribute('href')
            except:
                linkedin_url = ''

            try:
                facebook_url = driver.find_element(By.XPATH, f'(//div[@class="profile"])[{i+1}]//div[@class="contact-info-item"]/i[@class="icon-network-fb"]/following-sibling::a').get_attribute('href')
            except:
                facebook_url = ''

            try:
                threads_url = driver.find_element(By.XPATH, f'(//div[@class="profile"])[{i+1}]//a[@class="threads-url"]').get_attribute('href')
            except:
                threads_url = ''

            try:

                topics_div = driver.find_element(By.CLASS_NAME, 'row-item.topic-list.profile-block')
    
                # Find all topic links within the div
                topic_links = topics_div.find_elements(By.CSS_SELECTOR, 'a.action-link')
                
                # Extract topic texts and join them with commas
                topics = ", ".join([link.find_element(By.CSS_SELECTOR, 'span.topic-label.label-default').text for link in topic_links])

            except:
                topics = ''

            try:
                country = driver.find_element(By.CSS_SELECTOR, 'div.row-item.address-language > div.contact-info-item:nth-of-type(1)').text.strip()
            except:
                country = ''

            try:
                state = ""
            except:
                state = ''

            try:
                suburb = driver.find_element(By.XPATH, f'(//div[@class="profile"])[{i+1}]//div[@class="suburb"]').text
            except:
                suburb = ''

            try:
                email = driver.find_element(By.XPATH, f'(//div[@class="profile"])[{i+1}]//div[@class="contact-info-item"]/i[@class="icon-mail"]/following-sibling::a').get_attribute('href')
            except:
                email = ''

            try:
                phone = driver.find_element(By.XPATH, f'(//div[@class="profile"])[{i+1}]//div[@class="contact-info-item"]/i[@class="icon-phone"]/following-sibling::span').text
            except:
                phone = ''

            try:
                picture_url = driver.find_element(By.CSS_SELECTOR, 'div.avatar-wrapper > img').get_attribute('src')
            except:
                picture_url = ''

            try:
                source_url = driver.current_url
            except:
                source_url = ''

            try:
                # last_article_url = 
                first_item = driver.find_element(By.CSS_SELECTOR, 'ul.search-items > li.search-item.article-item:nth-of-type(1)')
    
                # Extract the URL from the first item using CSS selector
                last_article_url = first_item.find_element(By.CSS_SELECTOR, 'div.search-item-right > div.article-title > a').get_attribute('href')
            except:
                last_article_url = ''

            try:
                author_url = driver.find_element(By.XPATH, f'(//div[@class="profile"])[{i+1}]//a[@class="author-url"]').get_attribute('href')
            except:
                author_url = ''

            with open('jndata.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    name, job_title, outlet_name, outlet_url, biography,
                    x_url, linkedin_url, facebook_url, threads_url, topics, country, state,
                    suburb, email, phone, picture_url, source_url, last_article_url, author_url
                ])

            time.sleep(1)
            driver.close()

            driver.switch_to.window(driver.window_handles[0])
            time.sleep(2)

            # Host profiel scrape code

            comp_name = record.find_element(By.CSS_SELECTOR, "span.info-outlet-name > a")
            comp_name.click()
            driver.switch_to.window(driver.window_handles[-1])

            try:
                company_name = driver.find_element(By.CLASS_NAME, "info-name").text
            except:
                company_name = ""

            try:
                company_url = driver.find_element(By.CSS_SELECTOR, "div.row-item.profile-website > a").get_attribute('href')
            except:
                company_url = ""


            try:
                topics_div = driver.find_element(By.CLASS_NAME, 'row-item.topic-list.profile-block')
    
                # Find all topic links within the div
                topic_links = topics_div.find_elements(By.CSS_SELECTOR, 'a.action-link')
                
                # Extract topic texts and join them with commas
                topics = ", ".join([link.find_element(By.CSS_SELECTOR, 'span.topic-label.label-default').text for link in topic_links])
            except:
                topics = ""

            try:
                x_url = driver.find_element(By.XPATH, f'(//div[@class="profile"])[{i+1}]//div[@class="contact-info-item"]/i[@class="icon-twitter"]/following-sibling::a').get_attribute('href')
            except:
                x_url = ''

            try:
                linkedin_url = driver.find_element(By.XPATH, f'(//div[@class="profile"])[{i+1}]//div[@class="contact-info-item"]/i[@class="icon-linkedin-empty"]/following-sibling::a').get_attribute('href')
            except:
                linkedin_url = ''

            try:
                facebook_url = driver.find_element(By.XPATH, f'(//div[@class="profile"])[{i+1}]//div[@class="contact-info-item"]/i[@class="icon-network-fb"]/following-sibling::a').get_attribute('href')
            except:
                facebook_url = ''

            try:
                phone = driver.find_element(By.XPATH, f'(//div[@class="profile"])[{i+1}]//div[@class="contact-info-item"]/i[@class="icon-phone"]/following-sibling::span').text
            except:
                phone = ''


            try:
                email = driver.find_element(By.XPATH, f'(//div[@class="profile"])[{i+1}]//div[@class="contact-info-item"]/i[@class="icon-mail"]/following-sibling::a').get_attribute('href')
            except:
                email = ''


            try:
                picture_url = driver.find_element(By.CSS_SELECTOR, 'div.avatar-wrapper > img').get_attribute('src')
            except:
                picture_url = ''

            try:
                source_url = driver.current_url
            except:
                source_url = ''

            with open("hostdata.csv", mode="a", newline='') as hs_file:
                 hs_writer = csv.writer(hs_file)
                 hs_writer.writerow([company_name, company_url, "", x_url, linkedin_url, facebook_url, threads_url, topics, country, email, phone, picture_url, source_url])
    






            time.sleep(1)
            driver.close()

            driver.switch_to.window(driver.window_handles[0])
            time.sleep(2)

        # pagination
        try:
                # Find the element with the current page number
                current_page_element = driver.find_element(By.CSS_SELECTOR, "span.page-link.current-page")
                current_page = int(current_page_element.text.strip())  # Extract the current page number

                while True:

                    

                    current_page_element = driver.find_element(By.CSS_SELECTOR, "span.page-link.current-page")
                    current_page = int(current_page_element.text.strip())  # Extract the current page number

                    if current_page is None:
                        break

                
                    # Find the next page element
                    next_page_element = driver.find_element(By.XPATH, f"//a[@data-page='{current_page + 1}']")
                
                    # Click on the next page link
                    next_page_element.click()
                    time.sleep(1)
                    driver.execute_script("window.scrollTo(0, 0);")
                    # time.sleep(3)


                    records = driver.find_elements(By.CLASS_NAME, "search-item")
                    for record in records:
                        print("recaords")
                        name = record.find_element(By.CSS_SELECTOR, "span.info-name > a")
                        name.click()

                        # Switch to the new tab
                        driver.switch_to.window(driver.window_handles[-1])

                        news_articles_btn = driver.find_element(By.CSS_SELECTOR, 'a.action-link[content-id="author_articles"]')
                        news_articles_btn.click()
                        time.sleep(1)                       

                        # journaslist profile page scrape
                        try:
                            name = driver.find_element(By.CLASS_NAME, "info-name").text
                        except:
                            name = ''

                        try:
                            job_title = driver.find_element(By.CSS_SELECTOR, '.info-title > a').text
                        except:
                            job_title = ''

                        try:
                            outlet_name = driver.find_element(By.CSS_SELECTOR, '.info-outlet-name > a').text
                        except:
                            outlet_name = ''

                        try:
                            outlet_url = driver.find_element(By.CSS_SELECTOR, '.info-outlet-name > a').get_attribute('href')
                        except:
                            outlet_url = ''

                        try:
                            biography = driver.find_element(By.XPATH, f'(//div[@class="profile"])[{i+1}]//div[@class="biography"]').text
                        except:
                            biography = ''

                        try:
                            x_url = driver.find_element(By.XPATH, f'(//div[@class="profile"])[{i+1}]//div[@class="contact-info-item"]/i[@class="icon-twitter"]/following-sibling::a').get_attribute('href')
                        except:
                            x_url = ''

                        try:
                            linkedin_url = driver.find_element(By.XPATH, f'(//div[@class="profile"])[{i+1}]//div[@class="contact-info-item"]/i[@class="icon-linkedin-empty"]/following-sibling::a').get_attribute('href')
                        except:
                            linkedin_url = ''

                        try:
                            facebook_url = driver.find_element(By.XPATH, f'(//div[@class="profile"])[{i+1}]//div[@class="contact-info-item"]/i[@class="icon-network-fb"]/following-sibling::a').get_attribute('href')
                        except:
                            facebook_url = ''

                        try:
                            threads_url = driver.find_element(By.XPATH, f'(//div[@class="profile"])[{i+1}]//a[@class="threads-url"]').get_attribute('href')
                        except:
                            threads_url = ''

                        try:

                            topics_div = driver.find_element(By.CLASS_NAME, 'row-item.topic-list.profile-block')
                
                            # Find all topic links within the div
                            topic_links = topics_div.find_elements(By.CSS_SELECTOR, 'a.action-link')
                            
                            # Extract topic texts and join them with commas
                            topics = ", ".join([link.find_element(By.CSS_SELECTOR, 'span.topic-label.label-default').text for link in topic_links])

                        except:
                            topics = ''

                        try:
                            country =  driver.find_element(By.CSS_SELECTOR, 'div.row-item.address-language > div.contact-info-item:nth-of-type(1)').text.strip()
                        except:
                            country = ''

                        try:
                            state = ""
                        except:
                            state = ''

                        try:
                            suburb = driver.find_element(By.XPATH, f'(//div[@class="profile"])[{i+1}]//div[@class="suburb"]').text
                        except:
                            suburb = ''

                        try:
                            email = driver.find_element(By.XPATH, f'(//div[@class="profile"])[{i+1}]//div[@class="contact-info-item"]/i[@class="icon-mail"]/following-sibling::a').get_attribute('href')
                        except:
                            email = ''

                        try:
                            phone = driver.find_element(By.XPATH, f'(//div[@class="profile"])[{i+1}]//div[@class="contact-info-item"]/i[@class="icon-phone"]/following-sibling::span').text
                        except:
                            phone = ''

                        try:
                            picture_url = driver.find_element(By.CSS_SELECTOR, 'div.avatar-wrapper > img').get_attribute('src')
                        except:
                            picture_url = ''

                        try:
                            source_url = driver.current_url
                        except:
                            source_url = ''

                        try:
                            # last_article_url = 
                            first_item = driver.find_element(By.CSS_SELECTOR, 'ul.search-items > li.search-item.article-item:nth-of-type(1)')
                
                            # Extract the URL from the first item using CSS selector
                            last_article_url = first_item.find_element(By.CSS_SELECTOR, 'div.search-item-right > div.article-title > a').get_attribute('href')
                        except:
                            last_article_url = ''

                        try:
                            author_url = driver.find_element(By.XPATH, f'(//div[@class="profile"])[{i+1}]//a[@class="author-url"]').get_attribute('href')
                        except:
                            author_url = ''

                        with open('jndata.csv', mode='a', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow([
                                name, job_title, outlet_name, outlet_url, biography,
                                x_url, linkedin_url, facebook_url, threads_url, topics, country, state,
                                suburb, email, phone, picture_url, source_url, last_article_url, author_url
                            ])



                        time.sleep(1)
                        driver.close()

                        # Host page Scraper code here

                        driver.switch_to.window(driver.window_handles[0])
                        time.sleep(2)

                        # comp_name = record.find_element(By.CSS_SELECTOR, "span.info-outlet-name > a")
                        # comp_name.click()
                        # driver.switch_to.window(driver.window_handles[-1])

                        comp_name = record.find_element(By.CSS_SELECTOR, "span.info-outlet-name > a")
                        comp_name.click()
                        driver.switch_to.window(driver.window_handles[-1])

                        try:
                            company_name = driver.find_element(By.CLASS_NAME, "info-name").text
                        except:
                            company_name = ""

                        try:
                            company_url = driver.find_element(By.CSS_SELECTOR, "div.row-item.profile-website > a").get_attribute('href')
                        except:
                            company_url = ""


                        try:
                            topics_div = driver.find_element(By.CLASS_NAME, 'row-item.topic-list.profile-block')
                
                            # Find all topic links within the div
                            topic_links = topics_div.find_elements(By.CSS_SELECTOR, 'a.action-link')
                            
                            # Extract topic texts and join them with commas
                            topics = ", ".join([link.find_element(By.CSS_SELECTOR, 'span.topic-label.label-default').text for link in topic_links])
                        except:
                            topics = ""

                        try:
                            x_url = driver.find_element(By.XPATH, f'(//div[@class="profile"])[{i+1}]//div[@class="contact-info-item"]/i[@class="icon-twitter"]/following-sibling::a').get_attribute('href')
                        except:
                            x_url = ''

                        try:
                            linkedin_url = driver.find_element(By.XPATH, f'(//div[@class="profile"])[{i+1}]//div[@class="contact-info-item"]/i[@class="icon-linkedin-empty"]/following-sibling::a').get_attribute('href')
                        except:
                            linkedin_url = ''

                        try:
                            facebook_url = driver.find_element(By.XPATH, f'(//div[@class="profile"])[{i+1}]//div[@class="contact-info-item"]/i[@class="icon-network-fb"]/following-sibling::a').get_attribute('href')
                        except:
                            facebook_url = ''

                        try:
                            phone = driver.find_element(By.XPATH, f'(//div[@class="profile"])[{i+1}]//div[@class="contact-info-item"]/i[@class="icon-phone"]/following-sibling::span').text
                        except:
                            phone = ''


                        try:
                            email = driver.find_element(By.XPATH, f'(//div[@class="profile"])[{i+1}]//div[@class="contact-info-item"]/i[@class="icon-mail"]/following-sibling::a').get_attribute('href')
                        except:
                            email = ''


                        try:
                            picture_url = driver.find_element(By.CSS_SELECTOR, 'div.avatar-wrapper > img').get_attribute('src')
                        except:
                            picture_url = ''

                        try:
                            source_url = driver.current_url
                        except:
                            source_url = ''

                        with open("hostdata.csv", mode="a", newline='') as hs_file:
                            hs_writer = csv.writer(hs_file)
                            hs_writer.writerow([company_name, company_url, "", x_url, linkedin_url, facebook_url, threads_url, topics, country, email, phone, picture_url, source_url])
                        
                        time.sleep(2)
                        driver.close()

                        driver.switch_to.window(driver.window_handles[0])
                        time.sleep(2)
                
                     # Wait for some time for the page to load
                    time.sleep(2)
                
                # Now you can perform actions on the next page
                
        except Exception as e:
                print(f"Error: {e}")  

        
        # Deselect the option
        city_dropdown  = driver.find_element(By.CSS_SELECTOR, "select.facet-filter.SumoUnder[data-filter='city']")
        city_select = Select(city_dropdown)
        city_select.deselect_by_index(0)
        print(f"City Deselected")
        
        # Wait for 1 second before moving to the next option (optional)
        time.sleep(1)

    state_dropdown = driver.find_element(By.CSS_SELECTOR, "select.facet-filter.SumoUnder[data-filter='state']")
    state_select = Select(state_dropdown)
    state_select.deselect_by_index(0)
    print(f"state Deselected")



time.sleep(100)




