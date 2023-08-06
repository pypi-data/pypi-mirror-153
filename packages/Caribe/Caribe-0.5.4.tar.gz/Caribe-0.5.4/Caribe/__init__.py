# Author: Keston Smith
# Library: Caribe 
# Contact: keston.smith@my.uwi.edu
#Copyright: MIT 2021
from asyncio import wait_for
from gingerit.gingerit import GingerIt
import re
import nltk
from nltk import *
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import json
import requests
import time


caribedict = {
     
  "Know how long meen see you" : "I have not seen you in a long time",
  "Oo monsta" : "What's up",
  "Eyyy, look who" : "long time no see friend" ,
  "my g":"my friend",
  "Wais d word dawg":"what's up bro",
  "wam dawg": "how are you?",
  "everyting cool" : "how is everything",
  "wais d order": "What's up",
  "O dawg":"What's up",
  "Ah wah": "I want",
  "waz de scene": "How are you",
  "waz d scn":"How are you",
  "waz de scn":"How are you",
  "waz d scene":"How are you",
  "waz di scene":"How are you",
  "waz di scn":"How are you",
  "waiz d scn": "How are you",
  "waiz de scene": "How are you",
  "waiz d scene": "How are you",
  "waiz d scn":"How are you",
  "come nah boi": "I am being serious",
  "wais d scn": "How are you",
  "wais de scn":"How are you",
  "wais de scene": "How are you",
  "wais d scene": "How are you",
  "wuz de scene":"How are you?",
  "wuz d scene":"How are you?",
  "wuz d scn":"How are you?",
  "wuz de scn": "How are you?",
  "Father lawd": "Jesus help me", 
  "Skinnin yuh teet":"grinning",
  "Skinnin yuh teeth":"grinning",
  "Tabanca": "still holding feelings",
  "allyuh":"Everybody",
  "chupid": "stupid",
  "dotish": "stupid",
  "chupidee": "stupid",
  "fone":"phone",
  "tick":"thick",
  "wais":"what is",
  "crapo": "Frog",
  "trinbago": "Trinidad and Tobago",
  "dias":"that is",
  "lix" : "beating",
  "ent": "Is that not so?",
  "fed up": "tired",
  "preshah": "pressure",
  "presha": "pressure",
  "ahse": "ass",
  "arse":"ass",
  "wajang":"roudy",
  "tief":"thief",
  "hush": "quiet",
  "wat":"what",
  "oi": "Hello",
   "d" : "the",
  "whey":"where",
  "whey yuh say": "can you repeat?",
  "you an all":  "You too?",
  "you so": "people like you",
  "yuh makin joke":  "you can't be serious",
  "yuh look fuh dat": "it is your fault",
  "boldface": "ignorant",
  "bolface": "ignorant",
  "bacchanal":"confusion", 
  "liming": "hanging out",
  "hambug":"pester",
  "ting":"thing",
  "tanty":"aunty",
  "tantie":"aunty",
  "gyul": "girl",
  "gyal": "girl",
  "horn":"cheat",
  "wifey":"wife",
  "dey" : "they",
  "Yo": "Hi",
  "Yoo": "Hi",
  "Yooo": "Hi",
  "dis":"this",
  "wah": "want",
  "meh": "me",
   "waiz" : "what is",
   "moda":"mother",
   "modda" : "mother",
   "muda":"mother",
   "mudda":"mother",
  "fadda" : "father",
  "fada" : "father",
  "faddah": "father",
  "brodda": "brother",
  "broda": "brother",
  "dougla": "mixed race person",
  "backchat":"talks",
  "boi" : "boy",
  "yuh": "you",
  "tho":"though",
  'Ah' : 'I',
  "doh": "do not",
  'ah':'i',
  "eh" : "ain't",
  "cah": "cannot",
  "fuh":"for",
  "dat": "that",
  "waz": "was",
  "dah": "that",
  "nah": "no",
  "de": "the",
  "rel": "very",
  "mi": "my",
  "yh":"yes",
  "dias":"that is",
  "waiz":"what",
  "mi": "my",
  "ah": "I",
  "Eyyy":"Hey",
  "Eyy":"Hey",
  "Ey": "Hey",
  "Yo":"Hi",
  "Yoo": "Hi",
  "Oooo": "Hi",
  "Oo":"Hi",
  "cud":"could",
  "g":"friend",
  "dat": "that",
  "dawg":"friend",
  "iz":"is",
  "weh":"where",
  "y":"why",
  "shud":"should",
  "shudda": "should of",
  "cudda": "could of",
  "cuda": "could of",
  "boi":"boy",
  "bai":"boy",
  "aye":"hey",
  "nah":"no",
  "hv":"have",
  "wais":"what is",
  "waiz":"what is",
  "orhor":"alright",
  "wen":"when",
  "di": "the",
  "alyuh":"everyone",
  "gyal":"girl",
  "bout":"about",
  "mins":"minutes",
  "hrs":"hours",
  "hr":"hour",
  "dem":"them",
  "gud":"good",
  "yunno":"you know",
  "tho":"though",
  "Ik":"I know",
  "ik":"I know",
  "doh":"don't",
  "doe":"don't",
  "gosh":"god",
  "hardlucks":"sorry",
  "daz":"that is",
  "issa":"is a",
  "jusso":"just so",
  "cah":"can not",
  "ite":"alright",
  "aite":"alright",
  "rn":"right now",
  "smallie":"girl",
  "lova":"lover",
  "laterz":"later",
  "buh":"but",
  "lawd":"lord",
  "gawd":"god",
  "fren":"friend",
  "oh gosh":"oh my god",
  "lol":"haha",
  "Idk":"I don't know",
  #"n":"and",
  "prolly":"probably",
  "tryna":"try to",
  "sis":"sister",
  "sista":"sister",
  "sistas":"sisters",
  "cuz":"cause",
  "inno":"you know",
  "enno":"you know",
  "da":"that",
  "inna": "in a",
  "wok":"work",
  "wuk":"work",
  "sen":"send",
  "cyah":"can't",
  "sickenin":"annoying",
  "bcuz":"because",
  "bcus":"because",
  "cus":"cause",
  "cuz":"cause",
  "baigan":"eggplant",
  "manicou":"opossum",
  "hoss":"friend",
  "weys":"wow",
  "bess":"sexy",
  "ah lime": "a get together",
  "ey":"hey",
  "di":"the",
  "wam":"what happen",
  "wudda":"would of",
  "wuda":"would of",
  "hadda": "had to",
  "cudda":"could of",
  "hada":"had to",
  "wud":"would",
  "dese":"these",
  "tuh":"to",
  "den":"then",
  "lemme":"let me",
  "enuff":"enough",
  "enuf":"enough",
  "lewwe":"let we",
  "bouf":"scold",
  "wit":"with",
  "wid":"with",
  "mih":"my",
  "mihself":"myself",
  "Imma":"I am a",
  "muh":"my",
  "skool":"school",
  "maco":"eavesdrop",
  "macoing":"eavesdropping",
  "awa":"or what",
  "bambam":"buttocks",
  "blasted":"damn",
  "breds":"brethren",
  "bredda":"brother",
  "daz":"that is",
  "dutty":"dirty",
  "duttyness":"dirtyness",
  "nuttin":"nothing",
  "neva":"never",
  "snat":"snot",
  "snatty":"snotty",
  "tambran":"tamarind",
  "wham":"what happen",
  "wuddy":"what the",
  "widdi":"what the",
  "zaboca":"avacado",
  "manicou":"opposum",
  "magga":"very skinny",
  "gimme":"give me",
  "boof":"scold",
  "chook":"pierce",
  "sumn":"something",
  "srs":"serious",
  "wey":"where",
  "weys":"wow",
  "weyss":"wow",
  "yeah":"yes",
  "weh":"where",
  "bwoy":"boy",
  "deh":"there",
  "daht":"that",
  "topdawg":"friend",
  "top dawg":"friend",
  "hld":"hold",
  "tnx":"thanks",
  "dont":"don't",
  "wont":"won't",
  "trini":"trinidadian",
  "widdi":"what the",
  "wid":"with",
  "wajang":"ghetto",
  "vex":"angry",
  "diaz":"that is",
  "gih":"give",
  "leh":"let",


  
  

}
splitdict = {
  "waz":"was",
  "dawg": "friend",
  "topdawg": "friend",
  "d":"the",
  "y":"why",
  "dese":"these",
  "Tabanca": "still holding feelings",
  "allyuh":"Everybody",
  "chupid": "stupid",
  "dotish": "stupid",
  "chupidee": "stupid",
  "fone":"phone",
  "tick":"thick",
  "crapo": "Frog",
  "trinbago": "Trinidad and Tobago",
  "dias":"that is",
  "lix" : "beating",
  "ent": "Is that not so?",
  "fed up": "tired",
  "preshah": "pressure",
  "presha": "pressure",
  "ahse": "ass",
  "wajang":"roudy",
  "tief":"thief",
  "oi": "Hello",
   "d" : "the",
  "hush": "quiet",
  "whey":"where",
  "arse":"ass",
  "boldface": "ignorant",
  "bolface": "ignorant",
  "bacchanal":"confusion", 
  "liming": "hanging out",
  "hambug":"pester",
  "ting":"thing",
  "tanty":"aunty",
  "tantie":"aunty",
  "gyul": "girl",
  "gyal": "girl",
  "horn":"cheat",
  "Yo": "Hi",
  "Yoo": "Hi",
  "iz":"is",
  "Yooo": "Hi",
  "dis":"this",
  "wah": "want",
  "meh": "me",
  "waiz" : "what is",
  "wais": "what is",
  "modda" : "mother",
  "muda":"mother",
  "mudda":"mother",
  "fadda" : "father",
  "fada" : "father",
  "faddah": "father",
  "brodda": "brother",
  "broda": "brother",
  "dougla": "mixed race person",
  "backchat":"talks",
  "boi" : "boy",
  "yuh": "you",
  "tho":"though",
  "dey" : "they",
  "Ah" : "I",
  "doh": "do not",
  "ah":"i",
  "eh" : "ain't",
  "cah": "cannot",
  "cah":"can not",
  "fuh":"for",
  "dat": "that",
  "waz": "was",
  "dah": "that",
  "nah": "no",
  "de": "the",
  "scene":"weather",
  "rel": "very",
  "waiz":"what is",
  "mi": "my",
  "ah": "I",
  "Eyyy":"Hey",
  "Eyy":"Hey",
  "Ey": "Hey",
  "Yo":"Hi",
  "Yoo": "Hi",
  "g":"friend",
  "iz":"is",
  "Oooo": "Hi",
  "cud":"could",
  "wais":"what is",
  "dat": "that",
  "meh":"my",
  "cud":"could",
  "weh":"where",
  "y":"why",
  "wat":"what",
  "wa":"what",
  "wen":"when",
  "di": "the",
  "shud":"should",
  "cudda": "could of",
  "cuda": "could of",
  "boi":"boy",
  "sickenin":"annoying",
  "bai":"boy",
  "aye":"hey",
  "nah":"no",
  "wais":"what is",
  "waiz":"what is",
  "orhor":"alright",
  "alyuh":"everyone",
  "gyal":"girl",
  "bout":"about",
  "mins":"minutes",
  "hrs":"hours",
  "hr":"hour",
  "dem":"them",
  "gud":"good",
  "yunno":"you know",
  "tho":"though",
  "Ik":"I know",
  "ik":"I know",
  "doh":"don't",
  "doe":"don't",
  "gosh":"god",
  "hardlucks":"sorry",
  "daz":"that is",
  "issa":"is a",
  "jusso":"just so",
  "ite":"alright",
  "aite":"alright",
  "rn":"right now",
  "smallie":"girl",
  "lova":"lover",
  "laterz":"later",
  "buh":"but",
  "lawd":"lord",
  "gawd":"god",
  "fren":"friend",
  "oh gosh":"oh my god",
  "lol":"haha",
  "Idk":"I don't know",
  #"n":"and",
  "prolly":"probably",
  "tryna":"try to",
  "sis":"sister",
  "sista":"sister",
  "sistas":"sisters",
  "cuz":"cause",
  "inno":"you know",
  "enno":"you know",
  "da":"that",
  "inna": "in a",
  "sen":"send",
  "cyah":"can't",
  "bcuz":"because",
  "bcus":"because",
  "wok":"work",
  "wuk":"work",  
  "cus":"cause",
  "cuz":"cause",
  "baigan":"eggplant",
  "manicou":"opossum",
  "hoss":"friend",
  "weys":"wow",
  "bess":"sexy",
  "ah lime": "a get together",
  "ey":"hey",
  "di":"the",
  "wam":"what happen",
  "wudda":"would of",
  "wuda":"would of",
  "hadda": "had to",
  "cudda":"could of",
  "hada":"had to",
  "wud":"would",
  "tuh":"to",
  "den":"then",
  "lemme":"let me",
  "enuff":"enough",
  "enuf":"enough",
  "lewwe":"let we",
  "bouf":"scold",
  "wit":"with",
  "wid":"with",
  "mih":"my",
  "mihself":"myself",
  "Imma":"I am a",
  "muh":"my",
  "skool":"school",
  "maco":"eavesdrop",
  "macoing":"eavesdropping",
  "awa":"or what",
  "bambam":"buttocks",
  "blasted":"damn",
  "breds":"brethren",
  "bredda":"brother",
  "daz":"that is",
  "dutty":"dirty",
  "duttyness":"dirtyness",
  "nuttin":"nothing",
  "neva":"never",
  "snat":"snot",
  "snatty":"snotty",
  "tambran":"tamarind",
  "wham":"what happen",
  "wuddy":"what the",
  "widdi":"what the",
  "zaboca":"avacado",
  "manicou":"opposum",
  "magga":"very skinny",
  "gimme":"give me",
  "boof":"scold",
  "chook":"pierce",
  "sumn":"something",
  "srs":"serious",
  "wey":"where",
  "weys":"wow",
  "weyss":"wow",
  "yeah":"yes",
  "weh":"where",
  "bwoy":"boy",
  "top dawg":"friend",
  "deh":"there",
  "daht":"that",
  "hld":"hold",
  "tnx":"thanks",
  "dont":"don't",
  "wont":"won't",
  "trini":"trinidadian",
  "hv":"have",
  "widdi":"what the",
  "wid":"with",
  "wajang":"ghetto",
  "vex":"angry",
  "gih":"give",
  "diaz":"that is",
  "gih":"give",
  "leh":"let",
  

  
}


