# -*- coding: utf-8 -*-

import ast, sys, glob

# Import the trained model
inputFile = open( "nbmodel.txt", "r", encoding = "latin1")
lines = inputFile.readlines()
objects = []
for line in lines:
    objects.append( ast.literal_eval(line) )    
prior_prob_class = objects[0][0]
prob_word_ham = objects[0][1]
prob_word_spam = objects[0][2]
del objects, line, lines

# Set the dataset path
dataset = sys.argv[1:]
test_data = dataset[0]

# Declare variables
paths = []
predictions = []
actual_class_mapping = []

# Find all test/dev file paths
def findAllPaths():
    for filename in glob.iglob(test_data + '/**/*.txt', recursive = True):
        class_name = filename.split('.')[-2]
        if class_name == 'ham':
            actual_class_mapping.append("ham")
        else:
            actual_class_mapping.append("spam")
        paths.append(filename)

# Predict the classes
def predict():              
    for i in range(len(paths)):
        text = open(paths[i], "r", encoding = "latin1")
        prob_ham_product = prior_prob_class['ham'] 
        prob_spam_product = prior_prob_class['spam']
        for line in text:
            for word in line.split():
                if word.isnumeric():
                    word = "NUM"
                try:
                    prob_ham_product += prob_word_ham[word]
                    prob_spam_product += prob_word_spam[word]
                except KeyError:
                    continue
        predicted_class = "ham" if prob_ham_product > prob_spam_product else "spam"
        predictions.append(predicted_class)
                
# Calculate accuracy
def metrics():
    count_wrong = 0
    for i in range(len(paths)):
        if predictions[i] != actual_class_mapping[i]:
            count_wrong += 1
    accuracy = 1 - (count_wrong / len(paths))
    return accuracy

# Write output to file
def writeOutputToFile():
    file = open("nboutput.txt", "w", encoding = "latin1")
    for i in range(len(paths)):
        file.write('%s\t%s\n' % (predictions[i], paths[i]))

# Run methods
findAllPaths()
predict()
writeOutputToFile()

    


