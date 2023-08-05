class RequiredValuesNotProvidedDuringCreate(Exception):
    """Exception raised when the required values are not provided to the
    salesforce.create() function.

    Required Values:
        object_api: str -- The Object API name of the table to be inserted to in Salesforce.
        record_dataframe: pd.DataFrame() -- a DataFrame of the records to be inserted, including required fields are available
    """

    def __init__(self, message="Required parameters missing on create. An object_api and the record_dataframe must be provided"):
        self.message = message
        super().__init__(self.message)

class RequiredValuesNotProvidedDuringDelete(Exception):
    """Exception raised when the required values are not provided to the
    salesforce.delete() function.

    Required Values:
        object_api: str -- The Object API name of the table to be upserted to in Salesforce.
        record_dataframe: pd.DataFrame() -- a DataFrame of the records to be deleted. 
            The provided DataFrame must contain the "Id" column (Case sensitive)

    """

    def __init__(self, message="Required parameters missing on delete. \
        An object_api and the record_dataframe must be provided or the Id column missing in the provided dataframe."):
        self.message = message
        super().__init__(self.message)

class RequiredValuesNotProvidedDuringUpdate(Exception):
    """Exception raised when the required values are not provided to the
    salesforce.update() function.

    Required Values:
        object_api: str -- The Object API name of the table to be updated to in Salesforce.
        record_dataframe: pd.DataFrame() -- a DataFrame of the records to be updated. 
            The provided DataFrame must contain the "Id" column (Case sensitive)

    """

    def __init__(self, message="Required parameters missing on update. \
        An object_api and the record_dataframe must be provided or the Id column missing in the provided dataframe \
            or dataframe column names do not match a valid Salesforce field API name."):
        self.message = message
        super().__init__(self.message)

class RequiredValuesNotProvidedDuringUpsert(Exception):
    """Exception raised when the required values are not provided to the
    salesforce.upsert() function.

    Required Values:
        object_api: str -- The Object API name of the table to be upserted to in Salesforce.
        record_dataframe: pd.DataFrame() -- a DataFrame of the records to be upserted. 
            The provided DataFrame must contain the API name of an external ID column.

    """

    def __init__(self, message="Required parameters missing on upserted. \
        An object_api and the record_dataframe must be provided or and external ID column missing in the provided dataframe \
            or dataframe column names do not match a valid Salesforce field API name."):
        self.message = message
        super().__init__(self.message)

class RequiredFieldMissingDuringCreate(Exception):
    """Exception raised when the required fields are not provided to the
    salesforce.create() function.
    """
    def __init__(self, message="Required fields missing on create. Check your Salesforce datamodel to ensure all required fields are provided"):
        self.message = message
        super().__init__(self.message)

