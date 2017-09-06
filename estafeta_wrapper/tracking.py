import os
from requests import Session
import zeep
from lxml import etree
from zeep.transports import Transport
from datetime import datetime

def track(login,
          password,
          subscriber_id,
          waybill,
          production=False):
    """ Given a tracking number for a waybill, it returns it's current
    status.
    """
    if production:
        wsdl = 'https://tracking.estafeta.com/Service.asmx?wsdl'
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__)) + '/wsdl'
        wsdl = base_dir + '/Service.asmx.wsdl.xml'

    client = zeep.Client(wsdl=wsdl)
    factory0 = client.type_factory('ns0')

    # Datos de la lista de guías
    waybill_type = 'G'
    string = [waybill]
    array_of_string = factory0.ArrayOfString(string=string)
    waybill_list = factory0.WaybillList(waybillType=waybill_type,
                                        waybills=array_of_string)

    # Datos de la búsqueda
    s_type = 'L' # List, change for an enum with the proper options
    search_type = factory0.SearchType(waybillList=waybill_list,
                                      type=s_type)

    # Configuración de la búsqueda
    history_configuration = factory0.HistoryConfiguration(includeHistory=1,
                                                          historyType='ALL')
    filter_type = factory0.Filter(filterInformation=0)
    search_configuration = factory0.SearchConfiguration(includeDimensions=True,
                                                        includeWaybillReplaceData=False,
                                                        includeReturnDocumentData=False,
                                                        includeMultipleServiceData=False,
                                                        includeInternationalData=False,
                                                        includeSignature=False,
                                                        includeCustomerInfo=True,
                                                        historyConfiguration=history_configuration,
                                                        filterType=filter_type)

    return(client.service.ExecuteQuery(login=login,
                                       password=password,
                                       suscriberId=subscriber_id,
                                       searchType=search_type,
                                       searchConfiguration=search_configuration))
