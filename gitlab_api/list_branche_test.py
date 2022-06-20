#!/usr/bin/env python3

import sys
import yaml
from gitlab import Gitlab


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: " + sys.argv[0] + " <yaml_config>")
        print(" example: " + sys.argv[0] + " config.yml")
        sys.exit(0)
        
    yaml_config = sys.argv[1]
    with open(yaml_config, 'r') as f:
        data = f.read()
        config = yaml.load(data, Loader=yaml.FullLoader)
        url = config['url']
        private_token = config['private_token']
        project_name = config['project_name']

    gl = Gitlab(url=url, private_token=private_token)
    project = None
    try:
        project = gl.projects.get(project_name)
    except Exception as e:
        print(e)
        
    if project is not None:
        branchs = project.branches.list(all=True)
        for branch in branchs:
            print(branch.name)
