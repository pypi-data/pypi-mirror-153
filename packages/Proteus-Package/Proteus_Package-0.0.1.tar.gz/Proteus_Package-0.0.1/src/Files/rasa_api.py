from .rasa_id_interpreter import Rasa_id_interpreter
import subprocess, glob, os, shutil, tarfile, json

    ##### Create new rasa directory #####
class Rasa:


    @staticmethod
    def init_rasa( enterprise):
        print("init_rasa enterprise[",enterprise,"]")
        command = "mkdir proteus_services/resources/clients/"+enterprise+"|mkdir proteus_services/resources/clients/"+enterprise+"/data"+"|mkdir proteus_services/resources/clients/"+enterprise+"/models"
        os.system(command)


    ##### Train API #####
    @staticmethod
    def create_model(enterprise):
        print("create_model::enterprise[",enterprise,"]") 
        os.system("rasa train --data proteus_services/resources/clients/"+enterprise+"/data/nlu.json --out clients/"+enterprise+"/models")#company1


    @staticmethod
    def export_model(enterprise):
        print("export_model::enterprise[",enterprise,"]")
        file_path= 'proteus_services/resources/clients/'+enterprise+'/models/'
        list_of_files = glob.glob(file_path+'*.tar.gz')  # * means all if need specific format then *.csv
        latest_file = max(list_of_files, key=os.path.getctime)
        print("latest:",latest_file)
        latest_file_name = latest_file.split(file_path)[1]
        my_tar = tarfile.open(latest_file)
        my_tar.extractall(file_path+"models/"+latest_file_name)  # specify which folder to extract to
        my_tar.close()

    @staticmethod
    def convert_data(data):
        result = []
        for i in range(len(data)):
            numb_of_attr = int(data[i].get("no_of_attr"))
            attr=[]
            for j in range(numb_of_attr):
                attr_key = 'attr'+ str(j+1) #attr1,attr2,attr3..
                attr.append(data[i].get(attr_key, 0))
            text = data[i].get('descr', 0)
            rasa_dict = {}
            rasa_dict['text'] = text
            rasa_dict['intent'] = data[i].get("id", 0)
            rasa_dict['entities'] = []
            for value in range(len(attr)):
                if attr[value] !=0:
                    attr_key = 'attr'+ str(value+1)
                    attr_start = text.find(attr[value])
                    attr_end = attr_start + len(attr[value])
                    rasa_dict['entities'].append(
                        {"entity": attr_key, "start": attr_start, "end": attr_end, "value": attr[value]})
            result.append(rasa_dict)

        print("convert_data::result:",result)
        return result
    @staticmethod
    def format_rasa_data(self, data):
        converted_dict={}
        result = self.convert_data(data)
        converted_dict['rasa_nlu_data']={}
        converted_dict['rasa_nlu_data']['common_examples']=result
        converted_dict['rasa_nlu_data']['entity_synonyms']=[]
        print("format_rasa_data::format_rasa_data:",converted_dict)
        return converted_dict

    @staticmethod
    def export_train_data(converted_data,enterprise):
        print("export_train_data::converted_data[",converted_data,"]enterprise[",enterprise,"]") 
        os.system("pwd")
        with open("proteus_services/resources/clients/"+enterprise+"/data/nlu.json", "w") as outfile:
            json.dump(converted_data, outfile)


    @staticmethod
    def modify_train_data(self, new_data, enterprise):
        print("In modify_train_data[",new_data,"]enterprise[",enterprise,"]") 
        f = open('proteus_services/resources/clients/'+enterprise+'/data/nlu.json')
        data = json.load(f)
        product_data = new_data['product_data']
        synonym_data = new_data.get('synonym_data',0)
        print(synonym_data)
        converted_data = self.convert_data(product_data)
        for i in range(len(converted_data)):
            data['rasa_nlu_data']['common_examples'].append(converted_data[i])
        if synonym_data!=0:
            for value in synonym_data.keys():
                flag=0
                for j in range(len(data['rasa_nlu_data']['entity_synonyms'])):
                    if(value==data['rasa_nlu_data']['entity_synonyms'][j]['value']):
                        flag=1
                        data['rasa_nlu_data']['entity_synonyms'][j]['synonyms'].append(synonym_data[value])
                if flag==0:
                    new_synonym = {"value":value,"synonyms":synonym_data[value]}
                    data['rasa_nlu_data']['entity_synonyms'].append(new_synonym)
        self.export_train_data(data,enterprise)

            ##### Predict API #####
    @staticmethod
    def get_prediction(product_list ,attr_count,enterprise):
        print("get_prediction :: product_list[",product_list,"],attr_count[",attr_count,"]")
        rasa_id_interpreter = Rasa_id_interpreter()
        return rasa_id_interpreter.extract_entities(rasa_id_interpreter,product_list,attr_count,enterprise)