import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import tensorflow_hub as hub

embed = hub.KerasLayer("./tf_models")

class TopicStatistics:

    def __init__(self, sensitivity=0.6):
        # parameter for cos distance similarity
        self.sensitivity = sensitivity

        #self.embed = hub.KerasLayer("./tf_models")


    # topics: [['phrase_1', 'topic_1'], ['phrase_3', 'topic_4'], ...]
    # etalon_topics: [['topic_2', topic_count_2], ['topic_5', topic_count_5], ...]
    def fit(self, topics):
        self.topics = pd.DataFrame(topics, columns=['phrase', 'topic'])
        self.topic_names = pd.get_dummies(self.topics['topic']).drop_duplicates().reset_index(drop=True).idxmax(axis=1).values

        X = self.topics.phrase.apply(lambda x: embed([x]))
        self.X = np.vstack(X)

        # get dummy topics
        self.y = pd.get_dummies(self.topics['topic']).values # for _get_topics_for_message_exact

        # get unique dummy topics
        self.y_unique = pd.get_dummies(self.topics['topic']).drop_duplicates().reset_index(drop=True).values

        self._get_centroids()


    def _get_centroids(self):
        # get topic numbers from dummy
        yy = [i.argmax() for i in self.y]

        # get unique topic numbers from dummy
        yy_unique = [i.argmax() for i in self.y_unique]
        yy_unique.sort()

        # get indexes of embed phrases for each topic
        indexes = [np.argwhere(yy == i)[:, 0] for i in yy_unique]

        # get centroids for each topic
        centroids = []

        for topic_indexes in indexes:
            topic_embeds = [self.X[i] for i in topic_indexes]
            centroids.append(np.mean(topic_embeds, axis=0))

        self.centroids = np.array(centroids)


    def _get_topics_for_message_centroid(self, message):
        predicted_topics = set()

        for word in message.split():
            embed_word = embed([word])[0]

            c = 0
            for embed_centroid in self.centroids:
                cos = np.dot(embed_centroid, embed_word) / (np.linalg.norm(embed_centroid) * np.linalg.norm(embed_word))

                if cos >= self.sensitivity:
                    # find topic name
                    i = 0
                    for y in self.y_unique:
                        if y.argmax() == c:
                            predicted_topics.add(self.topic_names[i])
                        i += 1
            
                c += 1

        return predicted_topics

    
    def _get_topics_for_message_exact(self, message):
        predicted_topics = set()

        for word in message.split():
            embed_word = embed([word])[0]

            x_count = 0
            for embed_X in self.X:
                cos = np.dot(embed_X, embed_word) / (np.linalg.norm(embed_X) * np.linalg.norm(embed_word))

                if cos >= self.sensitivity:
                    # find topic name
                    i = 0
                    for y in self.y_unique:
                        if y.argmax() == self.y[x_count].argmax():
                            predicted_topics.add(self.topic_names[i])
                        i += 1
                
                x_count += 1

        return predicted_topics


    def get_topics_from_messages(self, messages):
        topics = []
        for msg in messages:
            topics.extend(self._get_topics_for_message_centroid(msg))
            #topics.extend(self._get_topics_for_message_exact(msg))
        
        df_raw = pd.DataFrame()
        df_raw['topic'] = topics

        df = pd.DataFrame(df_raw.value_counts(sort=True).index.tolist())
        df.columns = ['topic']
        df['count'] = list(map(lambda x: 100 * x / len(messages), df_raw.value_counts(sort=True).values.tolist()))

        return df


    def set_etalon_topics(self, etalon_topics):
        self.etalon_topics = pd.DataFrame(etalon_topics, columns=['topic', 'count'])


    def get_compared_topics(self, topics):
        compared_topics = []

        for index, row in self.etalon_topics.iterrows():
            try:
                topic_value = topics.loc[topics['topic'] == row['topic']]['count'].values[0]
            except:
                # topic not found
                topic_value = 0

            if topic_value > row['count']:
                compared_value = topic_value / row['count'] - 1
            elif topic_value == 0:
                compared_value = - row['count'] / 100
            else:
                compared_value = 1 - row['count'] / topic_value

            compared_topics.append({'topic': row['topic'], 'count': 100 * compared_value})

        # sort values
        return pd.DataFrame(compared_topics).sort_values(by=['count'], ascending=False).reset_index(drop=True)

    
    # compared_topics = dict: {topics: {...}, count: {...}}
    def get_plot(self, compared_topics):
        compared_topics = pd.DataFrame(compared_topics)

        f, ax = plt.subplots(figsize=(16, len(compared_topics)))

        sns_plot = sns.barplot(y="topic", x="count",
                    palette="ch:.25", edgecolor=".6",
                    data=compared_topics)

        ax.set(ylabel="",
            xlabel="SDR topic difference from average, %")

        return sns_plot.get_figure()

    
    # compared_topics = dict: {topics: {...}, count: {...}}
    def save_plot(self, compared_topics, filepath):
        compared_topics = pd.DataFrame(compared_topics)

        f, ax = plt.subplots(figsize=(16, len(compared_topics)))

        sns_plot = sns.barplot(y="topic", x="count",
                    palette="ch:.25", edgecolor=".6",
                    data=compared_topics)

        ax.set(ylabel="",
            xlabel="SDR topic difference from average, %")

        sns_plot.get_figure().savefig(filepath)
