#!/usr/bin/env python3

import sys
import yaml
import xmltodict
from jenkins import Jenkins

def update_dictionary(dictionary, key, value):
    for k, v in dictionary.items():
        if k == key:
            dictionary[k] = value
            return dictionary
        if isinstance(v, dict):
            dictionary[k] = update_dictionary(v, key, value)
    return dictionary

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: " + sys.argv[0] + " <yaml_config>")
        print(" example: " + sys.argv[0] + " config.yml")
        sys.exit(0)
        
    yaml_config = sys.argv[1]
    with open(yaml_config, 'r') as f:
        data = f.read()
        config = yaml.load(data, Loader=yaml.FullLoader)
        protocol = config['protocol']
        host = config['host']
        user = config['user']
        token = config['token']
        project = config['project']
        git_repository = config['git_repository']
        template_project = config['template_project']
        
    url = protocol + "://" + user + ":" + token + "@" + host
    j = Jenkins(url)
    if not j.job_exists(project):
        try:
            j.copy_job(template_project, project)
            job_config = j.get_job_config(project)
            d = xmltodict.parse(job_config)
            d = update_dictionary(d, 'remote', git_repository)
            j.reconfig_job(project, xmltodict.unparse(d))
        except Exception as e:
            print("copy job failure, {}".format(e))
            sys.exit(1)
    else:
        print("job already exists")
        sys.exit(0)
    print("copy job success")