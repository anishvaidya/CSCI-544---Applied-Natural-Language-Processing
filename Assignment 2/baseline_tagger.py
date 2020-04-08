'''Baseline Tagger
This code tags each utterance in a conversation with a label called dialog act.
The data source is taken from command line along with final out file name and destination.
'''


# Import required libraries
import sys
import pycrfsuite
import hw2_corpus_tool

# Retrieve file-paths and file-names from command line
INPUTDIR = sys.argv[1]
TESTDIR = sys.argv[2]
OUTPUTFILE = sys.argv[3]


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
    trainer=pycrfsuite.Trainer(verbose = True)
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
    predictor = pycrfsuite.Tagger(verbose = True)
    predictor.open("baseline_dialog_act_tagger.crfsuite")
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

def main():
    training_set = list(hw2_corpus_tool.get_data(INPUTDIR))
    dev_set = list(hw2_corpus_tool.get_data(TESTDIR))
    train_features, train_labels = generate_features_and_labels(training_set)
    test_features, test_labels = generate_features_and_labels(dev_set)
    train_model(train_features, train_labels)
    predict(test_features, test_labels)
    
if __name__ == "__main__":
    main()