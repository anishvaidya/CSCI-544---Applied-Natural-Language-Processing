# -*- coding: utf-8 -*-

inputFile = open( "nboutput.txt", "r", encoding = "latin1")
lines = inputFile.readlines()

list_of_predicted_classes = []
list_of_actual_classes = []
actual_class_count = {"ham": 0, "spam": 0}

def findPredictions():
    for line in lines:
        # predicted_class = line.split(" ")[0]
        # file_path = " ".join(line.split(" ")[1:])
        predicted_class = line.split("\t")[0]
        file_path = " ".join(line.split("\t")[1:])
        actual_class = file_path.split("/")[-2]
        if actual_class == "ham" or actual_class == "spam":
            list_of_predicted_classes.append(predicted_class)
            list_of_actual_classes.append(actual_class)
            actual_class_count[actual_class] += 1
        else:
            continue
        

def calculateMetrics():
    true_count = {"spam": 0, "ham": 0}
    false_count = {"spam": 0, "ham": 0}
    actual_count = {"spam": 0, "ham": 0}
    # for i in range(len(list_of_actual_classes)):
    #     if list_of_actual_classes[i] == list_of_predicted_classes[i]:
    #         true_count[list_of_predicted_classes[i]] += 1
    #     else:
    #         false_count[list_of_predicted_classes[i]] += 1
    # precision_ham = true_count["ham"] / (true_count["ham"] + false_count["ham"])
    # precision_spam = true_count["spam"] / (true_count["spam"] + false_count["spam"])
    # recall_ham = true_count["ham"] / (true_count["ham"] + false_count["spam"])
    # recall_spam = true_count["spam"] / (true_count["spam"] + false_count["ham"])
    # f1_score_ham = (2 * precision_ham * recall_ham) / (precision_ham + recall_ham)
    # f1_score_spam = (2 * precision_spam * recall_spam) / (precision_spam + recall_spam)
    # print ("Ham precision: ", precision_ham, "\nHam recall: ", recall_ham, "\nF1 score (ham): ", f1_score_ham)
    # print ("Spam precision: ", precision_spam, "\nSpam recall: ", recall_spam, "\nF1 score (spam): ", f1_score_spam)
    
    
    for i in range(len(list_of_actual_classes)):
        actual_count[list_of_actual_classes[i]] += 1
        if list_of_actual_classes[i] == list_of_predicted_classes[i]:
            if list_of_predicted_classes[i] == "ham":
                true_count["ham"] += 1
            elif list_of_predicted_classes[i] == "spam":
                true_count["spam"] += 1
        else:
            if list_of_predicted_classes[i] == "ham":
                false_count["ham"] += 1
            elif list_of_predicted_classes[i] == "spam":
                false_count["spam"] += 1
    print (actual_count)
    print (true_count, false_count)
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
    
