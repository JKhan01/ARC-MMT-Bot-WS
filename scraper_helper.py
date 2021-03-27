from bs4 import BeautifulSoup
import selenium.webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def get_flight_data(source,destination,travel_date,journey_type):
    lang = "eng"
    country_code = "IN"
    cabin_class = "E"
    is_international = "false"
    passenger_type = "A-1_C-0_I-0"
    itinerary_field = f"{source}-{destination}-{travel_date}"
    mmt_url = f"https://www.makemytrip.com/flight/search?itinerary={itinerary_field}&tripType={journey_type}&paxType={passenger_type}&intl={is_international}&cabinClass={cabin_class}&ccde={country_code}&lang={lang}"
    
    
    driver = selenium.webdriver.Chrome('/home/jkhan01/Desktop/chromedriver_linux64/chromedriver')
    driver.get(mmt_url)
    element = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.CLASS_NAME, "commonHeader")))

    body = driver.find_element_by_tag_name("body").get_attribute("innerHTML")
    soupBody = BeautifulSoup(body,'lxml')

    spanFlightName = soupBody.findAll("span", {"class": "airlineName"}) 			# Tags with Flight Name
    pFlightCode = soupBody.findAll("p", {"class": "fli-code"})				# Tags with Flight Code
    divDeptTime = soupBody.findAll("div", {"class": "flightTimeSection"})				# Tags with Departure Time
    pDeptCity = soupBody.findAll("p", {"class": "dept-city"})				# Tags with Departure City
    pFlightDuration = soupBody.findAll("div", {"class": "appendRight40"})			# Tags with Flight Duration
    pArrivalTime = soupBody.findAll("div", {"class": "flightTimeSection"}) 	# Tags with Arrival Time
    pArrivalCity = soupBody.findAll("p", {"class": "arrival-city"})				# Tags with Arrival City
    spanFlightCost = soupBody.findAll("div", {"class": "priceSection"})			# Tags with Flight Cost
    errorCheck = soupBody.find("div",{"id": "fullpage-error"})

    driver.quit()

    response_dict = {"error_flag": '', "response_list":[]}

    if errorCheck:
        print ("Query Didn't yield result")
        response_dict["error_flag"] = "1"
        response_dict["response_list"].append("Your Flight Enquiry Didn't yield any result")
    else:

        response_dict["error_flag"] = "0"
        count = 0
        for i in range(0, len(spanFlightName)):
            
            if count >= 2:
                break
            count += 1
            response_dict["response_list"].append({})   
            print (f"Flight Company: {spanFlightName[i].text}")
            response_dict["response_list"][count-1]["flight_company"] = spanFlightName[i].text 
            print (f"Departure Time: {divDeptTime[i*2].find('span').text}")
            response_dict["response_list"][count-1]["departure_time"] = divDeptTime[i*2].find('span').text
            txt = ''
            for j in pArrivalTime[i*2+1].findAll("span"):
                txt += j.text
            if "+" in txt:
                txt = txt.replace("+"," +")
            print (f"Arrival Time: {txt}")
            response_dict["response_list"][count-1]["arrival_time"] = txt
            flight_price = spanFlightCost[i].findAll('div')[0].text.replace("View Prices","")
            print (f"Ticket Price: {flight_price}")
            response_dict["response_list"][count-1]["flight_price"] = flight_price.split()[1]
            print (f"Flight Duration: {pFlightDuration[i].text}")
            response_dict["response_list"][count-1]["flight_duration"] = pFlightDuration[i].text

    return response_dict