phrasedict = {
  "whey yuh say": "can you repeat?",
  "Oh geed":"That is disgusting",
  "you an all": "You too?",
  "you so": "people like you",
  "yuh makin joke":  "you can't be serious",
  "yuh look fuh dat": "it is your fault",
  "ah wah": "I want",
  "laterz dey":"Goodbye",
  "laters dey":"Goodbye",
  "waz de scene": "How are you",
  "come nah boi": "I am being serious",
  "Father lawd": "Jesus help me", 
  "Skinnin yuh teet":"grinning",
  "Skinnin yuh teeth":"grinning",
  "Tabanca": "still holding feelings",
  "Wah foolishness is this" : "that was foolish",
  "Know how long meen see you" : "I have not seen you in a long time",
  "Oo monsta" : "What's up",
  "Eyyy, look who" : "long time no see friend" ,
  "My g":"my friend",
  "Wais d word dawg":"what's up bro",
  "wam dawg": "how are you?",
  "everyting cool" : "how is everything",
  "wais d order": "What's up",
  "wais d order": "What's up",  
  "ah wah": "I want",
  "waz de scene": "How are you",
  "waz d scn":"How are you",
  "waz de scn":"How are you",
  "waiz d scn": "How are you",
  "waiz de scene": "How are you",
  "waiz d scene": "How are you",
  "come nah boi": "I am being serious",
  "wais d scn": "How are you",
  "wais de scene": "How are you",
  "wais d scene": "How are you"

}



