"""Docstring for the net.py module.

This API is used to directly interact with your data on  MorphoNet

For any information for the installation go on https://pypi.org/project/morphonet/

"""

import sys,os
import time
import bz2
import json
import requests
import numpy as np
import gzip
import ast
from http.client import HTTPSConnection


from morphonet.tools import load_credentials,add_slashes,try_parse_int,strblue,strred,strgreen,nodata,ss,_get_objects,_get_object,_get_type,_get_last_curation,_get_string,_check_version,error_request

#New For https...
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import urllib3
urllib3.disable_warnings()


class Net:
    """Connect to the MorphoNet server.

    Use your credentials to connect to MorphoNet

    Parameters
    ----------
    login : string
        your login in MorphoNet
    passwd : string
        your password in MorphoNet
    new_url : string, optional
        for developmental purpose, you can specify a new server that will be used to compute API request and get/upload MorphoNet data. 
    new_port : int, optional
        for developmental purpose, you can specify an other port

    Returns
    -------
    MorphoConnection
        return an object of morphonet which will allow you to upload or download data



    Examples
    --------
    >>> import morphonet
    >>> mn=morphonet.Net("yourlogin","yourpassword")


     
    """
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    def __init__(self,login,passwd,new_url=None,new_port=-1):
        self.id_people=-1
        self.id_dataset=-1
        self.token = ""
        self.id_dataset_owner=-1
        self.dataset_name=""
        self.minTime=-1
        self.maxTime=-1
        self.login=login
        self.passwd=passwd
        self.bundle=0
        self.id_NCBI=1 #0 -> Unclassified 
        self.id_type=0; #0 Observed Data, 1 Simulated Data, 2 Drawing Data
        self.guys={}
        self.datasettype={}
        self.delta_t=0
        self.start_time=0

        if new_url is not None:
             self.url=new_url
        else:
            from morphonet import url
            self.url=url
        if new_port!=-1:    
            self.port=new_port 
        else:
            from morphonet import port
            self.port=port

        #Check if current Version is the last one
        _check_version()

        self._connect()

    # Internal Functions
    def _get_headers(self):
        if self.token == "":
            return {"Content-Type": "application/json"}
        return {"Content-Type": "application/json",'Authorization':'Token '+self.token}
    def _connect(self,timeout=None):
        if timeout == None:
            timeout=100
        #HTTPSConnection.debuglevel = 1
        conn = HTTPSConnection(self.url,timeout=timeout)
        params = json.dumps({'username': self.login, 'password': self.passwd})
        conn.request("POST", "/rest-auth/login/",params,self._get_headers())
        response=conn.getresponse()
        if response.status==200:
            data=json.loads(str(response.read().decode("utf-8")))
            conn.close()
            self.id_people=data['user']
            self.token=data['key']
            print(strblue(self.login+' is connected to MorphoNet'))
            return True
        else:
            print(strred(ss+" Invalid Credentials"))
            #print(strred(ss+'CONNECTION ERROR '+str(response.status)+" "+response.reason))
        conn.close()
        return False
    def _is_connected(self):
        if self.id_people==-1:
            print(strred(ss+'ERROR : You are not connected '))
            return False
        return True
    def _request(self,param,path,request_type,timeout=None):
        if self._is_connected():
            if timeout==None:
                timeout=100
            conn = HTTPSConnection(self.url,timeout=timeout)
            try:
                conn.request(request_type, path,json.dumps(param), self._get_headers())
                response=conn.getresponse()
                if response.status==200:
                    da=json.loads(str(response.read().decode("utf-8")))
                    conn.close()
                    return da
                else:
                    print(strred(ss+'CONNECTION ERROR '+str(response.status)+" "+response.reason))
                    self.id_people=-1
                    self.token=None
            except  Exception as e:
                print(ss+'Error cannot request ... '+str(e))
                time.sleep(5)
                print(' --> Retry')
                return self._request(param,path,request_type)
            conn.close()   
    def _binary_request(self,param,path,request_type):
        if self._is_connected():
            conn = HTTPSConnection(self.url,timeout=100)
            try:
                conn.request(request_type, path,json.dumps(param), self._get_headers())
                response=conn.getresponse()
                if response.status==200:
                    da=response.read()
                    conn.close()
                    return da
                else:
                    print(strred(ss+'CONNECTION ERROR '+str(response.status)+" "+response.reason))
                    self.id_people=-1
                    self.token=None
            except  Exception as e:
                print(ss+'Error cannot request ... '+str(e))
                time.sleep(5)
                print(' --> Retry')
                return self._binary_request(param,path,request_type)
            conn.close()   
    def _large_request(self,param,path,data):
        if self._is_connected():
            try:
                if os.path.isfile("temp.bz2"):
                    os.system('rm -f temp.bz2')
                if sys.version_info[0]>=3: #PYTHON 3
                    if isinstance(data,str):
                        data=bytes(data.encode('utf-8'))
                    with bz2.open("temp.bz2", "wb") as f:
                        unused = f.write(data)
                files = {'file': open("temp.bz2", 'rb')}
                session = requests.Session()
                del session.headers['User-Agent']
                del session.headers['Accept-Encoding']
                session.headers['Authorization'] = 'Token '+self.token 
                r = session.post("https://"+self.url+path, files=files,data=param,verify=False)
                if r.status_code == requests.codes.ok:
                    return r.text
                else:
                    print(strred(ss+'CONNECTION ERROR '+str(r.status_code)))
                    self.id_people=-1
                    self.token=None
                if os.path.isfile("temp.bz2"):
                    os.system('rm -f temp.bz2')
            except  Exception as e:
                print(ss+'ERROR cannot request ... '+str(e))
                quit()
    def _large_request_image(self,param,path,data,format):
        if self._is_connected():
            try:
                if os.path.isfile("temp."+format):
                    os.system('rm -f temp.'+format)
                if sys.version_info[0]>=3: #PYTHON 3
                    if isinstance(data,str):
                        data=bytes(data.encode('utf-8'))
                    f = open("temp."+format, "wb")
                    f.write(data)
                    f.close()
                files = {'file': open("temp."+format, 'rb')}
                session = requests.Session()
                del session.headers['User-Agent']
                del session.headers['Accept-Encoding']
                session.headers['Authorization'] = 'Token '+self.token 
                r = session.post("https://"+self.url+path, files=files,data=param,verify=False)
                if r.status_code == requests.codes.ok:
                    return r.text
                else:
                    print(strred(ss+'CONNECTION ERROR '+str(r.status_code)))
                    self.id_people=-1
                    self.token=None
                if os.path.isfile("temp.bz2"):
                    os.system('rm -f temp.bz2')
            except  Exception as e:
                print(ss+'ERROR cannot request ... '+str(e))
                quit()


    # PEOPLE
    def _get_guys(self):
        """ List all people in MorphoNet

        """
        data=self._request({},'/api/people/','GET')
        for g in data:
            self.guys[int(g['id'])]=g['surname']+" "+g['name']
    def get_guy_by_id(self,id_guy):
        """ Return the person corresponding to an id 
        
        Parameters
        ----------
        id_guy : int
            the id of the person you'r lokking for 
        
        Returns
        -------
        object
            name , surname and login

        Examples
        --------
        >>> mn.get_guy_by_id(1)
        """

        id_guy=int(id_guy)
        if self.guys=={}:
            self._get_guys()
        if id_guy in self.guys:
            return self.guys[id_guy]
        data= self._request({"id_user": id_guy}, '/api/getusernamebyid/', 'GET')

        if not nodata(data):
            self.guys[id_guy] = data['result']['surname'] + " " + data['result']['name']
            return self.guys[id_guy]
        return strred(ss+"User not found")
    def get_guy_by_name(self,name): # RETURN NAME + SURNAME + LOGIN FORM SPECIFIC ID
        """ Return the person corresponding to a specific name and surname 
        
        Parameters
        ----------
        name : string
            the name and surname separated by a space 
        
        Returns
        -------
        id_guy
            the id corresponding to the person, -1 if the person does not exist

        Examples
        --------
        >>> mn.get_guy_by_name("Faure Emmanuel")
        """

        values = name.split(' ')
        if len(values)!=2:
            print(strred(ss+"Please put <name> <surname>"))
            return -1
        u_name = str(values[0])
        u_surname = str(values[1])
        data=self._request({'name':u_name,'surname':u_surname},'/api/userbyname/','GET')
        if nodata(data):
            print(strred(ss+'User is unknown or input is incorrect. Please input as "name surname"'))
            return -1
        if data['result']=="[]":
            print(strblue(str(name)+" is unkown"))
            return -1
        else:
            #dataset=json.loads(data)
            return int(data['result']['id'])
    def get_group_by_name(self,name): # RETURN NAME + SURNAME + LOGIN FORM SPECIFIC ID
        """ Return the group corresponding to a specific name  
        
        Parameters
        ----------
        name : string
            the name of the group
        
        Returns
        -------
        id_group
            the id corresponding to the group, -1 if the group does not exist

        Examples
        --------
        >>> mn.get_group_by_name("The ascidians")
        """
        data=self._request({'name':name},'/api/groupidbyname/','GET')
        id_group=-1
        if not nodata(data):
            id_group=int(data['result']['id'])
        if id_group==-1:
            print(strred(ss+'Unknown group '+name+''))
        return id_group

    # NCBI Taxonomy
    def _get_NCBI_type_by_id(self,id_NCBI):
        """ Return the name of a specific NCBI id  c
        
        Parameters
        ----------
        id_NCBI : int
            the id of the NCBI Category 
        
        Returns
        -------
        name
            the corresponding name to the NCBI id coategory
        """
        if self._is_connected():
            data=self._request({},'/api/ncbitree/'+str(id_NCBI)+'/','GET')
            return data['name']

    # TYPE
    def _get_typename(self,id_type): #
        """ Return the name of a specific type
        
        Parameters
        ----------
        id_type : int
            0 for Observed Data, 1 for Simulated Data, 2 for Drawing Data 
        
        Returns
        -------
        name
            the corresponding name to the type 
        """
        if id_type==0:
            return "Observed Data"
        if id_type==1:
            return "Simulated Data"
        if id_type==2:
            return "Drawing Data"
        return "Unknown Data"


    # DATASET
    def _is_dataset(self):
        """ Return true if you selected a dataset, false if you didn't
        
        """
        if not self._is_connected():
            return False
        if self.id_dataset==-1:
            print(strgreen('you first have to select a dataset'))
            return False
        return True


    def _own_dataset(self):
        """ Return true if you are the owner of the dataset you select, false if you aren't

        """
        if not self._is_dataset():
            return False
        if str(self.id_dataset_owner)!=str(self.id_people):
            print(strgreen('you are not the owner of this dataset, ask '+self.get_guy_by_id(self.id_dataset_owner)))
            return False
        return True  
    def _init_time_point(self,minTime,maxTime): #INTERNAL FUNCTION TO INITIALISE TIME POINT
        """ Localy override min and max time for the current dataset
        
        Parameters
        ----------
        minTime : int
            The new min_time value

        maxTime : int
            The new max_time value
        
        """
        self.minTime=int(minTime)
        self.maxTime=int(maxTime)
    def _get_value(self,field,name):
        if name in field:
            return field[name]
        return None
    def _parse_dataset(self,data): #Parse id,name,minTime,maxTime,id_people to dataset structure
        """ Store values into the current dataset
        
        Parameters
        ----------
        data : object
            Contains all data to be parsed and stored inside the daraser
        
        """
        if nodata(data):
            print(strred(ss+'Dataset not found'))
        else:
            dataset=data
            ids=try_parse_int(dataset['id'])
            if ids is None:
                print(strgreen('dataset not found '+str(data)))
            else:
                self.dataset_name=dataset['name']
                self._init_time_point(dataset['mintime'],dataset['maxtime'])
                self.id_dataset_owner=try_parse_int(self._get_value(dataset,'id_people'))
                self.bundle=try_parse_int(self._get_value(dataset,'bundle'))
                self.id_NCBI=try_parse_int(self._get_value(dataset,'id_ncbi'))
                self.id_type=try_parse_int(self._get_value(dataset,'type'))
                self.delta_t=try_parse_int(self._get_value(dataset,'dt'))
                self.start_time = try_parse_int(self._get_value(dataset, 'spf'))
                self.id_dataset=ids
                print('found dataset '+self.dataset_name+' from '+str(self.minTime)+' to ' +str(self.maxTime)+' owned by '+str(self.get_guy_by_id(self.id_dataset_owner))+' with NCBI id='+str(self.id_NCBI))
    def format_date(self,date_string):
        return date_string.replace("T"," ").replace("t"," ").replace("z","").replace("Z","")

    def _show_datasets(self,data):
        """ Display the values given inside parameter, formatted like a dataset
        
        Parameters
        ----------
        data : object
            Contains all values to be displayed
        
        """
        #dataset=json.loads(data)
        for datas in data:  #id,name,minTime,maxTime,id_people,bundle,id_NCBI,type,date
            s='('+str(datas['id'])+') '+datas['name']
            if int(datas['mintime'])!=int(datas['maxtime']):
                s+=' from '+str(datas['mintime'])+' to '+str(datas['maxtime'])
            s+=' is '+self._get_typename(int(datas['type']))
            if datas['id_ncbi'] != 0 and datas['id_ncbi'] != -1:
                s+=' of '+self._get_NCBI_type_by_id(datas['id_ncbi'])
            s+=' created by '+self.get_guy_by_id(datas['id_people'])
            s+=' the '+self.format_date(datas['date'])
            print(s)
    def list_my_dataset(self): #LIST ALL MY dataset 
        """To display the datasets you own
        
        Examples
        --------
        >>> mn.list_my_dataset()

        Notes
        --------
        It will display all your datasets like this
        >>> (id_set) set_name is data_type created by set_owner the creation_date

        """
        if self._is_connected():
            data=self._request({},'/api/mydataset/','GET')
            self._show_datasets(data)
            return data
    def list_dataset(self): #LIST ALL  dataset 
        """To display dataset you can access (even if you re not owner) 
        
        Examples
        --------
        >>> mn.list_dataset()

        It will display all your datasets like this
        >>> (id_set) set_name is data_type created by set_owner the creation_date

    
        """
        if self._is_connected():
            data=self._request({},'/api/userrelatedset/','GET')
            self._show_datasets(data)
            return data
    def share_dataset_with_user(self,id_user,role): #SHARE A dataset with USER (role = 0:reader , 1:manager )
        """To share the current dataset with a specific user
        
        Parameters
        ----------
        id_user : int
            the id of the user
        role : int
            the role (Manager : 1, Reader : 0 ) which will be attribute to the user

        Examples
        --------
        >>> mn.share_dataset_with_user(1,0)

        """
        if self._own_dataset():
            if id_user==-1:
                print(" Unknown user ")
                return -1
            data=self._request({"sharedataset":self.id_dataset,"id_user":id_user,"how":role},'/api/shareuserapi/','POST')
            if nodata(data):
                print(strred(ss+'ERROR : Share not created '+str(data['error_message'])))
            else :
                ids=try_parse_int(data['result'])
                print("your share is created (with id "+str(data['result'])+')')
    def unshare_dataset_with_user(self,id_user): #UNSHARE A dataset with USER
        """To unshare the current dataset with a specific user
        
        Parameters
        ----------
        id_user : int
            the id of the user
       
        Examples
        --------
        >>> mn.unshare_dataset_with_user(1)

        """
        if self._own_dataset():
            if id_user==-1:
                print(" Unknown user ")
                return -1
            data=self._request({"sharedataset":self.id_dataset,"id_user":id_user},'/api/unshareuserapi/','POST')
            if nodata(data):
                print(strred(ss+'ERROR : Share not deleted '+str(data['error_message'])))
            else :
                print("The share is deleted")
    def change_dataset_owner(self, new_owner_id):
        """ Update the dataset on the server

        Parameters
        ----------
        new_owner_id : int
            Identifiant of the new owner
        """
        if self._is_dataset():
            data = self._request({"set_id": self.id_dataset, "new_owner_id": new_owner_id},
                                 '/api/updatesetowner/', 'POST')
            if nodata(data):
                print(strred(ss + "ERROR : Cannot transfer ownership to : " + str(new_owner_id)))
            else:
                print("Dataset succesfully transfered to : " + str(new_owner_id))


    def share_dataset_with_group(self,id_group,role): #SHARE A dataset with GROUP
        """To share the current dataset with a specific group
        
        Parameters
        ----------
        id_group : int
            the id of the group
        role : int
            the role (Manager : 1, Reader : 0 ) which will be attribute to the group

        Examples
        --------
        >>> mn.share_dataset_with_group(1,0)

        """
        if self._own_dataset():
            if id_group==-1:
                print(" Unknown group ")
                return -1
            data=self._request({"sharedataset":self.id_dataset,"id_group":id_group,"how":role},'/api/sharegroupapi/','POST')
            if nodata(data):
                print(strred(ss+'ERROR : Share not created '+str(data['error_message'])))
            else :
                ids=try_parse_int(data['result'])
                print("your share is created (with id "+str(data['result'])+')')
    def unshare_dataset_with_group(self,id_group): #SHARE A dataset with GROUP
        """To unshare the current dataset with a specific group
        
        Parameters
        ----------
        id_group : int
            the id of the group
       
        Examples
        --------
        >>> mn.unshare_dataset_with_group(1)

        """

        if self._own_dataset():
            if id_group==-1:
                print(" Unknown group ")
                return -1
            data=self._request({"sharedataset":self.id_dataset,"id_group":id_group},'/api/unsharegroupapi/','POST')
            if nodata(data):
                print(strred(ss+'ERROR : Share not deleted '+str(data['error_message'])))
            else :
                print("The share is deleted")
    def create_dataset(self,name,minTime=0,maxTime=0,id_NCBI=0,id_type=0,spf=-1,dt=-1,serveradress=None): #CREATE A NEW DATA SET
        """To create a data in the MorphoNet database 
        
        Parameters
        ----------
        name : string
            the given name of the dataset
        minTime : int, optional
            the time first time point for 3D (or 2D) + t dataset, default: 0
        maxTime : int, optional
            the last first time point for 3D (or 2D) + t dataset, default: 0
        id_NCBI :int, optional
            the NCBI id attribute to the dataset
        id_type : int, optional
            the tType of dataset :
                - 0 : Observed
                - 1 : Simulated
                - 2 : Drawed
        spf : int , optional
            the second post fertilization for the first time point
        dt : int , optional 
            the delta time in seconds between two consecutive time points
        serveradress : string , optional 
            you own server adress

        Examples
        --------
        >>> mn.create_dataset("test set",minTime=1,maxTime=150)

        """
        self.id_NCBI=id_NCBI
        self.id_type=id_type
        if self._is_connected():
            data=self._request({"createdataset":name,"minTime":minTime,"maxTime":maxTime,"serveradress":serveradress,"id_NCBI":self.id_NCBI,"id_type":self.id_type,"spf":spf,"dt":dt},'/api/createdatasetapi/','POST')
            self.id_dataset_owner=self.id_people
            if nodata(data):
                print(strred(ss+'ERROR : dataset not created '+data['error_message']))
                return False
            else :
                ids=try_parse_int(data['result'])
                self.dataset_name=name
                self.id_dataset=ids
                self.id_dataset_owner=self.id_people
                self._init_time_point(minTime,maxTime)
                print("your id dataset '"+name+"' is created (with id "+str(self.id_dataset)+')')
                return True
        return False
    def upload_description(self,description): #Upload a description 
        """ Change description of the selected dataset on the server
        
        Parameters
        ----------
        description : string
            New description to upload

        Examples
        --------
        >>> mn.upload_description("The new description attached")
        """
        if self._own_dataset():
            data=self._request({"uploadescription":self.id_dataset,"description":description},'/api/uploadcommentapi/','POST')
            if nodata(data):
                print(strred(ss+"Error during comment update : "+data['error_message']))
            else :
                print(data['result'])      
    def update_dataset(self,dataset_name="",minTime=-1,maxTime=-1,id_NCBI=-1,id_type=-1): #COMPLETE DELETE OF A dataset
        """ Change specified values for the selected dataset
        
        Parameters
        ----------
        dataset_name : string, optional
            New name of the dataset 
        minTime : int, optional
            New minimal time point
        maxTime : int, optional
            New maximum time point
        id_NCBI : int, optional
            New taxonomy category id
        id_type : int, optional
            New dataset stored type 
        

        Examples
        --------
        >>> mn.update_dataset("Changing name only")
        
        or
        
        >>> mn.update_dataset("new name",1,1,1000,1)
        """
        if dataset_name!="":
            self.dataset_name=dataset_name
        if minTime!=-1:
            self.minTime=minTime
        if maxTime!=-1:
            self.maxTime=maxTime
        if id_NCBI!=-1:
            self.id_NCBI=id_NCBI 
        if id_type!=-1:
            self.id_type=id_type 
        if self._own_dataset():
            data=self._request({"updatedataset":self.id_dataset,"minTime":self.minTime,"maxTime":self.maxTime,"id_NCBI":self.id_NCBI,"id_type":self.id_type,"dataname":self.dataset_name},'/api/updatesetapi/','POST')
            if nodata(data): 
                print(strred(ss+'ERROR during update : '+str(data['error_message'])))
            else:
                self._init_time_point(self.minTime,self.maxTime)
                print(data['result']) 
                
    def select_dataset_by_id(self,ids): #SELECT A dataset BY ID
        """ Select a dataset using an id
        
        Parameters
        ----------
        ids : int
            The dataset id to select

        Examples
        --------
        >>> mn.select_dataset_by_id(1)
        """
        if self._is_connected():
            self.id_dataset=-1
            data=self._request({"dataset":ids},'/api/datasetqueryapi/','GET')
            if not nodata(data):
                new_data = data['result']
                self._parse_dataset(new_data)
            else :
                print(strred(ss+"No dataset found"))
            return self.id_dataset != -1
        return False
    def select_dataset_by_name(self,name): #SELECT A dataset BY NAME
        """ Select a dataset using is name
        
        Parameters
        ----------
        name : string
            The dataset name to select

        Examples
        --------
        >>> mn.select_dataset_by_name("The name")
        """
        self.id_dataset=-1
        if self._is_connected():
            data=self._request({"datasetname":name},'/api/datasetnameapi/','GET')
            if len(data) > 0:
                self._parse_dataset(data[0])
            else :
                print(strred(ss+"No dataset found"))
        return self.id_dataset
    def delete_dataset(self): #COMPLETE DELETE OF A dataset
        """ Remove the selected dataset from the server

        Examples
        --------
        >>> mn.delete_dataset()
        """
        if self._own_dataset():
            data=self._request({"deletedataset":self.id_dataset},'/api/deletedatasetapi/','POST')
            if not nodata(data): 
                print('Dataset cleared')
                self.id_dataset=-1
                self.id_dataset_owner=-1
                self.minTime=-1
                self.maxTime=-1
                self.dataset_name=""
            else:
                print(strred(ss+'ERROR during clear : '+str(data['error_message'])))

    # TODO DELETE BY ID

    def delete_dataset_by_id(self,id_dataset): #COMPLETE DELETE OF A dataset
        """ Remove the selected dataset from the server using its id

        Examples
        --------
        >>> mn.delete_dataset()
        """
        if id_dataset == -1:
            print(strred("Id_dataset is incorrect !"))
            return False

        data=self._request({"deletedataset":id_dataset},'/api/deletedatasetapi/','POST')
        if not nodata(data):
            return True
        else:
            print(strred(ss+'ERROR during clear : '+str(data['error_message'])))
            return False

    #
    def clear_dataset(self): # CLEAR ALL TIME POINT AND INFOS
        """ Remove the 3D data and all informations for the selected dataset

        Examples
        --------
        >>> mn.clear_dataset()
        """
        if self._own_dataset():
            data=self._request({"cleardataset":self.id_dataset},'/api/cleardatasetapi/','POST')
            if not nodata(data):
                print('Dataset cleared')
            else:
                print(strred(ss+'ERROR during clear : '+str(data['error_message'])))
    
    # MESH
    def _compute_center(self,obj):
        """ Compute center of the given 3D object data
        
        Parameters
        ----------
        obj : bytes
            The 3D data to compute center
        
        Returns
        -------
        center : string
            The center formatted like this : X-value,Y-value,Z-value

        """
        objA=obj.split("\n")
        X=0.0; Y=0.0; Z=0.0; nb=0;
        for line in objA:
           if len(line)>2 and line[0]=='v' and line[1]!='n'  and line[1]!='t' :
               while line.find("  ")>=0:
                   line=line.replace("  "," ")
               tab=line.strip().split(" ")
               if len(tab)==4:
                   X+=float(tab[1].replace(',','.'))
                   Y+=float(tab[2].replace(',','.'))
                   Z+=float(tab[3].replace(',','.'))
                   nb+=1
        if nb==0:
           print(ss+'ERROR your obj does not contains vertex ')
           quit()                
        X/=nb
        Y/=nb
        Z/=nb
        return str(round(X,2))+','+str(round(Y,2))+','+str(round(Z,2))
    def read_mesh(self,filename):
        """ Read the mesh inside the given filename
        
        Parameters
        ----------
        filename : string
            the mesh file name

        
        Returns
        -------
        obj : string
            the mesh

        Examples
        --------
        >>> mn.read_mesh("path/to/myfile.obj")
        """
        f=open(filename,'r')
        obj=""
        for line in f:
            obj+=line
        f.close()
        return obj
    def get_number_of_mesh_at(self,t,quality=-1,channel=-1):
        """ Get the number of 3D data mesh for the selected dataset at a specifid time point, for a quality and a channel
        
        Parameters
        ----------
        t : int
            The time point to get the number of 3D data from
        quality : int
            The quality of the 3D data
        channel : int
            Wich channel of the object

        
        Returns
        -------
        count : int
            the number of the 3D meshes for the specified configuration

        Examples
        --------
        >>> mn.get_number_of_mesh_at(1,0,0)
        """
        if self._own_dataset():
            data=self._request({"getnumberofmeshat":self.id_dataset,"t":t,"quality":quality,"channel":channel},'/api/numbermeshapi/','GET')
            if nodata(data):
                print(strred(ss+'ERROR : Unable to get mesh count '+str(data['error_message'])))
            else :
                #print("Mesh count : "+str(data['result']))
                return int(data['result'])
        return -1
    def clear_mesh_at(self,t,quality=-1,channel=-1):
        """ Remove the 3D data for the selected dataset at a specified time point, for a quality and channel
        
        Parameters
        ----------
        t : int
            The time point to clear 3D data from
        quality : int
            The quality of the 3D data
        channel : int
            Wich channel of the object

        Examples
        --------
        >>> mn.clear_mesh_at(1,0,0)
        """
        if self._own_dataset():
            data=self._request({"clearmeshat":self.id_dataset,"t":t,"quality":quality,"channel":channel},'/api/clearmeshapi/','POST')
            #data2=json.loads(data)
            if not nodata(data): 
                if quality==-1 and channel==-1:
                    print('mesh cleared at '+str(t))
                elif quality==-1:
                    print('mesh cleared at '+str(t)+ " with channel "+str(channel))
                elif channel==-1:
                    print('mesh cleared at '+str(t)+ " with quality "+str(quality))
                else:
                    print('mesh cleared at '+str(t)+ " with quality "+str(quality)+ " and channel "+str(channel))
            else:
                print(strred(ss+'ERROR during mesh clear : '+str(data['error_message'])))
    def upload_mesh_at(self,t,obj,quality=0,channel=0,link="null",texture=None,material=None,ttype="bmp"): #UPLOAD TIME POINT IN dataset,new behaviour : do not override existing mesh in database (become uploadMultipleMesh)
        """ Upload a new mesh (3D data) to a specific time point, for a quality and channel given. You can upload a texture by giving a texture and a material, specifying the texture format
        In order to add mutliple meshes at the same time point, you can call mutliple times the upload_mesh function 
        Parameters
        ----------
        t : int
            The time point to set 3D data 
        obj : bytes
            The content of the 3D data
        quality : int, optional
            Which quality of the dataset
        channel : int, optional
            Which channel of the dataset
        link : string, optional 
            Do not specify this one if you don't know what you are doing !! If bundle already exist for this mesh on the server, specify it
        texture : bytes, optional
            The texture data content that will be applied to the mesh
        material : string, optional
            If texture is set, the name of the material that will be applied after applying the texure
        ttype : 
            If texture is set, the file format for the texture

        Returns
        -------
        id : int
            The id of the mesh created on the server

        Examples
        --------
        >>> #Specify a file on the hard drive by path, with rights
        >>> f = open(filepath,"r+")
        >>> #load content of file inside variable
        >>> content = f.read()    
        >>> mn.upload_mesh_at(1,content,0,0)
        >>> f.close()
        """
        if self._own_dataset():
            #First we have to upload the texture
            if texture is not None and  material is None:
                print("Please specify the material associate with the texture")
                quit()
            if texture is  None and  material is not None:
                print("Please specify the texture associate with the material")
                quit()
            if obj is None:
                print("The Object file you provided is empty or corrupted, please verify that it is correct")
                return
            id_texture=-1
            center=self._compute_center(obj)
            data=self._large_request({"uploadlargemesh":self.id_dataset,"t":t,"quality":quality,"channel":channel,"center":center,"link":link,"id_texture":id_texture},'/api/uploadlargemesh/',obj)
            data2 = json.loads(data)
            ids = -1
            if 'status' in data2: 
                print(strred(ss+'ERROR : time point not uploaded '+str(data)))
            else :
                ids = data2['id']
                print("meshes at time point "+str(t)+" uploaded ( with id "+str(ids)+' )')
                if texture is not None and material is not None:
                    data=self._large_request_image({"uploadlargetexture":self.id_dataset,"t":t,"id_mesh":ids,"quality":quality,"channel":channel,"type":ttype,"material":material},'/api/uploadtextureapi/',texture,ttype)
                    data2 = json.loads(data)
                    id_texture = -1
                    if 'status' in data2: 
                        print(strred(ss+'ERROR : texture not upload '+str(data)))
                    else :
                        id_texture = data2['id']
                        print("texture at time point "+str(t)+" uploaded ( with id "+str(id_texture)+' )')
            return ids
    def _get_URL_decompress(self,data):
        datadecomp=None
        if data is not None:
            try:
                if isinstance(data, (bytes, bytearray)):
                    data=data.decode("UTF-8")
                if "url" in data:
                    dict_str = ast.literal_eval(data)
                    if dict_str["url"] is None or dict_str["url"] == "None":
                        strred(ss+"No data found for this url")
                        return None
                    if "url" in dict_str:
                        url=dict_str["url"]
                else:
                    url=data
                if "http" not in url:
                    url="http://"+url
                #print("get mesh url : "+url)
                r = requests.get(url,verify = False)
                if url.endswith("gz"):
                    datadecomp=gzip.decompress(r.content)
                if url.endswith("bz2"):
                    datadecomp=bz2.decompress(r.content)
            except ValueError:
                print(ss+"Error failed to decompress " + str(data))
            try:
                datadecomp = str(datadecomp,'utf-8')
            except ValueError:
                a=1 #Cannot Convert
        return datadecomp
    def get_mesh_at(self,t,quality=0,channel=0):
        """ Retrieve the mesh on the server for the specified time, quality and channel
        
        Parameters
        ----------
        t : int
            The time point to get 3D data from
        quality : int, optional
            Which quality of the dataset
        channel : int, optional
            Which channel of the dataset

        Returns
        -------
        obj : string
            The 3D data for the mesh

        Examples
        --------
        >>> data = mn.get_mesh_at(1)
        """
        if self._is_dataset():
            data=self._binary_request({"getmesh":self.id_dataset,"t":t,"quality":quality,"channel":channel},'/api/getmeshapi/','GET')
            return self._get_URL_decompress(data)
        return None

    # RAW IMAGES
    def get_image_at(self,t,channel=0):
        """ Return the raw images (as a Numpy Matrix in uint8) from the server for the specified dataset
        Parameters
        ----------
        t : int
            The time point to upload raw images
        channel : int, optional
            For which channel of the dataset

        Returns
        -------
        mat : numpy
            the numpy matrix of the rawimage in uint8

        Examples
        --------
        >>> mat=mn.get_image(1)
        """
        if self._is_dataset():
            data=self._request({"id_dataset":self.id_dataset,"t":t,"channel":channel},'/api/rawimageslinkapi/','GET')
            if  not nodata(data):
                if 'url' in data and 'size' in data:
                    data_bytes=self._get_URL_decompress(data['url'])
                    size=[int(numeric_string) for numeric_string in data['size'].replace('(', '').replace(')', '').replace(' ', '').split(",")]
                    data_np=np.frombuffer(data_bytes.encode('utf-8'), dtype=np.uint8)
                    return data_np.reshape(size)
        return None
    def is_image_at(self,t,channel=0):
        """ Test is the raw images from the server for the specified dataset
        Parameters
        ----------
        t : int
            The time point to upload raw images
        channel : int, optional
            For which channel of the dataset

        Returns
        -------
        is : bool
            True if the raw image exist on the server

        Examples
        --------
        >>> mn.is_image_at(1)
        """
        if self._is_dataset():
            data=self._request({"id_dataset":self.id_dataset,"t":t,"channel":channel},'/api/containsrawimagesapi/','GET')
            if  not nodata(data):
                if 'count' in data and int(data['count'])>0:
                    return True
        return False
    def upload_image_at(self,t,rawdata,voxel_size="1,1,1",channel=0,scale=1):
        """ Upload the dataset raw images with a scale value for a specified time, channel,  
        It will erase any previous uploaded rawimages at this time point
        Parameters
        ----------
        t : int
            The time point to upload raw images
        rawdata : uint8
            The numpy array of the raw images of the dataset
        channel : int, optional
            For which channel of the dataset
        scale : float, optional
            Scale the raw images during the display to match the 3D data

        Returns
        -------
        id : int
            The id of the raw image created on the server

        Examples
        --------
        >>> im = imread(filepath) #Read your image
        >>> factor=2 #specify the rescale Factor
        >>> im=np.uint8(255*np.float32(im[::factor,::factor,::factor])/im.max())  #Convert it in 8 bits    
        >>> mn.upload_image_at(1,im,scale=factor)
        """
        if self._own_dataset():
            if not rawdata.dtype==np.uint8:
                print("Please first convert your data in uint8 ( actually in " + str(rawdata.dtype)+ " ) ")
                quit() 
            data=self._large_request({"uploadlargerawimages":self.id_dataset,"t":t,"channel":channel,"scale":scale,"voxel_size":str(voxel_size),"size":str(rawdata.shape)},'/api/uploadrawimageapi/',rawdata.tobytes(order="F"))
            data2 = json.loads(data)
            if 'status' in data2: 
                print(strred(ss+'ERROR : raw image not uploaded '+str(data)))
            else :
                print("raw image at time point "+str(t)+" uploaded ( with id "+str(data2['id'])+' )')
            return data2['id']
    def delete_images(self):
        """ Remove all the raw images from the server for the specified dataset

        """
        if self._own_dataset():
            data=self._request({"clearrawimages":self.id_dataset},'/api/clearrawimageapi/','POST')
            #data2 = json.loads(data)
            if not nodata(data):  
                print('All rawdata cleared ')
            else:
                print(strred(ss+'ERROR during raw data clear : '+str(data['error_message'])))
    def delete_image_at(self,t,channel=0):
        """ Remove the raw image of the 3D dataset on the server, but only for a specific time point and channel
        
        Parameters
        ----------
        t : int
            The time point to delete raw images
        channel : int, optional
            Which channel of the dataset

        >>> mn.delete_image_at(0)
        """
        if self._own_dataset():
            data=self._request({"deleterawimages":self.id_dataset,"t":t,"channel":channel},'/api/deleterawimageapi/','POST')
            if not nodata(data):  
                print('Rawdata cleared ')
            else:
                print(strred(ss+'ERROR during raw data clear : '+str(data['error_message'])))

    # PRIMITIVES
    def upload_mesh_with_primitive_at(self,t,obj,quality=0,channel=0):
        """ Upload a new mesh (3D data) to a specific time point, for a quality and channel given but using a primitive object
        
        Parameters
        ----------
        t : int
            The time point to store 3D data
        obj : string
            The mesh of the 3D data
        quality : int, optional
            Which quality of the dataset
        channel : int, optional
            Which channel of the dataset

        Returns
        -------
        id : int
            The id of the mesh created on the server

        Examples
        --------
        >>> 
        >>> with open('mymesh.obj','r') as f: #Specify a file on the hard drive by path, with rights
        >>>     obj = f.read()   #load mesh of the file inside variable
        >>> mn.upload_mesh_with_primitive_at(1,obj)
        """
        if self._own_dataset():
            data=self._large_request({"uploadmeshwithprimitive":self.id_dataset,"t":t,"quality":quality,"channel":channel},'/api/uploadmeshprimitiveapi/',obj)
            data2 = json.loads(data)
            if nodata(data2):
                print(strred(ss+"ERROR during upload : "+data2['error_message']))
            else :
                print("Uploaded with id : "+str(data2["result"]))     
    def upload_primitive(self,name,obj):
        """ Create a reusable 3D format instance in the database 
        
        Parameters
        ----------
        name : string
            Name of the primitive 
        obj : bytes
            The content of the primitive (3D Data)

        Returns
        -------
        id : int
            The id of the primitive created on the server

        Examples
        --------
        >>> with open('myprimitive.obj','r') as f: #Specify a file on the hard drive by path, with rights
        >>>     obj = f.read()   #load mesh of the file inside variable
        >>> mn.upload_primitive("a new primitive",obj)
        """
        if self._own_dataset():
            data=self._large_request({"uploadprimitive":self.id_dataset,"name":name},'/api/uploadprimitiveapi/',obj)
            data2 = json.loads(data)
            if 'status' in data2: 
                print(strred(ss+'ERROR : raw image not uploaded '+str(data)))
            else :
                print("Primitive "+name+" uploaded ( with id "+str(data2['id'])+' )')
            return data2['id']
    def delete_primitives(self):
        """ Clear all primitives existing for the selected dataset

        """
        if self._own_dataset():
            data=self._request({"clearprimitive":self.id_dataset},'/api/clearprimitiveapi/','POST')
           # data2 = json.loads(data)
            if not nodata(data): 
                print("Primitives all deleted")
            else:
                print(strred(ss+'ERROR during delete : '+str(data['error_message'])))
    def delete_primitive(self,name):
        """ Delete a specific primitive (specified by its name) for the selected dataset
        
        Parameters
        ----------
        name : string
            Name of the primitive 

        Examples
        -------- 
        >>> mn.delete_primitive("primitive to delete")
        """
        if self._own_dataset():
            data=self._request({"deleteprimitive":self.id_dataset,"name":name},'/api/deleteprimitiveapi/','POST')
           # data2 = json.loads(data)
            if not nodata(data): 
                print("Primitive deleted")
            else:
                print(strred(ss+'ERROR during delete : '+str(data['error_message'])))

    # INFOS
    def show_info_type(self):
        """ Display all informations type storing fomats
        
        """
        MorphoFormat={}
        MorphoFormat ["time"] = " objectID:objectID";
        MorphoFormat ["space"] = "objectID:objectID";
        MorphoFormat ["float"] = "objectID:float";
        MorphoFormat ["string"] = "objectID:string";
        MorphoFormat ["group"] = "objectID:string";
        MorphoFormat ["selection"] = "objectID:int";
        MorphoFormat ["color"] = "objectID:r,g,b";
        MorphoFormat ["dict"] = "objectID:objectID:float";
        MorphoFormat ["sphere"] = "objectID:x,y,z,r";
        MorphoFormat ["vector"] = "objectID:x,y,z,r:x,y,z,r";
        print("\nUpload Type : ")
        for s in MorphoFormat:
            print("   "+s+'->'+MorphoFormat[s])
        print('   where objectID : <t,id,ch> or <t,id> or <id>')
        print('\n')
    def get_infos(self):
        """ List all informations for the selected dataset 

        Returns
        -------
        data : list
            The list of informations

        """
        if self._is_dataset():
            data=self._request({"listinfos":self.id_dataset},'/api/correspondencelistapi/','GET')
            return data
    def upload_info(self,name,field): 
        """ Create a new information in the database 
        
        Parameters
        ----------
        name : string
            Name of the information 
        field : bytes
            The content of the infos (text Data respecting the corresponding format)

        Returns
        -------
        id : int
            The id of the information created on the server

        Examples_get_objects
        --------
        >>> #Specify a file on the hard drive by path, with rights
        >>> file = open(filepath,"r+")
        >>> #load content of file inside variable
        >>> content = f.read()    
        >>> mn.upload_info("a new info",content)
        """
        if self._is_dataset():
            tab=field.split('\n')
            nbL=0
            datatype=""
            while datatype=="" and nbL<len(tab):
                if len(tab[nbL])>0:
                    types=tab[nbL].split(":")
                    if len(types)==2 and types[0]=="type":
                        datatype=types[1]
                nbL+=1
            if datatype=="":
                self.show_info_type()
                print('You did not specify your type inside the file')
                quit()
            dtype=2 #TYPE =1 For direclty load upload and 2 for load on click
            if datatype=="time" or datatype=="group"  or datatype=="space" :
                dtype=1
            data=self._large_request({"uploadlargecorrespondence":self.id_dataset,"infos":name,"type":dtype,"datatype":datatype},'/api/uploadinfoapi/',field)
            data2 = json.loads(data)
            ids = -1
            if nodata(data2):
                print(strred(ss+'ERROR : info not uploaded '+str(data['error_message'])))
            else :
                ids = data2['result']
                print(name+" uploaded (with id "+str(ids)+')')
            return ids
    def delete_info_by_name(self,name):
        """ Delete an information specified by its name on the server
        
        Parameters
        ----------
        name : string
            Name of the information 

        Examples
        --------
        >>> mn.delete_info_by_name("information name")
        """
        if self._is_dataset():
            data=self._request({"deletecorrespondence":self.id_dataset,"infos":name},'/api/deleteinfonameapi/','POST')
            if nodata(data):
                print(strred(ss+"ERROR : Cannot delete info : "+name))
            else :
                print("Succefully deleted info : "+name)
    def delete_info_by_id(self,id_info):
        """ Delete an information specified by its id on the server
        
        Parameters
        ----------
        id : string
            id of the information

        Examples
        --------
        >>> mn.delete_info_by_id("1")
        """
        if self._is_dataset():
            data=self._request({"deletecorrespondenceid":self.id_dataset,"idinfos":id_info},'/api/deleteinfoidapi/','POST')
            if nodata(data):
                print(strred(ss+"ERROR : Cannot delete info : "+str(id_info)))
            else :
                print("Succefully deleted info : "+str(id_info))
    def get_info_by_name(self,name):
        """ Get the data of the information specified by its name
        
        Parameters
        ----------
        name : string
            Name of the information 

        Returns
        -------
        infos : bytes
            The data stored on the server

        Examples
        --------
        >>> mn.get_info_by_name("information name")
        """
        if self._is_dataset():
            data=self._binary_request({"getinfos":self.id_dataset,"infos":name},'/api/getinfonameapi/','GET')
            if isinstance(data,(bytes,bytearray)):
                new_data = None
                try :
                    new_data = data.decode("UTF-8")
                except :
                    pass
                if new_data is not None and "url" in new_data and not "None" in new_data:
                        return self._get_URL_decompress(data)
                elif new_data is None or not "url" in new_data:
                    return bz2.decompress(data)
        return None
    def get_info_by_id(self,id_info):
        """ Get the data of the information specified by its id
        
        Parameters
        ----------
        id : int
            ID of the information 

        Returns
        -------
        infos : bytes
            The data stored on the server

        Examples
        --------
        >>> mn.get_info_by_id("information name")
        """
        if self._is_dataset():
            data=self._binary_request({"getinfosid":self.id_dataset,"idinfos":id_info},'/api/getinfoidapi/','GET')
            if isinstance(data,(bytes,bytearray)):
                new_data = None
                try :
                    new_data = data.decode("UTF-8")
                except :
                    pass
                if new_data is not None and "url" in new_data and not "None" in new_data:
                        return self._get_URL_decompress(data)
                elif new_data is None or not "url" in new_data:
                    return bz2.decompress(data)
        return None
    def change_info_owner(self, info_id, new_owner_id):
        """ Update the correspondence on the server

        Parameters
        ----------
        info_id : int
            Correspondence to transfer
        new_owner_id : int
            Identifiant of the new owner
        """
        if self._is_dataset():
            data = self._request({"info_id": info_id, "new_owner_id": new_owner_id},
                                 '/api/updateinfoowner/', 'POST')
            if nodata(data):
                print(strred(ss + "ERROR : Cannot transfer ownership to : " + str(new_owner_id)))
            else:
                print("Correspondence succesfully transfered to : " + str(new_owner_id))

    def get_objects_from_info_by_id(self,id_info):
        """ Get the list of object of an information specified by its id
        
        Parameters
        ----------
        id_info : int
            ID of the infomation 

        Returns
        -------
        objects : list
            List of key/value corresponding to a split to the information data

        Examples
        --------
        >>> objetcs = mn.get_objects_from_info_by_id(1)
        """
        infos=self.get_info_by_id(id_info)
        if infos is None:
            return None
        return _get_objects(infos)
    def get_objects_from_info_by_name(self,name):
        """ Get the list of object of an information specified by its name
        
        Parameters
        ----------
        name : string
            name of the infomation 

        Returns
        -------
        objects : list
            List of key/value corresponding to a split to the information data

        Examples
        --------
        >>> objetcs = mn.get_objects_from_info_by_name("Information name")
        """
        infos=self.get_info_by_name(name)
        if infos is None:
            return None
        return _get_objects(infos)

    def share_info_by_id(self,id_info):
        """ The information specified by its id become accessible to everyone you shared it (or public if you shared the information with public)
        
        Parameters
        ----------
        id_info : int
            ID of the infomation 

        Examples
        --------
        >>> objetcs = mn.share_info_by_id(1)
        """
        if self._own_dataset():
            data=self._request({"idinfos":id_info},'/api/shareinfo/','POST')
            if nodata(data):
                print(strred(ss+"ERROR : Unable to share that information "+data['error_message']))
            else :
                print("The information has been shared")
    def unshare_info_by_id(self,id_info):
        """ The information specified by its id become unaccessible to everyone you shared it (or public if you shared the information with public)

        Parameters
        ----------
        id_info : int
        ID of the infomation 

        Examples
        --------
        >>> objetcs = mn.unshare_info_by_id(1)
        """
        if self._own_dataset():
            data=self._request({"idinfos":id_info},'/api/unshareinfo/','POST')
            if nodata(data):
                print(strred(ss+"ERROR : Unable to unshare that information "+data['error_message']))
            else :
                print("The information has been unshared")

    # CURATION
    def get_curation_by_id(self,id_info):
        """ Retrieve the curations for a information from MorphoNet
        
        Parameters
        ----------
        id_info : int
            ID of the information

        Returns
        -------
        file : string
            The curation txt file for this information

        Examples
        --------
        >>> data = mn.get_curation_by_id(1)
        """
        curation=None
        if self._is_dataset():
            data=self._binary_request({"id_dataset":self.id_dataset,"id_infos":id_info},'/api/curationfileapi/','GET')
            if data is not None:
                data = str(data,'utf-8')
                if data !=  "failed":
                    curation=data
                #    data
        if curation is None:
                print("No information currations found")
        return curation
    def get_info_curated_by_id(self,id_info):
        """ Retrieve directly the information curated from MorphoNet
        
        Parameters
        ----------
        id_info : int
            ID of the information

        Returns
        -------
        file : string
            The information with the last curation as a txt file in the MorphoNet Format

        Examples
        --------
        >>> data = mn.get_info_curated_by_id(1)
        """
        info_curated=None
        if self._is_dataset():
            info=self.get_info_by_id(id_info)
            if info is not None:
                info_objets=_get_objects(info)
                curation=self.get_curation_by_id(id_info)
                if curation is not None:
                    curation_objets=_get_objects(curation)
                    info_curated="#Infor Curated\n"
                    for line in info.split('\n'):  #Add the comments of the info 
                        if len(line)>0 and line[0]=="#":
                            info_curated+=line+"\n"

                    for line in curation.split('\n'):
                        if len(line)>0 and line[0]=="#":  #Add the comments of the curation 
                            info_curated+=line+"\n"

                    info_curated+="type:"+_get_type(info)+"\n"
                    for o in info_objets:
                        info_curated+=_get_string(o)+":"
                        if o in curation_objets:
                            oCurated=_get_last_curation(curation_objets[o])
                            info_curated+=str(oCurated.split(';')[0])
                        else:
                            info_curated+=str(info_objets[o])
                        info_curated+="\n"
                    
                    #Only Curated value
                    onlyCurated=[]
                    for o2 in curation_objets:
                        if o2 not in info_objets:
                            if o2 not in onlyCurated:
                                onlyCurated.append(o2)
                    for o2 in onlyCurated:
                        oCurated=_get_last_curation(curation_objets[o2])
                        info_curated+=_get_string(o2)+":"+str(oCurated.split(';')[0])+"\n"
                    
        return info_curated

    # ANISEED
    def get_developmental_table(self):
        """ Retrieve the corresponding developmental table of the specie of the dataset (avaible only for Ascidian )
         return the list of developmentale table information (id,id_datasettype,period,stage,developmentaltstage,description,hpf)
        """
        if self._is_dataset():
            data = self._request({"id_dataset": self.id_dataset}, '/api/aniseed/developmentalstagesapi/', 'GET')
            if nodata(data,"result"):
                return error_request(data,"requiring developmental table")
            return data["result"]
            
        return None
    def get_stages(self):
        """ Retrieve the list of stages for this specie
        FROM "anissed all stages"
        return a dictionnary with stage database id as key and  (Stage) as value
        """
        if self._is_dataset():
            data = self._request({"id_dataset": self.id_dataset}, '/api/aniseed/stageslist/', 'GET')
            if  nodata(data,"result"):
                return error_request(data,"requiring stages")
            return data["result"]
            
        return None

    # GET CELLS
    def get_cells_by_gene(self,gene_id):
        """ Retrieve the list of cells (with their expression value) for the gene passed in argument (gene id is the id inside the database)
        return a dictionnary with database id as key as value tuple containing (cell,stage,value)
        """
        if self._is_dataset():
            data = self._request({"id_dataset": self.id_dataset,"gene_id":gene_id}, '/api/aniseed/cellbygeneapi/', 'GET')
            if nodata(data,"result"):
                return error_request(data,"requiring cells by gene")
            return data["result"]
        return None
    def get_cells_by_gene_by_stage(self, gene_id,stage_id):
        """ Retrieve the list of cells (with their expression value) for the gene and the stage passed in argument (gene id and stage id are the id inside the database)
        return a dictionnary with database id as key as value tuple containing (cell,value)
        """
        if self._is_dataset():
            data = self._request({"id_dataset": self.id_dataset,"gene_id":gene_id,"stage_id":stage_id}, '/api/aniseed/cellbygenebystageapi/', 'GET')
            if nodata(data,"result"):
                return error_request(data,"requiring cells by gene by stage")
            return data["result"]
        return None

    # GET GENES
    def get_genes(self):
        """ Retrieve the list of genes for this specie
        return a list with (id,Gene Model, Gene Name, Unique Gene id)
        """
        if self._is_dataset():
            data = self._request({"id_dataset": self.id_dataset}, '/api/aniseed/geneslist/','GET')
            if nodata(data,"result"):
                return error_request(data,"requiring genes")
            return data["result"]
        return None
    def get_genes_by_cell(self,cell_name):
        """ Retrieve the list of genes (with their expression value) for the cell name in argument
        return a dictionnary with database id as key as value tuple containing (stage,gene,value)
        """
        if self._is_dataset():
            data = self._request({"id_dataset": self.id_dataset, "cell_name": cell_name}, '/api/aniseed/genebycellapi/','GET')
            if nodata(data,"result"):
                return error_request(data,"requiring genes by cell")
            return data["result"]
        return None
    def get_genes_by_stage(self,stage_id):
        """ Retrieve the list of genes (with their expression value) for the stage id  in argument
        return a dictionnary with database id as key as value tuple containing (gene,cell,value)
        """
        if self._is_dataset():
            data = self._request({"id_dataset": self.id_dataset, "stage_id": stage_id},'/api/aniseed/genebystageapi/', 'GET')
            if nodata(data,"result"):
                return error_request(data,"requiring genes by stage")
            return data["result"]
        return None
    def get_genes_by_cell_by_stage(self,cell_name,stage_id):
        """ Retrieve the list of genes (with their expression value) for the cell name and stage id in argument
        return a dictionnary with database id as key as value tuple containing (gene,value)
        """
        if self._is_dataset():
            data = self._request({"id_dataset": self.id_dataset, "cell_name": cell_name, "stage_id": stage_id}, '/api/aniseed/genebycellbystageapi/','GET')
            if nodata(data,"result"):
                return error_request(data,"requiring genes by cell by stage")
            return data["result"]
        return None

