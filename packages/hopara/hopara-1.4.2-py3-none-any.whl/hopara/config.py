import os

import toml


class Config:
    def __init__(self):
        self.__config = self.__get_file_config()

    def get_active_env(self) -> str:
        return self.__config.get('default')

    @staticmethod
    def __get_file_config():
        config_path = os.path.join(os.getenv("HOME", ''), '.hopara', 'default.toml')
        if os.path.exists(config_path):
            with open(config_path, 'r') as fp:
                return toml.load(fp)
        return None

    def get_auth_url(self) -> str:
        auth_url = os.getenv("HOPARA_AUTH_URL")
        if auth_url is None and self.__config:
            auth_url = self.__config[self.get_active_env()].get('authEndpoint')
        return auth_url

    def get_dataset_url(self) -> str:
        dataset_url = os.getenv("HOPARA_DATASET_URL")
        if dataset_url is None and self.__config:
            dataset_url = self.__config[self.get_active_env()].get('datasetEndpoint')
        return dataset_url

    def get_email(self) -> str:
        email = os.getenv("HOPARA_EMAIL")
        if email is None and self.__config:
            email = self.__config[self.get_active_env()].get('email')
        return email

    def get_password(self) -> str:
        password = os.getenv("HOPARA_PASSWORD")
        if password is None and self.__config:
            password = self.__config[self.get_active_env()].get('password')
        return password

    @staticmethod
    def get_client_id() -> str:
        return os.getenv("HOPARA_CLIENT_ID")

    @staticmethod
    def get_client_secret() -> str:
        return os.getenv("HOPARA_CLIENT_SECRET")

    def get_credentials(self) -> str:
        client_id, client_secret = self.get_client_id(), self.get_client_secret()
        if client_id and client_secret:
            return {'clientId': client_id, 'clientSecret': client_secret}
        else:
            email, password = self.get_email(), self.get_password()
            if email and password:
                return {'email': email, 'password': password}
        return None


if __name__ == "__main__":
    config = Config()
    print(config.get_dataset_url())
    print(config.get_email())
    print(config.get_client_id())
    print(config.get_client_secret())
    print(config.get_credentials())
