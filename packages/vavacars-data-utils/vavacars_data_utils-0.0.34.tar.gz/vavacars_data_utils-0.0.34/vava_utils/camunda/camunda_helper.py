import json
import requests
import logging
import pandas as pd

class Camunda_Helper():
    def __init__(self, url, token):
        """
        Camunda helper constructor.

        Parameters:
            url: Camunda endpoint
            bearer token:
        """
        self._url = url

        self._headers = {
            'Authorization': f'Basic {token}'
            , 'Content-Type': 'application/json'
        }


    def get_initial_offer(self, car):
        """
        Gets an a initial offer for a vehicle

        Parameters:
            car (pd.Series): vehicle details: year, make, model, bodytype, transmission, fueltype, trim, km, glassroof and retailprice
                - make: string
                - model: string
                - year: integer
                - bodytype: string
                - transmission: string
                - fueltype: string
                - trim: string
                - km: integer
                - glassroof: boolean
                - retailprice: integer
        Returns:
            quotation (pd.Series): Columns:
                - adjmargin: Margin due to price adjusting (fix_price)
                - margin: Total margin (adjmargin + strategymargin + miscmargin)
                - discountpercentage: Total discount applied
                - strategymargin: Margin due just to strategy application
                - minprice: Initial offer price
                - miscmargin: Margin due to other factors (glassroof, temporary strategy, ..)
                - discounttype: "Camunda" or "CamundaError"
        """
        payload = json.dumps({
                "variables": {
                    "make": {
                        "value": car['make'],
                        "type": "String"
                    },
                    "model": {
                        "value": car['model'],
                        "type": "String"
                    },
                    "year": {
                        "value": str(int(car['year'])),
                        "type": "Integer"
                    },
                    "body": {
                        "value": car['bodytype'],
                        "type": "String"
                    },
                    "transmissiontype": {
                        "value": car['transmission'],
                        "type": "String"
                    },
                    "fueltype": {
                        "value": car['fueltype'],
                        "type": "String"
                    },
                    "trimlevel": {
                        "value": car['trim'],
                        "type": "String"
                    },
                    "mileagevalue": {
                        "value": str(car['km']),
                        "type": "Integer"
                    },
                    "description": {
                        "value": "",
                        "type": "String"
                    },
                    "glassroof": {
                        "value": str(bool(car['glassroof'])),
                        "type": "boolean"
                    },
                    "retailprice": {
                    "value": str(int(car['retailprice'])),
                    "type": "Integer"
                    }
                }
        })
        
        try:

            response = requests.request("POST", self._url, headers=self._headers, data=payload)
            
            results_dict = json.loads(response.text)[0]
            return pd.Series(dict(((x, results_dict[x]['value']) for x in results_dict.keys())))
        
        except Exception as e:
            logging.warning(f"Exception {e}: Couldnt get Camunda modifier for {car}")
            return pd.Series({'adjmargin': 0, 'margin': 0, 'discountpercentage': 0, 'strategymargin': 0
                             , 'minprice': 0, 'miscmargin': 0, 'discounttype': 'CamundaError'})
        

