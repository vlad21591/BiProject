# -*- coding: utf-8 -*-
"""BiProject-STTM.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1HEQheGhM3VuwEjCHtdEmmWXozseWzeIf
"""

!pip install jsonpath_ng

"""### Imports"""

# Commented out IPython magic to ensure Python compatibility.
import os
import json
import numpy as np 
import pandas as pd 
import sqlite3
import functools as ft
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod
from jsonpath_ng import parse
from enum import Enum
# %matplotlib inline

with open("SMWB SET.json", "r") as file:
  data = json.load(file)
  for item in data:
    item["Account"] = item["Account"]
    item["ARR"] = int(item["ARR"])
    item["Stage"] = item["Stage"]
    item["Is_Win"] = int(item["Is_Win"])
    item["Employees size"] = int(item["Employees size"])
    item["Country"] = item["Country"]
    item["Created Date"] = datetime(item["Created Date"])
    item["Closed Date"] = datetime(item["Closed Date"])
    item["Month"] = int(item["Month"])
    item["Quarter"] = item["Quarter"]
    item["Closed lost reason"] = item["Closed lost reason"]
    item["Closed Won reason"] = item["Closed Won reason"]

class Interface(ABC):

    @abstractmethod
    def get_data_by_field(self, field_name):
        """Fetch the data by given feild name """

    @abstractmethod
    def get_data_by_id(self, id):
        """Fetch the data by given ID  """

    @abstractmethod
    def get(self):
        """Fetch all data """

class TransformMask(Enum):
    # add here any masks you want 
    CLEAN_STRING = ".strip().lower()" 
    CAPITAL_LETTER = ".strip().lower().title()"

"""### Database class"""

K_list = ["Account", "ARR", "Stage", "Is_Win", "Employees size", "Country", "Created Date", "Closed Date", "Month", "Quarter", "Closed lost reason", "Closed Won reason"]

class Database:
    def __init__(self):
        self.db = {
            "source": [],
            "destination": [],
            "mapping": []
        }

        self.add_source(1, "jobTitle", "$.jobTitle", "str", True)


    def add_source(self):
      for i in range (1, len(K_list)+1):
        self.db["source"].append({
                    "id": i,
                    "source_field_name": K_list[i-1],
                    "source_field_mapping": K_list[i-1],
                    "source_field_type": "str",
                    "is_required": True,
                     })
      
    def add_destination(self):
      for i in range (1, len(K_list)+1):
       self.db["destination"].append({
                    "id": i,
                    "destination_field_name": K_list[i-1],
                    "destination_field_mapping": K_list[i-1],
                    "destination_field_type": "str",
                    "default_value": "n/a",
                     })
      
    def add_transform(self):
       self.db["transform"] = [
          {
          "id":1
          "transform_mask": 'CAPITAL_LETTER'

          },
          {
          "id":2
          "transform_mask": 'CLEAN_STRING'
          }
       ]
     
     
    def add_mapping(self):
      for i in range (1, len(K_list)+1):
        self.db["mapping"].append({
                    "id": i,
                    "mapping_source": i,
                    "mapping_destination": i,
                    "mapping_transform": i
                     })
        
    def data_source_target_mapping(self):
      self.add_source()
      self.add_destination()
      self.add_transform()
      self.add_mapping()
      
    @property
    def get_data_source_target_mapping(self):
        self.data_source_target_mapping()
        return self.db

"""### Source class"""

class Source(Interface, Database):
    def __init__(self):
        Database.__init__(self)

    # should be implemented - inherited from Interface
    def get_data_by_field(self, field_name):
        data = self.get
        for item in data:
            for key, value in item.items():
                if key == field_name:
                    return item
        return None

    @property
    def get(self):
        return self.get_data_source_target_mapping.get("source")

    def get_data_by_id(self, id):
        self.id = id
        data = self.get
        for x in data:
            if x.get("id") == self.id:
                return x
        return None

"""### Target class"""

class Target(Interface, Database):

    def __init__(self):
        Database.__init__(self)

    # should be implemented - inherited from Interface
    def get_data_by_field(self, field_name):
        data = self.get
        for item in data:
            for key, value in item.items():
                if key == field_name:
                    return item
        return None

    @property
    def get(self):
        return self.get_data_source_target_mapping.get("destination")

    def get_data_by_id(self, id):
        self.id = id
        data = self.get
        for x in data:
            if x.get("id").__str__() == self.id.__str__():
                return x
        return None

"""### Transform class"""

