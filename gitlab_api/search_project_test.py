#!/usr/bin/env python3

import sys
import yaml
import gitlab


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
        group_name = config['group_name']
        project_name = config['project_name']

    gl = gitlab.Gitlab(url=url, private_token=private_token)
    project_id = None
    try:
        for item in gl.search(gitlab.const.SEARCH_SCOPE_PROJECTS, project_name):
            if item['namespace']['full_path'] == group_name and item['name'] == project_name:
                project_id = item['id']
                break
    except Exception as e:
        print(e)

    if project_id is not None:
        project = gl.projects.get(project_id)
        print(project)
