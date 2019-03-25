library(data.table)
library(magrittr)
library(text2vec)
library(stringr)
library(reticulate)


# IMPORT LIFE EXTENSION MAGAZINE CONTENT --------------

life_extension_content = data.table::fread("//lefdomain/files/Dept/Marketing/Marketing Analytics/AI MODELS/UNIVERSAL HEALTH TOPIC TAGS - CONTENT TAGGING NLP/life_extension_content.csv", header = T, stringsAsFactor = FALSE)


# lower case all words, remove non-alphanumeric characters, and collapse multiple spaces
text_data_prep = function(x) {
  x %>% 
    # make text lower case
    stringr::str_to_lower() %>% 
    # remove non-alphanumeric symbols
    stringr::str_replace_all("[^[:alpha:]]", " ") %>% 
    # collapse multiple spaces
    stringr::str_replace_all("\\s+", " ")
}

# clean text data
life_extension_content$article_clean = text_data_prep(life_extension_content$article)


# RUN PYTHON CODE TO LEMMATIZE AND REMOVE STOPWORDS -------------



# CONVERT TO DOCUMENT TERM MATRIX ----------------------

# parallel iterators
it = text2vec::itoken(life_extension_content$article_clean, progressbar = TRUE)
# creates vocabulary of unique terms and prunes for infrequent terms
v = text2vec::create_vocabulary(it) %>% prune_vocabulary(term_count_min = 5)
vectorizer = text2vec::vocab_vectorizer(v)
dtm = text2vec::create_dtm(it, vectorizer, type = "dgTMatrix")


# CREATE LDA TOPIC MODEL WITH 5 TOPICS-----------------


lda_model = LDA$new(n_topics = 5, doc_topic_prior = 0.1, topic_word_prior = 0.01)
doc_topic_distr = lda_model$fit_transform(x = dtm, n_iter = 1000, convergence_tol = 0.001, n_check_convergence = 25, progressbar = TRUE)

lda_model$get_top_words(n = 5, topic_number = c(1L, 5L), lambda = 1)