class POS_TAG:
    texts:str
    def __init__(self, sentence:str):
        self.sentence = sentence
        self.sentence = nltk.pos_tag(nltk.word_tokenize(self.sentence), lang="eng")
        
    def pos_report(self):
        return(self.sentence)
    

class Parser:
    def __init__(self, sentence:str):
        self.sentence =sentence
        self.correction = self
        tokenizer = AutoTokenizer.from_pretrained("KES/T5-TTParser")
        model = AutoModelForSeq2SeqLM.from_pretrained("KES/T5-TTParser")
        
        inputs = tokenizer("grammar:"+self.sentence, truncation=True, return_tensors='pt')
        output = model.generate(inputs['input_ids'], num_beams=7, max_length=512, early_stopping=True)
        self.correction=tokenizer.batch_decode(output, skip_special_tokens=True)
        
    
    def TT_Parser(self):
        return "".join(self.correction)
    
    def TTparser_api(self):
        try:
            API_TOKEN = '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'
            API_URL = "https://api-inference.huggingface.co/models/KES/T5-TTParser"
            headers = {"Authorization": f"Bearer {API_TOKEN}"}
            txt="grammar:"+self.sentence
            data = json.dumps({"inputs":txt, "options": {"wait_for_model": True}})
            response = requests.request("POST", API_URL, headers=headers, data=data)
            if response.status_code==503: # This is prevent KeyErrors and Model loading Errors
                timetowait = response.json()['estimated_time']
                time.sleep(timetowait)
                data = json.loads(data)
                data["options"] = {"wait_for_model": True}
                data = json.dumps(data)
                response = requests.request("POST", API_URL, headers=headers, data=data)
        
            correction=json.loads(response.content.decode("utf-8"))
            return correction[0]['generated_text']

        except KeyError:
            return correction[0]['generated_text']




