"""
The script contains view functions for api endpoint.
"""

#imports
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db.models import Q
from django.db.utils import IntegrityError
import json
from stocks.models import *
from stocks.constants.common import APIConstants
from stocks.utils import validate_apis, generate_traceback, get_data


# Create your views here.
def index(request):
    """
    The basic view function to check app is working or not.
    :param request: Http request object
    :return HttpResponse: Http response object with appropriate status_code as per the condition
    """
    if request.method == 'GET':
        return HttpResponse("<h1>Hello world from stocks app</h1>", status=status.HTTP_200_OK)
    return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def account_transactions(request):
    """
    This view function handles post request at account-transaction endpoint where it adds amount transaction details 
    related to account in the respective tables in database.
    :param request: Http request object
    :return JsonResponse/HttpResponse: returns JsonResponse with message success/error if post request else 
                                        HttpResponse object with appropriate status code
    """
    if request.method == 'POST':
        request_data = json.loads(request.body)
        status_code = status.HTTP_400_BAD_REQUEST
        message_name = APIConstants.DEFAULT_MESSAGE_NAME
        try: 
            trans_type, amount, user, msg = validate_apis.validate_amount_transaction_api(request_data)
            if msg:
                message_value = msg
                status_code = status.HTTP_404_NOT_FOUND
            else:
                if (trans_type.lower() == 'debited') and ((float(user.current_balance) - float(amount)) < 0):
                    message_value = APIConstants.INSUFFICIENT_BALANCE_MESSAGE
                else:
                    user.current_balance = float(user.current_balance)

                    if trans_type == 'credited':
                        user.current_balance += float(amount)
                        transaction_amount = f"+{amount}"
                    elif trans_type == 'debited':
                        user.current_balance -= float(amount)
                        transaction_amount = f"-{amount}"

                    transaction = UserTransactions(user=user, transaction_type=trans_type, amount=transaction_amount)
                    transaction_msg = transaction.validate_and_save()
                    user.updated_at =  timezone.now()
                    user_msg = user.validate_and_save()

                    if transaction_msg:
                        message_value = transaction_msg
                    elif user_msg:
                        message_value = user_msg
                    else:
                        message_name = "Success"
                        message_value = f"Amount has been {trans_type} successfully!"
                        status_code = status.HTTP_200_OK

        except Exception as e:
            message_value = APIConstants.COMMON_ERROR_MESSAGE.format(e=e)
            generate_traceback.generate_traceback()
        finally:  
            return JsonResponse({message_name:message_value}, status=status_code)

    return HttpResponse(status=400)


