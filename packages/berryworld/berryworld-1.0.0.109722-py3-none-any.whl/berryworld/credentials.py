from decouple import config as conf
from decouple import UndefinedValueError


class SQLCredentials:
    def __init__(self, db_name, config=conf, server_type=None):
        self.db_name = db_name
        self.config = config
        self.server_type = server_type

    def simple_creds(self):
        if self.server_type is None:
            raise ValueError("Please provide a value for server_type")

        try:
            server_name = self.config("SQL_" + self.db_name.upper() + '_' + self.server_type.upper())
            db_name = self.config("SQL_" + self.db_name.upper() + '_DB_NAME')
            user_name = self.config("SQL_" + self.db_name.upper() + '_USER_NAME')
            password = self.config("SQL_" + self.db_name.upper() + '_PASSWORD')

            return {'server_name': server_name,
                    'db_name': db_name,
                    'user_name': user_name,
                    'password': password}
        except UndefinedValueError as e:
            raise UndefinedValueError("Variable %s not found" % str(e))

    def all_creds(self):
        try:
            prod_ = self.config("SQL_" + self.db_name.upper() + '_PROD')
            test_ = self.config("SQL_" + self.db_name.upper() + '_TEST')
            try:
                dev_ = self.config("SQL_" + self.db_name.upper() + '_DEV')
            except Exception as e:
                print(e)
                dev_ = None
            db_name = self.config("SQL_" + self.db_name.upper() + '_DB_NAME')
            user_name = self.config("SQL_" + self.db_name.upper() + '_USER_NAME')
            password = self.config("SQL_" + self.db_name.upper() + '_PASSWORD')

            creds = {'prod': prod_,
                     'test': test_,
                     'db_name': db_name,
                     'user_name': user_name,
                     'password': password}

            if dev_ is not None:
                creds.update({'dev': dev_})
            return creds

        except UndefinedValueError as e:
            raise UndefinedValueError("Variable %s not found" % str(e))


class PostgresCredentials:
    def __init__(self, db_name, config=conf, server_type=None, local=False):
        self.db_name = db_name
        self.config = config
        self.server_type = server_type
        self.local = local

    def simple_creds(self):
        if self.server_type is None:
            raise ValueError("Please provide a value for server_type")

        try:
            if self.local:
                server_name = self.config(
                    "POSTGRESQL_" + self.db_name.upper() + '_' + self.server_type.upper() + '_LOCAL_SERVER_NAME')
                db_name = self.config(
                    "POSTGRESQL_" + self.db_name.upper() + '_' + self.server_type.upper() + '_LOCAL_DB_NAME')
                user_name = self.config(
                    "POSTGRESQL_" + self.db_name.upper() + '_' + self.server_type.upper() + '_LOCAL_USER_NAME')
                password = self.config(
                    "POSTGRESQL_" + self.db_name.upper() + '_' + self.server_type.upper() + '_LOCAL_PASSWORD')
            else:
                server_name = self.config(
                    "POSTGRESQL_" + self.db_name.upper() + '_' + self.server_type.upper() + '_SERVER_NAME')
                db_name = self.config(
                    "POSTGRESQL_" + self.db_name.upper() + '_' + self.server_type.upper() + '_DB_NAME')
                user_name = self.config(
                    "POSTGRESQL_" + self.db_name.upper() + '_' + self.server_type.upper() + '_USER_NAME')
                password = self.config(
                    "POSTGRESQL_" + self.db_name.upper() + '_' + self.server_type.upper() + '_PASSWORD')

            return {'server_name': server_name,
                    'db_name': db_name,
                    'user_name': user_name,
                    'password': password}
        except UndefinedValueError as e:
            raise UndefinedValueError("Variable %s not found" % str(e))


class BCCredentials:
    def __init__(self, config=conf, db_name=None, auth=False):
        self.config = config
        self.db_name = db_name
        self.auth = auth

    def simple_creds(self):
        try:
            if self.auth:
                scope = self.config("BC_AUTH_SCOPE")
                client_id = self.config("BC_AUTH_CLIENT_ID")
                client_secret = self.config("BC_AUTH_CLIENT_SECRET")

                return {'scope': scope,
                        'client_id': client_id,
                        'client_secret': client_secret}
            elif self.db_name is not None:
                server_type = self.config(f"BC_ENV_SERVER_{self.db_name.upper()}")

                return {'server_type': server_type}
            else:
                raise ValueError("Please provide a valid input")

        except UndefinedValueError as e:
            raise UndefinedValueError("Variable %s not found" % str(e))


class CDSCredentials:
    def __init__(self, env_name, config=conf, webhook=False, auth=False):
        self.config = config
        self.env_name = env_name
        self.webhook = webhook
        self.auth = auth

    def simple_creds(self):
        try:
            if self.auth:
                scope = self.config("CDS_AUTH_SCOPE")
                client_id = self.config("CDS_AUTH_CLIENT_ID")
                client_secret = self.config("CDS_AUTH_CLIENT_SECRET")

                return {'scope': scope,
                        'client_id': client_id,
                        'client_secret': client_secret}
            else:
                server = self.config(f"CDS_ENV_SERVER_{self.env_name.upper()}")
                organisation_id = self.config(f"CDS_ENV_ORG_{self.env_name.upper()}")
                environment_prefix = self.config(f"CDS_ENV_PREFIX_{self.env_name.upper()}")
                environment_url = self.config(f"CDS_ENV_URL_{self.env_name.upper()}")
                if self.webhook:
                    environment_name = self.config(f"CDS_ENV_NAME_{self.env_name.upper()}")
                else:
                    environment_name = self.env_name

                return {'server': server,
                        'environment_name': environment_name,
                        'organisation_id': organisation_id,
                        'environment_prefix': environment_prefix,
                        'environment_url': environment_url}

        except UndefinedValueError as e:
            raise UndefinedValueError("Variable %s not found" % str(e))

