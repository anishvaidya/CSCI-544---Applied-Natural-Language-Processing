import random
import sys
import shutil
import glob
import os
import subprocess

max_accuracy = 0
train_files = []
test_files = []
max_acc_test = []

def data_splitter():
    global train_files, test_files
    k = 4
    
    os.chdir("all")
    shutil.rmtree("test")
    shutil.rmtree("train")
    os.mkdir("train")
    os.mkdir("test")
    all_files = glob.glob("*.csv")
    random.shuffle(all_files)
    test_files = random.sample(all_files, len(all_files)//k)
    train_files = list(set(all_files) - set(test_files))
    os.chdir("..")
    
    for each_files in test_files:
        shutil.copy2(str("all/"+each_files), str("all/test/"+each_files))
    
    for each_files in train_files:
        shutil.copy2(str("all/"+each_files), str("all/train/"+each_files))
    
    print("TEST: ",len(test_files))
    print("TRAIN: ",len(train_files))

'''Baseline Tagger
This code tags each utterance in a conversation with a label called dialog act.
The data source is taken from command line along with final out file name and destination.
Author - Anish Amul Vaidya
'''


# Import required libraries
# import sys
import pycrfsuite
import hw2_corpus_tool

# Retrieve file-paths and file-names from command line
INPUTDIR = "all/train"
TESTDIR = "all/test"
# OUTPUTFILE = sys.argv[3]

class BaselineTagger():
    ''' Take the input data path and generate 2 lists:
        1. a list of list features for each utterance in each conversation.
        2. a list of labels for utterances in each conversation.
    '''
    def generate_features_and_labels(data):
        features = []
        labels = []
        for conversation in data:
            speaker1 = None
            speaker2 = None
            conversation_start = True
            conversation_features = []
            conversation_labels = []
            for dialog in conversation:
                dialog_features = []
                speaker2 = getattr(dialog, "speaker")
                if conversation_start:
                    dialog_features.append("First Utterance: True")
                    dialog_features.append("Speaker change: False")
                    conversation_start = False
                else:
                    if speaker1 != speaker2:
                        dialog_features.append("First Utterance: False")
                        dialog_features.append("Speaker change: True")
                    else:
                        dialog_features.append("First Utterance: False")
                        dialog_features.append("Speaker change: False")
                postag_object_list = getattr(dialog, "pos")
                if postag_object_list is not None:
                    for postag_object in postag_object_list:
                        dialog_features.append("TOKEN_" + getattr(postag_object, "token"))
                        dialog_features.append("POS_" + getattr(postag_object, "pos"))
                else:
                    dialog_features.append("TOKEN_BLANK")
                    dialog_features.append("POS_BLANK")   
                conversation_features.append(dialog_features)
                conversation_labels.append(getattr(dialog, "act_tag"))
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
        trainer.train("baseline_dialog_act_tagger.crfsuite")
    
        
    ''' Predict on test data:
        Use the trained model on the given test data.
    '''
    def predict(test_features, test_labels):
        global max_acc_test, test_files, max_accuracy
        predictor = pycrfsuite.Tagger(verbose = False)
        predictor.open("baseline_dialog_act_tagger.crfsuite")
        # output_file = open(OUTPUTFILE, "w+")
        correct_predictions = 0
        total_predictions = 0
        for conversation in range(len(test_features)):
            for label_index, predicted_label in enumerate(predictor.tag(test_features[conversation])):
                if predicted_label == test_labels[conversation][label_index]:
                    correct_predictions += 1
                total_predictions += 1
                predicted_label += "\n"
                # output_file.writelines(predicted_label)
            # output_file.writelines("\n")
        # output_file.close()
        accuracy = (correct_predictions / total_predictions)
        print ("Accuracy is " , accuracy)
        if accuracy > max_accuracy:
            max_accuracy = accuracy
            max_acc_test = test_files

def main():
    global max_accuracy
    for i in range(50):
        print ("-----------------------------------------------------------")
        print ("Iteration ", i)
        data_splitter()
        training_set = list(hw2_corpus_tool.get_data(INPUTDIR))
        dev_set = list(hw2_corpus_tool.get_data(TESTDIR))
        train_features, train_labels = BaselineTagger.generate_features_and_labels(training_set)
        test_features, test_labels = BaselineTagger.generate_features_and_labels(dev_set)
        BaselineTagger.train_model(train_features, train_labels)
        BaselineTagger.predict(test_features, test_labels)
    print ("Max accuracy is ", max_accuracy)
    
if __name__ == "__main__":
    main()