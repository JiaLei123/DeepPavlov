from datetime import datetime
import uuid

from deeppavlov import configs, build_model
from deeppavlov.core.agent_v2.agent import Agent
from deeppavlov.core.agent_v2.states_manager import StatesManager
from deeppavlov.core.agent_v2.preprocessor import Preprocessor

ner = build_model(configs.ner.ner_rus, download=True)
faq = build_model(configs.faq.tfidf_autofaq, download=True)
sentiment = build_model(configs.classifiers.rusentiment_elmo_twitter_rnn, download=True)
utterances = ['Привет, мир!', 'Сбербанк подтвердил про общежитие']
print("DeepPavlov configs output:")
print(ner(utterances))
print(faq(utterances))
print(sentiment(utterances))

sm = StatesManager()
preprocessor = Preprocessor(annotators={ner: ['ner.tokens', 'ner.tags'], faq: ['faq-answers', None],
                                        sentiment: 'sentiment'},
                            max_workers=4)

agent = Agent(sm, preprocessor)

# TEST predict_annotations()
annotations = agent.predict_annotations(utterances, should_reset=[False]*len(utterances))
print("Agent output:")
print(annotations)

# TEST __call__()
u_tg_ids = ['dc96f30c-4a45-4225-8c2a-f23294f1d651', '4f5928be-27dc-4ac0-a7ac-ea76f9022636', str(uuid.uuid4())]
utts = ['Что еще скажешь интересного?', 'Бот, ты тупой', '\\start']
u_d_types = ['iphone', 'android', 'iphone']
date_times = [datetime.utcnow(), datetime.utcnow(), datetime.utcnow()]
locations = ['moscow', 'novosibirsk', 'novokuznetsk']
ch_types = ['telegram', 'telegram', 'telegram']

agent(utterances=utts, user_telegram_ids=u_tg_ids, user_device_types=u_d_types,
      date_times=date_times, locations=locations, channel_types=ch_types)
