import os
from zipfile import ZipFile
from yaml import load
import requests
import boto3
from requests_aws4auth import AWS4Auth
from collector.domain_config import DomainConfig
import collector


def get_domain_endpoint(region, domain):
    es_client = boto3.client('es', region_name=region)
    response = es_client.describe_elasticsearch_domain(DomainName=domain)
    domain_status = response['DomainStatus']
    endpoint = domain_status.get("Endpoint")
    if endpoint:
        return endpoint

    return domain_status['Endpoints']['vpc']


def list_domains(region):
    es_client = boto3.client('es', region_name=region)
    domains = es_client.list_domain_names()
    print("Domain List:")
    for d in domains.get("DomainNames"):
        print(d)


def get_auth(region,is_fgac,is_iam,user,password):
    if is_fgac is False:
        return None
    credentials = boto3.Session().get_credentials()
    boto3_session = boto3.session.Session()
    if region is None:
        region = boto3_session.region_name
    service = 'es'
    if is_iam is True:
        print("Auth is IAM")
        auth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service,
                        session_token=credentials.token)
    else:
        print("Auth is Internal Database")
        auth = (user, password)
    return auth


def run_actions(region, domain, endpoint, auth,output_dir):
    try:
        from yaml import CLoader as Loader, CDumper as Dumper
    except ImportError:
        from yaml import Loader, Dumper
    config_file = os.path.join(collector.__path__[0],"action_config.yml")
    with open(config_file) as f:
        config = load(f,Loader=Loader)
        #print(config)
    for action in config:
        print("action:" + action + ":" + config[action]["cmd_type"] + ":" + config[action]["cmd"] + "->" + config[action]["file"])
        if(config[action]["cmd_type"] == "rest"):
            URL = "https://" + endpoint + config[action]["cmd"]
            response = requests.get(URL, auth=auth)
            status_code = response.status_code
            no_shard_assigned = "unable to find any unassigned shards to explain" in response.text
            invalid_hot_request = "Invalid index name [_hot], must not start with" in response.text
            invalid_warm_Request = "Invalid index name [_warm], must not start with" in response.text
            if status_code == 200:
                with open(output_dir + "/" + config[action]["file"], "w") as dest:
                    dest.write(response.text)
            elif no_shard_assigned or invalid_hot_request or invalid_warm_Request:
                print("ignore one request")
            else:
                print("ERROR when collecting metadata: " + response.text)
                exit(1)
        elif(config[action]["cmd_type"] == "method"):
            obj = DomainConfig()
            func = getattr(obj, config[action]["cmd"],"invalid config for method call")
            #func = getattr(collector.elasticsearch_data_collector, config[action]["cmd"], "invalid config for method call")
            if callable(func):
                if (config[action]["need_params"]):
                    out = func(region, domain)
                else:
                    out = func()
            with open(output_dir + "/" + config[action]["file"], "w") as dest:
                dest.write(str(out))
        else:
            print("invalid cmd type for " + action)

    collect_index_data(endpoint, auth, output_dir)

def collect_index_data(endpoint, auth,output_dir):
    os.mkdir(output_dir + "/index_settings")
    URL = "https://" + endpoint + "/_cat/indices?bytes=b&h=index"
    response = requests.get(URL, auth=auth)
    for index_name in response.text.splitlines():
        if index_name.startswith("."):
            continue
        print("index: " + index_name)
        URL = "https://" + endpoint + "/" + index_name + "/_settings"
        response = requests.get(URL, auth=auth)
        with open(output_dir + "/index_settings/" + index_name + ".json", "w") as dest:
            dest.write(response.text)

def archive_files(output_dir):
    compressed_files = output_dir + ".zip"
    parent_folder = os.path.dirname(output_dir)
    with ZipFile(compressed_files, 'w') as zipObj:
        for folderName, subfolders, filenames in os.walk(output_dir):
            for filename in subfolders:
                absolute_path = os.path.join(folderName, filename)
                relative_path = absolute_path.replace(parent_folder + '\\','')
                print("Adding '%s' to archive." % absolute_path)
                zipObj.write(absolute_path, relative_path)
            for filename in filenames:
                absolute_path = os.path.join(folderName, filename)
                relative_path = absolute_path.replace(parent_folder + '\\','')
                print("Adding '%s' to archive." % absolute_path)
                zipObj.write(absolute_path, relative_path)
    print("Completed Elasticsearch Metadata collection. Please send " + compressed_files + " to AWS team.")


def collect_data(region,domain,is_fgac,is_iam,user,password,output_dir):
    endpoint = get_domain_endpoint(region, domain)
    print("endpoint:" + endpoint)
    auth=get_auth(region, is_fgac,is_iam,user,password)
    run_actions(region, domain, endpoint,auth,output_dir)
