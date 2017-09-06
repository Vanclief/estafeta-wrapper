import os
from requests import Session
import zeep
from lxml import etree
from zeep.transports import Transport
from datetime import datetime


def ship(
    login,
    password,
    subscriber_id,
    customer_number,
    d_info,
    o_info,
    weight,
    content,
    additional_info='1',
    production=False
):
    """ Creates a new shipment with estafeta, with the provided data.

    """
    # Setup request session due to poor management of Certificates by Estafeta
    
    session = Session()
    session.verify = False
    transport = zeep.transports.Transport(session=session)
    if production:
        wsdl = 'https://label.estafeta.com/EstafetaLabel20/services/EstafetaLabelWS?wsdl'
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__)) + '/wsdl'
        wsdl = base_dir + '/EstafetaLabelWS.wsdl.xml'
        # wsdl = 'https://labelqa.estafeta.com/EstafetaLabel20/services/EstafetaLabelWS?wsdl'

    client = zeep.Client(wsdl=wsdl, transport=transport)
    factory0 = client.type_factory('ns0')
    factory1 = client.type_factory('ns1')
    factory2 = client.type_factory('ns2')


    # Datos de impresion
    # TODO: Change for an ENUM
    paper_type = 1 # Papel Bond Tamaño Carta
    
    # Datos de la guía
    valid = True
    label_description_list_count = 1

    d_info['customerNumber'] = customer_number
    d_info['valid'] = valid
    destination_info = factory0.DestinationInfo(**d_info)

    o_info['customerNumber'] = customer_number
    o_info['valid'] = valid
    origin_info = factory0.OriginInfo(**o_info)

    # labelDescriptionList
    delivery_to_estafeta_office = True
    number_of_labels = 1
    office_num=130
    parcel_type_id = 1 # 4 Sobre, 1 Paquete cambiar por Enum
    return_document = False
    service_type_id=70
    zip_code = o_info['zipCode']

    label_description_list = factory0.LabelDescriptionList(
        aditionalInfo=additional_info,
        content=content,
        deliveryToEstafetaOffice=delivery_to_estafeta_office,
        numberOfLabels=number_of_labels,
        officeNum=office_num,
        destinationInfo=destination_info,
        originInfo=origin_info,
        originZipCodeForRouting=zip_code,
        parcelTypeId=parcel_type_id,
        returnDocument=return_document,
        serviceTypeId=service_type_id,
        valid=valid,
        weight=weight
    )

    estafeta_label_request = factory0.EstafetaLabelRequest(
                                                  login=login,
                                                  password=password,
                                                  suscriberId=subscriber_id, # [sic]
                                                  customerNumber=customer_number,
                                                  paperType=paper_type,
                                                  quadrant=1,
                                                  valid=valid,
                                                  labelDescriptionListCount=label_description_list_count,
                                                  labelDescriptionList=[label_description_list]
                                                  )

    return(client.service.createLabel(in0=estafeta_label_request))