class nlp:
    def __init__(self):
        pass
    def caribe_pos(self, text:str):
     
        x = []
        full =[]
        
        status:int = 0
        
        for word in text.split():
            for items in splitdict:
                if word not in x:
                    if re.findall(r'\b%s\b' %word, items):
                        holder=nltk.pos_tag(caribe_word_tokenize(splitdict[items]), lang="eng")  
                        s1 ="".join(map(str, holder))
                        s1= s1.replace(splitdict[items], word)
                        x.append(eval(s1))
                        holder.clear()
                        break
                    
                    elif splitdict.get(word) is None:
                        holder=nltk.pos_tag(caribe_word_tokenize(word), lang="eng")  
                        s1 ="".join(map(str, holder))
                        x.append(eval(s1))
                        holder.clear()
                        break
                        
        return x 

class dict_generate:
    _dialect = []
    _standard = []

    def __init__(self):
        for words in splitdict:
            xar = words
            yar = splitdict[words]
            if xar not in self._dialect:
                self._dialect.append(xar)

            self._standard.append(yar)
        

    def generate_dictionary(self):
        df = pd.DataFrame({'Dialects':self._dialect,'Standard':self._standard})
        df.to_csv("Dictionary.csv", index=False, encoding='utf-8')

class file_encode:
    _data = []
    _out = []
    def __init__(self, filename:str, encode_filetype:str):
        self.filename = filename
        self.filetype = encode_filetype
        __mode = "r+"
        self.file = open(self.filename, __mode, encoding='utf-8') 

        for _ in self.file:
            self._data.append(_)
        for __ in self._data:
            encode = trinidad_encode(__)
            self._out.append(encode)
        self.file.close()
    
        if (self.filetype == "text" or self.filetype == "txt"):
            if (self.filename.endswith(".txt")):
                self.output = open("Translated.txt", "w")
                for x in self._out:
                    self.output.write(x)
                self.output.close()
            else:
                raise TypeError("filename type  and encode filetype mismatch")

        elif (self.filetype == "json"):
            if (self.filename.endswith(".json")):
                self.output = open("Translated.json", "w")
                for x in self._out:
                    self.output.write(x)
                self.output.close()
            else:
                raise TypeError("filename type  and encode filetype mismatch")

        elif(self.filetype == "csv"): 
            if (self.filename.endswith(".csv")):
                self.output = open("Translated.csv", "w")
                for x in self._out:
                    self.output.write(x)
                self.output.close()
            else:
                raise TypeError("filename type  and encode filetype mismatch")   

        else: 
            raise TypeError("filetype options only include 'text', 'json', 'xlsx' or 'csv'")

