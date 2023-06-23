#import sys, pathlib
#sys.path.append(pathlib.Path(__file__).parent.resolve())        

from selenium.webdriver.common.keys import Keys         
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from csv import writer as csv_writer
from smtplib import SMTP
from email.encoders import encode_base64
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os import environ as os_environ

from login import login
from find_email_info import find_email_info
from edit_cover_letter import edit_cover_letter
from send_mail import send_email

w=open('job_applications.csv', 'a', newline='')
writer1=csv_writer(w)
writer1.writerow(['Keyword', 'Zipcode', 'Job Title', 'Recruiter Name', 'Recruiter Email', 'Location', 'Application URL'])
application_url_log=[]
def zipcode_job_search(temp_keyword, zip_list, driver):
    job_match_count=0       #initialise a count variable to keep track of the number of relevant job listings
    negative_keyword_set=('assistant', 'hardware')
    for temp_zipcode in zip_list:
        zipcode_search_box=driver.find_element(by=By.XPATH, value='//input[@class="global-search-icon input-medium location-autocomplete"]')
        
        zipcode_search_box.send_keys(Keys.CONTROL, 'a')
        zipcode_search_box.send_keys(Keys.BACKSPACE)
        zipcode_search_box.send_keys(temp_zipcode)

        driver.find_element(by=By.XPATH, value='//button[@class="hidden-search-icon"]').send_keys(Keys.ENTER)

        try: pagecount=int(driver.find_element(by=By.XPATH, value='//div[@class="row-fluid search-paginate"]').get_attribute('data-maxpages'))
        except: pagecount=1

        #storing the url of the first page of search results in case we need to look through more pages for the same keycode-zipcode combination
        base_url=driver.current_url      
        for page in range(0, pagecount):
            if(page!=0):
                #changing the url to head to the next page of entries
                driver.get(base_url.replace('https://www.cybercoders.com/search/?', f'https://www.cybercoders.com/search/?page={page+1}&'))
            #iterating through all job-listings in a page
            for x in driver.find_elements(by=By.XPATH, value='//div[@class="job-listing-item"]'):       
                try:
                    temp_job_title=x.find_element(by=By.XPATH, value='.//div[@class="job-title"]').text.strip()
                    try: temp_job_title=temp_job_title[:temp_job_title.index('-')]
                    except ValueError: pass            #using error handling to slice the job title string
                    if(temp_keyword.lower() in temp_job_title.lower()):     #checking if current keyword is in the job title
                        for negative_keyword in negative_keyword_set:
                            if(negative_keyword not in temp_job_title):
                                application_url=x.find_element(by=By.XPATH, value='.//div[@class="job-title"]').find_element(by=By.CSS_SELECTOR, value='a').get_attribute('href')
                                if(application_url not in application_url_log):
                                    driver.execute_script("window.open('about:blank', 'tab2');")    #switching to a new tab 
                                    driver.switch_to.window("tab2")
                                    driver.get(application_url)

                                    #fetching the required email details from the relevant elements
                                    email_receiver, subject, location=find_email_info(driver)       
                                    recruiter_name=driver.find_element(by=By.XPATH, value='//div[@class="recruiter-apply-content-detail"]//following-sibling::p//following-sibling::a').text
                                    
                                    #editing the cover letter according to the details of the job listing
                                    email_body=edit_cover_letter(recruiter_name, temp_keyword, location)

                                    #sending the email with the resume attached
                                    send_email(email_receiver, subject, email_body)

                                    #applying for the job through cybercoders' application system
                                    #driver.find_element(by=By.XPATH, value='//a[@class="apply-btn btn-main-cta"]').click()
                                    #driver.find_element(by=By.XPATH, value='//button[@class="btn-main-cta"]').click()

                                    driver.close()         #closing tab2
                                    driver.switch_to.window(driver.window_handles[0])       #switching to the base(first) tab
                                    job_match_count+=1      #incrementing the count variable upon a successful job application
                                    application_url_log.append(application_url)
                                    writer1.writerow([temp_keyword, temp_zipcode, temp_job_title, recruiter_name, email_receiver, location, application_url])
                            else:
                                break
                except NoSuchElementException as e:         #catch embedded email alert elements
                    print(f'Encountered email service element on page {page+1}. Ignore this')
                    print(temp_keyword, temp_zipcode)
                    print(getattr(e, 'message', str(e))[:getattr(e, 'message', str(e)).find('\n')])

    return job_match_count

