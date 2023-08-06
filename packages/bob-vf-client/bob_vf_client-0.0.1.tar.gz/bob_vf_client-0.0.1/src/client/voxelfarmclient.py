import requests
import json
import base64
import time
from datetime import datetime, timedelta
import os
class rest:

    OrgId = '2343243456678890'
    class entity_type:
        View = 'VIEW'
        Project = 'PROJECT'
        VoxelTerrain = 'VOXSURF'
        RealtimeVoxelTerrain = 'VOXOP'
        BlockModel = 'VOXBM'
        IndexedPointCloud = 'IDXPC'
        VoxelGenerator = 'VOXGEN'
        RawPointCloud = 'RAWPC'
        RawHeightmap = 'RAWHM'
        RawBlockModel = 'RAWBM'
        RawMesh = 'RAWMESH'
        IndexedMesh = 'IDXMESH'
        VoxelMesh = 'VOXMESH'
        OrthoImagery = 'ORTHO'
        IndexedOrthoImagery = 'IDXORTHO'
        Program = 'PROGRAM'
        Folder = 'FOLDER'
        RawDensity = 'RAWDENSITY'
        IndexedDensity = 'IDXDENSITY'
        MaterialTracking = 'VOXMT'
        MaterialTrackingOperation = 'VOXMTOP'
        RawDrillHoles = 'RAWDH'
        DrillHoles = 'IDXDH'
        Export = 'EXPORT'
        Report = 'REPORT'


    class lambda_type:
        Generator = 'VOXEL'
        Report = 'REPORT'
        View = 'VIEW'

    CRSFields = [
        "coord_origin_x",
        "coord_origin_y",
        "coord_origin_z",
        "coord_hdatum",
        "coord_vdatum",
        "coord_projection",
        "coord_unit",
        "voxel_size",
        "coord_projection_tm_falseEasting",
        "coord_projection_tm_falseNorthing",
        "coord_projection_tm_latOriginDeg",
        "coord_projection_tm_longMeridianDeg",
        "coord_projection_tm_scaleFactor",
        "coord_projection_lcc_falseEasting",
        "coord_projection_lcc_falseNorthing",
        "coord_projection_lcc_latOfOriginDeg",
        "coord_projection_lcc_longOfOriginDeg", 
        "coord_projection_lcc_firstStdParallelDeg",
        "coord_projection_lcc_secondStdParallelDeg",
        "coord_projection_aeac_falseEasting",
        "coord_projection_aeac_falseNorthing",
        "coord_projection_aeac_latOfOriginDeg",
        "coord_projection_aeac_longOfOriginDeg", 
        "coord_projection_aeac_firstStdParallelDeg",
        "coord_projection_aeac_secondStdParallelDeg",
        "coord_projection_amg_zone",
        "coord_projection_utm_easting",
        "coord_projection_utm_northing"]

    DefaultFields = {
        entity_type.VoxelTerrain : {
            'include_classification' : '0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31',
        },
        entity_type.VoxelMesh : {
            'translate_x' : '0',
            'translate_y' : '0',
            'translate_z' : '0',
            'scale_x' : '1',
            'scale_y' : '1',
            'scale_z' : '1',
            'rotate_x' : '0',
            'rotate_y' : '0',
            'rotate_z' : '0',
            'rotation_order' : 'ZXZ',
        },
        entity_type.IndexedMesh : {
            'translate_x' : '0',
            'translate_y' : '0',
            'translate_z' : '0',
            'scale_x' : '1',
            'scale_y' : '1',
            'scale_z' : '1',
            'rotate_x' : '0',
            'rotate_y' : '0',
            'rotate_z' : '0',
            'rotation_order' : 'ZXZ',
        },
        entity_type.BlockModel : {
            'translate_x' : '0',
            'translate_y' : '0',
            'translate_z' : '0',
            'scale_x' : '1',
            'scale_y' : '1',
            'scale_z' : '1',
            'rotate_x' : '0',
            'rotate_y' : '0',
            'rotate_z' : '0',
            'rotation_order' : 'ZXZ',
            'bm_type': 'VOXBM1'
        }
    }

    HTTPSession = requests.Session()
    
    def __init__(self, apiurl):      
        self.proxy = None
        self.VFAPIURL = apiurl
        self.VFAPIURL_ENTITY = self.VFAPIURL + '/entity.ashx'
        self.VFAPIURL_FILE = self.VFAPIURL + '/file.ashx'
        self.VFAPIURL_EVENT = self.VFAPIURL + '/events.ashx'
        self.token: str = None
        self.aad_credentials : dict = None

    def set_proxy(self, proxy):
        self.proxy = proxy

    class api_result:
        success = False
        error_info = ''

    class creation_result(api_result):
        id = ''

    class wait_result(api_result):
        complete = False

    def add_default_fields(self, type, fields):
        if type in self.DefaultFields:
            for field in self.DefaultFields[type]:
                if not field in fields:
                    fields[field] = self.DefaultFields[type][field]
        if not 'file_date' in fields:
            fields['file_date'] = str(1000 * int(time.time()))

    class crs_result(api_result):
        crs = {}

    def get_project_crs(self, project):
        result = self.crs_result()
        params={'id': project}
        projectRequest = self.HTTPSession.get(self.VFAPIURL_ENTITY, params=params, headers=self.get_auth_headers(), proxies=self.proxy)
        if projectRequest.status_code != 200:
            result.success = False
            result.error_info = 'Error: Could not find project ' + project
            return result
        entityJson = json.loads(projectRequest.text)
        values = {
            'coord_hunit': entityJson['coord_unit'],
            'coord_vunit': entityJson['coord_unit']
        }
        for field in self.CRSFields:
            if field in entityJson:
                values[field] = entityJson[field]
            else:
                values[field] = '0'
        result.crs = values
        result.success = True
        return result

    def get_entity(self, id):
        params={'id': id}
        projectRequest = self.HTTPSession.get(self.VFAPIURL_ENTITY, params=params, headers=self.get_auth_headers(), proxies=self.proxy)
        if projectRequest.status_code != 200:
            return None
        entityJson = json.loads(projectRequest.text)
        return entityJson

    def get_projects_names(self):
        result = self.collection_result()
        entityRequest = self.HTTPSession.get(self.VFAPIURL_ENTITY, headers=self.get_auth_headers())
        if (entityRequest.status_code == 200):
            entityJson = entityRequest.json()
            items = []
            for x in entityJson:
                v = entityJson[x]
                if v["type"] == "PROJECT_REF":
                    items.append(v["project_ref"])

            result.items = items
            result.success = True
        else:
            result.success = False
            result.error_info = 'HTTP Error code ' + entityRequest.status_code
        return result


    def create_project(self, name, fields):
        result = self.creation_result()
        if fields == None:
            fields = {}
        fields['name'] = name
        self.add_default_fields(type, fields)
        data = {'operation': 'create', 'data': json.dumps(fields)}
        entityRequest = self.HTTPSession.post(self.VFAPIURL_ENTITY, data=data, headers=self.get_auth_headers(), proxies=self.proxy)
        if entityRequest.status_code == 200:
            apiResult = entityRequest.json()
            if apiResult['result'] != 'success':
                result.success = False
                result.error_info = base64.b64decode(apiResult['error_info']).decode('ascii')
                return result
            result.success = True
            result.id = apiResult['id']
        else:
            print('create_project error: ' + str(entityRequest.status_code))
            print(entityRequest.text)
            result.success = False
        return result

    def delete_project(self, project):
        items = []
        # Get all entities in project
        result = self.get_collection(project)
        if not result.success:
            print(result.error_info)
            exit(3)
        entities = result.items
        for e in entities:
            entity = entities[e]
            if entity['type'] != 'USER':
                if not ('virtual' in entity):
                    items.append(entity["ID"])
                elif entity['virtual']!="1":
                    items.append(entity["ID"])
                
        # Get all user_ref objects for project (users associated with the project)
        result = self.get_collection('users:' + project)
        if not result.success:
            print(result.error_info)
            exit(4)
        user_refs = result.items
        for user_ref in user_refs:
            if user_refs[user_ref]['type'] == 'USER_REF':
                user_id = user_refs[user_ref]['user_ref']
                items.append(user_id + ':' + project)
                items.append(project + ':' + user_id)
        items.append('R3Vlc3Q=:' + project) # guest user
        self.delete_entities(project, items)

    def clean_project(self, project):
        items = []
        # Get all entities in project
        result = self.get_collection(project)
        if not result.success:
            print(result.error_info)
            exit(3)
        entities = result.items
        for e in entities:
            entity = entities[e]
            if entity['type'] != 'USER' and entity['type'] != 'PROJECT':
                items.append(entity["ID"])

        self.delete_entities(project, items)        

    def create_entity_raw(self, project, type, name, fields, crs):
        result = self.creation_result()
        if fields == None:
            fields = {}
        fields['name'] = name
        fields['type'] = 'FILE'
        fields['file_type'] = type
        fields['state'] = 'COMPLETE'
        fields['project'] = project
        for key, value in crs.items():
            fields['entity_' + key] = value
        self.add_default_fields(type, fields)
        params={'project': project}
        entityRequest = self.HTTPSession.post(self.VFAPIURL_ENTITY, params=params, headers=self.get_auth_headers(), json=fields, proxies=self.proxy)
        apiResult = json.loads(entityRequest.text)
        if apiResult['result'] != 'success':
            result.success = False
            result.error_info = base64.b64decode(apiResult['error_info']).decode('ascii')
            return result
        result.success = True
        result.id = apiResult['id']
        return result

    def create_folder(self, project, folder, name):
        result = self.creation_result()
        if folder == None:
            folder = 0

        fields = {}
        fields['name'] = name
        fields['type'] = 'FILE'
        fields['file_type'] = 'FOLDER'
        fields['state'] = 'COMPLETE'
        fields['project'] = project
        fields['file_folder'] = folder
        self.add_default_fields(type, fields)
        params={'project': project}
        entityRequest = self.HTTPSession.post(self.VFAPIURL_ENTITY, params=params, headers=self.get_auth_headers(), json=fields, proxies=self.proxy)
        apiResult = json.loads(entityRequest.text)
        if apiResult['result'] != 'success':
            result.success = False
            result.error_info = base64.b64decode(apiResult['error_info']).decode('ascii')
            return result
        result.success = True
        result.id = apiResult['id']
        return result

    def create_entity_processed(self, project, type, name, fields, crs):
        result = self.creation_result()
        if fields == None:
            fields = {}
        fields['name'] = name
        fields['type'] = 'FILE'
        fields['file_type'] = type
        fields['project'] = project
        fields['state'] = 'PARTIAL'
        for key, value in crs.items():
            fields[key] = value
        self.add_default_fields(type, fields)
        params={'project': project}
        entityRequest = self.HTTPSession.post(self.VFAPIURL_ENTITY, params=params, headers=self.get_auth_headers(), json=fields, proxies=self.proxy)
        apiResult = json.loads(entityRequest.text)
        if apiResult['result'] != 'success':
            result.success = False
            result.error_info = base64.b64decode(apiResult['error_info']).decode('ascii')
            return result
        result.id = apiResult['id']
        params={'project': project, 'org': self.OrgId, 'id': result.id}
        data={'process':'PROCESS'}
        entityRequest = self.HTTPSession.post(self.VFAPIURL_EVENT, params=params, headers=self.get_auth_headers(), data=data, proxies=self.proxy)
        apiResult = json.loads(entityRequest.text)
        if apiResult['result'] != 'success':
            result.success = False
            result.error_info = base64.b64decode(apiResult['error_info']).decode('ascii')
        result.success = True
        return result

    def create_report(self, project, program, lod, region, name, fields, inputs):
        result = self.creation_result()
        if fields == None:
            fields = {}
        fields['name'] = name
        fields['type'] = 'FILE'
        fields['file_type'] = 'REPORT'
        fields['program'] = program
        fields['project'] = project
        fields['region'] = region
        fields['lod'] = str(lod)
        fields['state'] = 'PARTIAL'
        for input in inputs:
            fields['input_value_' + input] = inputs[input]
            fields['input_filter_' + input] = '0'
            fields['input_type_' + input] = '0'
            fields['input_label_' + input] = '0'
        self.add_default_fields(type, fields)
        params={'project': project}
        entityRequest = self.HTTPSession.post(self.VFAPIURL_ENTITY, params=params, headers=self.get_auth_headers(), json=fields, proxies=self.proxy)
        apiResult = json.loads(entityRequest.text)
        if apiResult['result'] != 'success':
            result.success = False
            result.error_info = base64.b64decode(apiResult['error_info']).decode('ascii')
            return result
        result.id = apiResult['id']
        params={'project': project, 'org': self.OrgId, 'id': result.id}
        data={'process':'RUN_REPORT'}
        entityRequest = self.HTTPSession.post(self.VFAPIURL_EVENT, params=params, headers=self.get_auth_headers(), data=data, proxies=self.proxy)
        apiResult = json.loads(entityRequest.text)
        if apiResult['result'] != 'success':
            result.success = False
            result.error_info = base64.b64decode(apiResult['error_info']).decode('ascii')
        else:
            result.success = True

        return result

    def reprocess_entity(self, id):
        result = self.creation_result()
        result.id = id

        report_entity = self.get_entity(id)
        if report_entity:
            project = report_entity["project"]

            params = {
                'project': project,
                'id' : id
            }

            fields = {
                'state': 'PARTIAL',
                'partial_progress': '0',
                'partial_status': '',
                'proccessing_time': '0'
            }

            entityRequest = self.HTTPSession.post(self.VFAPIURL_ENTITY, params=params, headers=self.get_auth_headers(), json=fields, proxies=self.proxy)
            apiResult = json.loads(entityRequest.text)
            if apiResult['result'] != 'success':
                result.success = False
                result.error_info = base64.b64decode(apiResult['error_info']).decode('ascii')
                return result

            params={'project': project, 'org': self.OrgId, 'id': id}
            data={'process':'RUN_REPORT'}
            entityRequest = self.HTTPSession.post(self.VFAPIURL_EVENT, params=params, headers=self.get_auth_headers(), data=data, proxies=self.proxy)
            apiResult = json.loads(entityRequest.text)
            if apiResult['result'] != 'success':
                result.success = False
                result.error_info = base64.b64decode(apiResult['error_info']).decode('ascii')
            else:
                result.success = True
        else:
            result.success = False

        return result        

    def create_lambda_python(self, project, type, name, code, fields):
        result = self.creation_result()
        if fields == None:
            fields = {}
        fields['name'] = name
        fields['type'] = 'FILE'
        fields['file_type'] = 'PROGRAM'
        fields['program_type'] = type
        fields['state'] = 'COMPLETE'
        generatorLambdaCode = code.encode('ascii')
        generatorLambdaCode = base64.b64encode(generatorLambdaCode).decode('ascii')
        fields['code'] = generatorLambdaCode
        fields['project'] = project
        self.add_default_fields(type, fields)
        params={'project': project}
        entityRequest = requests.post(self.VFAPIURL_ENTITY, params=params, headers=self.get_auth_headers(), json=fields, proxies=self.proxy)
        apiResult = json.loads(entityRequest.text)
        if apiResult['result'] != 'success':
            result.success = False
            result.error_info = base64.b64decode(apiResult['error_info']).decode('ascii')
            return result
        result.success = True
        result.id = apiResult['id']
        return result

    def create_generator(self, project, program, name, fields, inputs):
        result = self.creation_result()
        if fields == None:
            fields = {}
        fields['name'] = name
        fields['type'] = 'FILE'
        fields['file_type'] = 'VOXGEN'
        fields['program'] = program
        fields['state'] = 'COMPLETE'
        fields['project'] = project
        for input in inputs:
            fields['input_value_' + input] = inputs[input]
            fields['input_filter_' + input] = '0'
            fields['input_type_' + input] = '0'
            fields['input_label_' + input] = '0'
        self.add_default_fields(type, fields)
        params={'project': project}
        entityRequest = requests.post(self.VFAPIURL_ENTITY, params=params, headers=self.get_auth_headers(), json=fields, proxies=self.proxy)
        apiResult = json.loads(entityRequest.text)
        if apiResult['result'] != 'success':
            result.success = False
            result.error_info = base64.b64decode(apiResult['error_info']).decode('ascii')
            return result
        result.success = True
        result.id = apiResult['id']
        return result

    def is_processing_complete(self, project, ids):
        result = self.wait_result()
        for id in ids:
            params = {'id': id}
            entityRequest = self.HTTPSession.get(self.VFAPIURL_ENTITY, params=params, headers=self.get_auth_headers())
            if entityRequest.status_code == 200:
                entityJson = json.loads(entityRequest.text)
                if not 'state' in entityJson:
                    result.complete = False
                    result.success = False
                    result.error_info = json.dumps(entityJson)
                    break
                if entityJson['state'] == 'PARTIAL':
                    result.complete = False
                    result.success = True
                    break
                if entityJson['state'] == 'COMPLETE':
                    result.complete = True
                    result.success = True
                if entityJson['state'] == 'ERROR':
                    result.complete = False
                    result.success = False
                    result.error_info = base64.b64decode(entityJson['error_info']).decode('ascii')
                    break
            else:
                result.complete = False
                result.success = False
                result.error_info = 'HTTP Error ' + str(entityRequest.status_code)
                break

        return result

    def delete_entities(self, project, ids):
        result = self.api_result()
        deleteIdentifierList = ''
        for id in ids:
            deleteIdentifierList = deleteIdentifierList + id + ' '
        params = {'project': project, 'org': self.OrgId, 'operation': 'delete'}
        data = {'operation': 'delete', 'items': deleteIdentifierList}
        entityRequest = self.HTTPSession.post(self.VFAPIURL_ENTITY, params=params, headers=self.get_auth_headers(), data=data, proxies=self.proxy)
        apiResult = json.loads(entityRequest.text)
        if apiResult['result'] != 'success':
            result.success = False
            result.error_info = base64.b64decode(apiResult['error_info']).decode('ascii')
        result.success = True
        return result

    def attach_files(self, project, id, files):
        result = self.api_result()
        params = {'project': project, 'org': self.OrgId, 'id': id}
        entityRequest = self.HTTPSession.post(self.VFAPIURL_FILE, params=params, headers=self.get_auth_headers(), files=files, proxies=self.proxy)
        apiResult = json.loads(entityRequest.text)
        if apiResult['result'] != 'success':
            result.success = False
            result.error_info = base64.b64decode(apiResult['error_info']).decode('ascii')
        result.success = True
        return result

    def get_file(self, project, entity, filename):
        params = {'id': entity, 'project': project, 'org': self.OrgId, 'filename': filename}
        entityRequest = self.HTTPSession.get(self.VFAPIURL_FILE, params=params, headers=self.get_auth_headers(), proxies=self.proxy)
        return entityRequest.text

    def get_binary_file(self, project, entity, filename):
        params = {'id': entity, 'project': project, 'org': self.OrgId, 'filename': filename}
        entityRequest = self.HTTPSession.get(self.VFAPIURL_FILE, params=params, headers=self.get_auth_headers(), proxies=self.proxy)
        return entityRequest.content  

    class collection_result(api_result):
        items = None

    def get_collection(self, id):
        result = self.collection_result()
        params = {'project': id}
        entityRequest = self.HTTPSession.get(self.VFAPIURL_ENTITY, params=params, headers=self.get_auth_headers())
        if (entityRequest.status_code == 200):
            entityJson = json.loads(entityRequest.text)
            result.items = entityJson
            result.success = True
        else:
            result.success = False
            result.error_info = 'HTTP Error code ' + entityRequest.status_code
        return result