@csrf_exempt
def stocks_transactions(request):
    """
    This view function handles post request at stock-transaction endpoint where it adds stock transaction details 
    related to account in the respective tables in database.
    :param request: Http request object
    :return JsonResponse/HttpResponse: returns JsonResponse with message success/error if post request else 
                                        HttpResponse object with appropriate status code
    """
    if request.method == 'POST':
        request_data = json.loads(request.body)
        status_code = status.HTTP_400_BAD_REQUEST
        message_name = APIConstants.DEFAULT_MESSAGE_NAME
        try:
            trans_type, quantity, stock, user, msg = validate_apis.validate_stocks_transactions_api(request_data)
            if msg:
                message_value = msg
                status_code = status.HTTP_404_NOT_FOUND
            else:
                if trans_type == 'buy':
                    if (stock.current_price*quantity > user.current_balance):
                        message_value = APIConstants.INSUFFICIENT_BALANCE_MESSAGE
                    else:
                        try: 
                            user_holding = UserHoldings.objects.get(Q(user=user) & Q(stock_symbol=stock.stock_symbol))
                        except UserHoldings.DoesNotExist:
                            user_holding = UserHoldings(user=user, stock_symbol=stock, quantity=quantity)
                        else:
                            user_holding.quantity = user_holding.quantity
                            user_holding.quantity += quantity
                            user_holding.updated_at = timezone.now()
                        finally:
                            user.current_balance = float(user.current_balance)
                            user.current_balance -= float(stock.current_price*quantity)
                            user.updated_at = timezone.now()
                            transaction_amount = f"-{(stock.current_price*quantity)}"
                            transaction = UserTransactions(user=user, transaction_type=trans_type, 
                                                           amount=transaction_amount, stock_symbol=stock)
                            
                            trasaction_msg = transaction.validate_and_save()
                            user_holding_msg = user_holding.validate_and_save()
                            user_msg = user.validate_and_save()

                            if trasaction_msg:
                                message_value = trasaction_msg
                            elif user_holding_msg:
                                message_value = user_holding_msg
                            elif user_msg:
                                message_value = user_msg
                            else:
                                message_name = "Success"
                                message_value = "Successfully bought the stocks!"
                                status_code = status.HTTP_200_OK
                
                elif trans_type == 'sell':
                    try:
                        user_holding = UserHoldings.objects.get(Q(user=user) & Q(stock_symbol=stock.stock_symbol))
                    except UserHoldings.DoesNotExist:
                        message_value = APIConstants.HOLDING_NOT_PRESENT_MESSAGE
                        status_code = status.HTTP_404_NOT_FOUND
                    else:
                        if user_holding.quantity < quantity:
                            message_value = APIConstants.INSUFFICIENT_STOCKS_MESSAGE
                        else:
                            user_holding.quantity -= quantity
                            if user_holding.quantity == 0:
                                user_holding.delete()
                                user_holding_msg = None
                            else:
                                user_holding.updated_at = timezone.now()
                                user_holding_msg = user_holding.validate_and_save()
                            
                            user.current_balance = float(user.current_balance)
                            user.current_balance += float(stock.current_price*quantity)
                            user.updated_at = timezone.now()

                            transaction_amount = f"+{(stock.current_price*quantity)}"
                            transaction = UserTransactions(user=user, transaction_type=trans_type, 
                                                           amount=transaction_amount, stock_symbol=stock)
                            
                            trasaction_msg = transaction.validate_and_save()
                            user_msg = user.validate_and_save()
                            
                            if trasaction_msg:
                                message_value = trasaction_msg
                            elif user_holding_msg:
                                message_value = user_holding_msg
                            elif user_msg:
                                message_value = user_msg
                            else:
                                message_name = "Success"
                                message_value = "Successfully sold the stocks!"
                                status_code = status.HTTP_200_OK

        except Exception as e:
            generate_traceback.generate_traceback()
            message_value = APIConstants.COMMON_ERROR_MESSAGE.format(e=e)
        finally:
            return JsonResponse({message_name:message_value}, status=status_code)
    
    return HttpResponse(status=400)


