import corpus
import utils


class MyFilter():
    def __init__(self):
        self.spam_probability_dict = {}
        self.ham_probability_dict = {}
        self.prior_probs = {}

    def train(self, path):
        c = corpus.Corpus(path)
        vocabulary = utils.generate_vocabulary(c.emails())
        all_words = vocabulary.keys()

        spam_vocabulary = utils.generate_vocabulary(c.spams())
        ham_vocabulary = utils.generate_vocabulary(c.hams())

        # This is done to prevent probability value 0
        utils.increment_value_of_keys_by_1(spam_vocabulary, all_words)
        utils.increment_value_of_keys_by_1(ham_vocabulary, all_words)

        self.spam_probability_dict = utils.calculate_probability_for_words(spam_vocabulary)
        self.ham_probability_dict = utils.calculate_probability_for_words(ham_vocabulary)
        self.prior_probs = utils.get_prior_probabilities(f"{path}/!truth.txt")

    def test(self, path):

        c = corpus.Corpus(path)
        classification = {}

        # In case there are no words in an email we classify it as spam
        if self.spam_probability_dict == {} or self.ham_probability_dict == {}:
            for fname, body in c.emails():
                classification[fname] = utils.SPAM_TAG

        else:
            for fname, body in c.emails():
                spam_classification = utils.classify_email(body, self.spam_probability_dict, self.prior_probs[0])
                ham_classification = utils.classify_email(body, self.ham_probability_dict, self.prior_probs[1])

                if spam_classification > ham_classification:
                    classification[fname] = utils.SPAM_TAG
                else:
                    classification[fname] = utils.HAM_TAG

        utils.write_classification_to_file(path, classification)
