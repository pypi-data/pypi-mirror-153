
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT) ![PyPI](https://img.shields.io/pypi/v/Caribe) [![Transformer](https://img.shields.io/badge/Transformer-T5-blue.svg)](https://huggingface.co/docs/transformers/model_doc/t5) [![Pandas](https://img.shields.io/badge/Pandas-1.3.4-green.svg)](https://pandas.pydata.org/) [![AI](https://img.shields.io/badge/AI-Artifical_Intelligence-blue.svg)]() [![happytransformers](https://img.shields.io/badge/happytransformers-2.4.0-blue.svg)](https://happytransformer.com/) [![Python 3+](https://img.shields.io/badge/python-3+-blue.svg)]() [![NLP](https://img.shields.io/badge/nlp-natural_language_processing-blue.svg)]() [![T5-KES](https://img.shields.io/badge/T5-T5_KES-red.svg)](https://huggingface.co/KES/T5-KES) [![T5-TTParser](https://img.shields.io/badge/T5-TTParser-aqua.svg)](https://huggingface.co/KES/T5-TTParser)

<p align="center">
<img src="https://github.com/KestonSmith/CaribeLogo/raw/master/CaribeLOGO.png" title="Caribe">


</p>

# Caribe 




>This python library takes Trinidadian English Creole and converts it to Standard English.
Future updates would include the conversion of other Caribbean English Creole languages to Standard English and additional natural language processing methods.

____
## Installation
Use the below command to install package/library
```
pip install Caribe 

```
____
 ## Usage
 > Sample 1: Checks the english creole input against existing known creole phrases before decoding the sentence into a more standardized version of English language. A corrector is used to check and fix small grammatical errors.
```python
# Sample 1
import Caribe as cb


sentence = "Dey have dey reasons"
standard = cb.phrase_decode(sentence)
standard = cb.trinidad_decode(standard)
fixed = cb.caribe_corrector(standard)
print(fixed) #Output: They have their reasons.

```
>Sample 2: Checks the trinidad english creole input against existing known phrases
```python
# Sample 2 
import Caribe as cb


sentence = "Waz de scene"
standard = cb.phrase_decode(sentence)

print(standard) # Outputs: How are you

```
>Sample 3: Checks the sentence for any grammatical errors or incomplete words and corrects it.
```python
#Sample 3
import Caribe as cb


sentence = "I am playin fotball outsde"
standard = cb.caribe_corrector(sentence)

print(standard) # Outputs: I am playing football outside

```
>Sample 4: Makes parts of speech tagging on creole words.
```python
#Sample 4
import Caribe as cb

sentence = "wat iz de time there"
analyse = cb.nlp()
output = analyse.caribe_pos(sentence)

print(output) # Outputs: ["('wat', 'PRON')", "('iz', 'VERB')", "('de', 'DET')", "('time', 'NOUN')", "('there', 'ADV')"]

```
>Sample 5: Remove punctuation marks.
```python
#Sample 5
import Caribe as cb

sentence = "My aunt, Shelly is a lawyer!"
analyse = cb.remove_signs(sentence)


print(analyse) # Outputs: My aunt Shelly is a lawyer

```

>Sample 6: Sentence Correction using T5-KES.
```python
#Sample 6 Using t5_kes_corrector
import Caribe as cb


sentence = "Wat you doin for d the christmas"
correction = cb.t5_kes_corrector(sentence)


print(correction) # Output: What are you doing for christmas?

```
>Sample 7: Sentence Correction using Decoder and T5-KES.
```python
#Sample 7 Using t5_kes_corrector and decoder
import Caribe as cb


sentence = "Ah want ah phone for d christmas"
decoded= cb.trinidad_decode(sentence)
correction = cb.t5_kes_corrector(decoded)


print(correction) # Output: I want a phone for christmas.

```

---
- ## Additional Information
    - `trinidad_decode()` : Decodes the sentence as a whole string.
    - `trinidad_decode_split()`: Decodes the sentence word by word.
    - `phrase_decode()`: Decodes the sentence against known creole phrases.
    - `caribe_corrector()`: Corrects grammatical errors in a sentence using a trained NLP model.
    - `gingerit_corrector()`: Corrects grammatical errors in a sentence using gingerit.
    - `t5_kes_corrector()`: Corrects grammatical errors in a sentence using a trained NLP model.
    - `trinidad_encode()`: Encodes a sentence to Trinidadian English Creole.
    - `trinidad_direct_translation()`: Translates Trinidad English Creole to English.
    - `caribe_pos()`: Generates parts of speech tagging on creole words.
    - `pos_report()`: Generates parts of speech tagging on english words.
    - `remove_signs()`: Takes any sentence and remove punctuation marks. 

---
- ## File Encodings on NLP datasets
Caribe introduces file encoding (Beta) in version 0.1.0. This allows a dataset of any supported filetype to be translated into Trinidad English Creole. The file encoding feature only supports txt, json or csv files only.

- ### Usage of File Encodings:
```python
import Caribe as cb

convert = cb.file_encode("test.txt", "text")
# Generates a translated text file
convert = cb.file_encode("test.json", "json")
# Generates a translated json file
convert = cb.file_encode("test.csv", "csv")
# Generates a translated csv file


```
---
- ## First Parser for the Trinidad English Creole Language

This model utilises T5-base pre-trained model. It was fine tuned using a combination of a custom dataset and creolised JFLEG dataset. JFLEG dataset was translated using the file encoding feature of the library. 

Within the Creole continuum, there exists different levels of lects. These include: 

- Acrolect: The version of a language closest to standard international english.
- Mesolect: The version that consists of a mixture of arcolectal and basilectal features.
- Basilect: The version closest to a Creole language.

**This NLP task was difficult because the structure of local dialect is not standardised but often rely on the structure of its lexifier (English). Spelling also varies from speaker to speaker. Additionally, creole words/spelling are not initial present in the vector space which made training times and optimization longer .**

## Results
Initial results have been mixed.

| Original Text                            | Parsed Text                         | Expected or Correctly Parsed Text   |
|------------------------------------------|-------------------------------------|-------------------------------------|
| Ah have live with mi paremnts en London. | Ah live with meh parents in London. | Ah live with meh parents in London. |
| Ah can get me fone?                      | Ah cud get meh fone?                | Ah cud get meh fone?                |
| muh moda an fada is nt relly home        | muh moda an fada is nt relly home.  | muh moda an fada not really home.    |
| Me ah go market                     | Ah going tuh d market.             | Ah going tuh d market. / I going tuh de market.           |
| Ah waz a going tu school.                | Ah going to school.                 | Ah going to school.                 |
| Ah don't like her.                          | Ah doh like she.                   | Ah doh like she. / I doh like she. |
| Ah waz thinking bout goeng tuh d d Mall. | Ah thinking bout going tuh d Mall.  | Ah thinking bout going tuh d mall.  |


### Usage of the TrinEC Parser

```python
import Caribe as cb

text= "Ah have live with mi paremnts en London"

s= cb.Parser(text)

print(s.TT_Parser()) #Output: Ah live with meh parents in London.


```


---
## Dictionary Data
The encoder and decoder utilises a dictionary data structure. The data for the dictionary was gathered from web-scapping social media sites among other websites and using Lise Winer Dictionary of the English Creole of Trinidad and Tobago among other scholarly resources.

---
## Transformer Models
State of the art NLP grammar correction T5-KES model was trained on a modified version of the JFLEG dataset and is currently being tested against existing models and benchmarks. Another T5 model was used to parse Trinidad English Creole.

---
## Caribe_Corrector (T5-KES) vs Gingerit Corrector
Initial Tests were carried out with performance factors to measure the accuracy of the correction and the degree of sentence distortion from the correct sentence. Initial tests showed that the T5 corrector performed better in terms of accuracy with a lower sentence distortion and attained higher MT scores. The T5 corrector also outperforms Gingerit on positional translations as shown in the table below.

| **Original Creole Text**         | **Decoded Sentence**               | **Caribe Corrector (T5-KES)**       | **Gingerit Corrector**              | **Correct Output**                  |
|----------------------------------|------------------------------------|-------------------------------------|-------------------------------------|-------------------------------------|
| Ah need ah car fuh meh birthday  | I need I car for me birthday       | I need a car for my birthday.       | I need my car for my birthday       | I need a car for my birthday        |
| Wah iz d time on yuh side?       | want is the time on you side?      | What is the time on your side?      | Want is the time on your side?      | What is the time on your side?      |
| Ah man is d provider of de house | I man is the provider of the house | A man is the provider of the house. | My man is the provider of the house | A man is the provider of the house. |
| Ah orange issa fruit             | I orange is a fruit                | An orange is a fruit.               | My orange is a fruit                | An orange is a fruit.               |
| Wah time yuh wah come over?      | want time you want come over?      | What time do you want to come over? | Want time you want to come over?    | What time do you want to come over? |
|Dey make dey own choices at the end of de day  |their make their own choices at the end of the day |They make their own choices at the end of the day. |They make their own choices at the end of the day. |They make their own choices at the end of the day. |

---
# News, Issues and Future Plans (05/06/2022)

- Datasets are continuously being updated.
- NLP Models and Dictionaries are continuously updated.
- Plans to create new datasets and models for other Caribbean English Creole.
- Future plans to create translations, models and datasets for Caribbean French and Spanish Creoles to their respective lexifers (Requires extensive research).
- POS tagging on creole words feature will be temporary removed and replaced with a model. 

---
- ## Contact 
For any concerns, issues with this library or want to become a collaborator to this project.

Email: keston.smith@my.uwi.edu 
___