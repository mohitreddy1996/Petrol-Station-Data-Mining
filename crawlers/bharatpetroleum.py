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
        constants.ANDHRA_PRADESH: "ANDHRA PRADESH",
        constants.Assam: "ASSAM",
        constants.Bihar: "BIHAR",
        constants.Chandigarh: "CHANDIGARH",
        constants.Chhattisgarh: "CHHATTISGARH",
        constants.Dadra_and_Nagar_Haveli: "DADAR AND NAGAR HAVELI",
        constants.Daman_and_Diu: "DAMAN AND DIU",
        constants.Delhi: "DELHI",
        constants.Goa: "GOA",
        constants.Gujarat: "GUJRAT",
        constants.Haryana: "HARYANA",
        constants.Himachal_Pradesh: "HIMACHAL PRADESH",
        constants.Jammu_and_Kashmir: "JAMMU AND KASHMIR",
        constants.Jharkhand: "JHARKAND",
        constants.Kerala: "KERALA",
        constants.Madhya_Pradesh: "MADHYA PRADESH",
        constants.Maharashtra: "MAHARASHTRA",
        constants.Manipur: "MANIPUR",
        constants.Meghalaya: "MEGHALAYA",
        constants.Mizoram: "MIZORAM",
        constants.Nagaland: "NAGALAND",
        constants.ODISHA: "ODISHA",
        constants.Pondicherry: "PONDICHERRY",
        constants.Punjab: "PUNJAB",
        constants.Rajasthan: "RAJASTHAN",
        constants.Sikkim: "SIKKIM",
        constants.Tamil_Nadu: "TAMIL NADU",
        constants.Telangana: "TELANGANA",
        constants.Tripura: "TRIPURA",
        constants.Uttar_Pradesh: "UTTAR PRADESH",
        constants.Uttarakhand: "UTTRAKHAND",
        constants.West_Bengal: "WEST BENGAL"
    }

    ''' Attributes of the received data. Can be modified on how the data should look in the database. '''
    attributes = ["Address", "City", "ContactNo", "Latitude", "Longitude", "Office", "State", "__type", "instAddress", "instCity", "instLatitude", "instLongitude", "instState", "instType", "intLattitude", "intLogitude", "strATM", "strAddress1", "strAuto_Lpg", "strAutomation", "strBath_Facility", "strBranded_Fuels", "strCNG", "strCity", "strCooking_Area", "strCut_on_Divider", "strDormitory", "strEmergency", "strGhar_Dhaba", "strHighway_Type", "strHospitalName", "strHospitalNo", "strIn_Out", "strLoundry", "strLoyalty", "strOfficeType", "strPFS", "strPin", "strPinCode", "strPoliceStnName", "strPoliceStnNo", "strRo_Name", "strSFCCC", "strSapcc", "strSecured_Parking", "strServiceCenter", "strServices", "strSpaccImage", "strSpaccImageUrl", "strState", "strStreet", "strTYPE_OF_Ro", "strToilet"]

    # TODO -- More districts to be added
    curl_state_district_map = {
        constants.KARNATAKA: [
            "BAGALKOT",
            "BANGALORE RUR",
            "BANGALORE URB",
            "BELGAUM",
            "BELLARY",
            "BIDAR",
            "BIJAPUR",
            "CHAMARAJNAGAR",
            "CHICKMAGALUR",
            "CHIKBALLAPUR",
            "CHITRADURGA",
            "DAVANGERE",
            "DHARWAD",
            "GADAG",
            "GULBERGA",
            "HASSAN",
            "HAVERI",
            "KODAGU",
            "KOLAR",
            "KOPPAL",
            "MANDYA",
            "MYSORE",
            "NORTH KANARA",
            "RAICHUR",
            "RAMNAGARA",
            "SHIMOGA",
            "SOUTH KANNADA",
            "TUMKUR",
            "YADGIR",
            "UDUPI"
        ],
        constants.Arunachal_Pradesh: [
            "CHANGLANG",
            "PAPUM PARE",
            "SIANG WEST"
        ],
        constants.ANDHRA_PRADESH: [
            "ANANTAPUR",
            "CHITTOOR",
            "EAST GODAVARI",
            "GUNTUR",
            "KADAPA",
            "KRISHNA",
            "KURNOOL",
            "NELLORE",
            "PRAKASAM",
            "SRIKAKULAM",
            "VISAKHAPATNAM",
            "VIZIANAGARAM",
            "WEST GODAVARI"
        ],
        constants.Assam: [
            "BARPETA",
            "BONGAIGAON",
            "CACHAR",
            "DARRANG",
            "DHEMAJI",
            "DHUBRI",
            "DIBRUGARH",
            "GOALPARA",
            "JORHAT",
            "KAMRUP",
            "KOKRAJHAR",
            "MARIGAON",
            "NAGAON",
            "NALBARI",
            "SIBSAGAR",
            "SONITPUR",
            "TINSUKIA"
        ],
        constants.Bihar: [
            "ARARIA",
            "ARWAL",
            "AURANGABAD",
            "BANKA",
            "BEGUSARAI",
            "BHAGALPUR",
            "BHOJPUR",
            "BUXAR",
            "CHAMPARAN EAST",
            "CHAMPARAN WEST",
            "DARBHANGA",
            "GAYA",
            "GOPALGANJ",
            "JAMUI",
            "JEHANABAD",
            "KAIMUR",
            "KATIHAR",
            "KHAGARIA",
            "KISHANGANJ",
            "LAKHISARAI",
            "MADHEPURA",
            "MADHUBANI",
            "MUNGER",
            "MUZZAFARPUR",
            "NALANDA",
            "NAWADA",
            "PATNA",
            "PURNIA",
            "ROHTAS SASARAM",
            "SAHARSA",
            "SAMASTIPUR",
            "SARAN",
            "SHEIKHPURA",
            "SHEOHAR",
            "SIWAN",
            "SUPAUL",
            "VAISHALI"
        ],
        constants.Chandigarh: [

        ],
        constants.Chhattisgarh: [
            "BALOD",
            "BALODABAZAR",
            "BALRAMPUR",
            "BEMETARA",
            "BILASPUR",
            "DHAMTARI",
            "DURG",
            "GARIYABAND",
            "JANJGIR CHAMPA",
            "KANKER",
            "KORBA",
            "KOREA",
            "MAHASAMUND",
            "RAIGARH",
            "RAIPUR",
            "RAJANANDGAON",
            "SARGUJA",
            "SURAJPUR"
        ],
        constants.Dadra_and_Nagar_Haveli: [

        ],
        constants.Daman_and_Diu: [

        ],
        constants.Delhi: [
            "NORTH WEST DELHI"
            "SHAHDARA",
            "WEST DELHI"
        ],
        constants.Goa: [
            "NORTH GOA",
            "SOUTH GOA"
        ],
        constants.Gujarat: [
            "AHMEDABAD",
            "AMRELI",
            "ANAND",
            "ARVALLI",
            "BANASKAHTHA",
            "BHARUCH",
            "BHAVNAGAR",
            "BOTAD",
            "CHHOTAUDEPUR",
            "DAHOD",
            "DEVBHUMI DWARKA",
            "GANDHINAGAR",
            "GIR SOMNATH",
            "JAMNAGAR",
            "JUNAGADH",
            "KHEDA KAIRA",
            "KUTCHCHH",
            "MAHISAGAR",
            "MEHSANA",
            "MORBI",
            "NARMADA",
            "NAVSARI",
            "PATAN",
            "PORBANDAR",
            "RAJKOT",
            "SABARKANTHA",
            "SURAT",
            "SURENDRANAGAR",
            "TAPI",
            "VADODARA",
            "VALSAD"
        ],
        constants.Haryana: [
            "AMBALA",
            "BHIWANI",
            "FARIDABAD",
            "FATEHBAD",
            "GURGAON",
            "HISAR",
            "JHAJJAR",
            "JIND",
            "KAITHAL",
            "KARNAL",
            "KURUKSHETRA",
            "MAHENDERGARH",
            "MEWAT",
            "PALWAL",
            "PANCHKULA",
            "PANIPAT",
            "REWARI",
            "ROHTAK",
            "SIRSA",
            "SONEPAT",
            "YAMUNA NAGAR"
        ],
        constants.Himachal_Pradesh: [

        ],
        constants.Jammu_and_Kashmir: [
            "ANANTNAG",
            "BADGAM",
            "BANDIPORA",
            "BARAMULA",
            "GANDERBAL",
            "JAMMU",
            "KUPWARA",
            "POONCH",
            "PULWAMA",
            "REASI",
            "SHOPIAN",
            "SRINAGAR"
        ],
        constants.Jharkhand: [
            "BOKARO",
            "CHATRA",
            "DEOGHAR",
            "DHANBAD",
            "DUMKA",
            "GARHWA",
            "GIRIDIH",
            "GODDA",
            "GUMLA",
            "HAZARIBAGH",
            "JAMTARA",
            "KODERMA",
            "LATEHAR",
            "PALAMU",
            "RAMGARH",
            "RANCHI",
            "SAHEBGANJ",
            "SERAIKALA KARSAWAN",
            "SINGHBHUM EAST",
            "SINGHBHUM WEST",
        ],
        constants.Kerala: [
            "ALAPPUZHA",
            "ERNAKULUM",
            "IDUKKI",
            "KANNUR",
            "KASARGOD",
            "KOLLAM",
            "KOTTAYAM",
            "KOZHIKODE",
            "MALAPPURAM",
            "PALAKKAD",
            "PATHNAMTHITA",
            "THIRUVANANTHAPURAM",
            "THRISSUR",
            "WAYANAD"
        ],
        constants.Madhya_Pradesh: [
            "AGAR-MALWA",
            "ALIRAJPUR",
            "ANUPPUR",
            "ASHOKNAGAR",
            "BALAGHAT",
            "BARWANI",
            "BETUL",
            "BHIND",
            "BHOPAL",
            "CHHATTARPUR",
            "CHHINDWARA",
            "DAMOH",
            "DATIA",
            "DEWAS",
            "DHAR",
            "GUNA",
            "GWALIOR",
            "HARDA",
            "HOSHANGABAD",
            "INDORE",
            "JABALPUR",
            "JHABUA",
            "KHANDWA",
            "KHARGONE",
            "MANDASAUR",
            "MANDLA",
            "MORENA",
            "NARSINGHPUR",
            "PANNA",
            "RAISEN",
            "RAJGARH",
            "RATLAM",
            "REWA",
            "SAGAR",
            "SATNA",
            "SEHORE",
            "SEONI",
            "SHAHDOL",
            "SHAJAPUR",
            "SHIVPURI",
            "SIDHI",
            "SINGRAULI",
            "TIKAMGARH",
            "UJJAIN",
            "UMARIA",
            "VIDISHA"
        ],
        constants.Maharashtra: [
            "AHMEDNAGAR",
            "AKOLA",
            "AMRAVATI",
            "AURANGABAD",
            "BEED",
            "BHANDARA",
            "BHULDANA",
            "CHANDRAPUR",
            "DHULE",
            "GADCHIROLI",
            "GONDIA",
            "JALGAON",
            "JALNA",
            "KOLHAPUR",
            "LATUR",
            "MUMBAI CITY",
            "MUMBAI SUBURBAN",
            "NAGPUR",
            "NANDED",
            "NANDURBAR",
            "NASIK",
            "OSMANABAD",
            "PALGHAR",
            "PARBHANI",
            "PUNE",
            "RAIGAD",
            "RATNAGIRI",
            "SANGLI",
            "SATARA",
            "SHOLAPUR",
            "SINDHUDURG",
            "THANA",
            "WARDHA",
            "WASHIM",
            "YAVATMAL"
        ],
        constants.Manipur: [

        ],
        constants.Meghalaya: [
            "EAST KHASI HILLS",
            "RI BHOI",
            "WEST GARO HILLS",
            "WEST JAINTIA HILLS",
            "WEST KHASI HILLS"
        ],
        constants.Mizoram: [

        ],
        constants.Nagaland: [

        ],
        constants.ODISHA: [
            "ANGUL",
            "BALASORE",
            "BARGARH",
            "BHADRAK",
            "BOLANGIR",
            "CUTTACK",
            "DHENKANAL",
            "GANJAM",
            "JAGATSINGHPUR",
            "JAJPUR",
            "JHARSUGUDA",
            "KALAHANDI",
            "KANDHAMAL",
            "KENDRAPADA",
            "KENDUJHAR",
            "KHORDHA",
            "KORAPUT",
            "MAYURBHANJ",
            "NABARANGAPUR",
            "NAYAGARH",
            "PURI",
            "RAYAGADA",
            "SAMBALPUR",
            "SUNDERGARH"
        ],
        constants.Pondicherry: [

        ],
        constants.Punjab: [
            "AMRITSAR",
            "BARNALA",
            "BATHINDA",
            "FARIDKOT",
            "FATEHGARH SAHIB",
            "FAZILKA",
            "GURDASPUR",
            "HOSHIARPUR",
            "JALANDHAR",
            "KAPURTHALA",
            "LUDHIANA",
            "MAANSA",
            "PATHANKOT",
            "PATIALA",
            "SANGRUR",
            "SAS NAGAR",
            "TARAN TARAN"
        ],
        constants.Rajasthan: [
            "AJMER",
            "ALWAR",
            "BANSWARA",
            "BARAN",
            "BARMER",
            "BHARATPUR",
            "BHILWARA",
            "BIKANER",
            "BUNDI",
            "CHITTORGARH",
            "CHURU",
            "DAUSA",
            "DHOLPUR",
            "DUNGARPUR",
            "HANUMANGARH",
            "JAIPUR",
            "JAISALMER",
            "JALORE",
            "JHALAWAR",
            "JHUNJHUNU",
            "JODHPUR",
            "KARAULI",
            "KOTA",
            "NAGAUR",
            "PALI",
            "PRATAPGARH",
            "RAJ SAMAND",
            "SAWAIMADHOPUR",
            "SIKAR",
            "SIROHI",
            "SRI GANGANAGAR",
            "TONK",
            "UDAIPUR"
        ],
        constants.Sikkim: [
            "SIKKIM EAST",
            "SIKKIM NORTH",
            "SIKKIM SOUTH",
            "SIKKIM WEST"
        ],
        constants.Tamil_Nadu: [
            "ARIYALUR",
            "CHENNAI",
            "COIMBATORE",
            "CUDDALORE",
            "DHARMAPURI",
            "DINDIGUL",
            "ERODE",
            "KANCHIPURAM",
            "KANYA-KUMARI",
            "KARUR",
            "KRISHNAGIRI",
            "MADURAI",
            "NAGAPATTINAM",
            "NAMAKKAL",
            "PERAMBALUR",
            "PUDUKKOTTAI",
            "RAMANATHAPURAM",
            "SALEM",
            "SIVAGANGA",
            "THANJAVUR",
            "THENI",
            "THOOTHUKUDI",
            "TIRUCHIRAPPALLI",
            "TIRUNELVELI",
            "TIRUPPUR",
            "TIRUVALLUR",
            "TIRUVANNAMALAI",
            "TIRUVARUR",
            "VELLORE AMBEDKR",
            "VILLUPURAM",
            "VIRUDHUNAGAR"
        ],
        constants.Telangana: [
            "ADILABAD",
            "HYDERABAD",
            "KARIMNAGAR",
            "KHAMMAM",
            "MAHBUBNAGAR",
            "MEDAK",
            "NALGONDA",
            "NIZAMABAD",
            "RANGA REDDY",
            "WARANGAL"
        ],
        constants.Tripura: [

        ],
        constants.Uttar_Pradesh: [
            "AGRA",
            "ALIGARH",
            "ALLAHABAD",
            "AMBEDKAR NAGAR",
            "AMETHI",
            "AMROHA",
            "AURAIYA",
            "AZAMGARH",
            "BAGHPAT",
            "BAHRAICH",
            "BALLIA",
            "BALRAMPUR",
            "BANDA",
            "BARA BANKI",
            "BAREILLY",
            "BASTI",
            "BIJNOR",
            "BUDAUN",
            "BULANDSHAHR",
            "CHANDAULI",
            "CHITRUKUT",
            "DEORIA",
            "ETAH",
            "ETAWAH",
            "FAIZABAD",
            "FARRUKHABAD",
            "FATEHPUR EAST",
            "FEROZABAD",
            "GAUTAM BUDH NAGAR",
            "GAZIPUR",
            "GHAZIABAD",
            "GONDA",
            "GORAKHPUR",
            "HARDOI",
            "HATHRAS",
            "JALAUN",
            "JAUNPUR",
            "JHANSI",
            "KANNUJ",
            "KANPUR DEHAT",
            "KANPUR NAGAR",
            "KAUSHAMBI",
            "KUSHINAGAR",
            "LAKHIMPUR",
            "LALITPUR",
            "LUCKNOW",
            "MAHARAJGANJ",
            "MAHOBA",
            "MAINPURI",
            "MATHURA",
            "MEERUT",
            "MIRZAPUR",
            "MORADABAD",
            "MUZAFFARNAGAR",
            "PILBHIT",
            "PRATAPGARH",
            "RAE BAREILLY",
            "RAMPUR",
            "SAHARANPUR",
            "SAMBHAL",
            "SANT RAVI NAGAR",
            "SHAHJAHANPUR",
            "SHAMLI",
            "SIDHARATH NAGAR",
            "SITAPUR",
            "SONBHADRA",
            "SULTANPUR",
            "UNNAO",
            "VARANASI"
        ],
        constants.Uttarakhand: [
            "DEHRADUN",
            "HARIDWAR",
            "NAINITAL",
            "PAURI GARHWAL",
            "UDHAM SINGH NAGAR",
        ],
        constants.West_Bengal: [
            "ALIPURDUAR",
            "BANKURA",
            "BARDHAMAN",
            "BIRBHUM",
            "COOCHBEHAR",
            "DAKSHIN DINAJPUR",
            "DARJEELING",
            "HOOGHLY",
            "HOWRAH",
            "JALPAIGURI",
            "KOKATA",
            "MALDA",
            "MURSHIDABAD",
            "NADIA",
            "NORTH 24 PARGANAS",
            "PASCHIM MEDINIPUR",
            "PURBA MEDINIPUR",
            "PURULIA",
            "SOUTH 24 PARGANAS",
            "UTTAR DINAJPUR",
        ]
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
                try:
                    curl_command = curl_base_command.replace("__state_name__", "\"" + self.curl_state_names_map[state] + "\"")
                    curl_command = curl_command.replace("__district_name__", "\"" + district + "\"")
                    curl_command = curl_command.replace("__service_number__", "\"" + self.curl_service_number[
                        constants.ALL] + "\"")
                    curl_command = curl_command.replace("__category_name__", "\"" + self.curl_category_name[
                        constants.FUELSTATION] + "\"")
                    res = utils.robust_curl(curl_command, sleep_seconds=0)
                    data = json.loads(res)
                    self.get_attributes(data)
                    # ToDo - Currently adjusting with warning. Change it to info and change priority (google).
                    logging.warning("Items Saved as of now : " + str(self.count))
                except:
                    logging.warning("Failed for the curl : " + curl_command)

    def get_attributes(self, data):
        data = data["d"]
        for dataObj in data:
            dto = {}
            for attr in self.attributes:
                dto[attr] = utils.get_attr(dataObj, attr)
            self.store_dto(dto)
            self.count += 1


