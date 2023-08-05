# -*- coding: utf-8 -*-
import urllib
import logging
from datetime import datetime, timedelta

from vtex.connector import Connector, ConnectorException
from vtex.settings import api_settings

logger = logging.getLogger(__name__)


class VtexHandler:
    """
        Handler to deal with Vtex
    """

    def __init__(self, base_url=api_settings.VTEX['BASE_URL'],
                 app_key=api_settings.VTEX['APP_KEY'],
                 app_token=api_settings.VTEX['APP_TOKEN'],
                 verify=True):
        self.app_key = app_key
        self.app_token = app_token
        self.base_url = base_url
        self.verify = verify
        self.connector = Connector(self._headers(), verify_ssl=self.verify)

    def _headers(self):
        """
            Here define the headers for all connections with Vtex.
        """
        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-VTEX-API-AppKey': self.app_key,
            'X-VTEX-API-AppToken': self.app_token
        }

    def get_orders(self, offset=2):
        """
            This method obtain an order list from VTEX.
        """
        d_offset = datetime.now() - timedelta(hours=offset)
        start_date = d_offset.strftime('%Y-%m-%dT%X.%fZ')
        end_date = datetime.now().strftime('%Y-%m-%dT%X.%fZ')

        params = {
            'f_creationDate': f'creationDate:[{start_date} TO {end_date}]'}

        try:
            url = f'{self.base_url}orders/?{params}'
            response = self.connector.get(url)
            return response
        except ConnectorException as error:
            logger.error(error)
            return False

    def get_order_detail(self, identifier):
        """
            This method obtain an order detail from VTEX.
        """
        try:
            url = f'{self.base_url}orders/{identifier}'
            response = self.connector.get(url)
            return response
        except ConnectorException as error:
            logger.error(error)
            return False

    def create_invoice(self, identifier, instance):
        """
            This method create an invoice from order data in VTEX.
        """
        try:
            today = datetime.today().strftime('%Y-%m-%dT%H:%M:%S')
            data = {
                'type': 'Output',
                'invoiceNumber': instance.invoice_number,
                'courier': instance.courier,
                'trackingNumber': instance.tracking_number,
                'trackingUrl': instance.tracking_url,
                'items': instance.items,
                'issuanceDate': today,
                'invoiceValue': instance.total_value,
            }
            url = f'{self.base_url}orders/{identifier}/invoice'
            response = self.connector.post(url, data=data)
            return response
        except ConnectorException as error:
            logger.error(error)
            return False

    def update_order_status(self, identifier, status):
        """
            This method change the orders status taking one of
            [
                'order-completed', 'start-handling', 'handling',
                'ready-for-handling', 'waiting-ffmt-authorization', 'cancel'
            ].
        """
        try:
            if status not in [
                'order-completed',
                'start-handling',
                'handling',
                'ready-for-handling',
                'waiting-ffmt-authorization',
                'cancel'
            ]:
                raise ConnectorException(
                    'status param is invalid, please check allowed values',
                    'select a valid status',
                    400
                )
            url = f'{self.base_url}orders/{identifier}/{status}'
            response = self.connector.post(url, data={})

            logger.debug(response)
            return response
        except ConnectorException as error:
            logger.error(error)
            return False
        # TODO: Catch 409 Error trying to apply wrong status

    def update_tracking_status(self, identifier, invoice_number, events=[], is_delivered=False):
        """
            This method uptates the order tracking status
            e.g events = [
                {
                    'city': 'Rio de Janeiro',
                    'state': 'RJ',
                    'description': 'Coletado pela transportadora',
                    'date': '2015-06-23'},
                {
                    'city': 'Sao Paulo',
                    'state': 'SP',
                    'description': 'A caminho de Curitiba',
                    'date': '2015-06-24'
                }
            ]
        """
        data = {
            'isDelivered': is_delivered,
            'events': []
        }

        try:
            event_fields = ['city' 'state' 'description' 'date']
            for event in events:
                if set(event_fields) == set(event.keys()):
                    data['events'].append(event)
        except Exception as e:
            logger.error(
                "Error: events must have the following format: [{'city': 'Rio de Janeiro', 'state': 'RJ', 'description': 'Coletado pela transportadora', 'date': '2015-06-23'}]")
            return False

        try:
            url = f'{self.base_url}orders/{identifier}/invoice/{invoice_number}/tracking'
            response = self.connector.put(url, data=data)
            return response
        except ConnectorException as error:
            logger.error(error)
            return False

    def cancel_order(self, identifier):
        """
            This method cancels an order in VTEX.
        """
        try:
            url = f'{self.base_url}orders/{identifier}/cancel'
            response = self.connector.post(url, data={})
            return response
        except ConnectorException as error:
            logger.error(error)
            return False
