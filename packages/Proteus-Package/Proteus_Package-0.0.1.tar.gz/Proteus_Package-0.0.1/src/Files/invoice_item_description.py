import os
import json 
from pathlib import Path
#import requests
import requests
from flask import request, make_response


class ItemDescription:
    """
    A resource for extracting invoice data using invoice2data library
    """
    def __init__(self):
        self.itemMap ={
            "FLUTIVATE CREAM 0.05 %W/W 1X10G": "AF1652",
            "Flutivate Cream": "AF1652",
            "Flutivate Skin Ointment": "AF1663",
            "FLUTIVATE OINTMENT 0.005 %W/W 1X20G": "AF1663",
            "EUMOSONE M SKIN CREAM X15G": "60000000019657",
            "Eumosone M Cream": "60000000019657",
            "BREVOXYL CREAM  4% X20G": "60000000046791",
            "Brevoxyl Cream": "60000000046791",
            "ROSUTEC 5MG TABLET 10X10": "60000000020201",
            "Rosutec 5mg Tablets": "60000000020201",
            "Zyloric 300mg Tablets": "60000000012619",
            "PHEXIN REDISYP SUSP 125MG X60ML": "60000000013805",
            "Phexin Redisyp 125mg Syrup": "60000000013805",
            "FEFOL Z CAPS X15": "60000000019664",
            "Fefol Z Capsules": "60000000019664",
            "BECADEXAMIN CAPS X30": "60000000013384",
            "Becadexamin Capsules": "60000000013384",
            "Betnesol Forte Tablets": "AG1158",
            "BETNOVATE GM SKIN CREAM 20G": "AF1345",
            "Betnovate GM Skin Cream": "AF1345",
            "BETNOVATE S SKIN OINT 20G": "AF1325",
            "Betnovate S Skin Ointment": "AF1325",
            "BETNOVATE SKIN CREAM X20G": "AF1295",
            "Betnovate Cream": "AF1295",
            "ZODERM E CREAM 1% X50G": "AF2762",
            "Zoderm E Cream": "AF2762",
            "ZIMIG CREAM 1% X10G": "60000000021942",
            "Zimig Cream": "60000000021942",
            "ZimigCream": "60000000021943",
            "Tenovate Cream 30gms": "60000000019601",
            "Neosporin H Ointment": "60000000020515",
            "Neosporin Eye Ointment": "60000000020513",
            "CALPOL SUSPENSION 250MG X60 ML": "60000000025532",
            "Calpol 250mg Suspension": "60000000025532",
            "CALPOL SUSPENSION 120MG X60 ML": "60000000028632",
            "Calpol Suspension 120mg": "60000000028632",
            "AUGMENTIN TAB 375MG X10": "60000000029345",
            "Augmentin 375mg Tablets": "60000000029345",
            "AUGMENTIN I.V. 300MG X1": "60000000013648",
            "Augmentin 300mg Intravenous": "60000000013648",
            "Neosporin H Ear Drops": "60000000020511",
            "NEOSPORIN H EAR DROPS X5ML": "60000000020511",
            "Zentel Suspension": "60000000021619",
            "ZENTEL SUSPENSION X10ML": "60000000021619",
            "Seretide Accuhaler 50/250mcg 28s": "60000000105176",
            "T-bact Cream": "AF1571",
            "Betnovate C Cream 30gm": "AF1316",
            "BETNOVATE C SKIN CREAM 30 GM TP": "AF1316",
            "Dilosyn Syrup": "60000000041003",
            "DILOSYN SYRUP X100ML": "60000000041003",
            "Eltroxin 50mg Tablets": "AG3615",
            "ELTROXIN TABS 50MCG.20X100": "AG3615",
            "Eltroxin Tabs 75mcg": "AG3721",
            "ELTROXIN TABS 75MCG 20X60": "AG3721",
            "Zyloric 100mg Tablets": "60000000012603",
            "Benitec A Tablets": "60000000020107",
            "BENITEC A TABLET 10X10": "60000000020107",
            "Eumosone Skin Cream": "60000000019658",
            "EUMOSONE SKIN CREAM 1X15G": "60000000019658",
            "Augmentin 600mg": "60000000012996",
            "Augmentin DUO 1gm Tablets": "60000000029346",
            "AUGMENTIN TAB 1G X10": "60000000029346",
            "Avamys Nasal Spray": "60000000002007",
            "AVAMYS NASAL SPRAY 0.05% 1X120SPR_IN-GSK": "60000000002007",
            "Calpol Paediatric Drops": "60000000019522",
            "CALPOL PAED DROP X15ML": "60000000019522",
            "Calpol 500mg Tablets": "60000000019529",
            "CALPOL TAB 500MG 45X15": "60000000019529",
            "Calpol T Tablets": "60000000048347",
            "Neosporin Powder": "60000000020517",
            "Piriton Expectorant 100ml -": "60000000020840",
            "Piriton Expectorant 100ml": "60000000020840",
            "PIRITON EXPECTORANT X100ML": "60000000020840",
            "Dermocalm Lotion 50ml": "60000000042523",
            "DERMOCALM LOTION X50ML": "60000000042523",
            "Dermocalm Lotion": "60000000020035",
            "Tenovate Ointment": "60000000019605",
            "TENOVATE OINTMENT X15G": "60000000019605",
            "Zimig 250mg Tablets": "60000000116510",
            "Banocide Tablets (5%)": "AG9181",
            "BANOCIDE TAB 50MG 20X20": "AG9181",
            "Betnesol Tablets": "AG1069",
            "BETNESOL TABLET 0.5MG 1X20_(72)": "AG1069",
            "Cobadex Forte Capsules": "60000000046847",
            "COBADEX FORTE CAP 20X20": "60000000046847",
            "Fesovit Capsules": "60000000021778",
            "FESOVIT SPANS CAP X30": "60000000021778",
            "Banocide Forte Tablets": "AG9341",
            "BANOCIDE FORTE TAB 100MG 20X30": "AG9341",
            "Cobadex Syrup": "60000000019861",
            "COBADEX SYRUP X120ML": "60000000019861",
            "Eltroxin 125mcg Tablets": "AG3741",
            "ELTROXIN 125MCG TABS 20X60": "AG3741",
            "Eltroxin 25mg Tablets": "AG3715",
            "ELTROXIN 25MCG TABLETS 20X60": "AG3715",
            "Eltroxin Tablets": "AG3627",
            "ELTROXIN TABLET 100MCG 1X100": "AG3627",
            "Phexin 250mg Dispersible Tabs": "60000000046870",
            "PHEXIN DISP TAB 250MG 10X10": "60000000046870",
            "Sepmax DS Tablets": "60000000021449",
            "SEPMAX DS TABLET 20X10": "60000000021449",
            "Flutibact Ointment": "AF1642",
            "FLUTIBACT OINTMENT 1X10G": "AF1642",
            "Zimivir 1000mg Tablets": "60000000012130",
            "ZIMIVIR TAB 1000MG 7X3": "60000000012130",
            "PHYSIOGEL DMT CREAM": "60000000116150",
            "PHYSIOGEL HYPOALLERGENIC DMT CREAM 1X50G": "60000000116150",
            "PHYSIOGEL HYPO. AI CREAM": "60000000116149",
            "PHYSIOGEL HYPOALLERGENIC CR AI CREAM 50G": "60000000116149",
            "SARNA LOTION": "60000000046835",
            "SARNA LOTION X60G": "60000000046835",
            "AUGMENTIN 600MG(PED)INJ##": "60000000012996",
            "CALPOL (T) TAB.H1": "60000000048347",
            "NEOSPORIN EYE OINT.": "60000000020513",
            "NEOSPORIN H OINTMENT.": "60000000020515",
            "NEOSPORIN POWDER.": "60000000020517",
            "PIRITON CS COUGH SUPPRES": "60000000020842",
            "PIRITON CS COUGH SUPPRES X100ML": "60000000020842",
            "PIRITON EXP. (BIG).": "60000000029975",
            "PIRITON EXPECTORANT X460ML": "60000000029975",
            "CCM TAB.": "60000000028618",
            "CCM TABLET 6X30": "60000000028618",
            "COBADEX CZS TAB.": "60000000042591",
            "COBADEX CZS 6X15": "60000000042591",
            "PHEXIN BD 750MG.": "60000000013810",
            "PHEXIN BD TABS 750MG 10X10": "60000000013810",
            "SUPACEF 250MG INJ": "60000000048589",
            "SUPACEF 250MG/17 ML TP X5": "60000000048589",
            "SUPACEF 750MG INJ": "10000000079425",
            "SUPACEF 750MG/17ML TP X1 IN": "10000000079425",
            "ZYLORIC 300 MGTAB": "60000000012619",
            "ZYLORIC TAB": "60000000012603",
            "SERETIDE 25/125 MCG evo.": "10000000090872",
            "SERETIDE EVO 25/125MCG 120D IN/T": "10000000090872",
            "Seretide Accu 50/250 smal": "60000000105176",
            "seretide accu 50/500 smal": "60000000105177",
            "SERETIDE ACCUH 50/500MCG 1X28D_IN/T": "60000000105177",
            "seretide accu50/100(small": "60000000105178",
            "SERETIDE ACCUH 50/100MCG 1X28D_IN/T": "60000000105178",
            "SERETIDE ACCU. 50/100": "60000000032177",
            "SERETIDE ACCUH 50/100MCG 1X60D_IN/T": "60000000032177",
            "DERMOCALM LOTION": "60000000020035",
            "DERMOCALM LOTION X100ML": "60000000020035",
            "OILATUM CREAM": "60000000042000",
            "OILATUM CREAM 40GM": "60000000042000",
            "OILATUM BAR (BIG)": "60000000046857",
            "OILATUM BAR 100G": "60000000046857",
            "STIEPROX LIQUID": "60000000046842",
            "STIEPROX LIQUID X50ML": "60000000046842",
            "T-BACT CREAM.": "AF1571",
            "TENOVATE CREAM.": "60000000019601",
            "ZIMIG 250MG TAB.": "60000000116510",
            "BETNESOL FORT TAB.": "AG1158",
            "BETNESOL INJ.": "AC1124",
            "BETNESOL INJ 1ML X80": "AC1124",
            "BETNESOL ORAL DROP.": "60000000013403",
            "BETNESOL ORAL DROPS X15ML": "60000000013403",
            "BETNESOL TAB.": "AG1069",
            "LANOXIN TAB ##": "60000000020414",
            "LANOXIN TAB 250 MCG 25X10": "60000000020414",
            "SEPTRAN ADULT TAB.": "60000000021470",
            "SEPTRAN ADULT TAB 30X10": "60000000021470",
            "SEPTRAN PED SUSPENSION.": "60000000022604",
            "SEPTRAN PAED SUSPENSION X50ML": "60000000022604",
            "SEPTRAN PED TAB.": "60000000021469",
            "SEPTRAN PAED TAB 25X10": "60000000021469",
            "BETNESOL AMP": "AC1124",
            "BETNESOL INJ 1ML X80": "AC1124",
            "BETNESOL FORTE TAB": "AG1018",
            "BETNESOL TAB": "AG1018",
            "BETNELAN TABLETS 25X20'S": "AG1018",
            "CALPOL 120MG SYP": "60000000028632",
            "CALPOL SUSPENSION 120MG X60 ML": "60000000028632",
            "CALPOL 250 SYP": "60000000025532",
            "CALPOL SUSPENSION 250MG X60 ML": "60000000025532",
            "LANOXIN T": "60000000020414",
            "LANOXIN TAB 250 MCG 25X10": "60000000020414",
            "SERETIDE ACCU 50/250": "60000000032200",
            "SERETIDE ACCUH 50/250MCG 1X60D_IN/T": "60000000032200"
        }
   
    def getItemCode(self):
        description = request.args.get('description')
        
        value = ""
        if description in self.itemMap:
            value = self.itemMap[description]
        print("value["+str(value)+"]")

        return str(value)

    def getAllItemCode(self):
        return str(self.itemMap)
   
    # Added By Pravin K on 23-DEC-20 START
    # Added By Akshay S on 26-May-2021 START   [Train WIT data]
    def getAllItemCodeList(self, data):
        print("getAllItemCodeList>>>>>>>>>>>: ")
        print("getAllItemCodeList :",type(data) )
        text = []
        print("text>>>>>>>>>>>: ",text)
        for i in range(len(data)):
            if 'dom_id' in data[i].keys():
                text.append([data[i]['descr'],data[i]['dom_id']]) # to add dom_id logic
            else:
                text.append([data[i]['descr'],i+1]) # Changed By Pravin  K on 30-MAR-21
        return text


    #Added by Akshay S [Added enterprise] 2-JUN-21
    def get_id(self,product_list,enterprise):
        print("enterprise>>>>>>",enterprise)
        print("get_id product_list:",product_list)
        result={}
        missing=[]
        
        #Added by Akshay S [Added enterprise] 2-JUN-21 START
        file_path = 'proteus_services/resources/enterprises.json'
        f = open(file_path)
        ent_data = json.load(f)
        access_token = ent_data.get(enterprise).get("access_token")
        #Added by Akshay S [Added enterprise] 2-JUN-21 END
        
        for i in range(len(product_list)):
            product=product_list[i][0]
            dom_id = product_list[i][1]
            headers={'Authorization': 'Bearer '+access_token}
            url='https://api.wit.ai/message?v=20201118&q=' + product

            r = requests.get(url, headers=headers)
            r_dict = r.json()

            intent = r_dict.get('intents',0)
            print("get_id intent:",intent)
            med_id=None
            if len(intent) != 0:
                med_id= intent[0]['name']
                confidence=intent[0]['confidence']
            if med_id !=None and confidence > 0.95:
                result[product]={"item_code":med_id, "dom_id":dom_id}
                #result[med_id]={"descr":product, "dom_id":dom_id}
            else:
                missing.append({"product":product,"dom_id":dom_id})

        print("get_id result::",result)
        print("get_id missing::",missing)
        return result,missing

    #Added by Akshay S [Added product_dict] 2-JUN-21    
    #confidence for entities to be added, what should be done if confidence is low?
    def extract_entities(self, product_dict,enterprise) :
        print("extract_entities product_dict:",product_dict,"]type[",type(product_dict),"]")
        result = []
        print("extract_entities>>>>>>")
        file_path ='proteus_services/resources/enterprises.json'
        print("file_path>>>>>>",file_path)
        f = open(file_path)
        print("f>>>>>>",f)
        ent_data = json.load(f)
        print("ent_data>>>>",ent_data)
        for i in range(len(product_dict)):
            access_token = ent_data.get(enterprise,0).get("access_token")
            print("access_token>>>>>>",access_token)
            headers = {'Authorization': 'Bearer '+access_token, 'Content-Type':'application/json'}
            url = 'https://api.wit.ai/message?v=20201118&q=' + product_dict[i]['text']

            r = requests.get(url, headers=headers)
            r_dict = r.json()
            temp_dict={}
            temp_dict['intent']=product_dict[i]['item_code']
            temp_dict['text']=product_dict[i]['text']
            if 'delivery:delivery' in r_dict['entities'].keys():
                delivery = r_dict['entities']['delivery:delivery'][0]['body']
                temp_dict['delivery']=delivery

            if 'strength:strength' in r_dict['entities'].keys():
                strength = r_dict['entities']['strength:strength'][0]['body']
                temp_dict['strength']= strength

            if 'brand:brand' in r_dict['entities'].keys():
                brand = r_dict['entities']['brand:brand'][0]['body']
                temp_dict['brand']=brand
            result.append(temp_dict)

        return result


    def convert_data(self,entity_dict):
        print("convert_data>>>>>>>>")
        print("convert_data entity_dict:",entity_dict,"]type[",type(entity_dict),"]")
        result=[]
        for i in range(len(entity_dict)):
        	#Added by Akshay S  2-JUN-21 START
            intent = entity_dict[i].get("item_code",0)
            brand=entity_dict[i].get('attr1',0)
            delivery = entity_dict[i].get('attr2',0)
            strength = entity_dict[i].get("attr3",0)
            #Added by Akshay S  2-JUN-21 END
            text = entity_dict[i].get('text',0)
            wit_dict={}
            wit_dict['text']= text
            wit_dict['entities']=[]
            wit_dict['entities'].append({"entity":"intent","value":intent})
            if brand != 0:
                print("in brand")
                brand_start = text.find(brand)
                brand_end = brand_start + len(brand)
                wit_dict['entities'].append({"entity":"attr1", "start":brand_start,"end":brand_end,"value":brand})
            if strength!= 0:
                strength_start= text.find(strength)
                strength_end= strength_start +len(strength)
                wit_dict['entities'].append({"entity": "attr2", "start": strength_start, "end": strength_end, "value": strength})
            if delivery!=0:
                delivery_start= text.find(delivery)
                delivery_end = delivery_start +len(delivery)
                wit_dict['entities'].append({"entity": "attr3", "start": delivery_start, "end": delivery_end, "value": delivery})
            result.append(wit_dict)
        return result


    #Added by Akshay S [Added enterprise] 2-JUN-21 START
    def train_wit(self, data, enterprise):
        print("Starting1>>>>>>>>>>")
        print("enterprise>>>>>>>>>>",enterprise)
        file_path = 'proteus_services/resources/enterprises.json'
        print("file_path>>>>>>>>>>",file_path)
        f = open(file_path)
        print("f>>>>>>>>>>",f)
        ent_data = json.load(f)
        print("ent_data>>>>>>>>>>",ent_data)

        try:

            print(str(ent_data[enterprise]))
            
            access_token = ent_data[enterprise]['access_token']
            print("access_token>>>>>>>>>>",access_token)
            headers={'Authorization': 'Bearer '+access_token,'Content-Type': 'application/json'}
            print("headers>>>>>>>>>>",headers)
            url='https://api.wit.ai/samples?v=20170307'
            for i in range(len(data)):
                print("Starting3>>>>>>>>>>")
                intent=data[i].get('intent')
                print("intent>>>>>>>>>>",intent)
                intent_data= {"name":intent}
                print("intent_data>>>>>>>>>>",intent_data)
                x= requests.post(url='https://api.wit.ai/intents?v=20200513',headers=headers,data=json.dumps(intent_data))
                print("x>>>>>>>>>>",x)
                if x.status_code!=200: 
                    print(x.text)
                    print("intent creation error (intent may already exist)")  
            print(json.dumps(data))
            r = requests.post(url,data=json.dumps(data), headers=headers)
            print("r>>>>>>>>>>",r)  
            print(r.text)
        except:
            print("Could not retrieve wit access token for "+enterprise)  
        return r.status_code

    def create_wit_app(self,enterprise):
        print("Started")
        url = 'https://api.wit.ai/apps?v=20200513'
        headers = {'Authorization': 'Bearer R3C6Q3LWDL3SAUXJC5WW7AQ2AYGJJYIL', #Default Token used only to create new apps
               "Content-Type": "application/json"}
        data = {"name":enterprise, "lang": "en",
            "private": True,
            "timezone": "Asia/Kolkata"}
        print("Started step1>>>>>>>>>>>")

        x = requests.post(url, headers=headers, data=json.dumps(data))
        print("Started step2>>>>>>>>>>>")
        if x.status_code==200:
            data = x.json()
            print("Started step3>>>>>>>>>>>")
            f = open('proteus_services/resources/enterprises.json')
            enterprise_dict = json.load(f)
            print("Started step4>>>>>>>>>>>")
            enterprise_dict[enterprise] = data
            print("Started step5>>>>>>>>>>>")
            with open('proteus_services/resources/enterprises.json', "w") as outfile:
                json.dump(enterprise_dict, outfile)
            return 200
        else:
            return 400 

    def create_entities(self,enterprise,no_of_entities):
        print("create_entities>>>>>>")
        file_path ='proteus_services/resources/enterprises.json'
        print("file_path>>>>>>",file_path)
        f = open(file_path)
        print("f>>>>>>",f)
        ent_data = json.load(f)
        print("ent_data>>>>",ent_data)
        try:
            access_token = ent_data.get(enterprise,0).get("access_token")
            print("access_token>>>>>>",access_token)
            url= 'https://api.wit.ai/entities?v=20200513'
            headers={'Authorization': 'Bearer '+access_token,
                     'Content-Type':'application/json'}
            for i in range(int(no_of_entities)):
                entity = 'attr' +str(i+1)
                print("entity>>>>>>",entity)
                data={"name":entity,"roles":[]}
                print("data>>>>>>",data)
                print("data",data)
                x=requests.post(url,data=json.dumps(data),headers=headers)
                print("entity creation: ",x.text)
                if x.status_code!=200:
                    print('entity creation error')
        except Exception as e:
            print("create entities exception:",e)
            print("Could not retrieve wit access token for "+enterprise)


    # Added By Akshay S on 26-May-2021 END   [Train WIT data]
    # Added By Pravin K on 23-DEC-20 END