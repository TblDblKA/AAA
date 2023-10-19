from typing import List


class CountVectorizer:
    def __init__(self):
        self._word_dict = list()

    def fit_transform(self, documents: List[str]) -> List[List[int]]:
        words_matrix = []
        for ind, line in enumerate(documents):
            text = line.replace('\n', ' ')
            text = text.replace(",", "").replace(".", " ").replace("?", "").replace("!", "")
            text = text.lower()
            text = text.split()
            words_matrix.append(text)
            for word in text:
                if word not in self._word_dict:
                    self._word_dict.append(word)
        dt_matrix = list()
        for i, line in enumerate(words_matrix):
            dt_matrix.append(list())
            for j, word in enumerate(self._word_dict):
                dt_matrix[i].append(line.count(word))
        return dt_matrix

    def get_feature_name(self) -> List[str]:
        return list(self._word_dict)


if __name__ == '__main__':
    corpus = [
        'Crock Pot Pasta Never boil pasta again sadasd',
        'Pasta Pomodoro Fresh ingredients Parmesan to taste'
    ]
    vectorizer = CountVectorizer()
    print(vectorizer.fit_transform(corpus))
    print(vectorizer.get_feature_name())