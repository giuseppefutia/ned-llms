import unittest
import json
from src.nlp_task.ned_cs import CandidateSelection
from src.neo4j_graph.db_base import GraphDBBase

class TestCandidateSelection(unittest.TestCase):

    def setUp(self):
        self.store = GraphDBBase()

    def test_full_text_query(self):
        ner_out = [
            {
                "sentence": "Severe outcomes of Zika are due to its capacity to cross the placental barrier during pregnancy, causing microcephaly and congenital malformations.",
                "entities": [
                    {
                        "id": 0,
                        "mention": "Zika",
                        "label": "Organism",
                        "start": 19,
                        "end": 22
                    },
                    {
                        "id": 1,
                        "mention": "microcephaly",
                        "label": "Clinical finding (finding)",
                        "start": 105,
                        "end": 116
                    },
                    {
                        "id": 2,
                        "mention": "congenital malformations",
                        "label": "Clinical finding (finding)",
                        "start": 122,
                        "end": 145
                    }
                ]
            }
        ]

        labels = []
        for i in ner_out:
            for j in i['entities']:
                if j['label'] not in labels:
                    labels.append(j['label'])

        for index, value in enumerate(ner_out[0]["entities"]):
            candidates = CandidateSelection(self.store).get_candidates(value["mention"], labels, limit=4)
            ner_out[0]["entities"][index]["candidates"] = candidates
        
        print(json.dumps(ner_out, indent=4))

if __name__ == '__main__':
    unittest.main()
