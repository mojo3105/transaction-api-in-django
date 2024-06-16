"""
The script contains utility function to get data from all the tables.
"""

#imports
from stocks.models import AppUser, Stocks, UserTransactions, UserHoldings
from stocks.serializers import AppUserSerializers, StocksSerializers,  UserTransactionsSerializers, \
                            UserHoldingsSerializers
from stocks.constants.common import APIConstants
from stocks.utils import generate_traceback


def get_table_data(model, id=None):
    """
    The script will get the data from models.
    :param model: django model(class)
    :param id: id of object
    :return data: data to return in response
    :return msg: error msg if any
    """
    try:
        msg = None
        if id:
            model_object = model.objects.get(id=id)
            model_object = eval(f"{model.__name__}Serializers")(model_object)
        else:
            model_object = model.objects.all()
            model_object = eval(f"{model.__name__}Serializers")(model_object, many=True)
        data = model_object.data
        return data, msg
    except model.DoesNotExist:
        msg = APIConstants.COMMON_DOES_NOT_EXIST_MESSAGE.format(object=model.__name__)
        return None, msg
    except Exception as e:
        generate_traceback.generate_traceback()
        msg = APIConstants.COMMON_ERROR_MESSAGE.format(e=e)
        return None, msg
