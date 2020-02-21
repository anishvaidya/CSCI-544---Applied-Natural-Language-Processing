# -*- coding: utf-8 -*-

# nbmodel = open("nbmodel.txt", "r", encoding = "latin1").readlines()
# model = nbmodel[0][:]
import ast, sys, glob


inputFile = open( "nbmodel.txt", "r", encoding = "latin1")
lines = inputFile.readlines()

objects = []
for line in lines:
    objects.append( ast.literal_eval(line) )

prior_prob_class = objects[0][0]
prob_word_ham = objects[0][1]
prob_word_spam = objects[0][2]
del objects, line, lines
dataset = sys.argv[1:]
train_data = dataset[0] + '/dev'

paths = []
actual_class_mapping = []
def findAllPaths():
    for filename in glob.iglob(train_data + '/**/*.txt', recursive = True):
        class_name = filename.split('.')[-2]
        if class_name == 'ham':
            # prior_prob_class['ham'] += 1
            actual_class_mapping.append("ham")
        else:
            actual_class_mapping.append("spam")
        paths.append(filename)
 
prob_ham = []
prob_spam = []
predictions = []        

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
                    word = word.lower()
                    prob_ham_product += prob_word_ham[word]
                    prob_spam_product += prob_word_spam[word]
                except KeyError:
                    # prob_ham_product *= 1
                    continue
        prob_ham.append(prob_ham_product) 
        prob_spam.append(prob_spam_product)
        predicted_class = "ham" if prob_ham_product > prob_spam_product else "spam"
        predictions.append(predicted_class)
                

def metrics():
    count_wrong = 0
    for i in range(len(paths)):
        if predictions[i] != actual_class_mapping[i]:
            count_wrong += 1
    accuracy = 1 - (count_wrong / len(paths))
    return accuracy

def writeOutputToFile():
    file = open("nboutput.txt", "w", encoding = "latin1")
    for i in range(len(paths)):
        file.write('%s\t%s\n' % (predictions[i], paths[i]))
            
findAllPaths()
predict()
writeOutputToFile()
print(metrics())
    


