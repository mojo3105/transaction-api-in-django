"""
The script contains util functions to validate api request body.
"""

#imports
import cerberus
from stocks.constants.common import APIConstants, ValidationSchemas
from stocks.models import AppUser, Stocks
from stocks.utils import generate_traceback


def validate_amount_transaction_api(request_data):
    """
    The function will validate amount api request and return specific values from request data with error msg if any.
    :param request_data: dictionary containing amount transactions api request data
    :return trans_type: value of transaction type e.g. debited/credited
    :return amount: amount of transaction
    :return user: user object
    :return msg: error message if any
    """
    try:
        v = cerberus.Validator()
        schema = ValidationSchemas.AMOUNT_TRANSACTION_SCHEMA
        v.validate(request_data, schema)
        if not v.validate(request_data, schema):
            msg = v.errors
            return None, None, None, msg
        
        msg = None
        trans_type = request_data['transaction_type']
        amount = request_data['amount']
        user_id = request_data['user_id']
        
        if trans_type not in APIConstants.AMOUNT_TRANSACTIONS_VALUES:
            msg = APIConstants.TRANSACTION_VALUE_ERROR_MESSAGE.format(trans_values = 'debited/credited')
            return None, None, None, msg
    
        user = AppUser.objects.get(id=user_id)
        return trans_type.lower(), amount, user, msg
    
    except AppUser.DoesNotExist:
        msg = APIConstants.USER_NOT_EXIST_MESSAGE
        return None, None, None, msg

    except Exception as e:
        msg = APIConstants.COMMON_ERROR_MESSAGE.format(e=e)
        generate_traceback.generate_traceback()
        return None, None, None, msg


def validate_stocks_transactions_api(request_data):
    """
    The function will validate stocks api request and return specific values from request data with error msg if any.
    :param request_data: dictionary containing stocks transactions api request data
    :return trans_type: value of transaction type e.g. buy/sell
    :return quantity: quantity of stocks for transaction
    :return stocks: stocks object
    :return user: user object
    :return msg: error message if any
    """
    try:
        v = cerberus.Validator()
        schema = ValidationSchemas.STOCK_TRANSACTION_SCHEMA
        if not v.validate(request_data, schema):
            msg = v.errors
            return None, None, None, None, msg
        
        msg = None
        trans_type = request_data['transaction_type']
        quantity = request_data['quantity']
        stock_symbol = request_data['stock_symbol']
        user_id = request_data['user_id']

        if trans_type not in APIConstants.STOCKS_TRANSACTIONS_VALUES:
            msg = APIConstants.TRANSACTION_VALUE_ERROR_MESSAGE.format(trans_values = 'buy/sell')
            return None, None, None, None, msg
        
        user = AppUser.objects.get(id=user_id)
        stock = Stocks.objects.get(stock_symbol=stock_symbol.upper())
        return trans_type.lower(), quantity, stock, user, msg
    
    except KeyError as e:
        msg = APIConstants.KEY_INCORRECT_MESSAGE.format(e=e)
        return None, None, None, None, msg
    
    except AppUser.DoesNotExist:
        msg = APIConstants.USER_NOT_EXIST_MESSAGE
        return None, None, None, None, msg
    
    except Stocks.DoesNotExist:
        msg = APIConstants.STOCKS_NOT_EXIST_MESSAGE
        return None, None, None, None, msg

    except Exception as e:
        msg = APIConstants.COMMON_ERROR_MESSAGE.format(e=e)
        generate_traceback.generate_traceback()
        return None, None, None, None, msg


def validate_app_user_api(request_data, id=None):
    """
    The function will validate api request data for app_user api endpoint.
    :param request_data: dictionary with request data
    :param id: user id if any
    :return email: user email 
    :return balance: user account balance
    :return user: user object if id provided
    :return msg: error message if any
    """
    try:
        v = cerberus.Validator()
        schema = ValidationSchemas.USER_VALIDATION_SCHEMA
        if not v.validate(request_data, schema):
            msg = v.errors
            return None, None, None, msg
        
        msg = None
        email = request_data['email']
        balance = request_data['balance']
        user = None
        if id:
            user = AppUser.objects.get(id=id)
        
        return email, balance, user, msg

    except KeyError as e:
        msg = APIConstants.KEY_INCORRECT_MESSAGE.format(e=e)
        return None, None, None, msg
    
    except AppUser.DoesNotExist:
        msg = APIConstants.USER_NOT_EXIST_MESSAGE
        return None, None, None, msg
    
    except Exception as e:
        msg = APIConstants.COMMON_ERROR_MESSAGE.format(e=e)
        generate_traceback.generate_traceback()
        return None, None, None, msg


def validate_stocks_api(request_data, id=None):
    """
    The function will validate api request data for stocks api endpoint.
    :param request_data: dictionary with request data
    :param id: user id if any
    :return company_name: name of company for stock
    :return stock_symbol: unique string to identify stock
    :return current_price: current price of stock
    :return stock: stock object if id provided
    :return msg: error message if any
    """
    try:
        v = cerberus.Validator()
        schema = ValidationSchemas.STOCK_VALIDATION_SCHEMA
        if not v.validate(request_data, schema):
            msg = v.errors
            return None, None, None, None, msg
        
        msg = None
        company_name = request_data['company_name']
        stock_symbol = request_data['stock_symbol']
        current_price = request_data['current_price']
        stock = None
        if id:
            stock = Stocks.objects.get(id=id)
        
        return company_name, stock_symbol, current_price, stock, msg

    except KeyError as e:
        msg = APIConstants.KEY_INCORRECT_MESSAGE.format(e=e)
        return None, None, None, None, msg
    
    except Stocks.DoesNotExist:
        msg = APIConstants.STOCKS_NOT_EXIST_MESSAGE
        return None, None, None, None, msg
    
    except Exception as e:
        msg = APIConstants.COMMON_ERROR_MESSAGE.format(e=e)
        generate_traceback.generate_traceback()
        return None, None, None, None, msg