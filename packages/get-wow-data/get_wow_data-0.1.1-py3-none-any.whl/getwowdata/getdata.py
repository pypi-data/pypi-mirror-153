"""This module contains functions to query Blizzards World of Warcraft APIs.

Typical usage example:

from getwowdata import WowApi
from dotenv import load_dotenv

load_dotenv()

us_api = WowApi('us', 'en_US')
winterhoof_auctions = us_api.get_auctions(4)

Copyright (c) 2022 JackBorah
MIT License see LICENSE for more details
"""

import os
import requests
from getwowdata import exceptions
from getwowdata.urls import urls
from getwowdata.helpers import get_id_from_url

class WowApi:
    """Creates an object with access_key, region, and, optionally, locale attributes.

    Attributes:
        region (str): Ex: 'us'. The region where the data will come from.
            See https://develop.battle.net/documentation/guides/regionality-and-apis
        locale (str, optional): Ex: 'en_US'. The language data will be returned in.
            See https://develop.battle.net/documentation/world-of-warcraft/guides/localization.
            Default = None.
        wow_api_id (str, optional): Required to recieve an access token to
            query Blizzard APIs. Can be loaded from
            environment variables. See Setup in readme or
            visit https://develop.battle.net/ and click get started now.
            Default = None.
        wow_api_secret (str, optional): Required to recieve an access token to
            query Blizzard APIs. Can be loaded from
            environment variables. See Setup in readme or
            visit https://develop.battle.net/ and click get started now.
            Default = None.
    """

    def __init__(
        self,
        region: str,
        locale: str = None,
        wow_api_id: str = None,
        wow_api_secret: str = None,
    ):
        """Sets the access_token and region attributes.

        Args:
            region (str): Example: 'us'. Should be lowercase. Access tokens will
                work for all other regions except 'cn' (China).
            locale (str): Example: 'en_US'. The language that data will be returned in.
                Default = None which returns the data in all supported languages.
                See https://develop.battle.net/documentation/world-of-warcraft/guides/localization.
            wow_api_id (str, optional): Your client id from https://develop.battle.net/.
                Ignore if id is set as environment variable.
            wow_api_secret (str, optional): Your client secret from https://develop.battle.net/.
                Ignore if secret is set as environment variable.
        """
        self.region = region
        self.locale = locale
        self.wow_api_id = wow_api_id
        self.wow_api_secret = wow_api_secret
        self.access_token = self._get_access_token()

    def _get_access_token(
        self,
        timeout: int = 30,
    ) -> str:
        """Returns an access token.

        Requires wow_api_id and wow_api_secret to be set as environment variables or
        passed in. Remember not to expose your secret publicly. Each token expires
        after a day. Subsequent get_access_token calls returns the same token until
        it expires.

        Args:
            timeout (int): How long (in seconds) until the request to the API timesout
                Default = 30 seconds.

        Returns:
            The access token as a string.

        Raises:
            NameError: If wow_api_id and/or wow_api_secret is not set as
                environment variable or passed in.
            requests.exceptions.HTTPError: If status code 4XX or 5XX.
            exceptions.JSONChangedError: If 'access_token' was not found in
                access_token_response.json()['access_token'].
        """

        token_data = {"grant_type": "client_credentials"}

        try:
            auth = (os.environ["wow_api_id"], os.environ["wow_api_secret"])
            access_token_response = requests.post(
                urls["access_token"].format(region=self.region),
                data=token_data,
                auth=auth,
                timeout=timeout,
            )
            access_token_response.raise_for_status()
            try:
                return access_token_response.json()["access_token"]
            except KeyError:
                raise exceptions.JSONChangedError(
                    "access_token not found in access_token_response."
                    "The Api's repsonse format may have changed."
                ) from KeyError

        #if os.environ is not found
        except KeyError:
            if self.wow_api_id is None or self.wow_api_secret is None:
                raise NameError(
                    "No wow_api_id or wow_api_secret was found. "
                    "Set them as environment variables or "
                    "pass into get_access_token."
                ) from NameError

            auth = (self.wow_api_id, self.wow_api_secret)
            access_token_response = requests.post(
                urls["access_token"].format(region=self.region),
                data=token_data,
                auth=auth,
                timeout=timeout,
            )
            access_token_response.raise_for_status()
            try:
                return access_token_response.json()["access_token"]
            except KeyError:
                raise exceptions.JSONChangedError(
                    "access_token not found in access_token_response."
                    "The Api's repsonse format may have changed."
                ) from KeyError

    def connected_realm_search(self, **extra_params: dict) -> dict:
        """Uses the connected realms API's search functionaly for more specific queries.

        Searches can filter by fields returned from the API.
        Ex: filerting realms by slug == illidan.
        Below is the data returned from a regular realm query.

        {
            "page": 1,
            "pageSize": 58,
            "maxPageSize": 100,
            "pageCount": 1,
            "results": [
            {
                ...
            },
            "data": {
                "realms": {
                    ...
                    "slug":"illidan"
                }
        To only return the realm with the slug == illidan pass
        {'data.realms.slug':'illidan'} into **extra_params.
        See https://develop.battle.net/documentation/world-of-warcraft/guides/search
        for more details on search.

        Args:
            **extra_params (int/str, optional): Returned data can be filtered
                by any of its fields. Useful parameters are listed below.
                Parameters must be sent as a dictionary where keys are str and
                values are str or int like {'_page': 1, 'realms.slug':'illidan', ...}
            **timeout (int, optional): How long (in seconds) until the request to the API timesout
                Default = 30 seconds. Ex: {'timeout': 10}
            **_pageSize (int, optional): Number of entries in a result page.
                Default = 100, min = 1, max = 1000. Ex: {"_pageSize": 2}
            **_page (int, optional): The page number that will be returned.
                Default = 1. Ex: {"_page": 1}
            **orderby (str, optional): Accepts a comma seperated field of elements to sort by.
                See https://develop.battle.net/documentation/world-of-warcraft/guides/search.
                Ex: {"orderby":"data.required_level"}
            **data.realms.slug (str, optional): All realm slugs must be lowercase with spaces
                converted to dashes (-)

        Returns:
        A json looking dict with nested dicts and/or lists containing data from the API.
        """
        try:
            timeout = extra_params.pop("timeout", 30)
        except KeyError:
            timeout = 30

        conn_realm_search_params = {
            **{
                "namespace": f"dynamic-{self.region}",
                "access_token": self.access_token,
                "locale": self.locale,
            },
            **extra_params,
        }

        response = requests.get(
            urls["search_realm"].format(region=self.region),
            params=conn_realm_search_params,
            timeout=timeout,
        )
        response.raise_for_status()
        return response.json()

    def item_search(self, **extra_params: dict) -> dict:
        """Uses the items API's search functionality to make more specific queries.

        Ex: Filter by required level and name. Below is the data returned from some
        item search.

        {
        "page": 1,
        "pageSize": 3,
        "maxPageSize": 100,
        "pageCount": 1,
        "results": [
            {
                ...
            },
            "data": {
                "level": 35,
                "required_level": 30,
            ...
                ...
                name.en_US: Garrosh
        To filter by name and level, pass {"required_level": 30, "name.en_US: "Garrosh"}
        into **extra_params. Additional parameters must be sent as a dictionary where
        the keys strings and values are strings or ints.

        Args:
            **extra_params (int/str, optional): Returned data can be filtered by any
                of its fields. Useful parameters are listed below.
                Ex: {'data.required_level':35} will only return items where required_level == 35
            **timeout (int, optional): How long (in seconds) until the request to the API timesout
                Default = 30 seconds. Ex: {'timeout': 10}
            **_pageSize (int, optional): Number of entries in a result page.
                Default = 100, min = 1, max = 1000. Ex: {"_pageSize": 2}
            **_page (int, optional): The page number that will be returned.
                Default = 1. Ex: {"_page": 1}
            **orderby (str, optional): Accepts a comma seperated field of elements to sort by.
                See https://develop.battle.net/documentation/world-of-warcraft/guides/search.
                Ex: {"orderby":"data.required_level"}
            **id (int, optional): An item's id. Enter in the following format
                {'id': '(id_start, id_end)'} to specify a set of id's.
                See https://develop.battle.net/documentation/world-of-warcraft/guides/search.

        Returns:
        A json looking dict with nested dicts and/or lists containing data from the API.
        """
        try:
            timeout = extra_params.pop("timeout", 30)
        except KeyError:
            timeout = 30

        search_params = {
            **{
                "namespace": f"static-{self.region}",
                "access_token": self.access_token,
            },
            **extra_params
        }

        search_response = requests.get(
            urls["search_item"].format(region=self.region),
            params=search_params,
            timeout=timeout,
        )
        return search_response.json()

    def get_connected_realms_by_id(
        self, connected_realm_id: int, timeout: int = 30
    ) -> dict:
        """Gets all the realms that share a connected_realm id.

        Args:
            connected_realm_id (int): The connected realm id. Get from connected_realm_index().
            timeout (int): How long (in seconds) until the request to the API timesout
                Default = 30 seconds.

        Returns:
            A json looking dict with nested dicts and/or lists containing data from the API.
        """
        realm_params = {
            "namespace": f"dynamic-{self.region}",
            "locale": self.locale,
            "access_token": self.access_token,
        }
        return requests.get(
            urls["realm"].format(
                region=self.region, connected_realm_id=connected_realm_id
            ),
            params=realm_params,
            timeout=timeout,
        ).json()

    def get_auctions(self, connected_realm_id, timeout=30) -> dict:
        """Gets all auctions from a realm by its connected_realm_id.

        Args:
            connected_realm_id (int): The connected realm id.
                Get from connected_realm_index() or use connected_realm_search().
            timeout (int): How long until the request to the API timesout in seconds.
                Default: 30 seconds.

        Returns:
            A json looking dict with nested dicts and/or lists containing data from the API.
        """
        auction_params = {
            "namespace": f"dynamic-{self.region}",
            "locale": self.locale,
            "access_token": self.access_token,
        }
        return requests.get(
            urls["auction"].format(
                region=self.region, connected_realm_id=connected_realm_id
            ),
            params=auction_params,
            timeout=timeout,
        ).json()

    def get_profession_index(self, timeout=30) -> dict:
        """Gets all professions including their names and ids.

        Args:
            timeout (int): How long until the request to the API timesout in seconds.
                Default: 30 seconds.


        Returns:
            A json looking dict with nested dicts and/or lists containing data from the API.
        """
        prof_params = {
            "namespace": f"static-{self.region}",
            "locale": self.locale,
            "access_token": self.access_token,
        }
        return requests.get(
            urls["profession_index"].format(region=self.region),
            params=prof_params,
            timeout=timeout,
        ).json()

    # Includes skill tiers (classic, burning crusade, shadowlands, ...) id
    def get_profession_tiers(self, profession_id, timeout=30) -> dict:
        """Returns all profession teirs from a profession.

        A profession teir includes all the recipes from that expansion.
        Teir examples are classic, tbc, shadowlands, ...

        Args:
            profession_id (int): The profession's id. Found in get_profession_index().
            timeout (int): How long until the request to the API timesout in seconds.
                Default: 30 seconds.

        Returns:
            A json looking dict with nested dicts and/or lists containing data from the API.
        """
        prof_tier_params = {
            "namespace": f"static-{self.region}",
            "locale": self.locale,
            "access_token": self.access_token,
        }
        return requests.get(
            urls["profession_skill_tier"].format(
                region=self.region, profession_id=profession_id
            ),
            params=prof_tier_params,
            timeout=timeout,
        ).json()

    def get_profession_icon(self, profession_id, timeout=30) -> bytes:
        """Returns a profession's icon in bytes.

        Args:
            profession_id (int): The profession's id. Found in get_profession_index().
            timeout (int): How long until the request to the API timesout in seconds.
                Default: 30 seconds.

        Returns:
            The profession's icon in bytes.
        """
        prof_icon_params = {
            "namespace": f"static-{self.region}",
            "locale": self.locale,
            "access_token": self.access_token,
        }
        icon_response = requests.get(
            urls["profession_icon"].format(
                region=self.region, profession_id=profession_id
            ),
            params=prof_icon_params,
            timeout=timeout,
        ).json()

        return requests.get(icon_response["assets"][0]["value"], timeout=timeout).content

    # Includes the categories (weapon mods, belts, ...) and the recipes (id, name) in them
    def get_profession_tier_recipes(
        self, profession_id, skill_tier_id, timeout=30
    ) -> dict:
        """Returns all crafts from a skill teir.

        Args:
            profession_id (int): The profession's id. Found in get_profession_index().
            skill_tier_id (int): The skill teir id. Found in get_profession_teirs().
            timeout (int): How long until the request to the API timesout in seconds.
                Default: 30 seconds.

        Returns:
            A json looking dict with nested dicts and/or lists containing data from the API.
        """
        prof_teir_recipe_params = {
            "namespace": f"static-{self.region}",
            "locale": self.locale,
            "access_token": self.access_token,
        }
        return requests.get(
            urls["profession_tier_detail"].format(
                region=self.region,
                profession_id=profession_id,
                skill_tier_id=skill_tier_id,
            ),
            params=prof_teir_recipe_params,
            timeout=timeout,
        ).json()

    def get_recipe(self, recipe_id, timeout=30) -> dict:
        """Returns a recipes details by its id.

        Args:
            recipe_id (int): The recipe's id. Found in get_profession_tier_details().
            timeout (int): How long until the request to the API timesout in seconds.
                Default: 30 seconds.

        Returns:
            A json looking dict with nested dicts and/or lists containing data from the API.
        """
        return requests.get(
            urls["recipe_detail"].format(region=self.region, recipe_id=recipe_id),
            params={
                "namespace": f"static-{self.region}",
                "locale": self.locale,
                "access_token": self.access_token,
            },
            timeout=timeout,
        ).json()

    def get_recipe_icon(self, recipe_id, timeout=30) -> bytes:
        """Returns a recipes icon in bytes.

        Args:
            recipe_id (int): The recipe's id. Found in get_profession_tier_details().
            timeout (int): How long until the request to the API timesout in seconds.
                Default: 30 seconds.

        Returns:
            The recipe icon in bytes.
        """
        icon_response = requests.get(
            urls["repice_icon"].format(region=self.region, recipe_id=recipe_id),
            params={
                "namespace": f"static-{self.region}",
                "locale": self.locale,
                "access_token": self.access_token,
            },
            timeout=timeout,
        ).json()

        return requests.get(icon_response["assets"][0]["value"], timeout=timeout).content


    def get_item_classes(self, timeout=30) -> dict:
        """Returns all item classes (consumable, container, weapon, ...).

        Args:
            access_token (str): Returned from get_access_token().
            timeout (int): How long until the request to the API timesout in seconds.
                Default: 30 seconds.

        Returns:
            A json looking dict with nested dicts and/or lists containing data from the API.
        """
        return requests.get(
            urls["item_classes"].format(region=self.region),
            params={
                "namespace": f"static-{self.region}",
                "locale": self.locale,
                "access_token": self.access_token,
            },
            timeout=timeout,
        ).json()

    # flasks, vantus runes, ...
    def get_item_subclasses(self, item_class_id, timeout=30) -> dict:
        """Returns all item subclasses (class: consumable, subclass: potion, elixir, ...).

        Args:
            item_class_id (int): Item class id. Found with get_item_classes().
            timeout (int): How long until the request to the API timesout in seconds.
                Default: 30 seconds.

        Returns:
            A json looking dict with nested dicts and/or lists containing data from the API.
        """
        return requests.get(
            urls["item_subclass"].format(
                region=self.region, item_class_id=item_class_id
            ),
            params={
                "namespace": f"static-{self.region}",
                "locale": self.locale,
                "access_token": self.access_token,
            },
            timeout=timeout,
        ).json()

    def get_item_set_index(self, timeout=30) -> dict:
        """Returns all item sets. Ex: teir sets

        Args:
            timeout (int): How long until the request to the API timesout in seconds.
                Default: 30 seconds.

        Returns:
            A json looking dict with nested dicts and/or lists containing data from the API.
        """
        return requests.get(
            urls["item_set_index"].format(region=self.region),
            params={
                "namespace": f"static-{self.region}",
                "locale": self.locale,
                "access_token": self.access_token,
            },
            timeout=timeout,
        ).json()

    def get_item_icon(self, item_id, timeout=30) -> bytes:
        """Returns the icon for an item in bytes.

        Args:
            item_id (int): The items id. Get from item_search().
            timeout (int): How long until the request to the API timesout in seconds.
                Default: 30 seconds.

        Returns:
            Item icon in bytes.
        """
        icon_response = requests.get(
            urls["item_icon"].format(region=self.region, item_id=item_id),
            params={
                "namespace": f"static-{self.region}",
                "locale": self.locale,
                "access_token": self.access_token,
            },
            timeout=timeout,
        ).json()
        return requests.get(icon_response["assets"][0]["value"], timeout=timeout).content

    def get_wow_token(self, timeout=30) -> dict:
        """Returns the price of the wow token and the timestamp of its last update.

        Args:
            timeout (int): How long until the request to the API timesout in seconds.
                Default: 30 seconds.

        Returns:
            A json looking dict with nested dicts and/or lists containing data from the API.
            The price is in the format g*sscc where g=gold, s=silver, and c=copper.
            Ex: 123456 = 12g 34s 56c
        """
        return requests.get(
            urls["wow_token"].format(region=self.region),
            params={
                "namespace": f"dynamic-{self.region}",
                "locale": self.locale,
                "access_token": self.access_token,
            },
            timeout=timeout,
        ).json()

    def get_connected_realm_index(self, timeout=30) -> dict:
        """Returns a dict where {key = Realm name: value = connected realm id, ...}

        Args:
            timeout (int): How long until the request to the API timesout in seconds.
                Default: 30 seconds.

        Returns:
            A dict like {realm_name: connected_realm_id}
        """

        index = {}

        response_index = self.connected_realm_search(timeout=timeout)
        realms_list = response_index["results"]
        for connected_realms in realms_list:
            connected_realm_id = get_id_from_url(connected_realms["key"]["href"])
            for realm in connected_realms["data"]["realms"]:
                index[realm["slug"]] = connected_realm_id

        return index
