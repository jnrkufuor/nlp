import sys
import math
import io
from collections import defaultdict

class NaiveBayes(object):

    def __init__(self, trainingData):
        """
        Initializes a NaiveBayes object and the naive bayes classifier.
        :param trainingData: full text from training file as a single large string

        """
        self.classes = ["RED", "BLUE"]
        self.logpriors = {"RED": 0, "BLUE": 0}
        self.loglikelihoodred ={}
        self.loglikelihoodblue={}
        self.lllred=defaultdict(int)
        self.lllblue=defaultdict(int)
        self.vocab = defaultdict(int)
        s = trainingData.split("\n")
        class_count=0
        reds=0
        blue=0
        for f in s:
            st =f.split()
            self.logpriors[st[0]]+=1
            class_count +=1
            if st[0]=="RED":
                for i in range(1,len(st)):
                    self.lllred[st[i]]+=1
                    reds+=1
                    self.vocab[st[i]]+=1
            else:
                for i in range(1,len(st)):
                    self.lllblue[st[i]]+=1
                    blue+=1
                    self.vocab[st[i]]+=1
        self.logpriors["RED"]=math.log10(self.logpriors["RED"]/class_count)
        self.logpriors["BLUE"]=math.log10(self.logpriors["BLUE"]/class_count)

        for f in self.vocab.keys():
             self.loglikelihoodred[f] = math.log10((self.lllred[f]+1)/(reds+len(self.vocab)))
        for f in self.vocab.keys():
             self.loglikelihoodblue[f] = math.log10((self.lllblue[f]+1)/(blue+len(self.vocab)))

    def estimateLogProbability(self, sentence):
        """
        :param sentence: the test sentence, as a single string without label
        :return: a dictionary containing log probability for each category
        """
        str = sentence.split()
        red = self.logpriors["RED"]
        blue = self.logpriors["BLUE"]
        for i in str:
            red += self.loglikelihoodred[i]
        
            blue += self.loglikelihoodblue[i]

        return {'red': red, 'blue': blue}

    def testModel(self, testData):
        """
        :param testData: the test file as a single string
        :return: a dictionary containing each item as identified by the key
        """
        # s = io.StringIO(testData)
        s = testData.split("\n")
        count=0
        accuracy=0
        metrics_red={"tp":0,"fn":0,"fp":0}
        metrics_blue={"tp":0,"fn":0,"fp":0}
        act=[]
        predicted=[]
        pr =[]
        for f in s:
            count+=1
            str = f.split()
            probs =self.estimateLogProbability(f)
            min_class = max(probs, key=probs.get)
            act.append(str[0].lower())
            predicted.append(min_class)
            pr.append({min_class:probs[min_class]})
            if(str[0].lower())== min_class:
                accuracy+=1
        accuracy= accuracy/ float(count)
        for i in range(len(act)):
            if act[i]=="red" and act[i]==predicted[i]:
                metrics_red["tp"]+=1
            if act[i]=="blue" and predicted[i]=="red":
                metrics_red["fp"]+=1
            if act[i]=="red" and predicted[i]=="blue":
                metrics_red["fn"]+=1

            if act[i]=="blue" and act[i]==predicted[i]:
                metrics_blue["tp"]+=1
            if act[i]=="red" and predicted[i]=="blue":
                metrics_blue["fp"]+=1
            if act[i]=="blue" and predicted[i]=="red":
                metrics_blue["fn"]+=1

        return {'overall accuracy': accuracy,
                'precision for red': (metrics_red["tp"]/(metrics_red["tp"]+metrics_red["fp"])),
                'precision for blue': (metrics_blue["tp"]/(metrics_blue["tp"]+metrics_blue["fp"])),
                'recall for red': (metrics_red["tp"]/(metrics_red["tp"]+metrics_red["fn"])),
                'recall for blue': (metrics_blue["tp"]/(metrics_blue["tp"]+metrics_blue["fn"]))}



if __name__ == '__main__':

    if len(sys.argv) != 3:
        print("Usage: python3 naivebayes.py TRAIN_FILE_NAME TEST_FILE_NAME")
        sys.exit(1)

    train_txt = sys.argv[1]
    test_txt = sys.argv[2]

    with io.open(train_txt, 'r', encoding='utf8') as f:
        train_data = f.read()

    with io.open(test_txt, 'r', encoding='utf8') as f:
        test_data = f.read()

    model = NaiveBayes(train_data)

    evaluation = model.testModel(test_data)
    print("overall accuracy: " + str(evaluation['overall accuracy'])
          + "\nprecision for red: " + str(evaluation['precision for red'])
          + "\nprecision for blue: " + str(evaluation['precision for blue'])
          + "\nrecall for red: " + str(evaluation['recall for red'])
          + "\nrecall for blue: " + str(evaluation['recall for blue']))
