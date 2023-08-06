import requests
import json
import logging
import pandas as pd
import time
import redis
from ..utils.comparisons import get_best_match

_WAITING_TIME_AFTER_ERROR = 0.25
_MANDATORY_COLUMNS = {'year', 'make', 'model', 'bodytype', 'transmission', 'fueltype', 'trim', 'km'} 
_COLS_TO_MATCH = ['make', 'model', 'bodytype', 'transmission', 'fueltype', 'trim']
_KMS_CLOSE = 100

class SmartIq_Helper_v2():
    def __init__(self, url_quotation, api_user, api_key, redis_host, redis_port, redis_password):
        """
        SmartIq_helper constructor.

        Parameters:
            url_quotation: URL for GetQuotation in SmartIQ
            api_user:
            api_key:
            redis_host:
            redis_port:
            redis_password:

        In redis we will have two databases:
            0. Wizard
            1. Price cache
        
        We change using r.select(0) or r.select(1)

        """
        self._url_quotation = url_quotation
        self._auth_dict = {
            "apiUser": api_user,
            "apiKey": api_key
        }

        logging.info(f"Connecting to redis")
        self.redis_conn = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, ssl=True)
        self.redis_conn.ping() # TODO: If wrong, raise exception
        self.local_cache = {}


    def getRedisQueryString(self, query_string, value):
        # Redis query strings are stored like: siq-wizard:2018:Renault:Clio:Hatchback:Otomatik:Dizel:1.2 Tce Touch
        if value in self.local_cache:
            return ":".join([query_string, value])

        possible_values = [str(s, 'utf-8') for s in self.redis_conn.smembers(query_string)]
        best_value, best_score = get_best_match(str(value), possible_values)
        if best_score < 0.5:
            msg = f"Wrong combination of features with {query_string} + {value}, best was {best_value} with {best_score}"
            logging.warning(msg)
            raise Exception({'message': msg, 'wrong_value': value})

        return ":".join([query_string, best_value])


    def get_matching_labels(self, car):
        """
        For a vehicle (year, make, model, ...) get the make, model, body, trans, fuel and trim matching the catalog.

        First look into local cache, if not use redis where full catalog is stored
        """
        # Try local cache (trim is special concat all)
        labels = [car[x] for x in _COLS_TO_MATCH[:-1]]
        labels += [":".join(str(car[x]) for x in _COLS_TO_MATCH)]
        ids = [self.local_cache.get(l) for l in labels]

        if all(ids): # Found in local cache, return it
            return list(zip(_COLS_TO_MATCH, labels, ids))

        self.redis_conn.select(0) # db=0 for wizard
        query = f'siq-wizard:{car["year"]}'
        for x in _COLS_TO_MATCH:
            query = self.getRedisQueryString(query, car[x])
        
        labels = query.split(':')[2:-1] # Trim is special
        labels += [":".join([str(car['year'])] + query.split(':')[2:])]
        ids = [int(i) for i in self.redis_conn.mget(['siq-name-lkp:' + x for x in labels])]
        
        # make, model, bodytype, transmission, fuel, trim
        matching_labels_ids = list(zip(_COLS_TO_MATCH, labels, ids))

        # Locally cache it
        for _, l, i in matching_labels_ids:
            self.local_cache[l] = i
        
        return matching_labels_ids        

    def get_quotation(self, car, cache_only=False):
        """
        Gets an quotation for a vehicle

        Parameters:
            car (pd.Series): vehicle details: year, make, model, bodytype, transmission, fueltype, trim and km

        Returns:
            quotation (pd.Series): Columns: smartiq_retail, smartiq_io, smartiq_matching_trimelevel, smartiq_comments

        No damage support due to caching
        """
        missing_columns =  _MANDATORY_COLUMNS - set(car.keys())
        if missing_columns:
            return self.return_error_quotation(f"wrong request, missing car parameters: {missing_columns}")

        try:
            matching_labels_ids = self.get_matching_labels(car)
        except Exception as e:
            return self.return_error_quotation(str(e))

        # Check if price is cached
        vehicle_str_ids = ":".join([str(car['year']),] + [str(x[2]) for x in matching_labels_ids])
        vehicle_str_labels = ":".join([str(car['year']),] + [x[1] for x in matching_labels_ids])
        retail, io = self.get_cached_price(vehicle_str_ids, car['km'])
        if retail:
            return self.return_valid_quotation(retail, io, matching_labels_ids[5][1], 'OK (cache)')
        elif cache_only:
            return self.return_error_quotation(f"price not in cache and cache_only=True")

        try:
            quotation_body = {'auth': self._auth_dict
                              , 'carMetadata': {'year': car['year']
                                                , 'brandId': matching_labels_ids[0][2]
                                                , 'modelId': matching_labels_ids[1][2]
                                                , 'bodyTypeId': matching_labels_ids[2][2]
                                                , 'transmissionTypeId': matching_labels_ids[3][2]
                                                , 'fuelTypeId': matching_labels_ids[4][2]
                                                , 'versionId': matching_labels_ids[5][2] 
                                                }
                               , 'kilometer': int(car['km'])
                               , 'damages': []}

            x = requests.post(self._url_quotation, json=quotation_body)
            data = json.loads(x.text)['data']

            if 'prediction' not in data:
                return self.return_error_quotation(f"trim={matching_labels_ids[5][1]}, error={data['status_code']}")


            retail = int(data['prediction']['retailPrice'])
            io = int(data['prediction']['galleryPriceDown'])

            # Cache price
            self.cache_price(vehicle_str_ids, vehicle_str_labels, int(car['km']), retail, io)

            return self.return_valid_quotation(retail, io, matching_labels_ids[5][1], 'OK (request)')

        except Exception as e:
            time.sleep(_WAITING_TIME_AFTER_ERROR)
            return self.return_error_quotation(str(e))


    def return_error_quotation(self, comments_msg):
        logging.warning(f"Error when getting quotation: {comments_msg}")
        return pd.Series({'smartiq_retail': 0
                                , 'smartiq_io': 0
                                , 'smartiq_matching_trimlevel': None
                                , 'smartiq_comments': f"QUOTATION_EXCEPTION: {comments_msg}"})

    def return_valid_quotation(self, retail, io, trim, comment):
        return pd.Series({'smartiq_retail': int(retail)
                                 , 'smartiq_io': int(io)
                                 , 'smartiq_matching_trimlevel': trim
                                 , 'smartiq_comments': comment})


    def get_cached_price(self, vehicle_str, km):
        """
        If price is cached return it (retail, io), if not return (None, None)
        TODO: Remove io from here and move to Camunda
        """
        self.redis_conn.select(1) # db=1 for price cache

        l, x1, x2, c0, c1, st = self.redis_conn.hmget('siq-price:' + vehicle_str, ['labels', 'x1', 'x2', 'c0', 'c1', 'strategy'])
        y1, y2 = self.redis_conn.hmget('siq-price:' + vehicle_str, ['y1', 'y2']) 

        logging.info(f"a={(x1, y1)}, b={x2, y2}, c0={c0}, c1={c1} st={st}")

        if all([x1, x2, c0, c1, st]) and int(x1) <= km <= int(x2):
            retail = int(c0) + float(c1) * int(km)
            logging.debug(f"price from cache with regression")
        elif all([x1, st]) and (abs(float(x1) - km) <= _KMS_CLOSE):
            logging.debug(f"price from cache with single value")
            retail = int(y1)
        else:
            return None,None

        io = retail / (1 + int(st)/100)
        return retail, io


    def cache_price(self, vehicle_str, labels, km, retail, io):
        """ Store price in the cache"""
        self.redis_conn.select(1)

        l, x1, x2, y1, y2 = self.redis_conn.hmget('siq-price:' + vehicle_str, ['labels', 'x1', 'x2', 'y1', 'y2'])

        if not x1: # First point
            d = {'labels': labels, 'x1': km, 'y1': retail, 'strategy': round(((retail/io) - 1) * 100)}
            self.redis_conn.hmset('siq-price:' + vehicle_str, d)
            return

        x1, y1 = int(x1), int(y1)
        if abs(x1 - km) < _KMS_CLOSE: # to close, ignore
            return
        
        if not x2: # Second point
            x1_ = x1 if x1 < km else km
            y1_ = y1 if x1 < km else retail
            x2_ = km if x1 < km else x1
            y2_ = retail if x1 < km else y1
        else: # Third point (reinforce to extend the range)
            x2, y2 = int(x2), int(y2)

            if x1 <= km <= x2:
                logging.warning(f"should not be caching this: km={km}, cached points={(x1, x2)}. returning")
                return

            x1_ = x1 if x1 < km else km
            y1_ = y1 if x1 < km else retail
            x2_ = x2 if x2 > km else km
            y2_ = y2 if x2 > km else retail

        c1 = (y1_ - y2_) / (x1_ - x2_)
        c0 = ((y1_ + y2_) - c1 * (x1_ + x2_)) / 2

        d = {'labels': labels, 'x1': x1_, 'x2': x2_, 'y1': y1_, 'y2': y2_
            , 'c0': round(c0), 'c1': round(c1, 4), 'strategy': round(((retail/io) - 1) * 100)}
        
        logging.info(f"caching price for {vehicle_str} as {d}") 
        self.redis_conn.hmset('siq-price:' + vehicle_str, d)

        return



