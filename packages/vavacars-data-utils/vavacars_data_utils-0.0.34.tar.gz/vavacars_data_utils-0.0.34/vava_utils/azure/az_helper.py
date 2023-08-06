import logging
import re

from azureml.core import Environment, Dataset, Workspace
from azureml.core.model import InferenceConfig
from azureml.core.webservice import AciWebservice, LocalWebservice, Webservice
from azureml.core.authentication import ServicePrincipalAuthentication
from azureml.core.model import Model
from azureml.data.datapath import DataPath

from vava_utils.utils.singleton import singleton


@singleton
class Az_Helper:
    
    def __init__(self, config):
        """
        Azure helper constructor.

        Parameters:
            config: dictionary with the following keys for Azure authentication and setting up Workspace.
                - tenant_id
                - service_principal_id
                - service_principal_password
                - subscription_id
                - resource_group
                - workspace_name
        """
        self.auth = ServicePrincipalAuthentication(
            tenant_id=config["tenant_id"],
            service_principal_id=config["service_principal_id"],
            service_principal_password=config["service_principal_password"],
        )
        self.ws = Workspace(
            subscription_id=config["subscription_id"],
            resource_group=config["resource_group"],
            workspace_name=config["workspace"],
            auth=self.auth,
        )

    def register_model(self, path, name, include_version=True, **kwargs):
        """
        Register a new model version in Azure ML

        Args:
            path (str): local model file path
            name (str): model name
            include_version (boolean): True to include model version as model.properties parameter

        Returns:
            Model: Azure Model instance
        """
        if include_version:
            version = 1 if name not in self.ws.models else self.ws.models[name].version + 1
            properties = kwargs.pop("properties", {})
            properties['version'] = version
        else:
            properties = kwargs.pop("properties", {})

        return Model.register(model_path=path, model_name=name, workspace=self.ws, properties=properties, **kwargs)

    def get_model(self, name, version='latest'):
        """
        Returns an Azure ML Model instance with an option to filter an specific version found in model.properties.

        Args:
            name (str): model name
            version (str): Model version number, this is a custom version that should be under model.properties 
                           and not the azure model version. Defaults to 'latest', takes latest model on Azure.

        Returns:
            Model: Azure Model instance
        """
        
        if name not in self.ws.models:
            raise ValueError(f'Model {name} not found in workspace={self.ws.name}')
        
        if version == 'latest':
            return Model(name=name, workspace=self.ws)
        else:
            all_model_versions = Model.list(self.ws, name=name)
            matching_models = [mv for mv in all_model_versions if mv.properties.get('version', None) == str(version)]
            if len(matching_models) > 0:
                return matching_models[0]
            else:
                raise ValueError(f'Not found model {name} with properties={{version: {version}}}')

    def download_model(self, name, version='latest', path='.', exist_ok=False):
        """
        Download model file from a registered Azure ML Model

        Args:
            name (str): remote model name
            path (str): local path to download model, default is '.'
            version (str): Model version number, this is a custom version that should be under model.properties 
                           and not the azure model version. Defaults to 'latest', takes latest model on Azure.
        """
        return self.get_model(name, version).download(path, exist_ok)

    def deploy_endpoint(self, deploy_cfg, update=False, local=False):
        """
        Deploy Azure ML endpoint

        Args:
            deploy_cfg (dict): Dictionary with deployment config parameters.
                - name (str): endpoint name
                - models (list(str)): list of model names used in the endpoint
                - inference: InferenceConfig class parameters
                    - source_directory (str): local directoy with all required files (include dependencies)
                    - entry_script (str): entrypoint script
                - environment: Environment clas paramenters
                    - name (str): environment name
                    - python_packages list(str): list of required python packages
                - deploy: Webservice.deploy_configuration parameters
                    - cpu_cores (int)
                    - memory_gb (int)
                    - auth_enabled (bool)
                - local: Only when local=True, LocalWebservice.deploy_configuration parameters
                    port (int):
            update (bool, optional): True if updating a previously created Endpoint. Defaults to False.
            local (bool, optional): Deploy as local endpoint. Defaults to False.

        Returns:
            Webservice: instance of Azure Webservice
        """
            
        models = [Model(name=model_name, workspace=self.ws) for model_name in deploy_cfg['models']]
        
        env = Environment(name=deploy_cfg['environment']['name'])
        for package in deploy_cfg['environment']['python_packages']:
            env.python.conda_dependencies.add_pip_package(package)
        inference_config = InferenceConfig(environment=env, **deploy_cfg['inference'])
        
        if update:
            service = AciWebservice(name=deploy_cfg['name'], workspace=self.ws)
            service.update(models=models, inference_config=inference_config)
        else:
            if local:
                deployment_config = LocalWebservice.deploy_configuration(**deploy_cfg['local'])
            else:
                deployment_config = AciWebservice.deploy_configuration(**deploy_cfg['deploy'])
            service = Model.deploy(
                workspace=self.ws,
                name=deploy_cfg['name'],
                models=models,
                inference_config=inference_config,
                deployment_config=deployment_config,
                overwrite=True,
            )
        try:
            service.wait_for_deployment(show_output=True)
            logging.info(f"Completed: {service.state}, see first logs. Key={service.get_keys()}")
            logging.info(f"Endpoint URL: {service.scoring_uri}")
        except Exception as e:
            logging.warn(f"Exception ({e}) when updating endpoint: {service.get_logs()}")

        logging.info(f"Completed, logs: {service.get_logs()}")

        return service

    def ds_sql_query(self, datastore, query, timeout=600):
        """
        Run SQL query against an Azure Datastore - SQL Server.

        Args:
            datastore (str): datastore name
            query (str): sql query string
            timeout (int): query timeout

        Returns:
            pd.DataFrame: query results in DataFrame format. 
        """
        if datastore not in self.ws.datastores:
            ValueError(f'DataStore {datastore} not available in workspace={self.ws.name}')
        ds = self.ws.datastores[datastore]
        datapath = DataPath(ds, query)
        tab = Dataset.Tabular.from_sql_query(datapath, query_timeout=timeout)
        
        return tab.to_pandas_dataframe()

    def ds_sql_table(self, datastore, table, columns=None, **kwargs):
        """
        Load table from Azure Datastore - SQL Server.

        Args:
            datastore (str): datastore name
            table (str): table name

        Returns:
            pd.DataFrame: table in DataFrame format. 
        """
        query = f'SELECT * FROM {table};'
        df = self.ds_sql_query(datastore, query, **kwargs)
        
        return df[columns] if columns else df

    def ds_sql_query_file(self, datastore, filename, query_args={}, limit=None, **kwargs):
        """
        Read SQL query  query against an Azure Datastore - SQL Server.

        Parameters:
            filename (string): path to file containing the SQL query
            query_args (dict): query string is formatted with those params: string.format(**query_args)
                               example: {'max_date': '2020-01-01'}
            limit (int): maximum number of results
            **kwargs: additional keyword parameters passed to self.ds_sql_query

        Returns:
            pd.DataFrame: query results in DataFrame format. 
        """
        
        if (limit is not None) and (not isinstance(limit, int)):
            raise ValueError("Limit must be of type int")

        with open(filename, "r") as f:
            query_unformated = f.read().rstrip()
        query = query_unformated.format(**query_args)
        query = query if not limit else re.sub('^SELECT', f'SELECT TOP({limit})', query)
        
        return self.ds_sql_query(datastore, query, **kwargs)


        