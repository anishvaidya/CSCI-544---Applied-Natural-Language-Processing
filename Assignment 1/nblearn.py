# -*- coding: utf-8 -*-

# Import stuff
import sys, glob, math
import random
import time

# Get training set path
dataset = sys.argv[1:]
train_data = dataset[0]

# Declare variables
all_ham_paths = []
all_spam_paths = []
prior_prob_class = {'ham': 0, 'spam': 0}
count_total_words = {'ham': 0, 'spam': 0, 'total': 0}
prob_word_ham = {}
prob_word_spam = {}
vocabulary = {}

# Stopwords list
# stopwords_file = open( "english.txt", "r", encoding = "latin1")
# stopwords = stopwords_file.readlines()
stopwords = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '?', '~', '/', '\\', '|', '>', '<', ',', '.', ']', '[', '+', '-', 'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]

# Find paths of ham and spam files
def findAllPaths():
    for filename in glob.iglob(train_data + '/**/*.txt', recursive = True):
        class_name = filename.split('/')[-2]
        if class_name == 'ham':
            all_ham_paths.append(filename)
        else:
            all_spam_paths.append(filename)
               
# Calculate the counts of words
def findCounts():
    # Iterate through all ham files
    for i in range(len(all_ham_paths)):
        text = open(all_ham_paths[i], "r", encoding = "latin1")
        for line in text:
            for word in line.split():
                word = word.lower()
                count_total_words['total'] += 1
                count_total_words['ham'] += 1
                word = clubNumbers(word)

                if word in vocabulary:
                    vocabulary[word][0] += 1
                else:
                    vocabulary[word] = [1, 0]
        text.close()
                
    # Iterate through all spam files
    for i in range(len(all_spam_paths)):
        text = open(all_spam_paths[i], "r", encoding = "latin1")
        for line in text:
            for word in line.split():
                word = word.lower()
                count_total_words['total'] += 1
                count_total_words['spam'] += 1
                word = clubNumbers(word)

                if word in vocabulary:
                    vocabulary[word][1] += 1
                else:
                    vocabulary[word] = [0, 1]
        text.close()

# Calculate counts of words with stopwords
def findCountsWithStopwords():
    # Iterate through all spam files
    for i in range(len(all_ham_paths)):
        text = open(all_ham_paths[i], "r", encoding = "latin1")
        for line in text:
            for word in line.split():
                if word in stopwords:
                    continue
                else:
                    count_total_words['total'] += 1
                    count_total_words['ham'] += 1
                    word = clubNumbers(word)

                    if word in vocabulary:
                        vocabulary[word][0] += 1
                    else:
                        vocabulary[word] = [1, 0]
        text.close()
                
    # Iterate through all ham files            
    for i in range(len(all_spam_paths)):
        text = open(all_spam_paths[i], "r", encoding = "latin1")
        for line in text:
            for word in line.split():
                if word in stopwords:
                    continue
                else:
                    count_total_words['total'] += 1
                    count_total_words['spam'] += 1
                    word = clubNumbers(word)

                    if word in vocabulary:
                        vocabulary[word][1] += 1
                    else:
                        vocabulary[word] = [0, 1]
        text.close()
    
# Calculate the frequency of each word in unique documents
def findWordDocFreq():
    word_in_doc_count = {k: 0 for k in vocabulary.keys()}
    # Iterate through all ham files
    for i in range(len(all_ham_paths)):
        text = set(open(all_ham_paths[i], "r", encoding = "latin1").read().split())
        for word in vocabulary.keys():
            if word in text:
                word_in_doc_count[word] += 1
    # Iterate through all ham files
    for i in range(len(all_spam_paths)):
        text = set(open(all_spam_paths[i], "r", encoding = "latin1").read().split())
        for word in vocabulary.keys():
            if word in text:
                word_in_doc_count[word] += 1
    word_in_doc_count = {key: value for key, value in word_in_doc_count.items() if value > 5}
    return word_in_doc_count