class Transform(Interface, Database):

    def __init__(self):
        Database.__init__(self)

    # should be implemented - inherited from Interface
    def get_data_by_field(self, field_name):
        data = self.get
        for item in data:
            for key, value in item.items():
                if key == field_name:
                    return item
        return None

    @property
    def get(self):
        return self.get_data_source_target_mapping.get("transform", [])

    def get_data_by_id(self, id):
        self.id = id
        data = self.get
        for x in data:
            if x.get("id").__str__() == self.id.__str__():
                return x
        return None

"""### Mapping class"""

class Mappings(Interface, Database):

    def __init__(self):
        Database.__init__(self)

    def get_data_by_field(self, field_name):
        data = self. get
        for item in data:
          for key, value in item.items():
            if key == field_name:
              return item
        return None

    @property
    def get(self):
        return self.get_data_source_target_mapping.get("mapping")

    def get_data_by_id(self, id):
        self.id = id
        data = self.get
        for x in data:
            if x.get("id").__str__() == self.id.__str__():
                return x
        return None

"""### Format Class - JSON"""

class JsonQuery:
    def __init__(self, json_path, json_data):
        self.json_path = json_path
        self.json_data = json_data

    def get(self):
        jsonpath_expression = parse(self.json_path)
        match = jsonpath_expression.find(self.json_data)
        source_data_value = match[0].value
        return source_data_value

"""# STTM"""

class STTM:
    def __init__(self, input_json):
        self.input_json = input_json
        self.mapping_instance = Mappings()
        self.source_instance = Source()
        self.destination_instance = Target()
        self.transform_instance = Transform()
        self.look_up_mask = {i.name: i.value for i in TransformMask}
        self.json_data_transformed = {}

    def _get_mapping_data(self):
        return self.mapping_instance.get

    def _get_mapping_source_data(self):
        return self.source_instance.get

    def get_transformed_data(self):

        for mappings in self._get_mapping_data():

            """fetch the source mapping """
            mapping_source_id = mappings.get("mapping_source")
            mapping_destination_id = mappings.get("mapping_destination")
            mapping_transform_id = mappings.get("mapping_transform")

            mapping_source_data = self.source_instance.get_data_by_id(id=mapping_source_id)
            transform_data = self.transform_instance.get_data_by_id(id=mapping_transform_id)

            """Fetch Source  field Name"""
            source_field_name = mapping_source_data.get("source_field_name")

            """if field given is not present incoming json """
            if source_field_name not in self.input_json.keys():
                if mapping_source_data.get("is_required"):
                    raise Exception(
                        "Alert ! Field {} is not present in JSON please FIX mappings ".format(source_field_name))
                else:
                    pass

            else:
                source_data_value = JsonQuery(
                    json_path=mapping_source_data.get("source_field_mapping"),
                    json_data=self.input_json
                ).get()

                """check the data type for source if matches with what we have """
                if mapping_source_data.get("source_field_type") != type(source_data_value).__name__:
                    if source_data_value is not None:
                        _message = (
                            "Alert ! Source Field :{} Datatype has changed from {} to {} ".format(source_field_name,
                                                                                                  mapping_source_data.get(
                                                                                                      "source_field_type"),
                                                                                                  type(
                                                                                                      source_data_value).__name__))
                        print(_message)
                        raise Exception(_message)

                """Query and fetch the Destination | target """
                destination_mappings_json_object = self.destination_instance.get_data_by_id(
                    id=mappings.get("mapping_destination"))

                destination_field_name = destination_mappings_json_object.get("destination_field_name")
                destination_field_type = destination_mappings_json_object.get("destination_field_type")

                dtypes = [str, float, list, int, set, dict]

                for dtype in dtypes:

                    """Datatype Conversion """
                    if destination_field_type == str(dtype.__name__):

                        """is source is none insert default value"""
                        if source_data_value is None:
                            self.json_data_transformed[destination_field_name] = dtype.__call__(
                                destination_mappings_json_object.get("default_value")
                            )

                        else:
                            """check if you have items to transform"""
                            if transform_data is not None:
                                """ check for invalid mask name """
                                if transform_data.get("transform_mask") not in list(self.look_up_mask.keys()):
                                    raise Exception(
                                        f"Specified Transform {transform_data.get('transform_mask')} is not available please select from following Options :{list(self.look_up_mask.keys())}")
                                else:
                                    mask_apply = self.look_up_mask.get(transform_data.get("transform_mask"))
                                    converted_dtype = dtype.__call__(source_data_value)
                                    mask = f'converted_dtype{mask_apply}'
                                    curated_value = eval(mask)
                                    self.json_data_transformed[destination_field_name] = curated_value

                            else:
                                self.json_data_transformed[destination_field_name] = dtype.__call__(source_data_value)

        return self.json_data_transformed

transformed_data = []
for item in data:
    helper = STTM(input_json=item)
    response = helper.get_transformed_data()
    transformed_data.append(response)
    print(response)

pd.DataFrame(transformed_data)