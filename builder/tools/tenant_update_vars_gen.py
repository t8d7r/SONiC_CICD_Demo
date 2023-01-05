import sys
import os
import yaml
import subprocess
import jinja2
from jinja2 import Template

process = subprocess.Popen(['pwd'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
local_path, stderr = process.communicate()
local_path = str(local_path)
local_path = (local_path.split("b'",1)[1]).split("SONiC_CICD_Demo/",1)[0]+"SONiC_CICD_Demo/"

path_sot = local_path+'infra-SOT'
path_template = local_path+'/builder/template/'
hostname = str(sys.argv[1])
if_dict = {}
old_if_dict = {}
l2_to_update = {}
l3_to_update = {}
vlan_to_update = {}
found = False

def load_yaml_file(path):
    with open(path, 'r') as stream:
        dict = yaml.safe_load(stream)
    return dict

def reverse_mapping(mapping,hostname):
    idict = {}
    for vlan in mapping['mapping'][hostname]:
        if 'access' in vlan:
            for interface in vlan['access']:
                if not interface in idict:
                    idict[interface] = {}
                    idict[interface]['access'] = []
                if not vlan['id'] in idict[interface]['access']:
                    idict[interface]['access'].append(vlan['id'])
        if 'tagged' in vlan:
            for interface in vlan['tagged']:
                if not interface in idict:
                    idict[interface] = {}
                    idict[interface]['tagged'] = []
                elif interface in idict and 'tagged' not in idict[interface]:
                    idict[interface]['tagged'] = []
                if not vlan['id'] in idict[interface]['tagged']:
                    idict[interface]['tagged'].append(vlan['id'])
    return idict

tenants_mapping =  load_yaml_file(path_sot+'/tenants_mapping.yaml')
tenants =  load_yaml_file(path_sot+'/tenants.yaml')
fabric_model = load_yaml_file(path_sot+'/fabric_modeling.yaml')
if_dict = reverse_mapping(tenants_mapping,hostname)

vgf = jinja2.Environment(loader=jinja2.FileSystemLoader(path_template)).get_template('tenant_update_template.j2').render(inventory_hostname = hostname, if_dict = if_dict, tenants_mapping = tenants_mapping, tenants = tenants, fabric_model = fabric_model)

with open(local_path+'builder/host_vars/'+hostname+'.yaml','w') as f: f.write(vgf)
print (vgf)

