from .BaseMicrosoftAPI import BaseMicrosoftAPI

class AzureAPI(BaseMicrosoftAPI):
    def __init__(self, tenant_ID, app_ID, secret_key):
       super().__init__(tenant_ID, app_ID, secret_key,
                        'https://management.core.windows.net/.default')
       self.subscriptions = None
       self.resource_groups = None
       self.servers = None

    def list_subscriptions(self):
        url = 'https://management.azure.com/'\
              'subscriptions?api-version=2020-01-01'
        response = self.call_api(url)
        self.subscriptions = [item['subscriptionId'] for item in response]
        return response

    def subscriptionIds(self):
        subscriptions = self.list_subscriptions()
        return [item['subscriptionId'] for item in subscriptions]

    def list_virtual_networks(self, subscriptions=None):
        if subscriptions is None:
            if self.subscriptions is None:
                self.subscriptions = self.subscriptionIds()
            subscriptions = self.subscriptions
#            subscriptions = self.subscriptionIds()

        virtual_networks = []
        for subscription in subscriptions:
            url = f'https://management.azure.com/subscriptions/{subscription}/'\
                  f'providers/Microsoft.Network/'\
                  f'virtualNetworks?api-version=2021-03-01'
            virtual_networks += self.call_api(url)
        return virtual_networks

    def list_resource_groups(self, subscriptions=None):
        if subscriptions is None:
            if self.subscriptions is None:
                self.subscriptions = self.subscriptionIds()
            subscriptions = self.subscriptions
#            subscriptions = self.subscriptionIds()
        resource_groups = []
        for subscription in subscriptions:
            url = f'https://management.azure.com/subscriptions/{subscription}/'\
                  f'resourcegroups?api-version=2021-04-01'
            resource_groups += self.call_api(url)
        return resource_groups

    def resource_groups_id(self,subscriptions):
        resource_groups = self.list_resource_groups(subscriptions)
        return [item['id'] for item in resource_groups]

    def list_virtual_machines(self, subscriptions=None, status=False):
        if subscriptions is None:
            if self.subscriptions is None:
                self.subscriptions = self.subscriptionIds()
            subscriptions = self.subscriptions
#            subscriptions = self.subscriptionIds()

        virtual_machines = []
        for subscription in subscriptions:
            url = f'https://management.azure.com/subscriptions/{subscription}/'\
                  f'providers/Microsoft.Compute/'\
                  f'virtualMachines?api-version=2021-03-01&statusOnly={status}'
            virtual_machines += self.call_api(url)
        return virtual_machines



    def list_public_ip_addresses(self, subscriptions=None):
        if subscriptions is None:
            if self.subscriptions is None:
                self.subscriptions = self.subscriptionIds()
            subscriptions = self.subscriptions
