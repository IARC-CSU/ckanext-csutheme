import ckan.logic.schema
import logging 
from ckan.logic.action.get import organization_show

def csu_organization_show(context, data_dict):
    data_dict['include_users'] = False
    data_dict['include_tags'] = True
    logging.warning(' in csu_organization_show get.action')
    return organization_show(context, data_dict)

def csu_package_list(context, data_dict):
	logging.warning(' in csu_package_list get.list')
	return package_list(context, data_dict)