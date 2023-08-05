import boto3
import collector

class DomainConfig:
    def filter_domain_config(self,domain_config):
        for k, v in domain_config.items():
            if ("Date" in k):
                domain_config[k] = str(v)
            elif isinstance(v, dict):
                self.filter_domain_config(v)
        return domain_config

    def domain_config(self, region, domain_name):
        es_client = boto3.client('es', region_name=region)
        response = es_client.describe_elasticsearch_domain_config(DomainName=domain_name)
        filter_config = self.filter_domain_config(response['DomainConfig'])
        return filter_config


    def script_version(self):
        return collector.__version__