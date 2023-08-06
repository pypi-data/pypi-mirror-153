"""This module contains functions that preform common tasks."""
import re

def as_gold(amount: int) -> str:
    """Formats a integer as n*g nns nnc where n is some number, g = gold, s = silver, and c = copper.
    
    Args:
        amount (int): The value of something in WoW's currency.

    Returns:
        A string formatted to WoW's gold, silver, copper currency.
    """
    if amount >= 0:
        return (f"{int(str(amount)[:-4]):,}g {str(amount)[-4:-2]}s {str(amount)[-2:]}c")
    else:
        return (f"{int(str(amount)[:-4]):,}g {str(amount)[-4:-2]}s {str(amount)[-2:]}c")

def get_id_from_url(url: str) -> int:
    """Returns the id from a url.

        This matches to the first number in a string. As of writing the only number
        in blizzard's urls is an id.

    Args:
        url (str): The url that contains a single number id.

    Returns:
        The number found in the url.
    """
    pattern = re.compile(r'[\d]+')
    return pattern.search(url).group()
