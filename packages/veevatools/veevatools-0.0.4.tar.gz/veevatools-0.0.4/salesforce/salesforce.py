from sys import platform
from numpy import deprecate
import pandas as pd
import os
from simple_salesforce import Salesforce
from simple_salesforce import SalesforceLogin
from salesforce_bulk import SalesforceBulk
from sfdclib import SfdcSession
from sfdclib import SfdcMetadataApi
from sfdclib import SfdcToolingApi
import re
import time
import json
from salesforce_bulk.util import IteratorBytesIO
import pandas as pd
import requests
import base64
from typing import List, Tuple, Optional, Union, Type
from collections import OrderedDict
import sys
sys.path.append("..")
from custom_exceptions.salesforce_exceptions import *
from utilities.df_utils import *
from salesforce.decorators import *



class Sf:
    _REGEX_PARSE_SOQL_FIELDS = "(?<=select)(.*?)(?<!, )(?=from)"
    _REGEX_PARSE_SOQL_OBJECT = "(?<!, from )(?<=from )\w*"
    
    def __init__(self) -> None:
        self.filename: str = None
        self.os_platform: str = platform
        self.credentials: pd.DataFrame = pd.DataFrame()
        self.sfUsername: str = None
        self.sfPassword: str = None
        self.sfOrgId: str = None
        self.isSandbox: bool = None
        self.session_id: str = None
        self.instance: str = None
        self.domain: str = None
        self.security_token: str = ''
        self.sf: Salesforce = None
        self.bulk: SalesforceBulk = None
        self.sfMeta: SfdcMetadataApi = None
        self.tooling: SfdcToolingApi = None
        self.api_version: str = 'v52.0'
        self.record_count: dict = {}
        self.record_count_caseinsensitive: dict = {}
        self.debug: bool = False
    
    def authenticate(self, sfUsername: Optional[str]=None, 
                                sfPassword: Optional[str]=None, 
                                sfOrgId: Optional[str]=None, 
                                isSandbox: Optional[str]=None, 
                                session_id: Optional[str]=None, 
                                instance: Optional[str]=None, 
                                security_token: Optional[str] = None,
                                domain: Optional[str] = None,
                                if_return: Optional[bool] = False,
                                *args, **kwargs) -> Optional[dict]:
        """
        Authenticates Salesforce and retrieves the auth token.

        Dependencies:
            from simple_salesforce import Salesforce
            from simple_salesforce import SalesforceLogin
            from salesforce_bulk import SalesforceBulk
            from sfdclib import SfdcSession
            from sfdclib import SfdcMetadataApi
            from sfdclib import SfdcToolingApi
        """
        
        sfUsername = self.sfUsername if sfUsername is None else sfUsername
        sfPassword = self.sfPassword if sfPassword is None else sfPassword
        sfOrgId = self.sfOrgId if sfOrgId is None else sfOrgId
        isSandbox = self.isSandbox if isSandbox is None else isSandbox
        session_id = self.session_id if session_id is None else session_id
        instance = self.instance if instance is None else instance
        security_token = self.security_token if security_token is None else security_token
        domain = self.domain if domain is None else domain
        
        # If session ID already exists and instance URL is already populated,
        # reauthenticate using existing session ID
        if session_id is not None and instance is not None:
            sf = Salesforce(session_id = session_id, instance_url = instance)
            self.sf = sf
        
        # If username, password, org ID, and isSandbox flags are all provided,
        # authenticate using provided credentials
        elif sfUsername is not None and sfPassword is not None and sfOrgId is not None and isSandbox is not None:
            
            # SFDC Sandbox authentication
            if isSandbox:
                self.domain = 'test'
                sf = Salesforce(password=sfPassword, 
                                username=sfUsername, 
                                organizationId=sfOrgId, 
                                security_token = self.security_token,domain='test')
                session_id, instance = SalesforceLogin(
                username=sfUsername,
                password=sfPassword,
                security_token=self.security_token,
                domain= self.domain)
                self.session_id = session_id
                self.instance = instance
                self.sf = sf
                self.sfUsername = sfUsername
                self.sfPassword = sfPassword
                self.sfOrgId = sfOrgId
                self.isSandbox = isSandbox
                
            else:
                sf = Salesforce(password=sfPassword, 
                                username=sfUsername, 
                                organizationId=sfOrgId, 
                                security_token=self.security_token)
                session_id, instance = SalesforceLogin(
                username=sfUsername,
                password=sfPassword,
                security_token=self.security_token)
                self.session_id = session_id
                self.instance = instance
                self.sf = sf
                self.sfUsername = sfUsername
                self.sfPassword = sfPassword
                self.sfOrgId = sfOrgId
                self.isSandbox = isSandbox
                
        else:
            raise Exception('Either sfUsername, sfPassword, sfOrgId and isSandbox must be populated, OR session_id and instance must be populated.')

        # Alternative way to authenticate using SFDC Bulk API
        # bulk = SalesforceBulk(username=sfUsername, password=sfPassword, security_token='')
        bulk = SalesforceBulk(sessionId = session_id, host = instance)
        self.bulk = bulk
        # SFDC Metadata API
        sfMeta = SfdcSession(session_id=session_id, instance=".".join(instance.split(".")[:2]))
        self.sfMeta = sfMeta
        # Alternative way to authenticate using SFDC Metadata API
        # sfMeta = SfdcSession(username=sfUsername,password=sfPassword,token='',is_sandbox=isSandbox)
        sfMeta._api_version = "51.0"
        tooling = SfdcToolingApi(sfMeta)
        self.tooling = tooling
        
        self.api_version = 'v' + self.sf_api_call('/services/data')[-1]['version']
        
        for x in self.sf_api_call('/services/data/'+self.api_version+'/limits/recordCount')['sObjects']:
            self.record_count[x['name']] = x['count']
            self.record_count_caseinsensitive[x['name'].lower()] = x['count']
        
        if if_return:
            return {'sf':sf, 
                    'bulk':bulk, 
                    'sfMeta': sfMeta, 
                    'tooling':tooling, 
                    'session_id':session_id, 
                    'instance':instance, 
                    'sfMeta_is_connected':sfMeta.is_connected(), 
                    'bulk_api_sessionId':bulk.sessionId}

    def query(self, query: str, excludedFields: Optional[List] = []) -> pd.DataFrame:
        """
        Using SFDC SOQL Syntax, and allowing for Relationships and group bys. 
        
        Arguments:
            query (str): A Standard SFDC SOQL Query allowing for relationships (Owner.Name)
                Asterisks(*) represents all queryable fields and can be used in conjunction
                with other relationship fields. 
                i.e. (Select *, Owner.Profile.Name, Owner.Name From Account)
        
        Returns:
            Pandas Dataframe Object.
        
        Raises:
            KeyError: Typically raised when 0 records exist for the object
                
            badfield: A self-correcting error that is raised when a field is unqueriable, i.e. Address Fields
            
            Exception: When relationship query contains more than 4 layers, an Exception is raised.
            i.e. Parent_Account_vod__r.Owner.Profile.LastModifiedBy.Name (<- a 5 layer deep relationship is not supported)
        
        Example of Usage:
            sf.query("Select *, Owner.Profile.Name From Account ORDER BY CreatedDate DESC LIMIT 100")
            
            return:
            A Pandas Dataframe of the last created 100 account records, with all queriable fields included in the query and a relationship field.
            
        """
        objectName = re.search(self._REGEX_PARSE_SOQL_OBJECT, query.lower()).group(0)
        successful = False
        
        extracted_object = pd.DataFrame()
        # replaces "*" in query with all fields on object
        sfSchema = getattr(self.sf, objectName).describe().get('fields')

        schemaDict = {}
        for x in sfSchema:
            schemaDict[x['name']] = x

        while not successful:
            try:
                results = []
                for field in schemaDict:
                    if (schemaDict[field]['type'] != 'location' and 
                        schemaDict[field]['type'] != 'address' and 
                        schemaDict[field]['name'] not in excludedFields):
                        results.append(field)
                final_query = query.replace("*", ", ".join(results))                
                query_response = self.sf.query_all(final_query)
                # if the object has 0 records in Salesforce, return empty dataframe
                if query_response['totalSize'] == 0:
                    fields_preparsed = re.search(self._REGEX_PARSE_SOQL_FIELDS, query,  re.IGNORECASE).group(0).split(",")
                    return pd.DataFrame(columns=fields_preparsed)
                else:
                    result = pd.DataFrame(query_response)['records']
                    for _ in result:
                        del _['attributes']
                    successful = True
            except KeyError:
                if self.debug:
                    print(objectName + ' skipped. (Potentially due to no records found.)')
                    
                return pd.DataFrame(columns=results)
            except Exception as badfield:
                field_exclusion = badfield.state_message[badfield.state_message.find("No such column '")+\
                    16:badfield.state_message.find("No such column '")+16+\
                        badfield.state_message[badfield.state_message.find("No such column '")+16:].find("'")]
                excludedFields.append(field_exclusion)
                print("Excluded unqueriable field: " + field_exclusion)
                if query.find("*") == -1:
                    raise Exception(f"Unqueriable field {field_exclusion} found in query.")
                else:
                    continue
            
            result = result.apply(lambda x: pd.Series(x)).copy()

            relationship_fields_preparsed = re.search(self._REGEX_PARSE_SOQL_FIELDS, query,  re.IGNORECASE).group(0).split(",")
            # relationship_fields_prepared Example:
            # ['*',
            #  ' Parent_Account_vod__r.Owner.Profile.Name',
            #  ' Child_Account_vod__r.Owner.Profile.Name',
            #  'Parent_Account_vod__r.Owner.Profile.Id ']

            relational_fields = [{x.strip(): x.strip().split(".")} for x in relationship_fields_preparsed if "." in x]
            # relationship_fields Example:
            # [{'Parent_Account_vod__r.Owner.Profile.Name': ['Parent_Account_vod__r',
            #    'Owner',
            #    'Profile',
            #    'Name']},
            #  {'Child_Account_vod__r.Owner.Profile.Name': ['Child_Account_vod__r',
            #    'Owner',
            #    'Profile',
            #    'Name']},
            #  {'Parent_Account_vod__r.Owner.Profile.Id': ['Parent_Account_vod__r',
            #    'Owner',
            #    'Profile',
            #    'Id']}]

            columns_to_remove = set()
            for x in relational_fields:
                if len(list(x.values())[0]) > 4:
                    raise Exception("Too Many Relationship Levels. The Query you have entered contains more than 4 levels deep and is not supported.")
                elif len(list(x.values())[0]) == 4:
                    result[list(x.keys())[0]] = result[list(x.keys())[0].split(".")[0]].\
                        apply(lambda z: z[list(x.values())[0][1]][list(x.values())[0][2]][list(x.values())[0][3]])
                    columns_to_remove.add(list(x.values())[0][0])
                elif len(list(x.values())[0]) == 3:
                    result[list(x.keys())[0]] = result[list(x.keys())[0].split(".")[0]].\
                        apply(lambda z: z[list(x.values())[0][1]][list(x.values())[0][2]])
                    columns_to_remove.add(list(x.values())[0][0])
                elif len(list(x.values())[0]) == 2:
                    result[list(x.keys())[0]] = result[list(x.keys())[0].split(".")[0]].\
                        apply(lambda z: z[list(x.values())[0][1]])
                    columns_to_remove.add(list(x.values())[0][0])
            result.drop(columns_to_remove, axis=1, inplace=True)        

                
        return result

    def create(self, object_api: str=None, record_dataframe: pd.DataFrame = pd.DataFrame()) -> pd.DataFrame:
        """
        Function creates records within the Salesforce instance using bulk api.

        Arguments:
        object_api: str: API name of the Salesforce Object for which the records are to be created.

        record_dataframe: pd.DataFrame: A pandas dataframe object containing all the required fields for a record.

        Returns:
        result: pd.DataFrame: A pandas dataframe with the following columns:
            success: boolean: indicates whether the create request was successful
            created: boolean: this value should always be False in a create request
            id: object[str]: this value typically is None in a create request
            statusCode: object[str] - Optional: the error code of the create operation if failed
            message: object[str] - Optional: the error message of the create operation if failed
            fields: object[List[str]] - Optional: the fields for which the error code and message applies to.

        Raises:
            RequiredValuesNotProvidedDuringUpdate
        """
        if (object_api is None) or (len(record_dataframe) == 0):
            raise RequiredValuesNotProvidedDuringCreate()
        else:
            result = getattr(self.sf.bulk, object_api).insert(record_dataframe.to_dict('records'))
            result = pd.DataFrame(result)
            result = unpack_column(result, "errors")

        return pd.DataFrame(result.rename(columns={'id': 'Id'}))

    def delete(self, object_api: str=None, record_dataframe: pd.DataFrame = pd.DataFrame()) -> pd.DataFrame:
        """
        Function deletes records within the Salesforce instance using bulk api.

        Arguments:
        object_api: str: API name of the Salesforce Object for which the records are to be deleted from.

        record_dataframe: pd.DataFrame: A pandas dataframe object containing at least 1 column with an Id column (case sensitive)

        Returns:
        result: pd.DataFrame: A pandas dataframe with the following columns:
            success: boolean: indicates whether the delete request was successful
            created: boolean: this value should always be False in a delete request
            id: object[str]: this value typically is None in a delete request
            statusCode: object[str] - Optional: the error code of the delete operation if failed
            message: object[str] - Optional: the error message of the delete operation if failed
            fields: object[List[str]] - Optional: the fields for which the error code and message applies to.

        Raises:
            RequiredValuesNotProvidedDuringDelete
        """
        if (object_api is None) or (len(record_dataframe) == 0) or record_dataframe.columns.__contains__('Id') == False:
            raise RequiredValuesNotProvidedDuringDelete()
        else:
            result = getattr(self.sf.bulk, object_api).delete(record_dataframe['Id'].to_frame().to_dict('records'))
            result = pd.DataFrame(result)
            result = unpack_column(result, "errors")

        return pd.DataFrame(result.rename(columns={'id': 'Id'}))
    def update(self, object_api: str=None, record_dataframe: pd.DataFrame = pd.DataFrame()) -> pd.DataFrame:
        """
        Function updates records within the Salesforce instance using bulk api.

        Arguments:
        object_api: str: API name of the Salesforce Object for which the records are to be updated.

        record_dataframe: pd.DataFrame: A pandas dataframe object containing at least 1 column with an Id column (case sensitive)
            and additional columns matching the Salesforce field api names.

        Returns:
        result: pd.DataFrame: A pandas dataframe with the following columns:
            success: boolean: indicates whether the update request was successful
            created: boolean: this value should always be False in a update request
            id: object[str]: this value typically is None in a update request
            statusCode: object[str] - Optional: the error code of the update operation if failed
            message: object[str] - Optional: the error message of the update operation if failed
            fields: object[List[str]] - Optional: the fields for which the error code and message applies to.

        Raises:
            RequiredValuesNotProvidedDuringUpdate
        """

        field_metadata = self.field_describe([object_api])

        if ((object_api is None) or 
        (len(record_dataframe) == 0) or 
        record_dataframe.columns.__contains__('Id') == False or
        # checks whether any of the columns in the dataframe passed in are not valid field API names
        ~record_dataframe.columns.isin(field_metadata[object_api]).all()
        # checks whether an reference (lookup/master-detail) field is included in the source dataframe
        #  or ~record_dataframe.columns.isin(field_metadata[field_metadata['Type'] == 'reference'][object_api]).any()
        ):
            raise RequiredValuesNotProvidedDuringUpdate()
        else:
            result = getattr(self.sf.bulk, object_api).update(record_dataframe.to_dict('records'))
            result = pd.DataFrame(result)
            result = unpack_column(result, "errors")

        return pd.DataFrame(result.rename(columns={'id': 'Id'}))

    def upsert(self, object_api: str=None, external_id_field_api: str="", record_dataframe: pd.DataFrame = pd.DataFrame()) -> pd.DataFrame:
        """
        Function upserts records within the Salesforce instance using bulk api.

        Arguments:
        object_api: str: API name of the Salesforce Object for which the records are to be upserted into.

        external_id_field_api: str: API name of the external ID field used for the upsert operation.

        record_dataframe: pd.DataFrame: A pandas dataframe object containing the External column (case sensitive)
            and additional columns matching the Salesforce field api names.

        Returns:
        result: pd.DataFrame: A pandas dataframe with the following columns:
            success: boolean: indicates whether the upsert request was successful
            created: boolean: this value should always be False in a upsert request
            id: object[str]: this value typically is None in a upsert request
            statusCode: object[str] - Optional: the error code of the upsert operation if failed
            message: object[str] - Optional: the error message of the upsert operation if failed
            fields: object[List[str]] - Optional: the fields for which the error code and message applies to.

        Raises:
            RequiredValuesNotProvidedDuringUpsert
            SalesforceMalformedRequest
        """

        field_metadata = self.field_describe([object_api], ['name', 'type', 'length','externalId'])

        if ((object_api is None) or 
        (len(record_dataframe) == 0) or 
        # record_dataframe.columns.__contains__('Id') == False or
        # checks whether any of the columns in the dataframe passed in are not valid field API names
        ~record_dataframe.columns.isin(field_metadata[object_api]).all()
         or external_id_field_api==""
        ):
            raise RequiredValuesNotProvidedDuringUpsert()
        else:
            result = getattr(self.sf.bulk, object_api).upsert(record_dataframe.to_dict('records'), external_id_field_api)
            result = pd.DataFrame(result)
            result = unpack_column(result, "errors")

        return pd.DataFrame(result)

    def extract_bulk(self, og_query: str, 
                        excludedFields: Optional[List] = []) -> pd.DataFrame:
        """
        Uses a standard SOQL query to extract Salesforce Data and outputs a pandas dataframe
        
        Dependencies:
            import re
            import time
            import json
            from salesforce_bulk.util import IteratorBytesIO
            import pandas as pd
        
        """
        objectName = re.search(self._REGEX_PARSE_SOQL_OBJECT, og_query.lower()).group(0)
        successful = False
        
        extracted_object = pd.DataFrame()
        # replaces "*" in query with all fields on object
        sfSchema = getattr(self.sf, objectName).describe().get('fields')

        schemaDict = {}
        for x in sfSchema:
            schemaDict[x['name']] = x

        while not successful:
            try:
                results = []
                for field in schemaDict:
                    if (schemaDict[field]['type'] != 'location' and 
                        schemaDict[field]['type'] != 'address' and 
                        schemaDict[field]['name'] not in excludedFields):
                        results.append(field)
                query = og_query.replace("*", ", ".join(results))
                
