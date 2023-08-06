import requests
import json


class NectarAuth:
    domain = None

    def __init__(self, authusr, authpwd, domain='https://us.nectar.services', tenant='client1'):
        self.domain = domain
        self.tenant = tenant
        self.authusr = authusr
        self.authpwd = authpwd
        self.apiauth = requests.auth.HTTPBasicAuth(self.authusr, self.authpwd)

    def retrieve_credentials(self):
        credentials = {
            "domain": self.domain,
            "tenant": self.tenant,
            "authusr": self.authusr,
            "authpwd": self.authpwd
        }
        return credentials


class GetTenant:
    def value(self, tenant):
        if tenant is None:
            tenant = self.tenant
        return tenant


class UserEndpoints(NectarAuth):
    def __init__(self, domain, tenant, apiauth):
        super().__init__(domain, tenant, apiauth)
        # self.domain = NectarAuth.domain
        # self.tenant = NectarAuth.tenant

    def search_users_by_query_string(self, username, pagesize='10', pagenumber='1', tenant=None):
        tenant = GetTenant.value(self, tenant)
        response = requests.get(self.domain + "/dapi/user/search?tenant=" + tenant + "&pageSize=" + pagesize + "&pageNumber=" + pagenumber + "&q=" + username, auth=self.apiauth)
        return json.loads(response.text)

    def get_user_quantity_summary(self, username, timeperiod, tenant=None):
        tenant = GetTenant.value(self, tenant)
        userid = UserEndpoints.search_users_by_query_string(self, username=username)["elements"][0]["userId"]
        response = requests.get(self.domain + "/dapi/user/" + userid + "/summary/quantity?tenant=" + tenant + "&timePeriod=" + timeperiod, auth=self.apiauth)
        return json.loads(response.text)

    def get_user_quality_summary(self, username, timeperiod, tenant=None):
        tenant = GetTenant.value(self, tenant)
        userid = UserEndpoints.search_users_by_query_string(self, username=username)["elements"][0]["userId"]
        response = requests.get(self.domain + "/dapi/user/" + userid + "/summary/quality?tenant=" + tenant + "&timePeriod=" + timeperiod, auth=self.apiauth)
        return json.loads(response.text)

    def get_user_server_summary(self, username, timeperiod, tenant=None):
        tenant = GetTenant.value(self, tenant)
        userid = UserEndpoints.search_users_by_query_string(self, username=username)["elements"][0]["userId"]
        response = requests.get(self.domain + "/dapi/user/" + userid + "/summary/server?tenant=" + tenant + "&timePeriod=" + timeperiod, auth=self.apiauth)
        return json.loads(response.text)

    def get_user_client_types_summary(self, username, timeperiod, tenant=None):
        tenant = GetTenant.value(self, tenant)
        userid = UserEndpoints.search_users_by_query_string(self, username=username)["elements"][0]["userId"]
        response = requests.get(self.domain + "/dapi/user/" + userid + "/summary/client/types?tenant=" + tenant + "&timePeriod=" + timeperiod, auth=self.apiauth)
        return json.loads(response.text)

    def get_user_devices_summary(self, username, timeperiod, tenant=None):
        tenant = GetTenant.value(self, tenant)
        userid = UserEndpoints.search_users_by_query_string(self, username=username)["elements"][0]["userId"]
        response = requests.get(self.domain + "/dapi/user/" + userid + "/summary/devices?tenant=" + tenant + "&timePeriod=" + timeperiod, auth=self.apiauth)
        return json.loads(response.text)

    def get_user_network_types_summary(self, username, timeperiod, tenant=None):
        tenant = GetTenant.value(self, tenant)
        userid = UserEndpoints.search_users_by_query_string(self, username=username)["elements"][0]["userId"]
        response = requests.get(self.domain + "/dapi/user/" + userid + "/summary/network/types?tenant=" + tenant + "&timePeriod=" + timeperiod, auth=self.apiauth)
        return json.loads(response.text)

    def get_user_info(self, username, tenant=None):
        tenant = GetTenant.value(self, tenant)
        userid = UserEndpoints.search_users_by_query_string(self, username=username)["elements"][0]["userId"]
        response = requests.get(self.domain + "/dapi/user/" + userid + "?tenant=" + tenant, auth=self.apiauth)
        return json.loads(response.text)

    def get_advanced_user_info(self, username, tenant=None):
        tenant = GetTenant.value(self, tenant)
        userid = UserEndpoints.search_users_by_query_string(self, username=username)["elements"][0]["userId"]
        response = requests.get(self.domain + "/dapi/user/" + userid + "/advanced?tenant=" + tenant, auth=self.apiauth)
        return json.loads(response.text)

    def get_user_advanced_info_only_status(self, username, tenant=None):
        tenant = GetTenant.value(self, tenant)
        userid = UserEndpoints.search_users_by_query_string(self, username=username)["elements"][0]["userId"]
        response = requests.get(self.domain + "/dapi/user/" + userid + "/advanced/only?tenant=" + tenant, auth=self.apiauth)
        return json.loads(response.text)

    def get_pinned_users(self, tenant=None):
        tenant = GetTenant.value(self, tenant)
        response = requests.get(self.domain + "/dapi/user/pinned?tenant=" + tenant, auth=self.apiauth)
        return json.loads(response.text)
