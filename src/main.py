from logger import Logger
from llm_model.model import LLM_Model
from neo4j_graph.db_base import GraphDBBase
from nlp_task.ner import NamedEntityRecognition
from nlp_task.ned_cs import CandidateSelection
from nlp_task.path_manager import PathExtraction

class NED():
    def __init__(self, model, store, input, logger=None):
        self.model = model
        self.store = store
        self.input= input
        self.logger = logger if logger else Logger(self.__class__.__name__)
    
    def add_candidates(self, sentence):
        for index, value in enumerate(sentence["entities"]):
            candidates = CandidateSelection(self.store).get_candidates(value["mention"])
            sentence["entities"][index]["candidates"] = candidates
    
    def retrieve_paths(self, sentence, labels):
        pe = PathExtraction(self.model, self.store, sentence, labels)
        paths = pe.get_paths()

        return paths
    
    def run(self):
        self.logger.info("Named Entity Recognition (NER) Phase")
        ner = NamedEntityRecognition(self.model, self.store, self.input)
        out = ner.make_ner()
        # Entity labels
        labels = []
        for i in out:
            for j in i['entities']:
                if j['label'] not in labels:
                    labels.append(j['label'])

        self.logger.info("Candidate Selection Phase")
        # Candidate Selection per sentence
        for sentence in out:
            self.add_candidates(sentence)
        
        self.logger.info("Path-based Context Phase")
        for sentence in out:
        # Graph paths generation for each sentence
            paths = self.retrieve_paths(sentence, labels)
        
if __name__ == '__main__':
    model = LLM_Model()
    store = GraphDBBase()
    input = """Zika belongs to the Flaviviridae virus family and it is spread by Aedes mosquitoes.
            Individuals affected by Zika disease and other syndromes like the chikungunya fever often experience symptoms like viral myalgia, infectious edema, and infective conjunctivitis.
            Severe outcomes of Zika are due to its capacity to cross the placental barrier during pregnancy, causing microcephaly and congenital malformations."""
    ned = NED(model, store, input)
    ned.run()