#                 # if the object has 0 records in Salesforce, return empty dataframe
#                 if objectName not in self.record_count_caseinsensitive.keys():
#                     return pd.DataFrame(columns=results)
                    
                job = self.bulk.create_query_job(objectName, contentType='JSON')
                batch = self.bulk.query(job, query)
                while not self.bulk.is_batch_done(batch):
                    time.sleep(1)
                sfdf = pd.DataFrame()
                for result in self.bulk.get_all_results_for_query_batch(batch):
                    result = json.load(IteratorBytesIO(result))
                    sfdf = sfdf.append(pd.DataFrame(result))

                # drops attributes column in dataframe
                sfdf.drop(columns="attributes", inplace = True)

                # formats all datetime to the proper formatting
                for column in sfdf:
                    if schemaDict[column]['type'] == 'datetime':
                        sfdf[column] = pd.to_datetime(sfdf[column], unit='ms')
                    # if the column has a 'scale' or salesforce's decimal places, then turn the column into an int
                    elif schemaDict[column]['type'] == 'double' and schemaDict[column]['scale'] == 0:
                        sfdf[column] = pd.to_numeric(sfdf[column], downcast='integer')

            #                         pd.to_datetime(sfdf[column], unit = 's')
            #                         sfdf[column].apply(lambda x : datetime.fromtimestamp(int(x), tz).isoformat())
            #                 sfdf.convert_dtypes()
                # converts the output of the bulk query to text so that the unix timestamp displays property, and fills and empty values with the '' string.
                sfdf = sfdf.fillna('').astype(str)
                successful = True
            except KeyError:
                if self.debug:
                    print(objectName + ' skipped. (Potentially due to no records found.)')
                    
                return pd.DataFrame(columns=results)
            except Exception as badfield:
                field_exclusion = badfield.state_message[badfield.state_message.find("No such column '")+\
                    16:badfield.state_message.find("No such column '")+16+\
                        badfield.state_message[badfield.state_message.find("No such column '")+16:].find("'")]
                excludedFields.append(field_exclusion)
                print("Excluded unqueriable field: " + field_exclusion)
                if og_query.find("*") == -1:
                    raise Exception(f"Unqueriable field {field_exclusion} found in query.")
                else:
                    continue
        if self.debug:
            print("Extracted " + objectName + " successfully!")
        return sfdf

    def join(self, 
                dataframe, 
                rt_dataframe, 
                left_on="", 
                right_on="", 
                new_columns=[], 
                suffix = "_new"):
        """
        Joins and appends the Name and DeveloperName columns of record type to the dataframe.
        The dataframe must contain a column named "RecordTypeId" with the 18 digit SFID of the record type.
        """
        df_columns = dataframe.columns.to_list()
        if right_on not in new_columns:
            new_columns.insert(0,right_on)
        dataframe = pd.merge(dataframe, rt_dataframe[new_columns], how = 'inner', 
                                left_on = left_on,right_on = right_on, suffixes=('', suffix))