@csrf_exempt
def app_user(request, id=None):
    """
    The view function to handle the CRUD operations for AppUser model.
    :param request: Http request object
    :param id: user id from path parameters
    :return JsonResponse/HttpResponse: returns data or message as per request in JsonResponse or else HttpResponse
                                        if request method not handled 
    """
    if request.method == 'GET':
        msg_name = APIConstants.DEFAULT_MESSAGE_NAME
        data, msg = get_data.get_table_data(AppUser, id)
        if not msg:
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)
        return JsonResponse({msg_name:msg}, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'POST':
        msg_name = APIConstants.DEFAULT_MESSAGE_NAME
        status_code = status.HTTP_400_BAD_REQUEST
        try:
            request_data = json.loads(request.body)
            user_email, current_balance, user, msg = validate_apis.validate_app_user_api(request_data)
            if msg:
                msg_value = msg
            else:
                user = AppUser(user_email=user_email, current_balance=current_balance)
                usr_msg = user.validate_and_save()
                if usr_msg:
                    msg_value = usr_msg
                else:
                    msg_name = "Success"
                    msg_value = APIConstants.SUCCESSFULLY_ADDED_MESSAGE.format(object=user)
                    status_code = status.HTTP_200_OK
        except Exception as e:
            msg_value = APIConstants.COMMON_ERROR_MESSAGE.format(e=e)
            generate_traceback.generate_traceback()
        finally:
            return JsonResponse({msg_name:msg_value}, status=status_code)
        
    elif request.method == 'PUT':
        msg_name = APIConstants.DEFAULT_MESSAGE_NAME
        status_code = status.HTTP_404_NOT_FOUND
        try:
            if not id:
                msg_value = APIConstants.ID_NOT_FOUND_MESSAGE.format(object='User')
            else:
                request_data = json.loads(request.body)
                email, balance, user, msg = validate_apis.validate_app_user_api(request_data, id=id)
                if msg:
                    msg_value = msg
                else: 
                    if email != user.user_email:
                        user.user_email = email
                    if balance != user.current_balance:
                        if balance > user.current_balance:
                            transaction = UserTransactions(user=user, transaction_type="credited", 
                                                        amount=(balance-user.current_balance))
                        else:
                            transaction = UserTransactions(user=user, transaction_type="debited", 
                                                        amount=(user.current_balance-balance))
                        trans_msg = transaction.validate_and_save()
                        user.current_balance = balance
                    user.updated_at = timezone.now()
                    user_msg = user.validate_and_save()
                    if trans_msg: 
                        msg_value = trans_msg
                    elif user_msg:
                        msg_value = user_msg
                    else:
                        msg_name = "Success"
                        msg_value = APIConstants.SUCCESSFULLY_UPDATED_MESSAGE.format(object=user)
                        status_code = status.HTTP_200_OK
        except Exception as e:
            msg_value = APIConstants.COMMON_ERROR_MESSAGE.format(e=e)
            status_code = status.HTTP_400_BAD_REQUEST
            generate_traceback.generate_traceback()
        finally:
            return JsonResponse({msg_name:msg_value}, status=status_code)

    elif request.method == 'DELETE':
        msg_name = APIConstants.DEFAULT_MESSAGE_NAME
        try:
            if not id:
                msg_value = APIConstants.ID_NOT_FOUND_MESSAGE.format(object='User')
                status_code = status.HTTP_404_NOT_FOUND
            else:
                user = AppUser.objects.get(id=id)
                user.delete()
                msg_name = "Success"
                msg_value = APIConstants.SUCCESSFULLY_DELETED_MESSAGE.format(object=user)
                status_code = status.HTTP_200_OK
        except AppUser.DoesNotExist:
            msg_value = APIConstants.USER_NOT_EXIST_MESSAGE
            status_code = status.HTTP_404_NOT_FOUND
        except Exception as e:
            msg_value = APIConstants.COMMON_ERROR_MESSAGE.format(e=e)
            status_code = status.HTTP_400_BAD_REQUEST
        finally:
            return JsonResponse({msg_name:msg_value}, status=status_code)

    return HttpResponse(status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def stocks(request, id=None):
    """
    The view function to handle the CRUD operations for Stocks model.
    :param request: Http request object
    :param id: stock id from path parameters
    :return JsonResponse/HttpResponse: returns data or message as per request in JsonResponse or else HttpResponse
                                        if request method not handled 
    """
    if request.method == 'GET':
        msg_name = APIConstants.DEFAULT_MESSAGE_NAME
        data, msg = get_data.get_table_data(Stocks, id)
        if not msg:
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)
        return JsonResponse({msg_name:msg}, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'POST':
        msg_name = APIConstants.DEFAULT_MESSAGE_NAME
        status_code = status.HTTP_400_BAD_REQUEST
        try:
            request_data = json.loads(request.body)
            company_name, stock_symbol, current_price, stock, msg = validate_apis.validate_stocks_api(request_data)
            if msg:
                msg_value = msg
            else:
                stock = Stocks(company_name=company_name, stock_symbol=stock_symbol, current_price=current_price)
                stock_msg = stock.valiate_and_save()
                if stock_msg:
                    msg_value = stock_msg
                else:
                    msg_name = "Success"
                    msg_value = APIConstants.SUCCESSFULLY_ADDED_MESSAGE.format(object=stock)
                    status_code = status.HTTP_200_OK
        except Exception as e:
            msg_value = APIConstants.COMMON_ERROR_MESSAGE.format(e=e)
            status_code = status.HTTP_400_BAD_REQUEST
            generate_traceback.generate_traceback()
        finally:
            return JsonResponse({msg_name:msg_value}, status=status_code)

    elif request.method == 'PUT':
        msg_name = APIConstants.DEFAULT_MESSAGE_NAME
        status_code = status.HTTP_404_NOT_FOUND
        try:
            if not id:
                msg_value = APIConstants.ID_NOT_FOUND_MESSAGE.format(object='Stock')
                status_code = status.HTTP_404_NOT_FOUND
            else:
                request_data = json.loads(request.body)
                company_name, stock_symbol, current_price, stock, msg = validate_apis.\
                                                                        validate_stocks_api(request_data,id=id)
                if msg:
                    msg_value = msg
                else:
                    if company_name != stock.company_name:
                        stock.company_name = company_name
                    if stock_symbol != stock.stock_symbol:
                        raise IntegrityError
                    if current_price != stock.current_price:
                        stock.current_price = current_price
                    stock.updated_at = timezone.now()
                    stock_msg = stock.valiate_and_save()
                    if stock_msg:
                        msg_value = stock_msg
                    else:
                        msg_name = "Success"
                        msg_value = APIConstants.SUCCESSFULLY_UPDATED_MESSAGE.format(object=stock)
                        status_code = status.HTTP_200_OK
        except IntegrityError:
            msg_value = APIConstants.FOREIGN_KEY_ERROR_MESSAGE.format(key="stock_symbol")
            status_code = status.HTTP_424_FAILED_DEPENDENCY
        except Exception as e:
            msg_value = APIConstants.COMMON_ERROR_MESSAGE.format(e=e)
            status_code = status.HTTP_400_BAD_REQUEST
            generate_traceback.generate_traceback()
        finally:
            return JsonResponse({msg_name:msg_value}, status=status_code)

    elif request.method == 'DELETE':
        msg_name = APIConstants.DEFAULT_MESSAGE_NAME
        try:
            if not id:
                msg_value = APIConstants.ID_NOT_FOUND_MESSAGE.format(object='Stock')
                status_code = status.HTTP_404_NOT_FOUND
            else:
                stock = Stocks.objects.get(id=id)
                stock.delete()
                msg_name = "Success"
                msg_value = APIConstants.SUCCESSFULLY_DELETED_MESSAGE.format(object=stock)
                status_code = status.HTTP_200_OK
        except Stocks.DoesNotExist:
            msg_value = APIConstants.STOCKS_NOT_EXIST_MESSAGE
            status_code = status.HTTP_404_NOT_FOUND
        except Exception as e:
            msg_value = APIConstants.COMMON_ERROR_MESSAGE.format(e=e)
            status_code = status.HTTP_400_BAD_REQUEST
        finally:
            return JsonResponse({msg_name:msg_value}, status=status_code)

    return HttpResponse(status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def user_holdings(request, id=None):
    """
    The view function to handle the read operations for UserHoldings model.
    :param request: Http request object
    :param id: user_holding id from path parameters
    :return JsonResponse/HttpResponse: returns data or message as per request in JsonResponse or else HttpResponse
                                        if request method not handled 
    """
    if request.method == 'GET':
        msg_name = APIConstants.DEFAULT_MESSAGE_NAME
        data, msg = get_data.get_table_data(UserHoldings, id)
        if not msg:
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)
        return JsonResponse({msg_name:msg}, status=status.HTTP_400_BAD_REQUEST)

    return HttpResponse(status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def user_transactions(request, id=None):
    """
    The view function to handle the read operations for UserTransactions model.
    :param request: Http request object
    :param id: user_transactions id from path parameters
    :return JsonResponse/HttpResponse: returns data or message as per request in JsonResponse or else HttpResponse
                                        if request method not handled 
    """
    if request.method == 'GET':
        msg_name = APIConstants.DEFAULT_MESSAGE_NAME
        data, msg = get_data.get_table_data(UserTransactions, id)
        if not msg:
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)
        return JsonResponse({msg_name:msg}, status=status.HTTP_400_BAD_REQUEST)
    
    return HttpResponse(status=status.HTTP_400_BAD_REQUEST)