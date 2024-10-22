import unittest
import json

from src.llm_model.model import LLM_Model
from src.nlp_task.ned_dis import CandidateDisambiguation
from src.neo4j_graph.db_base import GraphDBBase

class TestCandidateDisambiguation(unittest.TestCase):

    def setUp(self):
        self.model = LLM_Model()
        self.store = GraphDBBase()

    def test_path_translation(self):
        sentences = [
            {
                "sentence": "Severe outcomes of Zika are due to its capacity to cross the placental barrier during pregnancy, causing microcephaly and congenital malformations.",
                "entities": [
                    {
                        "id": 0,
                        "mention": "Zika",
                        "start": 19,
                        "end": 22,
                        "candidates": [
                            {
                                "snomed_id": "50471002",
                                "name": "Zika virus"
                            },
                            {
                                "snomed_id": "3928002",
                                "name": "Zika virus disease"
                            },
                            {
                                "snomed_id": "762725007",
                                "name": "Congenital Zika virus infection"
                            }
                        ]
                    },
                    {
                        "id": 1,
                        "mention": "microcephaly",
                        "start": 105,
                        "end": 116,
                        "candidates": [
                            {
                                "snomed_id": "204030002",
                                "name": "Micrencephaly"
                            },
                            {
                                "snomed_id": "48069004",
                                "name": "Acrocephaly"
                            },
                            {
                                "snomed_id": "30470009",
                                "name": "Gutierrezia microcephala"
                            },
                            {
                                "snomed_id": "45999009",
                                "name": "Pimelea microcephala"
                            }
                        ]
                    },
                    {
                        "id": 2,
                        "mention": "congenital malformations",
                        "start": 122,
                        "end": 145,
                        "candidates": [
                            {
                                "snomed_id": "116022009",
                                "name": "Multiple congenital malformations"
                            },
                            {
                                "snomed_id": "276654001",
                                "name": "Congenital malformation"
                            },
                            {
                                "snomed_id": "205973003",
                                "name": "[X]Other congenital malformations"
                            }
                        ]
                    }
                ]
            }
        ]
        
        context = {"context": "A Congenital Zika virus infection occurrence is associated with various congenital malformations, including Micrencephaly, Acrocephaly, Multiple congenital malformations, and Other congenital malformations. These conditions all share a common link to the Congenital entity."}
        sentences[0].update(context)
        cd = CandidateDisambiguation(self.model, sentences[0], context)
        disambiguations = cd.disambiguate_paths()
        print(json.dumps(disambiguations, indent=4))

if __name__ == '__main__':
    unittest.main()
