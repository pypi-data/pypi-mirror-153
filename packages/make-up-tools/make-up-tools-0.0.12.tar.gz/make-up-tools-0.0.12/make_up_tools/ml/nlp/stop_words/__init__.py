from settings import BASE_DIR, relative

__path = relative(BASE_DIR, 'ml/nlp/stop_words/stop_words.txt')
stop_words = open(__path, mode='r', encoding='utf=8').readlines()
stop_words = [i.strip('\n') for i in stop_words]

