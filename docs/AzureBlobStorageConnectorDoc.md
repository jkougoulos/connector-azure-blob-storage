## About the connector
Azure Blob Storage is Microsoft's object storage solution for the cloud. Blob Storage is optimized for storing massive amounts of unstructured data. Azure Blob Storage stores text and binary data as objects in the cloud. This connector helps you to perform REST operations for working with blobs in the Blob service.
<p>This document provides information about the Azure Blob Storage Connector, which facilitates automated interactions, with a Azure Blob Storage Blob server using FortiSOAR&trade; playbooks. Add the Azure Blob Storage Connector as a step in FortiSOAR&trade; playbooks and perform automated operations with Azure Blob Storage.</p>

### Version information

Connector Version: 1.0.0


Authored By: spryIQ.co

Certified: No
## Installing the connector
<p>From FortiSOAR&trade; 5.0.0 onwards, use the <strong>Connector Store</strong> to install the connector. For the detailed procedure to install a connector, click <a href="https://docs.fortinet.com/document/fortisoar/0.0.0/installing-a-connector/1/installing-a-connector" target="_top">here</a>.<br>You can also use the following <code>yum</code> command as a root user to install connectors from an SSH session:</p>
`yum install cyops-connector-azure-blob-storage`

## Prerequisites to configuring the connector
- You must have the Azure Storage Account Name, SAS Token and Container Name to perform automated operations.
- The FortiSOAR&trade; server should have outbound connectivity to port 443 on the Azure Blob Storage server.

## Minimum Permissions Required
- N/A

## Configuring the connector
For the procedure to configure a connector, click [here](https://docs.fortinet.com/document/fortisoar/0.0.0/configuring-a-connector/1/configuring-a-connector)
### Configuration parameters
<p>In FortiSOAR&trade;, on the Connectors page, click the <strong>Azure Blob Storage</strong> connector row (if you are in the <strong>Grid</strong> view on the Connectors page) and in the <strong>Configurations&nbsp;</strong> tab enter the required configuration details:&nbsp;</p>
<table border=1><thead><tr><th>Parameter<br></th><th>Description<br></th></tr></thead><tbody><tr><td>Storage Account Name<br></td><td>Name of the storage account from which you want to perform the automated operations.<br>
<tr><td>Account SAS Token<br></td><td>Account Shared Access Signature(SAS) to perform automated operations on Blob Storage Service.<br>
<tr><td>Container Name<br></td><td>Specify the name of the azure container within your storage account.<br>
<tr><td>Verify SSL<br></td><td>Specifies whether the SSL certificate for the server is to be verified or not. <br/>By default, this option is set as True.<br></td></tr>
</tbody></table>

## Actions supported by the connector
The following automated operations can be included in playbooks and you can also use the annotations to access operations from FortiSOAR&trade; release 4.10.0 and onwards:
<table border=1><thead><tr><th>Function<br></th><th>Description<br></th><th>Annotation and Category<br></th></tr></thead><tbody><tr><td>Put Blob<br></td><td>Creates a new blob or replaces an existing blob within a container.<br></td><td>create_blob <br/>Investigation<br></td></tr>
<tr><td>List Blob<br></td><td>The List Blob operation returns a list of the blobs under the specified container.<br></td><td>list_blob <br/>Investigation<br></td></tr>
</tbody></table>

### operation: Put Blob
#### Input parameters
<table border=1><thead><tr><th>Parameter<br></th><th>Description<br></th></tr></thead><tbody><tr><td>Blob Name<br></td><td>Specify the name of the blob to create or replace.<br>
</td></tr><tr><td>File Attachment/IRI Reference<br></td><td>File Attachment/IRI Reference that is used to access the attachment metadata from the FortiSOAR™ Attachments module. In the playbook, if you select 'Attachment ID', this defaults to the {{vars.attachment_id}} value or if you select 'File IRI', then this defaults to the {{vars.file_iri}} value.<br>
</td></tr><tr><td>Type<br></td><td>Choose between Attachment ID or a File IRI.<br>
</td></tr></tbody></table>

#### Output

 {
     "status": "",
     "message": ""
 }
### operation: List Blob
#### Input parameters
None.
#### Output

{
    "EnumerationResults": {
        "@ServiceEndpoint": "",
        "@ContainerName": "",
        "Blobs": {
            "Blob": [
                {
                    "Name": "",
                    "Properties": {
                        "Creation-Time": "",
                        "Last-Modified": "",
                        "Etag": "",
                        "Content-Length": "",
                        "Content-Type": "",
                        "Content-Encoding": "",
                        "Content-Language": "",
                        "Content-CRC64": "",
                        "Content-MD5": "",
                        "Cache-Control": "",
                        "Content-Disposition": "",
                        "BlobType": "",
                        "AccessTier": "",
                        "AccessTierInferred": "",
                        "LeaseStatus": "",
                        "LeaseState": "",
                        "ServerEncrypted": ""
                    },
                    "OrMetadata": ""
                }
            ]
        },
        "NextMarker": ""
    }
}
## Included playbooks
The `Sample - azure-blob-storage - 1.0.0` playbook collection comes bundled with the Azure Blob Storage connector. These playbooks contain steps using which you can perform all supported actions. You can see bundled playbooks in the **Automation** > **Playbooks** section in FortiSOAR<sup>TM</sup> after importing the Azure Blob Storage connector.

- List Blob
- Put Blob

**Note**: If you are planning to use any of the sample playbooks in your environment, ensure that you clone those playbooks and move them to a different collection, since the sample playbook collection gets deleted during connector upgrade and delete.
