import requests
import json
import logging
import pandas as pd
import time
from ..utils.comparisons import get_best_match

_WAITING_TIME_AFTER_ERROR = 0.25
_MANDATORY_COLUMNS = {'year', 'make', 'model', 'bodytype', 'transmission', 'fueltype', 'trim', 'km'} 
_COLS_TO_MATCH = ['make', 'model', 'bodytype', 'transmission', 'fueltype', 'trim']

def catalog_to_wizard_cache(df):
    """
    Creates a dictionary to be used as wizard cache from SmartIQ Catalog.

    Parameters:
        df (pd.DataFrame): SmartIQ Catalog. Columns: make_id, make, model_id, model, bodytype_id, bodytype, 
                           transmission_id, transmission, fueltype_id, fueltype, trim_id, trim 

    Returns:
        wizard_cache (dict): dictionary with all wizard IDs retrieved from the catalog 
    """
    df = df.copy() # is there a better way to do this?
    df['trim'] = df[_COLS_TO_MATCH].apply(':'.join, axis=1)
    df['model'] = df[['make', 'model']].apply(':'.join, axis=1)
    wizard_cache = {}
    for name in _COLS_TO_MATCH:
        wizard_cache.update({
            k:v for k,v in df[[name, name + '_id']].values
        })
    return wizard_cache

class SmartIq_Helper():
    def __init__(self, url_basewizard, url_quotation, api_user, api_key, wizard_cache={}):
        """
        SmartIq_helper constructor.

        Parameters:
            url_basewizard: URL for SmartIQ wizard
            url_quotation: URL for GetQuotation in SmartIQ
            api_user:
            api_key:
        """
        self._url_basewizard = url_basewizard
        self._url_quotation = url_quotation
        self._auth_dict = {
            "apiUser": api_user,
            "apiKey": api_key
        }

        self.wizard_cache = wizard_cache        

    def getWizardId(self, query_string, keyname, value):
        """
        Gets an id using the SmartIQ Wizard. Id could be for year, brand, make, model, fuel, transmission or trim

        Parameters:
            query_string (str): query string (including url) to invoke wizard
            keyname (str): "BrandId"/"ModelId"/...
            value (str): Value to look for in all the ones returned by wizard

        Returns:
            new_query_string (str): Next query string (adding &keyname=bestid)
            best_value: value that was a closer match to the one requested

        Raises:
            Exception if there is no valid value (similar to the one we are looking)
        """
        # Look in cache
        if value in self.wizard_cache:
            return f"{query_string}&{keyname}={self.wizard_cache[value]}", value

        try:
            x = requests.post(query_string, json=self._auth_dict)
            if x.status_code != 200:
                raise Exception(f"Error when querying wizard - status code = {x.status_code}")
        except Exception as e:
            raise Exception({'message': str(e), 'wrong_value': value})

        items = json.loads(x.text)['data']['items']
        
        rev_dic = {i['name']: i['id'] for i in items}
        best_value, best_score = get_best_match(value.split(':')[-1], rev_dic.keys())
        
        # Cache values (do not cache partial matches, contextual options may vary)

        self.wizard_cache.update({value.replace(value.split(':')[-1],k):v for k,v in rev_dic.items()})
        
        if best_score < 0.5:
            msg = f"Wrong combination of features with: {query_string.split('?')[1]} + {keyname}: {value}, best was {best_value} with {best_score}"
            logging.warn(msg)

            raise Exception({'message': msg, 'wrong_value': value})

        best_id = rev_dic[best_value]
        return f"{query_string}&{keyname}={best_id}", best_value

    def get_quotation(self, car):
        """
        Gets an quotation for a vehicle

        Parameters:
            car (pd.Series): vehicle details: year, make, model, bodytype, transmission, fueltype, trim and km + damages (optional, see below)

        Returns:
            quotation (pd.Series): Columns: smartiq_retail, smartiq_io, smartiq_matching_trimelevel, smartiq_comments

        Damages are optional, if you want a quotation including damages, add them using the following format in the proper column (car['damages']):

        damages = [  
            {'sectionType': 'LEFT_FRONT_FENDER', 'state': 'SCRATCHED'}, 
            {'sectionType': 'CEILING', 'state': 'PAINTED'},
            ...
        ]

        where:

        section_types can be:
            * 'LEFT_FRONT_FENDER'
            * 'RIGHT_FRONT_FENDER'
            * 'LEFT_FRONT_DOOR'
            * 'RIGHT_FRONT_DOOR'
            * 'LEFT_REAR_FENDER'
            * 'RIGHT_REAR_FENDER'
            * 'LEFT_REAR_DOOR'
            * 'RIGHT_REAR_DOOR' 
            * 'FRONT_HOOD'
            * 'REAR_HOOD'
            * 'CEILING'
        
        and state:
            * 'REPLACED'
            * 'PAINTED'
            * 'SCRATCHED'
        """

        missing_columns =  _MANDATORY_COLUMNS - set(car.keys())
        if missing_columns:
            logging.warning(f"Missing car parameters: {missing_columns}")
            return pd.Series({'smartiq_retail': 0
                             , 'smartiq_io': 0
                             , 'smartiq_matching_trimlevel': None
                             , 'smartiq_comments': f"WRONG REQUESTS, missing parameters: {missing_columns}"})

        try:
            url = self._url_basewizard + f"?year={car['year']}"
            url, _ = self.getWizardId(url, 'brandId', car['make'])
            url, _ = self.getWizardId(url, 'modelId', ':'.join(car[['make', 'model']]))
            url, _ = self.getWizardId(url, 'bodyTypeId', car['bodytype'])
            url, _ = self.getWizardId(url, 'transmissionTypeId', car['transmission'])
            url, _ = self.getWizardId(url, 'fuelTypeId', car['fueltype'])
            url, smartiq_trim = self.getWizardId(url, 'versionId', ':'.join(car[_COLS_TO_MATCH]))
        except Exception as e:
            logging.warning(e)
            return pd.Series({'smartiq_retail': 0
                                 , 'smartiq_io': 0
                                 , 'smartiq_matching_trimlevel': None
                                 , 'smartiq_comments': f"WIZARD_ERROR: {e.args[0]['wrong_value']}"})

        car_metadata = {y[0]: y[1] for y in [x.split('=') for x in url.split("?")[1].split('&')]}
                                                      
        try:

            quotation_body = {
                'auth': self._auth_dict
                , 'carMetadata': car_metadata
                , 'kilometer': int(car['km'])
                , 'damages': car.get('damages', [])
            }

            x = requests.post(self._url_quotation, json=quotation_body)
            data = json.loads(x.text)['data']

            if 'prediction' not in data:
                logging.warning(f"Error when getting quotation: {data}")
                return pd.Series({'smartiq_retail': 0
                                     , 'smartiq_io': 0
                                     , 'smartiq_matching_trimlevel': smartiq_trim
                                     , 'smartiq_comments': f"QUOTATION_ERROR: {data['status_code']}"})

            retail = int(data['prediction']['retailPrice'])
            io = int(data['prediction']['galleryPriceDown'])
            return pd.Series({'smartiq_retail': retail
                                 , 'smartiq_io': io
                                 , 'smartiq_matching_trimlevel': smartiq_trim
                                 , 'smartiq_comments': "OK"})

        except Exception as e:
            logging.warning(e)
            time.sleep(_WAITING_TIME_AFTER_ERROR)
            return pd.Series({'smartiq_retail': 0
                                 , 'smartiq_io': 0
                                 , 'smartiq_matching_trimlevel': None
                                 , 'smartiq_comments': f"QUOTATION_EXCEPTION: {str(e)}"})
