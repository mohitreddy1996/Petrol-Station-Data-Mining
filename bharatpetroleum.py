import json
import logging
import re
from lxml import html

import constants
import utils


# Helper class for BharatPetroluem data crawling.

class BharatPetroleumHelper:

    curl_template_map = {
        constants.BP_CURL: """ curl 'https://bharatpetroleum.com/Our-Businesses/Fuels-and-Services/Ajaxmap.aspx/GetAllOffice' -H 'Cookie: TriedTohack=True; _ga=GA1.2.1200029132.1472066719; _gat=1; ASP.NET_SessionId=od2iujvaxu3jkeqzealiqimmQmB7JGBEkCqvqMlHOtVG67/gTV8=' -H 'Origin: https://bharatpetroleum.com' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.8' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36' -H 'Content-Type: application/json' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Referer: https://bharatpetroleum.com/Our-Businesses/Fuels-and-Services/Ajaxmap.aspx' -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' --data-binary '{"strState": __state_name__ ,"strCity": __city_name__,"strCategory": __category_name__,"strService": __service_number__,"strOffice":"noofficefound"}' --compressed """
    }

    # TODO -- More to be added.
    curl_state_names_map = {
        constants.KARNATAKA: "KARNATAKA",
        # constants.ANDHRA_PRADESH: "ANDHRA PRADESH"
    }

    # TODO -- More to be added
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

    # TODO -- More to be added.
    curl_category_name = {
        constants.FUELSTATION: "fulestation"
    }

    # TODO -- more to be added.
    curl_service_number = {
        constants.ALL: "24"
    }

    def __init__(self):
        pass

    @staticmethod
    def get_retailer():
        return constants.bp

    def fetch_details(self):
        # Take the curl command. replace the state name, and put each district and category and service name of choice and fetch details.
        curl_base_command = self.curl_template_map[constants.BP_CURL]
        for state in self.curl_state_names_map:
            for district in self.curl_state_district_map[state]:
                # currently doing only for service number 24 and category fuel station. TODO -- Will extend to other category and services(if required).
                curl_command = curl_base_command.replace("__state_name__", state)
                curl_command = curl_command.replace("__district_name__", district)
                curl_command = curl_command.replace("__service_number__", self.curl_service_number[constants.ALL])
                curl_command = curl_command.replace("__category_name__", self.curl_category_name[constants.FUELSTATION])
                res = utils.robust_curl(curl_command, sleep_seconds=0)
                data = json.loads(res)

                logging.info(data);
