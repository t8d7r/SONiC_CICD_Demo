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

#path_sot = local_path+'infra-SOT'
path_sot = '../../infra-SOT'
#path_template = local_path+'/builder/template/'
path_template = '../template/'
hostname = str(sys.argv[1])
if_dict = {}
old_if_dict = {}
l2_to_delete = {}
l3_to_delete = {}
vlan_to_delete = {}
found = False

def load_old_yaml(path):
    process = subprocess.Popen(['git','show','HEAD~1:'+path],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    output = yaml.safe_load(stdout)
    return (output)

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

old_tenants_mapping = load_old_yaml('infra-SOT/tenants_mapping.yaml')
old_tenants = load_old_yaml('infra-SOT/tenants.yaml')
tenants_mapping =  load_yaml_file(path_sot+'/tenants_mapping.yaml')
tenants =  load_yaml_file(path_sot+'/tenants.yaml')
old_if_dict = reverse_mapping(old_tenants_mapping,hostname)
if_dict = reverse_mapping(tenants_mapping,hostname)

if old_tenants_mapping['mapping'] != None and old_tenants_mapping['mapping'][hostname] != None:
    for old_vlan in old_tenants_mapping['mapping'][hostname]:
        found = False
        for vlan in tenants_mapping['mapping'][hostname]:
            if old_vlan['id'] == vlan['id']:
                found = True
        if not found:
            vlan_to_delete[old_vlan['id']] = {}
            vlan_to_delete[old_vlan['id']] = old_tenants['vlans_list'][old_vlan['id']]

if old_if_dict != None:
    for interface in old_if_dict:
        if interface not in if_dict:
            if interface not in l2_to_delete:
                l2_to_delete[interface] = {}
                if 'access' in old_if_dict[interface]:
                    l2_to_delete[interface]['access'] =  old_if_dict[interface]['access']
                if 'tagged' in old_if_dict[interface]:
                    l2_to_delete[interface]['tagged'] =  old_if_dict[interface]['tagged']
        else:
            if 'access' in old_if_dict[interface]:
                for vlan in old_if_dict[interface]['access']:
                    if vlan not in if_dict[interface]['access']:
                        if interface not in l2_to_delete:
                            l2_to_delete[interface] = {}
                            l2_to_delete[interface]['access'] = []
                        l2_to_delete[interface]['access'].append(vlan)
            if 'tagged' in old_if_dict[interface]:
                for vlan in old_if_dict[interface]['tagged']:
                    if vlan not in if_dict[interface]['tagged']:
                        if interface not in l2_to_delete:
                            l2_to_delete[interface] = {}
                            l2_to_delete[interface]['tagged'] = []
                        elif 'tagged' not in l2_to_delete[interface]:
                            l2_to_delete[interface]['tagged'] = []
                        l2_to_delete[interface]['tagged'].append(vlan)

vgf = jinja2.Environment(loader=jinja2.FileSystemLoader(path_template)).get_template('tenant_delete_template.j2').render(inventory_hostname = hostname,vlan_to_delete = vlan_to_delete, l2_to_delete = l2_to_delete)
#with open(local_path+'builder/host_vars/'+hostname+'.yaml','w') as f: f.write(vgf)
with open('../host_vars/DELETE'+hostname+'.yaml','w') as f: f.write(vgf)
#print (vgf)
