from collections import Counter;
import os, os.path
import nltk
nltk.download('punkt')

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

fileLocations={} #Keeps track of every word's file locations
sentenceDict={} #Keeps track of every word' sentence locations
wordFrequency = Counter(); #Keeps track of frequency of every word

for filename in os.listdir("Documents"): #For every file in our Documents folder

    fileFull="Documents/"+filename #Grab the file name
    addedFileName = False #Make sure we only add the file name to the list of files a given word is in once

    currentFile = open(fileFull, 'r', encoding='UTF_8') #And open it with UTF_8 encoding, because other encodings break
    data = currentFile.read() #Read the file into memory


    fileSentenceList = (tokenizer.tokenize(data)) #Get a list of all the sentences in the given file
    for sentence in fileSentenceList: #For every sentence in our file
        sentenceWordList=(nltk.word_tokenize(sentence)) #List of words in the sentence
        for word in sentenceWordList: #For every word in the sentence
            if word.lower() in sentenceDict and sentence not in sentenceDict.get(word.lower()): #If our word is already in the dict of words/sentences
                sentenceDict[word.lower()]+=sentence+"\n" #Simply add this sentence to the list for this word
            elif word.lower() not in sentenceDict: #Otherwise
                sentenceDict.setdefault(word.lower(),sentence) #This sentence is the first with this word in it
            #Get word counts
            if len(word.lower())==1 and word.lower().isalpha() or len(word.lower())>1: #If the word is not just a special character (IE '-')
                wordFrequency[word.lower()] += 1 #Increment its count
            if word.lower() in fileLocations and fileFull not in fileLocations.get(word.lower()): #If we haven't registered this file for this word yet
                fileLocations[word.lower()]+= fileFull + " " #Add this to the list of files in which the word appears
                addedFileName=True #Don't do it again for this file
            elif word.lower() not in fileLocations: #If it hasn't been in any files until now
                fileLocations.setdefault(word.lower(), fileFull + " ") #This is the default value for the word key
                addedFileName=True #Don't do it again for this file

    currentFile.close() #Close the file when we're done with it so we don't use too much memory


# Once done with all the files, get the five most common words in the file
fiveMostCommon = wordFrequency.most_common(5)
fiveMostCommonWords = [word for word,count in fiveMostCommon]
fiveMostCommonFrequencies = [count for word,count in fiveMostCommon]
i=0
for word in fiveMostCommonWords: #Print frequency, file locations and sentences for 5 most frequent words
    print("\n\nWord:", "'"+fiveMostCommonWords[i]+"'","occurs", fiveMostCommonFrequencies[i], "times")
    print("This word is in: ", fileLocations.get(word))
    print("Sentences\n-------------\n", sentenceDict.get(word))
    i+=1