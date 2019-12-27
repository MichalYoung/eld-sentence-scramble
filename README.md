# eld-sentence-scramble
A simple sentence unscrambling game 
for elementary school  English language 
development students.

Sentences to be scrambled and unscrambled are in 
"level" files, in static/data.  Each such level 
file needs a line in templates/choose_level.html. 

Note that "correctness" is a simple equality 
check with the source
sentence from one of the 'level' 
files in static/data.  If there is
more than one correct order, alternatives 
will be rejected.  To
avoid this, create sample sentences with 
semantic constraints, e.g.,
'The feral hog ate the pretty princess' 
would be grammatically
correct but semantically strange as 
'The feral princess ate the pretty hog'.

Now running as https://eld-sentence-scramble.herokuapp.com/ , 
but with a very small set of sample sentences. 
