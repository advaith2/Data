Description:
	The python code 'tfidf_computation.py' computes tfidf for the science fiction corpus.
	The python code 'swr_v1.py' removes stop words (except top 25% high tfidf words).

tfidf_computation.py
--------------------

Input:
	Each input document must be a text file (Story book).
	All input files must be put in a folder named 'texts'

Output:
	idf.txt -> The inverse document frequency of every word in the corpus.
	tfidf-final.xlsx -> tfidf of every term in each document (One sheet per document), sorted in ascending order.

Assumptions:
	At least 1 file must be present in the folder texts.
	The code should be in the same directory as the folder 'texts'.
	The current working directory should not contain any folders named 'wordcounts' and 'tfidf'
	The code should have sufficient privileges to create and delete temp folders in the working directory.

Code Flow:
	The term frequency of every term (terms after performing special characters removal, sentence tokenizing and lemmatizing) in every text is computed and the results are stored under a new directory 'wordcounts'
	Every file in the directory 'wordcounts' is read to compute inverse document frequency which is in turn stored in 'idf.txt'
	tf-idf values are computed and appended for every term in the 'wordcounts' folder.
	A sorting function is run on every file in the 'wordcounts' folder based on tf-idf value. The sorted list of each file is stored in a new folder 'tfidf'
	An excel sheet is created to add each term in a file as a sheet. [File name: 'tfidf-final.xlsx']
	The created folders 'wordcounts' and 'tfidf' are then removed.

Modifications:
	Input folder names, excel sheet name and temp folder names are stored as global variables in the beginning of the code which can be modified to have custom folder names.


swr_v1.py
---------

Input:
	Each input document must be a text file (Story book).
	All input files must be put in a folder named 'texts'
	The excel sheet tfidf-final.xlsx should be present in the same directory

Output:
	result.xlsx -> One sheet per document in which each sentence and the words after removing stopwords are present.

Assumptions:
	At least 1 file must be present in the folder texts.
	The code should be in the same directory as the folder 'texts'.

Code Flow:
	The tf-idf values (excel sheet) is loaded into program memory.
	Each document is read, and its stop words are removed and stored in a sheet of a new workbook.
	The new workbook is then saved as result.xlsx
