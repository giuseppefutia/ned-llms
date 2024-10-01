from llm_model.model import LLM_Model
from neo4j_graph.db_base import GraphDBBase
from nlp_task.ner import NamedEntityRecognition
from nlp_task.ned_cs import CandidateSelection

class NED():
    def __init__(self, model, store, input):
        self.model = model
        self.store = store
        self.input= input
    
    def select_candidates(self, sentence):
        for index, value in enumerate(sentence["entities"]):
            selected_candidates = CandidateSelection(self.store).get_candidates(value["mention"])
            sentence["entities"][index]["candidates"] = selected_candidates
    
    
    def run(self):
        ner = NamedEntityRecognition(self.model, self.store, self.input)
        out = ner.make_ner()
        
        # Entity labels
        labels = []
        for i in out:
            for j in i['entities']:
                if j['label'] not in labels:
                    labels.append(j['label'])

        # Candidate Selection per sentence
        for sentence in out:
            self.select_candidates(sentence)
        
        print(out)

model = LLM_Model()
store = GraphDBBase()
input = """Zika belongs to the Flaviviridae virus family and it is spread by Aedes mosquitoes.
           Individuals affected by Zika disease and other syndromes like the chikungunya fever often experience symptoms like viral myalgia, infectious edema, and infective conjunctivitis.
           Severe outcomes of Zika are due to its capacity to cross the placental barrier during pregnancy, causing microcephaly and congenital malformations."""
ned = NED(model, store, input)
ned.run()