from alas_ce0.common.client_base import EntityClientBase


class BulkClient(EntityClientBase):
    entity_endpoint_base_url = '/management/bulks/'

    def __init__(self, country_code='cl', **kwargs):
        super(BulkClient, self).__init__(**kwargs)
        self.entity_endpoint_base_url += country_code + '/'
        self.headers['Authorization'] = self.headers['Authorization'].replace("\n", "")

    def generate_bulks(self, params):
        return self.http_post_json(self.entity_endpoint_base_url + "_generate-bulks", params)

    def change_status(self, params):
        return self.http_post_json(self.entity_endpoint_base_url + "_change-status", params)

    def ti_controlled_receive(self, code):
        return self.http_post_json(self.entity_endpoint_base_url + "_ti-controlled-receive", code)

    def ser_travelling_receive(self, code):
        return self.http_post_json(self.entity_endpoint_base_url + "_ser-travelling-receive", code)
