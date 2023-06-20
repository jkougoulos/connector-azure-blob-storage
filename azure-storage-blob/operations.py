""" Copyright start
  Copyright (C) 2008 - 2023 Fortinet Inc.
  All rights reserved.
  FORTINET CONFIDENTIAL & FORTINET PROPRIETARY SOURCE CODE
  Copyright end """

import xmltodict
from connectors.core.connector import get_logger, ConnectorError
import requests
from os.path import join
from connectors.cyops_utilities.builtins import download_file_from_cyops
from integrations.crudhub import make_request

logger = get_logger('azure-storage-blob')

STORAGE_SERVICE_ENDPOINT = ".blob.core.windows.net"


def api_request(method, endpoint, params=None, data=None, verify_ssl=False, headers={}):
    try:
        headers['Content-Type'] = 'application/json'
        headers['Accept'] = 'application/json'
        response = requests.request(method, endpoint, headers=headers, params=params, data=data, verify=verify_ssl)
        if response.status_code in [200, 201, 202, 204]:
            content_type = response.headers.get('Content-Type')
            if response.text != "" and 'application/xml' in content_type:
                return response.text
            return response
        else:
            raise ConnectorError("{0}".format(response.content))
    except requests.exceptions.SSLError:
        raise ConnectorError('SSL certificate validation failed')
    except requests.exceptions.ConnectTimeout:
        raise ConnectorError('The request timed out while trying to connect to the server')
    except requests.exceptions.ReadTimeout:
        raise ConnectorError(
            'The server did not send any data in the allotted amount of time')
    except requests.exceptions.ConnectionError:
        raise ConnectorError('Invalid Credentials')
    except Exception as err:
        raise ConnectorError(str(err))


def _check_health(config, connector_info):
    try:
        if list_blob(config, None, connector_info):
            return True
        else:
            raise ConnectorError("Invalid Credentials")
    except Exception as err:
        raise ConnectorError(str(err))


def handle_params(params):
    value = str(params.get('value'))
    input_type = params.get('input')
    try:
        if isinstance(value, bytes):
            value = value.decode('utf-8')
        if input_type == 'Attachment ID':
            if not value.startswith('/api/3/attachments/'):
                value = '/api/3/attachments/{0}'.format(value)
            attachment_data = make_request(value, 'GET')
            file_iri = attachment_data['file']['@id']
            file_name = attachment_data['file']['filename']
            logger.info('file id = {0}, file_name = {1}'.format(file_iri, file_name))
            return file_iri
        elif input_type == 'File IRI':
            if value.startswith('/api/3/files/'):
                return value
            else:
                raise ConnectorError('Invalid File IRI {0}'.format(value))
    except Exception as err:
        logger.info('handle_params(): Exception occurred {0}'.format(err))
        raise ConnectorError('Requested resource could not be found with input type "{0}" and value "{1}"'.format
                             (input_type, value.replace('/api/3/attachments/', '')))


def submitFile(file_iri):
    try:
        file_path = join('/tmp', download_file_from_cyops(file_iri)['cyops_file_path'])
        logger.info(file_path)
        with open(file_path, 'rb') as attachment:
            file_data = attachment.read()
        if file_data:
            files = {'file': file_data}
            return files
        raise ConnectorError('File size too large, submit file up to 32 MB')
    except Exception as Err:
        logger.error('Error in submitFile(): %s' % Err)
        raise ConnectorError('Error in submitFile(): %s' % Err)


def put_blob(config, params, connector_info):
    headers = dict()
    file_iri = handle_params(params)
    files = submitFile(file_iri)
    headers["x-ms-blob-type"] = "BlockBlob"
    endpoint = f"https://{config.get('account_name')}{STORAGE_SERVICE_ENDPOINT}/{config.get('container_name')}/{params.get('blob_name')}{config.get('sas_token')}"
    response = api_request("PUT", endpoint, connector_info, data=files, headers=headers)
    return "Successfully Created"


def list_blob(config, params, connector_info):
    endpoint = f"https://{config.get('account_name')}{STORAGE_SERVICE_ENDPOINT}/{config.get('container_name')}?restype=container&comp=list&{(config.get('sas_token')).strip('?')}"
    response = api_request("GET", endpoint, config)
    data_dict = xmltodict.parse(response)
    return data_dict


operations = {
    'create_blob': put_blob,
    'list_blob': list_blob
}