def trinidad_decode(sentence:str):
    sentence=sentence.lower()
    sentence = " " + sentence 

    for x in caribedict:
        if sentence.find(x):
            sentence = re.sub(r'\b%s\b' %x, caribedict[x], sentence)
    return sentence.strip()


def phrase_decode(sentence:str):
    sentence=sentence.lower()
    sentence = " " + sentence
    for x in phrasedict:
        if sentence.find(x):
            sentence=sentence.replace(x, phrasedict[x])
    return sentence.strip()


def trinidad_decode_split(sentence:str):
    sentence= sentence.lower()

    for subs in sentence.split():
        if subs in splitdict: 	
            sentence = sentence.replace(subs, str(splitdict[subs.lower()]))
    return sentence

def t5_kes_corrector(sentence:str):
    tokenizer = AutoTokenizer.from_pretrained("KES/T5-KES")
    model = AutoModelForSeq2SeqLM.from_pretrained("KES/T5-KES")
    
    inputs = tokenizer("grammar:"+sentence, truncation=True, return_tensors='pt')
    output = model.generate(inputs['input_ids'], num_beams=4, max_length=512)
    correction=tokenizer.batch_decode(output, skip_special_tokens=True)
    return "".join(correction)

API_TOKEN = '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'
API_URL = "https://api-inference.huggingface.co/models/KES/T5-KES"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def t5_kes_api_corrector(sentence:str):
    txt="grammar:"+ sentence
    data = json.dumps({"inputs":txt, "options": {"wait_for_model": True}})
    response = requests.request("POST", API_URL, headers=headers, data=data)
    if response.status_code==503: # This is prevent KeyErrors and Model loading Errors
        timetowait = response.json()['estimated_time']
        time.sleep(timetowait)
        data = json.loads(data)
        #data['options'] = {'wait_for_model': True}
        data = json.dumps(data)
        response = requests.request("POST", API_URL, headers=headers, data=data)
        
    correction=json.loads(response.content.decode("utf-8"))
    return correction[0]['generated_text']
    

    
