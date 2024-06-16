"""
The script contains constant values.
"""


class APIConstants:
    """
    The class contains constants used in transaction api related operations.
    """
    
    DEFAULT_MESSAGE_NAME = "Error"
    AMOUNT_TRANSACTIONS_VALUES = ['debited', 'credited']
    STOCKS_TRANSACTIONS_VALUES = ['buy', 'sell']
    USER_NOT_EXIST_MESSAGE = "User does not exist!"
    STOCKS_NOT_EXIST_MESSAGE = "Stock does not exist!"
    HOLDING_NOT_EXIST_MESSAGE = "User holding does not exist!"
    TRANSACTION_NOT_EXIST_MESSAGE = "Transaction does not exist!"
    COMMON_ERROR_MESSAGE = "An error occured {e}!"
    KEY_INCORRECT_MESSAGE = "Please provide correct field {e}!"
    INSUFFICIENT_BALANCE_MESSAGE = "User don't have sufficient account balance to complete transaction!"
    HOLDING_NOT_PRESENT_MESSAGE = "User don't have this stocks, can't complete sell!"
    INSUFFICIENT_STOCKS_MESSAGE = "User don't have sufficient stocks to sell!"
    INVALID_TYPE_MESSAGE = "Provide correct non null {field_type} type field '{field_name}'!" 
    TRANSACTION_VALUE_ERROR_MESSAGE = "Please provide correct value for transaction type {trans_values}!"
    INCORRECT_INTEGER_VALUE = "{field_name} should always > 0!"
    EMAIL_PATTERN = r'@.*\..*com$'
    SUCCESSFULLY_ADDED_MESSAGE = "{object} added successfully!"
    SUCCESSFULLY_UPDATED_MESSAGE = "{object} updated successfully!"
    SUCCESSFULLY_DELETED_MESSAGE = "{object} deleted successfully!"
    FOREIGN_KEY_ERROR_MESSAGE = "Can't update field {key} because of Foreign-Key dependencies with other tables!"
    COMMON_DOES_NOT_EXIST_MESSAGE = "{object} does not exist!"
    ID_NOT_FOUND_MESSAGE = "{object} id does not found please provide correct id!"


class ValidationSchemas:
    AMOUNT_TRANSACTION_SCHEMA = {
        'transaction_type': {
            'type': 'string',
            'required': True
        },
        'amount': {
            'type': ['integer', 'float'],
            'min': 1,
            'required': True
        },
        'user_id': {
            'type': 'integer',
            'min': 1,
            'required': True
        }
    }
    STOCK_TRANSACTION_SCHEMA = {
            'transaction_type': {
                'type': 'string',
                'required': True
            },
            'quantity': {
                'type': 'integer',
                'min': 1,
                'required': True
            },
            'stock_symbol': {
                'type': 'string',
                'required': True
            },
            'user_id': {
                'type': 'integer',
                'min': 1,
                'required': True
            }
    }
    USER_VALIDATION_SCHEMA = {
        'email': {
            'type': 'string',
            'required': True
        },
        'balance': {
            'type': ['integer', 'float'],
            'min': 1,
            'required': True
        },
    }
    STOCK_VALIDATION_SCHEMA = {
        'company_name': {
            'type': 'string',
            'required': True
        },
        'stock_symbol': {
            'type': 'string',
            'required': True
        },
        'current_price': {
            'type': ['integer', 'float'],
            'min': 1,
            'required': True
        }
    }