#            subscriptions = self.subscriptionIds()

        public_ips = []
        for subscription in subscriptions:
            url = f'https://management.azure.com/subscriptions/{subscription}/'\
                  f'providers/Microsoft.Network/'\
                  f'publicIPAddresses?api-version=2021-02-01'
            public_ips += self.call_api(url)
        return public_ips

    def list_locations(self, subscriptions=None):
        if subscriptions is None:
            if self.subscriptions is None:
                self.subscriptions = self.subscriptionIds()
            subscriptions = self.subscriptions
        
        locations = []
        for subscription in subscriptions:
            url = f'https://management.azure.com/subscriptions/{subscription}/'\
                  f'locations?api-version=2020-01-01'
            locations += self.call_api(url)
        return locations

    # Microsoft states this API is deprecated.
    def list_virtual_machine_sizes(self, subscriptions=None, locations=None):
        if subscriptions is None:
            if self.subscriptions is None:
                self.subscriptions = self.subscriptionIds()
            subscriptions = self.subscriptions

        if locations is None:
            locations = self.list_locations()

        sizes = []
        for location in locations:
            subscription = location['subscription']
            location_name = location['location']
            url = f'https://management.azure.com/subscriptions/'\
                  f'{subscription}/providers/Microsoft.Compute/locations/'\
                  f'{location_name}/vmSizes?api-version=2021-07-01'
            result = self.call_api(url)
            if result:
                sizes += result
        return sizes

    def list_network_interfaces(self, subscriptions=None):
        if subscriptions is None:
            if self.subscriptions is None:
                self.subscriptions = self.subscriptionIds()
            subscriptions = self.subscriptions

        net_interfaces = []
        for subscription in subscriptions:
            url = f'https://management.azure.com/subscriptions/{subscription}'\
                  f'/providers/Microsoft.Network/'\
                  f'networkInterfaces?api-version=2021-03-01'
            net_interfaces += self.call_api(url)
        return net_interfaces



    def list_application_gateways(self, subscriptions=None):
        if subscriptions is None:
            if self.subscriptions is None:
                self.subscriptions = self.subscriptionIds()
            subscriptions = self.subscriptions

        app_gateways = []
        for subscription in subscriptions:
            url = f'https://management.azure.com/subscriptions/{subscription}'\
                  f'/providers/Microsoft.Network/'\
                  f'applicationGateways?api-version=2021-05-01'
            app_gateways += self.call_api(url)
        return app_gateways

    def list_databricks_workspaces(self, subscriptions=None):
        if subscriptions is None:
            if self.subscriptions is None:
                self.subscriptions = self.subscriptionIds()
            subscriptions = self.subscriptions

        databricks_workspaces = []
        for subscription in subscriptions:
            url = f'https://management.azure.com/subscriptions/{subscription}'\
                  f'/providers/Microsoft.Databricks/'\
                  f'workspaces?api-version=2018-04-01'
            databricks_workspaces += self.call_api(url)
        return databricks_workspaces

    def list_factories(self, subscriptions=None):
        if subscriptions is None:
            if self.subscriptions is None:
                self.subscriptions = self.subscriptionIds()
            subscriptions = self.subscriptions

        factories = []
        for subscription in subscriptions:
            url = f'https://management.azure.com/subscriptions/{subscription}'\
                  f'/providers/Microsoft.DataFactory/'\
                  f'factories?api-version=2018-06-01'
            factories += self.call_api(url)
        return factories

    def list_mssql_server(self, resource_groups=None):

        if self.subscriptions is None:
            self.subscriptions = self.subscriptionIds()
        subscriptions = self.subscriptions

        if resource_groups is None:
            if self.resource_groups is None:
                self.resource_groups = self.resource_groups_id(subscriptions)
            resource_groups = self.resource_groups

        subs = []
        rgs = []
        for row in resource_groups:
            splited = row.split('/')
            subs.append(splited[2].lower())
            rgs.append(splited[4].lower())

        servers = []
        for i in range(len(subs)):
                url = f'https://management.azure.com/subscriptions/{subs[i]}'\
                    f'/resourceGroups/{rgs[i]}/providers/Microsoft.Sql/'\
                    f'servers?api-version=2021-11-01-preview'
                servers += self.call_api(url)
        return servers

    def servers_ids(self,resource_groups):
        servers = self.list_mssql_server(resource_groups)
        return [item['id'] for item in servers]

    def list_mssql_database(self, servers=None):

        if self.subscriptions is None:
            self.subscriptions = self.subscriptionIds()
        subscriptions = self.subscriptions

        if self.resource_groups is None:
            self.resource_groups = self.resource_groups_id(subscriptions)
        resource_groups = self.resource_groups

        if servers is None:
            if self.servers is None:
                self.servers = self.servers_ids(resource_groups)
            servers = self.servers        

        subs = []
        rgs = []
        server_names = []
        for row in servers:
            splited = row.split('/')
            subs.append(splited[2].lower())
            rgs.append(splited[4].lower())
            server_names.append(splited[8].lower())

        databases = []
        for i in range(len(server_names)):
                    url = f'https://management.azure.com/subscriptions/{subs[i]}'\
                        f'/resourceGroups/{rgs[i]}/providers/Microsoft.Sql/servers/{server_names[i]}/'\
                        f'databases?api-version=2021-11-01-preview'
                    databases += self.call_api(url)
        return databases