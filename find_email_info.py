from selenium.webdriver.common.by import By


def find_email_info(driver):
    mailto_url = driver.find_element(by=By.XPATH, value='//a[@class="recruiter-email-link s-link"]').get_attribute(
        'href').replace('%20', ' ')

    # slicing the mailto url string to get the email contents
    email_receiver = mailto_url[mailto_url.index('mailto:') + 7:mailto_url.index('?subject=')]
    subject = mailto_url[mailto_url.index('?subject=') + 9:]

    # finding the location of where the job listing is
    location = driver.find_element(by=By.XPATH,
                                   value='//div[@class="location"]//following-sibling::span//following-sibling::span').text
    try:
        location = location[:location.index('•')]
    except:
        pass
    print(location)
    return email_receiver, subject, location
