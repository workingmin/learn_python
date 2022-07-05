#!/usr/bin/env python3

import sys
import yaml
from jenkins import Jenkins


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
        job = config['job']

    url = protocol + "://" + user + ":" + token + "@" + host
    j = Jenkins(url)
    if j.job_exists(job):
        try:
            j.build_job(job)
        except Exception as e:
            print("build job failure, {}".format(e))
            sys.exit(1)
