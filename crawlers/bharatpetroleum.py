import json

import utils.constants
from utils import utils, constants, properties as props
from Storage import mongo_client
import logging

# TODO -- Try to index each entry. Think of something unique in each entry.

# TODO -- set logging info to print in the console.
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# Helper class for BharatPetroluem data crawling.

class BharatPetroleumHelper:

    curl_template_map = {
        constants.BP_CURL: """ curl 'https://bharatpetroleum.com/Our-Businesses/Fuels-and-Services/Ajaxmap.aspx/GetAllOffice' -H 'Cookie: TriedTohack=True; _ga=GA1.2.1200029132.1472066719; _gat=1; ASP.NET_SessionId=od2iujvaxu3jkeqzealiqimmQmB7JGBEkCqvqMlHOtVG67/gTV8=' -H 'Origin: https://bharatpetroleum.com' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.8' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36' -H 'Content-Type: application/json' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Referer: https://bharatpetroleum.com/Our-Businesses/Fuels-and-Services/Ajaxmap.aspx' -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' --data-binary '{"strState": __state_name__ ,"strCity": __district_name__,"strCategory": __category_name__,"strService": __service_number__,"strOffice":"noofficefound"}' --compressed """
    }

    # TODO -- More states to be added.
    curl_state_names_map = {
        constants.KARNATAKA: "KARNATAKA",
        # constants.ANDHRA_PRADESH: "ANDHRA PRADESH"
    }

    ''' Attributes of the received data. Can be modified on how the data should look in the database. '''
    attributes = ["Address", "City", "ContactNo", "Latitude", "Longitude", "Office", "State", "__type", "instAddress", "instCity", "instLatitude", "instLongitude", "instState", "instType", "intLattitude", "intLogitude", "strATM", "strAddress1", "strAuto_Lpg", "strAutomation", "strBath_Facility", "strBranded_Fuels", "strCNG", "strCity", "strCooking_Area", "strCut_on_Divider", "strDormitory", "strEmergency", "strGhar_Dhaba", "strHighway_Type", "strHospitalName", "strHospitalNo", "strIn_Out", "strLoundry", "strLoyalty", "strOfficeType", "strPFS", "strPin", "strPinCode", "strPoliceStnName", "strPoliceStnNo", "strRo_Name", "strSFCCC", "strSapcc", "strSecured_Parking", "strServiceCenter", "strServices", "strSpaccImage", "strSpaccImageUrl", "strState", "strStreet", "strTYPE_OF_Ro", "strToilet"]

    # TODO -- More districts to be added
    curl_state_district_map = {
        constants.KARNATAKA: {
            constants.BAGALKOT: "BAGALKOT",
            constants.BANGALORE_RUR: "BANGALORE RUR",
            constants.BANGALORE_URB: "BANGALORE URB",
            constants.BELGAUM: "BELGAUM",
            constants.BELLARY: "BELLARY",
            constants.BIDAR: "BIDAR",
            constants.BIJAPUR: "BIJAPUR",
            constants.CHAMARAJNAGAR: "CHAMARAJNAGAR",
            constants.CHICKMAGALUR: "CHICKMAGALUR",
            constants.CHIKBALLAPUR: "CHIKBALLAPUR",
            constants.CHITRADURGA: "CHITRADURGA",
            constants.DAVANGERE: "DAVANGERE",
            constants.DHARWAD: "DHARWAD",
            constants.GADAG: "GADAG",
            constants.GULBERGA: "GULBERGA",
            constants.HASSAN: "HASSAN",
            constants.HAVERI: "HAVERI",
            constants.KODAGU: "KODAGU",
            constants.KOLAR: "KOLAR",
            constants.KOPPAL: "KOPPAL",
            constants.MANDYA: "MANDYA",
            constants.MYSORE: "MYSORE",
            constants.NORTH_KANARA: "NORTH KANARA",
            constants.RAICHUR: "RAICHUR",
            constants.RAMNAGARA: "RAMNAGARA",
            constants.SHIMOGA: "SHIMOGA",
            constants.SOUTH_KANNADA: "SOUTH KANNADA",
            constants.TUMKUR: "TUMKUR",
            constants.YADGIR: "YADGIR",
            constants.UDUPI: "UDUPI"
        }
    }

    # TODO -- More categories to be added.
    curl_category_name = {
        constants.FUELSTATION: "fulestation"
    }

    # TODO -- more service numbers to be added.
    curl_service_number = {
        constants.ALL: "24"
    }

    def __init__(self):
        self.count = 0
        pass

    @staticmethod
    def get_retailer():
        return constants.bp

    ''' Stores the dto - data object, in the mongo database. Database code abstracted out. For general Use. '''
    @staticmethod
    def store_dto(dto):
        mongo_client.insert_dto(props.COLL_BHARAT_PETROLEUM, dto)

    ''' Main Function which fetches the data from the website and stores in the database.'''
    def fetch_details(self):
        # Take the curl command. replace the state name, and put each district and category and service name of choice and fetch details.
        curl_base_command = self.curl_template_map[constants.BP_CURL]
        for state in self.curl_state_names_map:
            for district in self.curl_state_district_map[state]:
                # currently doing only for service number 24 and category fuel station. TODO -- Will extend to other category and services(if required).
                curl_command = curl_base_command.replace("__state_name__", "\"" + self.curl_state_names_map[state] + "\"")
                curl_command = curl_command.replace("__district_name__", "\"" + self.curl_state_district_map[state][district] + "\"")
                curl_command = curl_command.replace("__service_number__", "\"" + self.curl_service_number[
                    constants.ALL] + "\"")
                curl_command = curl_command.replace("__category_name__", "\"" + self.curl_category_name[
                    constants.FUELSTATION] + "\"")
                res = utils.robust_curl(curl_command, sleep_seconds=0)
                data = json.loads(res)
                self.get_attributes(data)
                # ToDo - Currently adjusting with warning. Change it to info and change priority (google).
                logging.warning("Items Saved as of now : " + str(self.count))

    def get_attributes(self, data):
        data = data["d"]
        for dataObj in data:
            dto = {}
            for attr in self.attributes:
                dto[attr] = utils.get_attr(dataObj, attr)
            self.store_dto(dto)
            self.count += 1


