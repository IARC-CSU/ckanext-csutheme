import ckan.plugins as plugins
import ckan.authz as authz
import ckan.plugins.toolkit as toolkit
import ckan.lib.helpers as lib_helpers
import ckanext.csutheme.action.get
# import ckanext.csutheme.controller.dataset
import requests
import json
import logging 
from flask import Flask, Blueprint, url_for
from ckan.lib.mailer import mail_recipient, MailerException
from ckanext.csutheme import validators , controller
from ckan.common import config



app = Flask(__name__)

def site_read(context, data_dict):

    # List of allowed paths, when not logged in
    #allowed_anon_paths = ['/user/login']

    # Prevent "site read" if the user is not logged in and the
    # request path is not in the list of allowed anonymous paths
    #if not context.get('user') and toolkit.request.path not in allowed_anon_paths:
        #return {'success': False}

    user_name = context['user']
    user_name = toolkit.c.user
    is_admin = authz.is_sysadmin(user_name) 

    # url_for('dataset.search', ver=3, logic_function='dataset_search')

    logging.warning(' Controller => {0} , Action => {1} : '.format(toolkit.c.controller,toolkit.c.action))
    userobj = context.get('auth_user_obj')

    if not userobj:
        return {'success': False , 'msg': 'You must be logged in'}

    return {'success': True }

def sandbox_index():
    custom_array = ['test','test1','test2','test3','test4','test5','test6','test7']
    custom_string = 'Custom string'
    response = requests.get("https://gco.iarc.fr/api/globocan/v2/2020/meta/cancers/all/")

    cancers_dict = response.json()

    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        # if "GET" in rule.methods and has_no_empty_params(rule):
            # url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append(rule)

    # print(json.dumps(response))
    return plugins.toolkit.render('sandbox/index.html',extra_vars={
        'custom_array': custom_array,
        'custom_string': custom_string,
        "globocan_cancers" : cancers_dict , 
        'links' : links
    })

def questionnaires_index():

    custom_survey = ['test','test1','test2','test3','test4','test5','test6','test7']
    custom_string = 'Custom string'
    response = requests.get("https://gco.iarc.fr/api/globocan/v2/2020/meta/cancers/all/")

    cancers_dict = response.json()

    # print(json.dumps(response))
    return plugins.toolkit.render('questionnaires/index.html',extra_vars={
        'custom_array': custom_survey,
        'custom_string': custom_string,
        "globocan_cancers" : cancers_dict
    })


class CsuThemePlugin(plugins.SingletonPlugin):

    # logging.warning('CsuThemePlugin init')

    # router handled by blueprint now, not mconnect
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.IRoutes)
    # auth function (see get_auth_function)
    plugins.implements(plugins.IAuthFunctions,inherit=True)
    # setup configuration with public dir, resource dir and tpl dir
    plugins.implements(plugins.IConfigurer)
    # see helpers.actions
    plugins.implements(plugins.IActions)
    # middleware
    # plugins.implements(plugins.IMiddleware)
    
    # only alow authenticated user
    def get_auth_functions(self):
        logging.warning('Start get auth function')
        # logging.warning('And this, too')
        return {'site_read': site_read }
        # we need to prevent some actions being authorized.

    # the issue: https://github.com/ckan/ckan/discussions/6505
    # doc & list of methods for flask.Blueprint: https://tedboy.github.io/flask/generated/generated/flask.Blueprint.html
    # ex1 : https://tech.datopian.com/ckan/create-extension.html#edit-the-extension
    # ex2 : https://github.com/ckan/ckan/blob/master/ckanext/example_flask_iblueprint/plugin.py
    def get_blueprint(self):
        blueprint = Blueprint(self.name, self.__module__)
        rules = [
            ('/sandbox', 'sandbox', sandbox_index ),
            ('/questionnaires', 'index_questionnaires', questionnaires_index )
        ]
        for rule in rules:
            # doc: https://tedboy.github.io/flask/interface_api.application_object.html#flask.Flask.add_url_rule
            blueprint.add_url_rule(*rule)

        # blueprint.url_for
        blueprint.route('/suzie')

        return blueprint

    #def before_map(self, map): 
        #map.connect(
            #'csutheme',
            #'/api/3/action/organization_list',
            #controller='controller',
            #action='dataset_loader',
            #logic_function='controller.dataset_loader'
        #)

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic','csutheme')

    # IActions
    def get_actions(self):
        return dict(
            organization_show=ckanext.csutheme.action.get.csu_organization_show,
            package_list=ckanext.csutheme.action.get.csu_package_list,
            #dataset_search=ckanext.csutheme.controller.dataset.search
        )
        #return {
            #'dataset_loader': controller.dataset_loader
            #'xloader_hook': action.xloader_hook,
            #'xloader_status': action.xloader_status,
        #}

    def make_middleware(self, app, config):
        # mail = Mail(app)
        return app ; 

class CsuThemeGroupPlugin(plugins.SingletonPlugin):

    plugins.implements(plugins.IGroupController, inherit=True)

    # read (IGroupController)
    def before_view(self, grp_dict):
        # logging.warning('before_view() Group' )
        return grp_dict

    def read(self,entity):
        logging.warning('plugin_group_read() func {0}'.format(config.get('ckan.site_url')) )
    
    def create(self,entity):
        mail_recipient(config.get('ckan_site_title'), config.get('ckan_sysadmin_email'), "Add a new call for dataset", "A new call for data has been set. ")

class CsuThemeOrganizationPlugin(plugins.SingletonPlugin):

    plugins.implements(plugins.IOrganizationController,inherit=True)

    def read(self,entity):
        logging.warning('plugin_organization_read() func {0}'.format(entity) )

    def create(self,entity):
        mail_recipient(config.get('ckan_site_title'), config.get('ckan_sysadmin_email'), "Add a new organization", "A new registry/organization has been created. Please")

# Dataset (Package) 
class CsuThemeDatasetPlugin(plugins.SingletonPlugin):

    plugins.implements(plugins.IPackageController,inherit=True)
    
    def before_index(self,entity):
        logging.warning('before_view() func inside CsuThemeDatasetPlugin {0}'.format(config.get('ckan.site_url')) )

    def read(self,entity):
        # toolkit.redirect_to('home.index')
        logging.warning('plugin_dataset_read() func {0}'.format(config.get('ckan.site_url')) )
        

    def create(self,entity):
        mail_recipient(config.get('ckan_site_title'), config.get('ckan_sysadmin_email'), "Create a dataset", "A new dataset has been submitted. Please review ... ")

# Resources are sub items of dataset
class CsuThemeResourcePlugin(plugins.SingletonPlugin):

    plugins.implements(plugins.IResourceController,inherit=True)

    def before_show(self,entity):
        logging.warning('plugin_resource_before_show() func {0}'.format(entity) )

    def after_create(context,resource,param3):
        logging.warning('plugin_resource_after_create() {0} {1}'.format(resource,param3) )
        mail_recipient(config.get('ckan_site_title'), config.get('ckan_sysadmin_email'), "Add a resource to a dataset", "After creating a new resource into the dataset {0} {1}".format(resource.user,resource.package))
