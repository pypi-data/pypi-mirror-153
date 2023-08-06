import json
import uuid
from typing import List

import requests


class InvalidFarmQuestAnswer(Exception):
    """Raised when the FarmQuest API does not return a valid answerCode"""

    def __init__(self, message):
        super().__init__(message)


class FarmQuestAPI:
    def __init__(self, username: str, password: str, customer_id: int):
        self.headers = {
            "username": username,
            "password": password,
            "Content-Type": "application/json",
        }
        self.customer_id = customer_id

        # API base url. The way the API is built, this isn't supposed to change between requests
        self.url = "https://www.farmquest.com/FarmQuestWebServiceRestful/GetInfos"

    def _make_request(self, id: str, body: dict):
        """Private function to call the FarmQuest API and return the response

        Args:
            id (str): Id of the request
            body (dict): Body of the request

        Returns:
            list of dict: The formatted API response

        """

        response = requests.post(self.url, headers=self.headers, data=body)
        if response.status_code == 200:
            raw_response = response.json()
            if raw_response["answerCode"] == 0:

                # Parse the content in the result key because it is returned as a string by the API
                dict_response = json.loads(raw_response["result"])

                return dict_response["listResultInfo"][id]["listInfo"]
            else:
                raise InvalidFarmQuestAnswer(
                    f"FarmQuest answerCode is invalid. Got {raw_response['answerCode']} insteaf of 0."
                )

    def _generate_uuid(self):
        """Private function to generate a UUID

        Args:
            None

        Returns:
            str: Randomly generated UUID

        """
        return str(uuid.uuid4())

    def get_batches(self):
        """List all batches for the current customer

        Args:
            None

        Returns:
            list of dict: A list of batch objects

        """
        request_id = self._generate_uuid()
        request_body = json.dumps(
            {
                "className": "RequestGetInfos",
                "listKey": {
                    request_id: {
                        "className": "BatchKey",
                        "filters": {
                            "listFilter": [
                                {"className": "FilterDate", "type": "ALL_IN_RANGE"}
                            ]
                        },
                    }
                },
            }
        )

        return self._make_request(request_id, request_body)

    def get_sites(self):
        """List all sites for the current customer

        Args:
            None

        Returns:
            list of dict: A list of sites objects

        """
        request_id = self._generate_uuid()
        request_body = json.dumps(
            {
                "className": "RequestGetInfos",
                "listKey": {request_id: {"className": "SiteKey"}},
            }
        )
        return self._make_request(request_id, request_body)

    def get_buildings(self):
        """List all buildings for the current customer

        Args:
            None

        Returns:
            list of dict: A list of sites objects

        """
        request_id = self._generate_uuid()
        request_body = json.dumps(
            {
                "className": "RequestGetInfos",
                "listKey": {request_id: {"className": "BuildingKey"}},
            }
        )
        return self._make_request(request_id, request_body)

    def get_site_buildings(self, site_id: int):
        """List all buildings for the specified site for the current customer

        Args:
            site_id (int): Id of the site

        Returns:
            list of dict: A list of building     objects

        """
        request_id = self._generate_uuid()
        request_body = json.dumps(
            {
                "className": "RequestGetInfos",
                "listKey": {
                    request_id: {"className": "BuildingKey", "siteId": site_id}
                },
            }
        )
        return self._make_request(request_id, request_body)

    def get_feed_bins_weight_for_all_batches(
        self,
        site_id: int,
        building_id: int,
        bins_id: List[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        time_filter: str = "LAST",
    ):
        """Get the weight of each feed bins in a building grouped by batch

        Args:
            site_id (int): The site id
            building_id (int): The building id within the site
            bins_id (Optinal, list of int): List of bins id. Defaults to a list of 1 through 10.
            time_filter (Optional, str): Time filter code to use. Valid values are NOT_EQUAL, EQUAL,GREATER, GREATER_EQUAL, LOWER, LOWER_EQUAL, ALL, ALL_IN_RANGE, LAST, BEFORE_LAST, LAST_IN_RANGE, BEFORE_LAST_IN_RANGE, ACTUAL, SIZE, OFFSET, LAST_COMPLETED, BEFORE_LAST_COMPLETED

        Returns:
            list of dict: A list of weight objects

        """
        request_id = self._generate_uuid()
        request_body = json.dumps(
            {
                "className": "RequestGetInfos",
                "listKey": {
                    request_id: {
                        "className": "ReportDataKey",
                        "parentKey": {
                            "dataSourceType": "BATCH",
                            "parentKey": {
                                "customerId": self.customer_id,
                                "siteId": site_id,
                                "buildingId": building_id,
                            },
                        },
                        "controlIndex": 0,
                        "filters": {
                            "listFilter": [
                                {
                                    "className": "FilterFieldsValues",
                                    "mainFilterFieldsValue": {
                                        "listFilterFieldValue": [
                                            {
                                                "fieldName": "dayIndex",
                                                "filterValueType": time_filter,
                                            }
                                        ]
                                    },
                                    "listFilterFieldsValue": [
                                        {
                                            "listFilterFieldValue": [
                                                {
                                                    "fieldName": "typeValueId",
                                                    "value": 614,
                                                },
                                                {
                                                    "fieldName": "numIndex",
                                                    "listValue": bins_id,
                                                },
                                            ]
                                        }
                                    ],
                                }
                            ]
                        },
                    }
                },
            }
        )

        return self._make_request(request_id, request_body)

    def get_feed_bins_weight_for_specific_batch(
        self,
        site_id: int,
        building_id: int,
        batch_id: int,
        bins_id: List[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        time_filter: str = "LAST",
    ):
        """Get the weight of each feed bins in a building for a specific batch

        Args:
            site_id (int): The site id
            building_id (int): The building id within the site
            batch_id (int): The batch id
            bins_id (Optinal, list of int): List of bins id. Defaults to a list of 1 through 10.
            time_filter (Optional, str): Time filter code to use. Valid values are NOT_EQUAL, EQUAL,GREATER, GREATER_EQUAL, LOWER, LOWER_EQUAL, ALL, ALL_IN_RANGE, LAST, BEFORE_LAST, LAST_IN_RANGE, BEFORE_LAST_IN_RANGE, ACTUAL, SIZE, OFFSET, LAST_COMPLETED, BEFORE_LAST_COMPLETED

        Returns:
            list of dict: A list of weight objects

        """
        request_id = self._generate_uuid()
        request_body = json.dumps(
            {
                "className": "RequestGetInfos",
                "listKey": {
                    request_id: {
                        "className": "ReportDataKey",
                        "parentKey": {
                            "dataSourceType": "BATCH",
                            "parentKey": {
                                "customerId": self.customer_id,
                                "siteId": site_id,
                                "buildingId": building_id,
                                "batchId": batch_id,
                            },
                        },
                        "controlIndex": 0,
                        "filters": {
                            "listFilter": [
                                {
                                    "className": "FilterFieldsValues",
                                    "mainFilterFieldsValue": {
                                        "listFilterFieldValue": [
                                            {
                                                "fieldName": "dayIndex",
                                                "filterValueType": time_filter,
                                            }
                                        ]
                                    },
                                    "listFilterFieldsValue": [
                                        {
                                            "listFilterFieldValue": [
                                                {
                                                    "fieldName": "typeValueId",
                                                    "value": 614,
                                                },
                                                {
                                                    "fieldName": "numIndex",
                                                    "listValue": bins_id,
                                                },
                                            ]
                                        }
                                    ],
                                }
                            ]
                        },
                    }
                },
            }
        )

        return self._make_request(request_id, request_body)

    def get_feed_bins_weight_section_batch(
        self,
        site_id: int,
        building_id: int,
        batch_id: int,
        section_id: int,
        bins_id: List[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        time_filter: str = "LAST_IN_RANGE",
    ):
        """Get the weight of each feed bins in a building section for a specific batch

        Args:
            site_id (int): The site id
            building_id (int): The building id within the site
            batch_id (int): The batch id
            section_id (int): The section id
            bins_id (Optinal, list of int): List of bins id. Defaults to a list of 1 through 10.
            time_filter (Optional, str): Time filter code to use. Valid values are NOT_EQUAL, EQUAL,GREATER, GREATER_EQUAL, LOWER, LOWER_EQUAL, ALL, ALL_IN_RANGE, LAST, BEFORE_LAST, LAST_IN_RANGE, BEFORE_LAST_IN_RANGE, ACTUAL, SIZE, OFFSET, LAST_COMPLETED, BEFORE_LAST_COMPLETED

        Returns:
            list of dict: A list of weight objects

        """
        request_id = self._generate_uuid()
        request_body = json.dumps(
            {
                "className": "RequestGetInfos",
                "listKey": {
                    request_id: {
                        "className": "ReportDataKey",
                        "parentKey": {
                            "dataSourceType": "BATCH",
                            "parentKey": {
                                "customerId": self.customer_id,
                                "siteId": site_id,
                                "buildingId": building_id,
                                "sectionId": section_id,
                                "batchId": batch_id,
                            },
                        },
                        "filters": {
                            "listFilter": [
                                {
                                    "className": "FilterFieldsValues",
                                    "mainFilterFieldsValue": {
                                        "listFilterFieldValue": [
                                            {
                                                "fieldName": "dayIndex",
                                                "filterValueType": time_filter,
                                            }
                                        ]
                                    },
                                    "listFilterFieldsValue": [
                                        {
                                            "listFilterFieldValue": [
                                                {
                                                    "fieldName": "typeValueId",
                                                    "listValue": [687],
                                                },
                                                {
                                                    "fieldName": "numIndex",
                                                    "listValue": bins_id,
                                                },
                                            ]
                                        },
                                    ],
                                }
                            ]
                        },
                    }
                },
            }
        )

        return self._make_request(request_id, request_body)