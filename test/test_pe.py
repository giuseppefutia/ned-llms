import unittest
import json

from src.nlp_task.path_manager import PathExtraction
from src.neo4j_graph.db_base import GraphDBBase

class TestPathExtraction(unittest.TestCase):

    def setUp(self):
        self.store = GraphDBBase()

    def test_path_retrieval(self):
        sentence = [
            {
                "sentence": "Severe outcomes of Zika are due to its capacity to cross the placental barrier during pregnancy, causing microcephaly and congenital malformations.",
                "entities": [
                    {
                        "id": 0,
                        "mention": "Zika",
                        "label": "Organism",
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
                        "label": "Clinical finding (finding)",
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
                        "label": "Clinical finding (finding)",
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
        pe = PathExtraction(self.model, self.store, sentence[0])
        paths = pe.get_paths()
        print(json.dumps(paths, indent=4))

if __name__ == '__main__':
    unittest.main()
