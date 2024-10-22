import unittest
import json

from src.llm_model.model import LLM_Model
from src.nlp_task.path_manager import PathSummarization
from src.neo4j_graph.db_base import GraphDBBase

class TestPathSummarization(unittest.TestCase):

    def setUp(self):
        self.model = LLM_Model()
        self.store = GraphDBBase()

    def test_path_translation(self):
        text_paths = [
            {
                "sentence": "A Congenital Zika virus infection occurrence is associated with a Congenital occurrence, which in turn is associated with Micrencephaly."
            },
            {
                "sentence": "A Congenital Zika virus infection occurrence is associated with a Congenital occurrence, which in turn is associated with an Acrocephaly occurrence."
            },
            {
                "sentence": "A Congenital Zika virus infection occurs in a Congenital entity, and Multiple congenital malformations also occur in the same Congenital entity."
            },
            {
                "sentence": "A Congenital Zika virus infection occurs in a Congenital, and this occurrence is also associated with a Congenital malformation."
            },
            {
                "sentence": "A Congenital Zika virus infection occurs in a Congenital and is also an occurrence of Other congenital malformations."
            },
            {
                "sentence": "Micrencephaly occurs in Congenital and Multiple congenital malformations also occur in Congenital."
            },
            {
                "sentence": "Micrencephaly occurs in Congenital and is also an occurrence of Congenital malformation."
            },
            {
                "sentence": "Micrencephaly occurs in Congenital and Other congenital malformations."
            },
            {
                "sentence": "Acrocephaly occurs in Congenital and Multiple congenital malformations also occur in Congenital."
            },
            {
                "sentence": "Acrocephaly is a type of craniosynostosis syndrome, which is itself a type of congenital malformation."
            },
            {
                "sentence": "Acrocephaly is a pathological process with the attribute of being a pathological developmental process. This pathological developmental process is also an attribute of Congenital malformation."
            },
            {
                "sentence": "Acrocephaly occurs in Congenital and is also an occurrence of Congenital malformation."
            },
            {
                "sentence": "Acrocephaly occurs in Congenital and Other congenital malformations also occur in Congenital."
            }
        ]
        
        summarizer = PathSummarization(self.model, text_paths)
        summary = summarizer.summarize_paths()
        print(json.dumps(summary, indent=4))

if __name__ == '__main__':
    unittest.main()
