'''Advanced Tagger
This code tags each utterance in a conversation with a label called dialog act.
The data source is taken from command line along with final out file name and destination.
This is the advanced version of the baseline tagger.
Author - Anish Amul Vaidya
'''

import hw2_corpus_tool
import pycrfsuite
import sys
import time
from collections import deque

# Retrieve file-paths and file-names from command line
INPUTDIR = sys.argv[1]
TESTDIR = sys.argv[2]
OUTPUTFILE = sys.argv[3]

class AdvancedTagger:
    ''' Take the input data path and generate 2 lists:
        1. a list of list features for each utterance in each conversation.
        2. a list of labels for utterances in each conversation.
    '''
    
    def generate_features_and_labels(data, n):
        features = []
        labels = []
        for conversation in data:
            speaker1 = None
            speaker2 = None
            conversation_start = True
            conversation_features = []
            conversation_labels = []
            previous_dialog_pos_list = deque(maxlen = n)
            speaker_continuous_sentence_count = 0
            for dialog in conversation:
                previous_dialog_pos = []
                dialog_features = []
                text = getattr(dialog, "text")
                pos_dict = {}
                last_char = "" if len(text) < 1 else text[-1]
                last_2_char = "" if len(text) < 2 else text[-2:]
                last_3_char = "" if len(text) < 3 else text[-3:]
                
                speaker2 = getattr(dialog, "speaker")
                if conversation_start:
                    dialog_features.append("Speaker change: False")
                    dialog_features.append("First Utterance: True")
                    speaker_continuous_sentence_count = 1
                    conversation_start = False
                else:
                    if speaker1 != speaker2:
                        dialog_features.append("Speaker change: True")
                        dialog_features.append("First Utterance: False")
                        speaker_continuous_sentence_count = 1
                        
                    else:
                        dialog_features.append("Speaker change: False")
                        dialog_features.append("First Utterance: False")
                        speaker_continuous_sentence_count += 1
                
                
                if len(previous_dialog_pos_list) != 0:
                    for a in range(len(previous_dialog_pos_list)):
                        for i in range(len(previous_dialog_pos_list[a])):
                            dialog_features.append("Previous_" + str(a + 1) + "_" + previous_dialog_pos_list[a][i])

                postag_object_list = getattr(dialog, "pos")
                
                if postag_object_list is not None:
                    for postag_object in postag_object_list:
                        token = getattr(postag_object, "token")
                        pos = getattr(postag_object, "pos")
                        key = "POS_" + pos
                        dialog_features.append("TOKEN_" + token)
                        dialog_features.append("POS_" + pos)
                        if key in pos_dict:
                            pos_dict[key] += 1
                        else:
                            pos_dict[key] = 1
                        previous_dialog_pos.append("POS_" + pos)
                    dialog_features.append(last_char)
                    dialog_features.append(last_2_char)
                    dialog_features.append(last_3_char)
                    for key in pos_dict:
                        dialog_features.append(key + ": " + str(pos_dict[key]))
                    previous_dialog_pos.append("Prev_char: " + last_char)
                    previous_dialog_pos.append("Prev_char2: " + last_2_char)
                    previous_dialog_pos.append("Prev_char3: " + last_3_char)
                else:
                    previous_dialog_pos.append("POS_BLANK")
                    dialog_features.append("Text " + text)
                    dialog_features.append("Text " + text)
                    # dialog_features.append("Inaudible text")
                    dialog_features.append("NO_POS")
                    
                dialog_features.append("Speaker continuous sentence: " + str(speaker_continuous_sentence_count))
                
                
                if text.endswith(" /"):
                    dialog_features.append("Last char slash: True")
                    dialog_features.append("Last char hyphen: False")
                    previous_dialog_pos.append("last char slash: True")
                    previous_dialog_pos.append("last char hyphen: False")
                elif text.endswith("-/") or text.endswith("- /"):
                    dialog_features.append("Last char slash: False")
                    dialog_features.append("Last char hyphen: True")
                    previous_dialog_pos.append("last char slash: False")
                    previous_dialog_pos.append("last char hyphen: True")
                else:
                    dialog_features.append("Last char slash: False")
                    dialog_features.append("Last char hyphen: False")
                    previous_dialog_pos.append("last char slash: False")
                    previous_dialog_pos.append("last char hyphen: False")
                
                
                if "?" in text:
                    dialog_features.append("Contains question: True") 
                    previous_dialog_pos.append("contains question: True")
                else:
                    dialog_features.append("Contains question: False") 
                    previous_dialog_pos.append("contains question: False")
                
                previous_dialog_pos_list.append(previous_dialog_pos)
                conversation_features.append(dialog_features)
                act_tag = getattr(dialog, "act_tag")
                if act_tag:
                    conversation_labels.append(act_tag)
                speaker1 = speaker2
            
            features.append(conversation_features)
            labels.append(conversation_labels)
        return features, labels
    
    ''' Train the pycrfsuite model:
        Set the required model parameters.
        Input data to model and train.
    '''
    def train_model(train_features, train_labels):
        trainer=pycrfsuite.Trainer(verbose = False)
        for x, y in zip(train_features, train_labels):
            trainer.append(x, y)
        trainer.set_params({
         'c1': 1.0, # coefficient for L1 penalty
         'c2': 1e-3, # coefficient for L2 penalty
         'max_iterations': 50, # stop earlier
         # include transitions that are possible, but not observed
         'feature.possible_transitions': True
         })
        trainer.train("advanced_dialog_act_tagger.crfsuite")
    
        
    ''' Predict on test data:
        Use the trained model on the given test data.
    '''
    def predict(test_features, test_labels):
        predictor = pycrfsuite.Tagger(verbose = False)
        predictor.open("advanced_dialog_act_tagger.crfsuite")
        output_file = open(OUTPUTFILE, "w+")
        correct_predictions = 0
        total_predictions = 0
        for conversation in range(len(test_features)):
            for label_index, predicted_label in enumerate(predictor.tag(test_features[conversation])):
                if predicted_label == test_labels[conversation][label_index]:
                    correct_predictions += 1
                total_predictions += 1
                predicted_label += "\n"
                output_file.writelines(predicted_label)
            output_file.writelines("\n")
        output_file.close()    
        print ("Accuracy is " , (correct_predictions / total_predictions))
        
        
    
if __name__ == "__main__":
    start = time.time()
    training_set = list(hw2_corpus_tool.get_data(INPUTDIR))
    dev_set = list(hw2_corpus_tool.get_data(TESTDIR))
    train_features, train_labels = AdvancedTagger.generate_features_and_labels(training_set, 3)
    test_features, test_labels = AdvancedTagger.generate_features_and_labels(dev_set, 3)
    print ("Training model")
    AdvancedTagger.train_model(train_features, train_labels)
    AdvancedTagger.predict(test_features, test_labels)
    print ("Time taken (in seconds) :", (time.time() - start))
