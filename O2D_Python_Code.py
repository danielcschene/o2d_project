"""
This script contains all the code we've been working on during the project.
We've decided to include everything from the first 'baby steps' to the eventual
code we ended up with after a few weeks of playing around with both python in
general and the nltk package specifically. We've been using the Spyder IDE for
no particular reason other than that it is intergrated/included in Anaconda.
The code is chunked with the the '#%%' operator in Spyder, which may cause
trouble running the script in other IDEs. We've done our best to include
our comments and any other noteworthy remarks, but not everything will be 
described in great detail. This is also done to provide some insigth into the
learning process we've been going through during the project, which is also quite
interesting to read back ourselves.
"""

"""
As a first step, after spending some time manually cleaning texts of chapter
headings, we've used regular expressions to do this. This still required some
work because every .txt file had its own way of defining chapters (roman numerals,
normal digits, lower or upper case, or a combination of both, etc.). Nevertheless
it saved us some valuable time.
"""

#%% Using regex for cleaning .txt files
import re

fileName = 'File.txt'
chapterPattern = re.compile('^CHAPTER\s[A-Z]*$')

originalFile = open(fileName, 'r', encoding="utf8")
originalLines = originalFile.readlines()
originalFile.close()

newFile = open(fileName, 'w+')

for line in originalLines:
	if not chapterPattern.match(line):
            newFile.write(line)
      
newFile.close()

#%% 
"""
This cell contains our first attempt at using nltk for text analysis
"""
import nltk
#nltk.download('punkt')

file = open('PrideandPrejudice.txt', encoding="utf8")
f = file.read()

sentencetokens = nltk.sent_tokenize(f)
ns = len(sentencetokens)
print("The number of sentences is:")
print(ns)

wordtokensraw = nltk.word_tokenize(f)
NoWord = [',','(',')',':',';','.','%','\x96','{','}','[',']','!','?',"''","``"]
wordtokens = [i for i in wordtokensraw if i not in NoWord]
nw = len(wordtokens)
print("The number of words is:")
print(nw)

avgwps = (nw/ns)
print("The average number of words per sentence is:")
print(avgwps) 

wordtokenset = set(wordtokens)
uniquewords = len(wordtokenset)
print("The number of unique words is:")
print(uniquewords)

uniquewordper = (uniquewords/nw*100)
print("The percentage of unique words is:")
print(uniquewordper,"%")

longestsentence = max(sentencetokens, key=len)
wordtokensrawls = nltk.word_tokenize(longestsentence)
wordtokensls = [i for i in wordtokensrawls if i not in NoWord]
longestsentencenw = len(wordtokensls)
print("The number of words in the longest sentence is:")
print(longestsentencenw)

no_function_words = ['the', 'and', 'a', 'an', 'is', 'be', 'of', 'it', 'i', 'to', 'in', 'have']
word_tokens_no_function = [i for i in wordtokens if i not in no_function_words]
average_word_length = sum(len(word) for word in word_tokens_no_function) / len(word_tokens_no_function)

print("The average word length is: ", average_word_length)


file.close()

#%%
"""
This is the second version, in which we've put our different lines into a 
function, so we can call the function on any desired text file.
Another improvement (an important one) is that this function also writes the
acquired data from the function into a csv file. This was a nice step forward
in the handeling of the project data.
"""
import csv