#         dataframe.drop([col for col in dataframe.columns if 'drop' in col], axis=1, inplace=True)
        return dataframe

    def object_describe(self, sobject_api_name: str, export_excel: bool=False):
        """

        """
        sfSchema = getattr(self.sf, sobject_api_name).describe()
        boolMetadata = {}
        nonetypeMetadata = {}
        strMetadata = {}
        orderedDictMetadata = pd.Series(dtype='object')
        childRelationshipsPD = pd.DataFrame()
        recordTypeInfosPD = pd.DataFrame()
        fieldsPD = pd.DataFrame()
        supportedScopesPD = pd.DataFrame()
        namedLayoutInfosPD = pd.DataFrame()
        actionOverridesPD = pd.DataFrame()

        for metadata in sfSchema:
            ## Processes all metadata that would return a boolean datatype
            if type(sfSchema[metadata]) is bool:
                boolMetadata[metadata] = sfSchema[metadata]

            ## Processes all metadata that would return a NoneType datatype
            elif type(sfSchema[metadata]) == type(None):
                nonetypeMetadata[metadata] = sfSchema[metadata]

            ## Processes all metadata that would return a string datatype
            elif type(sfSchema[metadata]) is str:
                strMetadata[metadata] = sfSchema[metadata]
            ## Processes all metadata that would return an OrderedDict data type
            elif type(sfSchema[metadata]) is OrderedDict and len(sfSchema[metadata]) != 0:
                orderedDictMetadata = pd.concat([orderedDictMetadata,pd.Series(sfSchema['urls'])])
            elif type(sfSchema[metadata]) is OrderedDict and len(sfSchema[metadata]) == 0:
                nonetypeMetadata[metadata] = "None"

            ## Processes all metadata that would return a list data type
            elif type(sfSchema[metadata]) is list and len(sfSchema[metadata]) != 0:
                if metadata == 'childRelationships':
                    childRelationshipsPD = pd.DataFrame(sfSchema['childRelationships'], index = pd.DataFrame(sfSchema['childRelationships'])['field'])
                    childRelationshipsPD = childRelationshipsPD.drop('field', axis=1).T
                if metadata == 'recordTypeInfos':
                    recordTypeInfosPD = pd.DataFrame(sfSchema['recordTypeInfos'], index = pd.DataFrame(sfSchema['recordTypeInfos'])['name'])
                    recordTypeInfosPD = recordTypeInfosPD.drop('name', axis = 1).T  
                if metadata == 'fields':
                    fieldsPD = pd.DataFrame(sfSchema['fields'], index = pd.DataFrame(sfSchema['fields'])['name'])
                    fieldsPD = fieldsPD.drop('name', axis = 1).T
                if metadata == 'supportedScopes':
                    supportedScopesPD = pd.DataFrame(sfSchema['supportedScopes'], index = pd.DataFrame(sfSchema['supportedScopes'])['name'])
                    supportedScopesPD = supportedScopesPD.drop('name', axis = 1).T
                if metadata == 'actionOverrides':
                    actionOverridesPD = pd.DataFrame(sfSchema['actionOverrides'], index = pd.DataFrame(sfSchema['actionOverrides'])['name'])
                    actionOverridesPD = actionOverridesPD.drop('name', axis = 1).T
                if metadata == 'namedLayoutInfos':
                    namedLayoutInfosPD = pd.DataFrame(sfSchema['namedLayoutInfos'], index = pd.DataFrame(sfSchema['namedLayoutInfos'])['name'])
                    namedLayoutInfosPD = namedLayoutInfosPD.drop('name', axis = 1).T
            ## Parses all empty list metadata
            elif type(sfSchema[metadata]) is list and len(sfSchema[metadata]) == 0:
                nonetypeMetadata[metadata] = "None"
            else:
                nonetypeMetadata[metadata] = "Unrecognized metadata type: " + metadata

        output = {'metadata': pd.concat([pd.Series(nonetypeMetadata),
                    pd.Series(boolMetadata),
                    pd.Series(strMetadata),
                    orderedDictMetadata]),
                    'childRelationships': childRelationshipsPD if len(childRelationshipsPD)!=0 else None,
                    'recordTypeInfos': recordTypeInfosPD if len(recordTypeInfosPD)!=0 else None,
                    'fields': fieldsPD if len(fieldsPD)!=0 else None,
                    'supportedScopes': supportedScopesPD if len(supportedScopesPD)!=0 else None, 
                    'namedLayoutInfos': namedLayoutInfosPD if len(namedLayoutInfosPD)!=0 else None,
                    'actionOverrides': actionOverridesPD if len(actionOverridesPD)!=0 else None}
        if export_excel:
            with pd.ExcelWriter(sobject_api_name + ' describe output.xlsx') as writer:  
                for key in output.keys():
                    try:
                        pd.DataFrame(output[key]).to_excel(writer, sheet_name=key)
                    except:
                        continue

        return output

    def field_describe(self, objects: List = ['Account','Address_vod__c','Child_Account_vod__c'], 
    attributes: List = ['name','type','length']) -> pd.DataFrame:
        """
        TODO:
        
        Description of what it does
        
        Description of arguments and data types
        
        Description of return values and data types
        
        Description of Errors raised
        
        Extra Notes and Examples of Usage
        """
        outputList = []
        columnNames = []
        for sObjectAPIName in objects:
            for attribute in attributes:
                outputList.append([field[attribute] for field in getattr(self.sf, sObjectAPIName).describe()['fields']])
                if attribute == "name":
                    columnNames.append(sObjectAPIName)
                else:
                    columnNames.append(attribute.title())
        field_describe = pd.DataFrame(outputList).transpose()
        field_describe.columns = columnNames
        return field_describe

    def picklist_dataframe_stacked(self,objects: List =['Account','Address_vod__c','Child_Account_vod__c']) -> pd.DataFrame:
        """
        TODO:
        
        Description of what it does
        
        Description of arguments and data types
        
        Description of return values and data types
        
        Description of Errors raised
        
        Extra Notes and Examples of Usage
        """
        output_df = pd.DataFrame()
        for object in objects:
            objectDescribe = getattr(self.sf, object).describe()
            processing_df = pd.DataFrame(pd.DataFrame([pd.Series(data = [picklist['value'] for picklist in field['picklistValues']], 
                                                                   name = object + "." + field["name"]) for field in objectDescribe['fields'] if field['type'] == 'picklist']).stack())
            processing_df.columns = ['Picklist API Value']
            processing_df['CRM Object and Field API'] = processing_df.index.get_level_values(0)
            processing_df[['CRM Object API','CRM Field API']] = processing_df['CRM Object and Field API'].str.split(".", expand = True)
            processing_df.reset_index(drop=True, inplace=True)
            output_df = output_df.append(processing_df)
        return output_df

    def picklist_dataframe(self,objects = ['Account','Address_vod__c','Child_Account_vod__c']) -> List:
        """
        TODO:
        
        Description of what it does
        
        Description of arguments and data types
        
        Description of return values and data types
        
        Description of Errors raised
        
        Extra Notes and Examples of Usage
        """
        referenceList = []
        for object in objects:
            objectDescribe = getattr(self.sf, object).describe()
            objectPicklistValues = pd.DataFrame(index=range(0,max(len(field["picklistValues"]) for field in objectDescribe['fields'] if field['type'] == 'picklist')))
            for x in [pd.Series(data = [picklist['value'] for picklist in field['picklistValues']], name = object + "." + field["name"]) for field in objectDescribe['fields'] if field['type'] == 'picklist']:
                objectPicklistValues.insert(0, str(x.name), x)
            referenceList.append(objectPicklistValues)
        return referenceList

    def record_type_retrieval(self, objectAPIName, fieldAPINames = ["Id","Name",'SobjectType']):
        """
        TODO:
        
        Description of what it does
        
        Description of arguments and data types
        
        Description of return values and data types
        
        Description of Errors raised
        
        Extra Notes and Examples of Usage
        """
        sfRTDF = pd.DataFrame(self.sf.query("SELECT "+ ",".join(fieldAPINames) + " from RecordType WHERE SobjectType = '" + objectAPIName + "'")['records'])
        sfRTDF.drop(columns="attributes", inplace = True)
        return sfRTDF

    
    @serialze_zeep
    def metadata_read(self, metadata_type: str, fullName: str):
        return getattr(self.sf.mdapi, metadata_type).read(fullName)

    def metadata_delete(self, metadata_type: str, fullName: str):
        return getattr(self.sf.mdapi, metadata_type).delete(fullName)

    def metadata_update(self, metadata_type: str, parsed_metadata: dict):
        mdapi_object = getattr(self.sf.mdapi, metadata_type)()
        for key in parsed_metadata:
            setattr(mdapi_object, key, parsed_metadata[key])
        getattr(self.sf.mdapi, metadata_type).update(mdapi_object)
        return mdapi_object

    def metadata_create(self, metadata_type: str, parsed_metadata: dict):
        mdapi_object = getattr(self.sf.mdapi, metadata_type)()
        for key in parsed_metadata:
            setattr(mdapi_object, key, parsed_metadata[key])
        getattr(self.sf.mdapi, metadata_type).create(mdapi_object)
        return mdapi_object

    def metadata_list(self, metadata_type: str) -> list:
        query = self.sf.mdapi.ListMetadataQuery(type=metadata_type)
        query_response = self.sf.mdapi.list_metadata(query)
        return query_response
    
    def metadata_rename(self, metadata_type: str, previous_name: str, new_name: str): 
        """
        Renames the API name of SFDC metadata
        """
        getattr(self.sf.mdapi, metadata_type).rename(previous_name, new_name)
    


    def sf_api_call(self, action, parameters = {}, method = 'get', data = {}):
        """
        Helper function to make calls to Salesforce REST API.
        Parameters: action (the URL), URL params, method (get, post or patch), data for POST/PATCH.
        """
        headers = {
            'Content-type': 'application/json',
            'Accept-Encoding': 'gzip',
            'Authorization': 'Bearer %s' % self.session_id
        }
        if method == 'get':
            r = requests.request(method, 'https://'+self.instance+action, headers=headers, params=parameters, timeout=30)
        elif method in ['post', 'patch']:
            r = requests.request(method, 'https://'+self.instance+action, headers=headers, json=data, params=parameters, timeout=10)
        else:
            # other methods not implemented in this example
            raise ValueError('Method should be get or post or patch.')
#         print('Debug: API %s call: %s' % (method, r.url) )
        if r.status_code < 300:
            if method=='patch':
                return None
            else:
                return r.json()
        else:
            raise Exception('API error when calling %s : %s' % (r.url, r.content))
    