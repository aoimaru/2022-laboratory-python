from datetime import datetime

from gensim.models.doc2vec import Doc2Vec
from gensim.models.doc2vec import TaggedDocument

class D2V(object):
    @staticmethod
    def create_model(training_data, min_count=100, dm=1, window=5, name="default_name"):
        current_time = datetime.now()
        current_time_str = current_time.strftime('%Y.%m.%d.%H.%M.%S')
        documents = [TaggedDocument(words=token, tags=[tag_name]) for tag_name, token in training_data.items()]
        model = Doc2Vec(
            documents=documents,
            min_count=min_count,
            dm=dm,
            window=window
        )
        model.save("./model/doc2vec.model")
        