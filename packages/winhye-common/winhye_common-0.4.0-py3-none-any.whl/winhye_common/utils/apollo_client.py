from pyapollos import ApolloClient

__all__ = ["ApolloClientInit"]


class ApolloClientInit:

    def __init__(self, app_id, config_server_url, cluster="default"):
        self.app_id = app_id
        self.config_server_url = config_server_url
        self.cluster = cluster
        self.apollo_client = ApolloClient(app_id=self.app_id, cluster=self.cluster,
                                          config_server_url=self.config_server_url)

    def get_config(self, config_key, namespace="application"):
        return self.apollo_client.get_value(config_key, namespace=namespace)
