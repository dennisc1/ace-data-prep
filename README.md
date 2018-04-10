# ACE 2005 Event Extraction Data Preprocess

## Description

This project ties together numerous tools. It converts from the [ACE2005 file format](https://catalog.ldc.upenn.edu/LDC2006T06) (.sgm and .apf.xml files) to Concrete.
It also annotates the ACE 2005 data using Stanford CoreNLP and the chunklink.pl script from CoNLL-2000.
By the way, the data is converted to json and [brat](http://brat.nlplab.org/) annotations.
See below for possible appropriate citations. (Later)
This project is modified from [this repo](https://github.com/mgormley/ace-data-prep).

The output of the pipeline is available in three formats: Concrete, JSON, and Brat Annotation.
Concrete is a data serialization format for NLP. See the [primer on Concrete](http://hltcoe.github.io/) for additional details. As a convenience, the output is also converted to an easy-to-parse [Concatenated JSON format](https://en.wikipedia.org/wiki/JSON_Streaming#Concatenated_JSON). This conversion is done by [Pacaya NLP](https://github.com/mgormley/pacaya-nlp). An example sentence is shown below. 

A document will be splited into sentences by Stanford CoreNLP and each document will be trnasfered into a new file with the same name prefix.
Here is a JSON example of a sentence.
```json
[
    {
        "penn-treebank": "(ROOT (S (NP (DT Some) (CD 70) (NNS people)) (VP (VBD were) (VP (VBN arrested) (NP-TMP (NNP Saturday)) (PP (IN as) (NP (NP (NNS demonstrators)) (VP (VBN clashed) (PP (IN with) (NP (NP (NN police)) (PP (IN at) (NP (NP (DT the) (NN end)) (PP (IN of) (NP (DT a) (JJ major) (NN peace) (NN rally))))))) (ADVP (RB here))))) (, ,) (SBAR (IN as) (S (NP (QP (IN at) (JJS least) (CD 200,000)) (JJ anti-war) (NNS protesters)) (VP (VBD took) (PP (TO to) (NP (DT the) (NNS streets))) (PP (IN across) (NP (DT the) (NNP United) (NNPS States) (CC and) (NNP Canada)))))))) (. .)))", 
        "golden-entity-mentions": [
            {
                "phrase-type": "NOM", 
                "end": 8, 
                "text": "demonstrators", 
                "entity-type": "PER:Group", 
                "start": 7, 
                "id": "EM 0-8-3"
            }, 
            {
                "phrase-type": "NOM", 
                "end": 3, 
                "text": "Some 70 people", 
                "entity-type": "PER:Group", 
                "start": 0, 
                "id": "EM 0-10-0"
            }, 
            {
                "phrase-type": "PRO", 
                "end": 20, 
                "text": "here", 
                "entity-type": "GPE:Population-Center", 
                "start": 19, 
                "id": "EM 0-20-2"
            }, 
            {
                "phrase-type": "NOM", 
                "end": 37, 
                "text": "the streets across the United States and Canada", 
                "entity-type": "FAC:Path", 
                "start": 29, 
                "id": "EM 0-34-0"
            }, 
            {
                "phrase-type": "NAM", 
                "end": 37, 
                "text": "Canada", 
                "entity-type": "GPE:Nation", 
                "start": 36, 
                "id": "EM 0-36-0"
            }, 
            {
                "phrase-type": "NOM", 
                "end": 27, 
                "text": "at least 200,000 anti-war protesters", 
                "entity-type": "PER:Group", 
                "start": 22, 
                "id": "EM 0-38-1"
            }, 
            {
                "phrase-type": "NAM", 
                "end": 35, 
                "text": "the United States", 
                "entity-type": "GPE:Nation", 
                "start": 32, 
                "id": "EM 0-53-13"
            }, 
            {
                "phrase-type": "TIM", 
                "end": 6, 
                "text": "Saturday", 
                "entity-type": "TIM:time", 
                "start": 5, 
                "id": "EM 0-66-0"
            }, 
            {
                "phrase-type": "NOM", 
                "end": 11, 
                "text": "police", 
                "entity-type": "PER:Group", 
                "start": 10, 
                "id": "EM 0-113-2"
            }
        ], 
        "conll-head": [3, 3, 5, 5, 0, 5, 5, 7, 8, 9, 10, 11, 14, 12, 14, 19, 19, 19, 15, 9, "", 28, 25, 23, 27, 27, 28, 5, 28, 31, 29, 28, 35, 35, 32, 35, 35, ""], 
        "chunk": ["B-NP", "I-NP", "I-NP", "B-VP", "I-VP", "B-NP", "B-PP", "B-NP", "B-VP", "B-PP", "B-NP", "B-PP", "B-NP", "I-NP", "B-PP", "B-NP", "I-NP", "I-NP", "I-NP", "B-ADVP", "O", "B-SBAR", "B-NP", "I-NP", "I-NP", "I-NP", "I-NP", "B-VP", "B-PP", "B-NP", "I-NP", "B-PP", "B-NP", "I-NP", "I-NP", "I-NP", "I-NP", "O"], 
        "lemma": [ "some", "70", "people", "be", "arrest", "Saturday", "as", "demonstrator", "clash", "with", "police", "at", "the", "end", "of", "a", "major", "peace", "rally", "here", ",", "as", "at", "least", "200,000", "anti-war", "protester", "take", "to", "the", "street", "across", "the", "United", "States", "and", "Canada", "."], 
        "stanford-ner": ["O", "NUMBER", "O", "O", "O", "DATE", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "NUMBER", "O", "O", "O", "O", "O", "O", "O", "O", "LOCATION", "LOCATION", "O", "LOCATION", "O"], 
        "words": ["Some", "70", "people", "were", "arrested", "Saturday", "as", "demonstrators", "clashed", "with", "police", "at", "the", "end", "of", "a", "major", "peace", "rally", "here", ",", "as", "at", "least", "200,000", "anti-war", "protesters", "took", "to", "the", "streets", "across", "the", "United", "States", "and", "Canada", "."], 
        "pos-tags": ["DT", "CD", "NNS", "VBD", "VBN", "NNP", "IN", "NNS", "VBN", "IN", "NN", "IN", "DT", "NN", "IN", "DT", "JJ", "NN", "NN", "RB", ",", "IN", "IN", "JJS", "CD", "JJ", "NNS", "VBD", "TO", "DT", "NNS", "IN", "DT", "NNP", "NNPS", "CC", "NNP", "."], 
        "golden-event-mentions": [
            {
                "arguments": [
                    {
                        "start": 0, 
                        "role": "Person", 
                        "end": 3, 
                        "entity-type": "PER:Group", 
                        "text": "Some 70 people"
                    }, 
                    {
                        "start": 19, 
                        "role": "Place", 
                        "end": 20, 
                        "entity-type": "GPE:Population-Center", 
                        "text": "here"
                    }, 
                    {
                        "start": 5, 
                        "role": "Time-Within", 
                        "end": 6, 
                        "entity-type": "TIM:time", 
                        "text": "Saturday"
                    }
                ], 
                "trigger": {
                    "start": 4, 
                    "end": 5, 
                    "text": "arrested"
                }, 
                "id": "SM 0-4-0", 
                "event_type": "Justice:Arrest-Jail"
            }
        ]
    }
]
```

The words, entities, and events are given by the original ACE 2005 data.
The lemmas, part-of-speech tags, labeled syntactic dependency parse (parents), and constituency parse (penn-treebank) are automatically annotated by [Stanford CoreNLP](https://github.com/stanfordnlp/CoreNLP).
The chunks are derived from the constituency parse using a [python wrapper](https://github.com/mgormley/concrete-chunklink) of the chunklink.pl script from CoNLL-2000.

After executing ```make LDC_DIR=./LDC OUT_DIR=./output ace05splits``` (see details below), the output will consist of the following directories:

* `LDC2006T06_temp_copy/`: A copy of the LDC input directory with DTD files placed appropriately.
* `ace-05-comms/`: The ACE 2005 data converted to Concrete.
* `ace-05-comms-ptb-anno/`: The ACE 2005 data converted to Concrete and annotated with Stanford CoreNLP.
* `ace-05-comms-ptb-anno-chunks/`: The ACE 2005 data converted to Concrete and annotated with Stanford CoreNLP and chunklink.pl.
* `ace-05-json/`: The fully annotated data converted to Concatenated JSON.
* `ace-05-brat/`: The fully annotated data converted to Brat Annotation.

We recommend all users of this pipeline use the files in `ace-05-splits` for good.

## Requirements

- Java 1.8+
- Maven 3.4+
- Python 2.7.x
- GNU Make

## Convert and Annotate Full Dataset

A Makefile is included to  to convert the full ACE 2005 dataset to
Concrete. The same Makefile will also add Stanford CoreNLP annotations
and convert the constituency trees to chunks with chunklink.pl. 
It will also require install the latest version of concrete-python and
clone the concrete-chunklink repository. 

The command below will convert the data to Concrete
(with AceApf2Concrete), annotate (with Stanford and chunklink.pl), and
transform the data into JSON and Brat Annotation (with concrete2json.py and json2brat.py).

    make LDC_DIR=<path to LDC dir> \
         OUT_DIR=<path for output dir> \
         ace05splits

## One More Step to Vistualize ACE2005 in Brat
1. Copy the `ace-05-brat/` to a place under `$BRAT_ROOT$/data/`
2. Copy the `brat-dataconverter/visual.conf` to `$BRAT_ROOT$`, and of course plesse backup the old one. 

## Citations
Later