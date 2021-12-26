"""
This module contains static values classes.
ErroMessages , Statuses
"""


class ErroMessages:
    '''
    A class contain Error messages.
    '''

    DATES_ARE_PAST = "Error: Dates are past."
    START_IS_BIGGER_THAN_END = "Error: Start date is bigger than end date."
    ROOM_NOT_AVAILABLE = "Error :The room is not available."
    ROOM_NOT_EXISTING = "Error: The room is not exist."

    HOSE_DOSE_NOT_EXIST = "Error : The hose dose not exist."
    LISTING_OWNER_DOSE_NOT_EXIST = "Error : The listing owner dose not exist."

class SuccessMessage:
    SUCCESS_OPERATION = "The operations was successful."

class status:
    GET_RESERVED_ROOM_LIST_ALL = "ALL"
    GET_RESERVED_ROOM_LIST_FROM_NOW = "FROME_NOW"