#region AAD_Credentials
    def set_file_credentials(self, filename: str):
        self.aad_credentials = self.get_env_file_as_dict(filename)
        self.token = self.get_token()
        if (self.token == None):
            print("credentials file: "+filename )
            raise Exception("Check that the credentials are correct")

    def get_env_file_as_dict(self, path: str) -> dict:
        if not os.path.isfile(path):
            t_path = os.path.dirname(__file__)+ path
            if os.path.isfile(t_path):    
                path = t_path
        with open(path, 'r') as f:
            return dict(tuple(line.replace('\n', '').split('=')) for line 
                        in f.readlines() if not line.startswith('#'))

    def get_token(self):
        if (self.aad_credentials["TENANT"] != None):
            authority = "https://login.microsoftonline.com/"+self.aad_credentials["TENANT"]+"/oauth2/token"
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            data = {
                "grant_type" : "client_credentials",
                "client_id" : self.aad_credentials["CLIENT_ID"],
                "client_secret": self.aad_credentials["CLIENT_SECRET"],
                "scope" : "https://graph.microsoft.com/.default",
                "resource" : self.aad_credentials["CLIENT_ID"],
            }

            HTTPSession = requests.Session()
            tokenRequest = HTTPSession.post(authority, data=data, headers=headers)
            HTTPSession.close()

            if tokenRequest.status_code == 200:
                tokenResult = tokenRequest.json()
                return tokenResult["access_token"]
        return None

    def check_ExpiredToken(self, token: str):
        body = token.split(".")[1]
        body += "=" * ((4 - len(body) % 4) % 4) #ugh
        txt = base64.b64decode(body).decode('utf-8')
        jwt = json.loads(txt)
        expire = int(jwt["exp"])
        return (datetime.fromtimestamp(expire)) < (datetime.now()+timedelta(minutes=2))

    def get_auth_headers(self):
        if (self.token==None):
            return None
        if self.check_ExpiredToken(self.token):
            self.token = self.get_token()    
        
        return { 'Authorization': f'Bearer {self.token}' }

#endregion AAD_Credentials