# Delete the less used words
def removeLessUsedWords():
    for word in vocabulary.keys():
        if word not in word_in_doc_count.keys():
            count_total_words['ham'] -= vocabulary[word][0]
            count_total_words['spam'] -= vocabulary[word][1]
            count_total_words['total'] -= (vocabulary[word][0] + vocabulary[word][1])
            vocabulary[word] = [0, 0]
    return {word: counts for word, counts in vocabulary.items() if counts != [0, 0]}
            
# Club numbers under 1 tag
def clubNumbers(word):
    if word.isnumeric():
        word = "NUM"
    return word
    
# Calculate probabilaties, Add one smoothing
def findProbabilities():
    try:
        prior_prob_class['ham'] = math.log((len(all_ham_paths) + 1 ) / (len(all_ham_paths) + len(all_spam_paths) + len(vocabulary)))
    except ZeroDivisionError:
        prior_prob_class['ham'] = 0.5
    try:
        prior_prob_class['spam'] = math.log((len(all_spam_paths) + 1 ) / (len(all_ham_paths) + len(all_spam_paths) + len(vocabulary)))
    except ZeroDivisionError:
        prior_prob_class['spam'] = 0.5    
    for word in vocabulary:
        # Add one smoothing
        try:
            prob_word_ham[word] = math.log((vocabulary[word][0] + 1) / (count_total_words['ham'] + len(vocabulary)))
        except ZeroDivisionError:
            prob_word_ham[word] = 0
        try:
            prob_word_spam[word] = math.log((vocabulary[word][1] + 1) / (count_total_words['spam'] + len(vocabulary)))
        except ZeroDivisionError:
            prob_word_spam[word] = 0

# Calculate probabilaties, Add K smoothing            
def findProbabilitiesWithAlpha(alpha):
    prior_prob_class['ham'] = math.log(count_total_words['ham'] / count_total_words['total'])
    prior_prob_class['spam'] = math.log(count_total_words['spam'] / count_total_words['total'])
    for word in vocabulary:
        # Add K smoothing
        prob_word_ham[word] = math.log((vocabulary[word][0] + alpha) / (count_total_words['ham'] + (alpha * len(vocabulary))))
        prob_word_spam[word] = math.log((vocabulary[word][1] + alpha) / (count_total_words['spam'] + (alpha * len(vocabulary))))

# Build the model file        
def buildModel():
    dicts_to_write = [prior_prob_class, prob_word_ham, prob_word_spam]
    file = open("nbmodel.txt", "w", encoding = "latin1")
    
    file.write(str(dicts_to_write))
    file.flush()
    file.close()

# Select 10 % of original dataset    
def chooseSmallDataset(list_of_paths):
    return random.sample(list_of_paths, len(list_of_paths) // 10)

# Store the dataset file names
def writeDataset(all_ham_paths, all_spam_paths):
    lists_to_write = [all_ham_paths, all_spam_paths]
    file = open("ten_percent_dataset" + str(time.time()) + ".txt", "w", encoding = "latin1")
    
    file.write(str(lists_to_write))
    file.flush()
    file.close()

# Default model trainer    
def defaultTrainer():
    findAllPaths()
    findCounts()
    findProbabilities()
    buildModel()

# Trainer for 10% of dataset    
def tenPercentDataTrainer():
    findAllPaths()
    global all_ham_paths, all_spam_paths
    all_ham_paths = chooseSmallDataset(all_ham_paths)  
    all_spam_paths = chooseSmallDataset(all_spam_paths)  
    findCounts()
    findProbabilitiesWithAlpha(0.6)
    buildModel()

# Trainer with less used words
def lessUsedWordsRemovedTrainer():
    global vocabulary, word_in_doc_count
    findAllPaths()
    findCounts()
    word_in_doc_count = findWordDocFreq()
    vocabulary = removeLessUsedWords()
    findProbabilitiesWithAlpha(0.6)
    buildModel()

# Master Trainer    
def masterTrainer():
    global vocabulary, word_in_doc_count
    findAllPaths()
    findCountsWithStopwords()
    word_in_doc_count = findWordDocFreq()
    vocabulary = removeLessUsedWords()
    findProbabilitiesWithAlpha(0.75)
    buildModel()

# defaultTrainer()
masterTrainer()    