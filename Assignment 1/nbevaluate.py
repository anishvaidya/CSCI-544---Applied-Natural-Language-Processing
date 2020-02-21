# -*- coding: utf-8 -*-

# Read the predictions file
inputFile = open( "nboutput.txt", "r", encoding = "latin1")
lines = inputFile.readlines()

# Declare variables
list_of_predicted_classes = []
list_of_actual_classes = []
actual_class_count = {"ham": 0, "spam": 0}

# Find predicted labels and actual labels
def findPredictions():
    for line in lines:
        predicted_class = line.split("\t")[0]
        file_path = " ".join(line.split("\t")[1:])
        actual_class = file_path.split(".")[-2]
        if actual_class == "ham" or actual_class == "spam":
            list_of_predicted_classes.append(predicted_class)
            list_of_actual_classes.append(actual_class)
            actual_class_count[actual_class] += 1
        else:
            continue
        
# Calculate precision, recall and F-1 score for both classes
def calculateMetrics():
    true_count = {"spam": 0, "ham": 0}
    false_count = {"spam": 0, "ham": 0}
    for i in range(len(list_of_actual_classes)):
        if list_of_actual_classes[i] == list_of_predicted_classes[i]:
            true_count[list_of_predicted_classes[i]] += 1
        else:
            false_count[list_of_predicted_classes[i]] += 1
    precision_ham = true_count["ham"] / (true_count["ham"] + false_count["ham"])
    precision_spam = true_count["spam"] / (true_count["spam"] + false_count["spam"])
    recall_ham = true_count["ham"] / (true_count["ham"] + false_count["spam"])
    recall_spam = true_count["spam"] / (true_count["spam"] + false_count["ham"])
    f1_score_ham = (2 * precision_ham * recall_ham) / (precision_ham + recall_ham)
    f1_score_spam = (2 * precision_spam * recall_spam) / (precision_spam + recall_spam)
    print ("Ham precision: ", precision_ham, "\nHam recall: ", recall_ham, "\nF1 score (ham): ", f1_score_ham)
    print ("Spam precision: ", precision_spam, "\nSpam recall: ", recall_spam, "\nF1 score (spam): ", f1_score_spam)


findPredictions()
calculateMetrics()       
    
