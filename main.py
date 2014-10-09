import json
import string
import dewiki
import nltk
from gensim.models import word2vec
import numpy as np

sentence_detector = nltk.data.load( 'tokenizers/punkt/english.pickle' )

model = word2vec.Word2Vec.load_word2vec_format( '/Users/hendrikheuer/Projects/text_summary_experiments/data/vectors.bin', binary=True )

WORD2VEC_DIM = len( model[ "computer" ] )

def cosine_similarity(v1, v2):
    return np.dot( v1, v2.T ) / np.linalg.norm( v1 ) / np.linalg.norm( v2 )

def open_json_file_and_return_sentences( filename ):
    json_data = open( filename )
    data = json.load( json_data )
    json_data.close()

    data = data[ "query" ][ "pages" ].values()[ 0 ][ "revisions" ][ 0 ][ "*" ]

    plain_text = dewiki.from_string( data )
    
    sentences = sentence_detector.tokenize( plain_text )

    return sentences


def split_sentence_and_return_sentence_vector( sentence ):
    words = sentence.replace('\n', ' ').split(" ")

    sentence_vector = np.zeros( WORD2VEC_DIM )

    if len( words ) <= 30:
        for w in words:
            if w in model:
                # remove puncation and turn it into lowercase
                w = w.lower()
                w = "".join(l for l in w if l not in string.punctuation)

                sentence_vector += model[ w ]
            
    return sentence_vector

def calculate_sentence_vectors( sentences ):
    sentences_lookup = {}

    for s in sentences[0:20]:
        sentences_lookup[ hash( s ) ] = split_sentence_and_return_sentence_vector( s )

    return sentences_lookup

def compute_sentence_similiarity_matrix( simple_sentences, english_sentences ):
    simple_array = simple_sentences.values()
    english_array = english_sentences.values()

    len_simple = len( simple_array )
    len_english = len( english_array )

    similiarity_matrix = np.zeros( (len_simple, len_english) )

    for i_s in xrange( len_simple ):
        for i_e in xrange( len_english ):
            similiarity_matrix[ i_s ][ i_e ] = cosine_similarity( simple_array[ i_s ], english_array[ i_e ]  )
            
            if np.isnan( similiarity_matrix[ i_s ][ i_e ] ):
                similiarity_matrix[ i_s ][ i_e ] = 0.0

    return similiarity_matrix

def print_top_n_sentences( similiarity_matrix, N=5 ):
    len_simple, len_english = similiarity_matrix.shape

    for i_s in xrange( len_simple ):
        top_idx = np.argpartition( similiarity_matrix[ i_s ], -N )[ -N: ]

        print similiarity_matrix[ i_s ][ top_idx ]

en_file = "data/en.dog.txt"
simple_file = "data/simple.dog.txt" 

simple_sentences = open_json_file_and_return_sentences( simple_file )
simple_sentence_vectors = calculate_sentence_vectors( simple_sentences )

en_sentences = open_json_file_and_return_sentences( en_file )
en_sentence_vectors = calculate_sentence_vectors( en_sentences )

similarity_matrix = compute_sentence_similiarity_matrix( simple_sentence_vectors, en_sentence_vectors )

print_top_n_sentences( similarity_matrix )
