""" Copyright start
  Copyright (C) 2008 - 2023 Fortinet Inc.
  All rights reserved.
  FORTINET CONFIDENTIAL & FORTINET PROPRIETARY SOURCE CODE
  Copyright end """

from connectors.core.connector import get_logger, ConnectorError
import requests

logger = get_logger('azure-storage-blob')

STORAGE_SERVICE_ENDPOINT = ".blob.core.windows.net"


def api_request(method, endpoint, params=None, Json=None, verify_ssl=False, headers={}):
    try:
        headers['Content-Type'] = 'application/json'
        headers['Accept'] = 'application/json'
        response = requests.request(method, endpoint, headers=headers, params=params, json=Json, verify=verify_ssl)
        if response.status_code in [200, 201, 202, 204]:
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


def put_blob(config, params, connector_info):
    headers = dict()
    payload = None
    if params.get("blob_type") == 'AppendBlob':
        headers["x-ms-blob-type"] = "AppendBlob"
    elif params.get("blob_type") == 'PageBlob':
        headers["x-ms-blob-type"] = "PageBlob"
        headers["x-ms-blob-content-length"] = "1024"
    else:
        headers["x-ms-blob-type"] = "BlockBlob"
        payload = {"data": params.get("blob_data")}

    endpoint = "https://" + config.get("account_name") + STORAGE_SERVICE_ENDPOINT + config.get("container_name") + '/' + params.get("blob_name") + "?" + config.get("sas_token")
    response = api_request("PUT", endpoint, connector_info, Json=payload, headers=headers)
    return response


def list_blob(config, params, connector_info):
    endpoint = "https://" + config.get("account_name") + STORAGE_SERVICE_ENDPOINT + config.get("container_name") + "?restype=container&comp=list&" + config.get("sas_token")
    response = api_request("GET", endpoint, config)
    return response


operations = {
    'create_blob': put_blob,
    'list_blob': list_blob
}
