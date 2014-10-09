import json
import string
import dewiki
import nltk
from gensim.models import word2vec
import numpy as np

sentence_detector = nltk.data.load('tokenizers/punkt/english.pickle')

model = word2vec.Word2Vec.load_word2vec_format('/Users/hendrikheuer/Projects/text_summary_experiments/data/vectors.bin', binary=True)

WORD2VEC_DIM = len( model["jesus"] )

def cosine_similarity(v1, v2):
    return np.dot( v1, v2.T ) / np.linalg.norm(v1) / np.linalg.norm(v2)

def open_json_file_and_return_sentences( filename ):
    json_data = open( filename )
    data = json.load( json_data )
    json_data.close()

    data = data["query"]["pages"].values()[0]["revisions"][0]["*"]

    plain_text = dewiki.from_string( data )
    
    sentences = sentence_detector.tokenize( plain_text )

    return sentences

sentences_lookup = {}

def split_sentence_and_return_sentence_vector( doc_id, sentence ):
    words = sentence.split(" ")

    sentence_vector = np.zeros( WORD2VEC_DIM )

    if len( words ) <= 30:
        
        for w in words:
            # remove puncation and turn it into lowercase
            w = w.lower()
            w = "".join(l for l in w if l not in string.punctuation)

            sentence_vector += model[ w ]
            
    sentences_lookup.setdefault( doc_id , {} )
    sentences_lookup[ doc_id ][ hash( sentence ) ] = sentence_vector

    print sentence_vector

"""
print model[ "beer" ]
print model[ "wine" ]

print "beer == wine", word2vec_cosine_similarity( "beer", "beer" )
print "beer == wine", word2vec_cosine_similarity( "beer", "wine" )
print "beer == jesus", word2vec_cosine_similarity( "beer", "jesus" )
print "wine == jesus", word2vec_cosine_similarity( "wine", "jesus" )
"""

en_file = "en.dog.txt"
simple_file = "simple.dog.txt" 

#en_dog_sentences = open_json_file_and_return_sentences( en_file )
sentences = open_json_file_and_return_sentences( simple_file )

for s in sentences[0:4]:
    split_sentence_and_return_sentence_vector( simple_file, s )