def send_csv_to_self():
    msg = MIMEMultipart()
    msg['From'] = "login.docplus@gmail.com"
    msg['To'] = 'login.docplus@gmail.com'
    msg['Subject'] = 'This csv file contains info about the relevant applications'

    # string to store the body of the mail
    body = ''

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # open the file to be sent
    filename = "job_applications.csv"
    #attachment = open(f"{pathlib.Path(__file__).parent.resolve()}\Manish Kothary -Chief Technology Officer Resume.DOCX", "rb")
    attachment = open(f"job_applications.csv", "rb")
    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form
    p.set_payload((attachment).read())

    # encode into base64
    encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # attach the instance 'p' to instance 'msg'
    msg.attach(p)

    # creates SMTP session
    s = SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    password=os_environ.get("GMAIL_APP_PASSWORD")
    s.login('login.docplus@gmail.com', password)       #USE YOUR OWN APP PASSWORD; DIFFERENT FROM YOUR GMAIL PASSOWRD

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail('login.docplus@gmail.com', 'login.docplus@gmail.com', text)
    print('A MAIL HAS BEEN SENT')
    # terminating the session
    s.quit()



def main():
    print('STARTING MAIN')
    driver=login()
    
    keyword_list=['CTO', 'Chief Technical officer', 'Technical Engineer', 'Technical officer', 'Technical manager', 'Product Manager', 'Senior Product Manager', 'Senior Architect', 'VP of Engineering', 'VP - IT', 'SVP of Engineering', 'Vice President of Engineering', 'Senior Software Engineer', 'Technical Product Manager', 'Technical Project Manager', 'Technical Program Manager', 'Technical Manager']
    zipcode_list1=['19736', '38157', '60043', '94027','02199','11962','94957','33109','93108','90402','98039','19085','46290','22066']
    zipcode_list2=['77449','11368','60629','79936','90011','11385','90650','77494','91331','77084','90201','10467','11226','11211','11236','11220','92335','8701','11208','11234','90250','11373','91342','90805','75034','37013','90280','60618','90044','10456','92503','10025','92336','11214','75052','11219','94565','75070','78521','11207','92683','60632','60639','92704','11230','10314','11377','30044','91710','77479']
    zipcode_list3=['10001','10018','10022','10036','10016','10013','10017','10019','10003','92101','33166','92660','10011','90025','92618','11354','33134','33131','60606','80202','80112','85260','91436','11201','94103','11219','92626','92121','11101','98004','92705','78701','30024','78216','11211','10002','10010','80111','60611','98101','60062','30096','08701','20850','32819','10012','21401','91730','94538','11235','33186','10021','96813','77056','11220','20036','33172','75034','90015','33431','19103','33139','94111','97701','91367','90067','77002','98052','30339','75093','91761','77036','91710','37027','29607','33178','43215','90010','29464','60007','30328','37203','32256','91748','14221','93003','92108','22030','22314','92024','97401','92780','78746','60601','90064','92037','90069','30004','77024','92614']
    for temp_keyword in keyword_list:
        job_title_search_box=driver.find_element(by=By.XPATH, value='//input[@class="global-search-icon jobtitle-autocomplete"]')
        
        job_title_search_box.send_keys(Keys.CONTROL, 'a')
        job_title_search_box.send_keys(Keys.BACKSPACE)
        job_title_search_box.send_keys(temp_keyword)
        
        zipcode_job_search(temp_keyword, zipcode_list1, driver)
        zipcode_job_search(temp_keyword, zipcode_list2, driver)         #look for job listings in the second job listing list
        zipcode_job_search(temp_keyword, zipcode_list3, driver)
    send_csv_to_self()


main()