def my_text_analysis(txtfile):
    file = open(txtfile, 'r')
    f = file.read()
    
    sentence_tokens = nltk.sent_tokenize(f)
    ns = len(sentence_tokens)
    #print(("The number of sentences in %s is:\n %d") % (txtfile, ns))
    
    wordtokens_raw = nltk.word_tokenize(f)
    NoWord = [',','(',')',':',';','.','%','\x96','{','}','[',']','!','?',"''","``"]
    word_tokens = [i for i in wordtokens_raw if i not in NoWord]
    nw = len(word_tokens)
    #print(("The number of words in %s is:\n %d") % (txtfile, nw))
    
    avgwps = (nw/ns)
    #print(("The average amount of words per sentence in %s is:\n %d") % (txtfile, avgwps))
    
    wordtoken_set = set(word_tokens)
    unique_words = len(wordtoken_set)
    #print(("The number of unique words in %s is:\n %d") % (txtfile, unique_words))
    
    unique_word_ratio = (unique_words/nw*100)
    #print(("The percentage of unique words in %s is:\n %d") % (txtfile, (float(unique_word_ratio))))
    
    longest_sentence = max(sentence_tokens, key=len)
    wordtokens_raw_ls = nltk.word_tokenize(longest_sentence)
    wordtokens_ls = [i for i in wordtokens_raw_ls if i not in NoWord]
    longest_sentence_w = len(wordtokens_ls)
    #print(("The longest sentence in %s is %d words long\n") % (txtfile, longest_sentence_w))
    
    no_function_words = ['the', 'and', 'a', 'an', 'is', 'be', 'of', 'it', 'i', 'to', 'in', 'have']
    word_tokens_no_function = [i for i in word_tokens if i not in no_function_words]
    average_word_length = sum(len(word) for word in word_tokens_no_function) / len(word_tokens_no_function)
    #print(("The average word length for words in %s is:\n %d") % (txtfile, average_word_length))
    
    csv_txt_data = [['Work', 'No.OfSen', 'No.OfWords', 'AvgWperS', 'UniqueW', 'UniqRatio', 'LongstSen', 'AvgWLen'], [txtfile, ns, nw, avgwps, unique_words, unique_word_ratio, longest_sentence_w, average_word_length]]
    with open(str(txtfile) + '.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(csv_txt_data)
   
#%%     
"""
We logically wanted to call the function/script on a whole diretory, so that we
didn't have to manually call it on each individual file. The following code was
used to do this.
"""
#to call the function for all .txt files in a directory:

import glob
path = '/Path/to/directory/...'
filenames = glob.glob(path + '/*.txt')
for filename in filenames:
    my_text_analysis(filename)

#%%
"""
Now that we've acquired a csv file with our data for each text individually,
the next step was merging all these files into one csv, so we could import with
other software such as Google sheets and R, for further cleaning and analysis.
"""

path = 'Path/to/directory/of/csvs/...'


from collections import OrderedDict

files = glob.glob(path + '/*.csv')
header = OrderedDict()
data = []
for filename in files:
    with open(filename, 'r') as fin:
        csvin = csv.DictReader(fin)
        header.update(OrderedDict.fromkeys(csvin.fieldnames))
        data.append(next(csvin))
with open('output_filename_version2.csv', 'w', newline='') as fout:
    csvout = csv.DictWriter(fout, fieldnames=list(header))
    csvout.writeheader()
    csvout.writerows(data)

#%%
"""
Now that we had a complete dataframe with the data of all our texts contained in
it, our work with python was basically done. Nevertheless, during the project
we kept working on improving the code, changing it, acquiring values in improved
ways according the background literature on textual analysis. This last cell
contains a function which we developed quite late in the project, and contains 
more detailed information and commentary on what it does, and more importantly:
why.
"""

def my_text_analysis_2(txtfile):
    file = open(txtfile, 'r')
    f = file.read()
    from nltk.corpus import stopwords
    stop_words = stopwords.words('english') #We could have known, but it turns out that the nltk.corpus contains set of english stopwords already.
    
    '''Average sentence length in words, improved when compared the the older version.
    Where the older version just divided the total number of words by the total number of sentences,
    this version splits the sentences tokenized by the sent_tokenize() function, so that we get a 
    list of lists, basically. Words are items in a list which is the sentences, and sentences are
    items in a list which is the whole text. In this way, the number of words and number of sentences
    should corresspond more accurately, because both measures have been taken on the sentence level.'''
    
    sentence_tokens = nltk.sent_tokenize(f)
    total_sentences = len(sentence_tokens)
    sentences_split = [sentence.split() for sentence in sentence_tokens]
    total_words = sum([len(sentence) for sentence in sentences_split])
    avg_sen_length = total_words / total_sentences
    print(round(avg_sen_length, 2))

    '''Average word length with stop words left out. 
    This perhaps better measures the average word length because the group of content/stop words is
    here taken from the nltk.corpus, and this set is larger than the one we made ourselves.
    Because this set is larger, the variable avg_w_length turns out higher (on average) than the previous 
    variable we calculated. The desired effect here is that because there are more stop words (common) 
    left out, the text's distinct vocabulary is more effectively measured, and differences in this word
    length better captures differences in vocabulary between texts.'''
    
    word_tokens = nltk.word_tokenize(f)
    words_filtered = [word for word in word_tokens if word.isalpha() and word not in stop_words]
    avg_w_length = sum([len(word) for word in words_filtered]) / len(words_filtered)
    print(round(avg_w_length, 2))

    '''One of the main problems with comparing texts is their difference in size. Size affects vocabulary
    in that a text's vocabulary growns very fast at first, but flattens out as the text gets longer. 
    Because of this, we've tried to come up with a relatively simple way of overcoming this length effect.
    In the end, we've decided to take three 5000 word chunks of the text to measure vocabulary. This gets
    rid of length differences between texts, even though it is perhaps much worse in capturing vocabulary
    complexity than more complicated formulas.'''
    
    words_filtered_2 = [word for word in word_tokens if word.isalpha()]
    middle_point = len(words_filtered_2) // 2
    mid_min = (middle_point) - 2500
    mid_max = (middle_point) + 2500

    sample_1 = words_filtered_2[:5000]
    sample_2 = words_filtered_2[mid_min : middle_point] + words_filtered_2[middle_point : mid_max]
    sample_3 = words_filtered_2[-5000:]
    
    '''Now we can get the average percentage of unique words for the three samples'''
    
    average_unique_over_3_samples = (((len(set(sample_1)) + len(set(sample_2)) + len(set(sample_3))) / 3) / (5000)) * 100
    print(round(average_unique_over_3_samples, 3))
    
    '''Previous research has also highlighted the amount of simple/function words of a text as a
    possible measure or proxy of readability and thus complexity. Now that we have three samples
    anyway, we might as well get a measure of this too.'''
    
    average_function_over_3_samples = ((((len([word for word in sample_1 if word in stop_words])) + len([word for word in sample_2 if word in stop_words]) + len([word for word in sample_3 if word in stop_words])) / 3) / (5000)) * 100
    print(round(average_function_over_3_samples, 3))
    
    '''The relative amount of words longer than 7 characters (letters) has also previously been used as a measure of complexity. Intuitively, this measure is as simple 
    as counting the total number of 7-or-more letter words and calulating the percentage of these long words over the whole. Yet, if we consider that a longer text also 
    contains more function words, because they are the most frequent in the language in general, this "simple" calculation is affected by text length, which we don't want.
    A random sample would be a better measure, even though this might still be affected by text length, because as a text gets longer, the chances of randomly picking a 
    function word increase. This means that the sample used for finding this percentage-of-7+-words should not be entirely random, but as in the average percentage of unique 
    and function word measures, it should be a given portion of the text which is structurally intact, so to speak. Therefor we use the previous middle_point variable and 
    take a sample from the middle of the text, this time of the previous 5000 and following 5000 words of the middle. Even if this is still not entirely accurate, it is 
    currently the most independent measure we can think of considering the scope of this project.'''

    mid_min2 = (middle_point) - 5000
    mid_max2 = (middle_point) + 5000

    sample_10000 = words_filtered_2[mid_min2 : middle_point] + words_filtered_2[middle_point : mid_max2]

    average_7plus_words = ((len([word for word in sample_10000 if len(word) > 7])) / len(sample_10000)) * 100
    print(round(average_7plus_words, 3))
    
    
    csv_txt_data = [['Work', 'AvgSentLen', 'AvgWordLen', 'UniqueWordSample', 'FunctionWordSample', 'LongWordSample'], [txtfile, avg_sen_length, avg_w_length, average_unique_over_3_samples, average_function_over_3_samples, average_7plus_words]]
    with open(str(txtfile) + '.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(csv_txt_data)