def caribe_corrector(sentence:str):
    tokenizer = AutoTokenizer.from_pretrained("KES/T5-KES")
    model = AutoModelForSeq2SeqLM.from_pretrained("KES/T5-KES")
    inputs = tokenizer("grammar:"+sentence, truncation=True, return_tensors='pt')
    output = model.generate(inputs['input_ids'], num_beams=4, max_length=512)
    correction=tokenizer.batch_decode(output, skip_special_tokens=True)
    return "".join(correction)

def gingerit_corrector(sentence:str):
    parser = GingerIt()
    sentence = parser.parse(sentence)
    sentence = sentence['result']
    return str (sentence)

def remove_signs(sentence:str)->str:
    stop_signs = ['!', ".", "%", '"', "'", "`", "*", "&", ",", "-", "+", "/", "'\'", "?", ";", ":", "$", "%", "#", "@", "=", "-", "~", "(", ")", "[", "]" ]
    for signs in stop_signs:
        sentence = sentence.replace(signs, "")
    return sentence

def caribe_word_tokenize(sentence:str):
    sentence = remove_signs(sentence)
    sentence = re.split("\s", sentence)
    return sentence

def trinidad_direct_translation(sentence:str):
    decoded=trinidad_decode(sentence)
    new_sentence=t5_kes_corrector(decoded)
    return new_sentence


def trinidad_encode(sentence:str):
    sentence=sentence.lower()
    #sentence = " " + sentence 
    for words in caribedict:
        if caribedict[words].lower() in sentence:
            sentence = re.sub(r'\b%s\b' %caribedict[words].lower(), words, sentence)
    return sentence



