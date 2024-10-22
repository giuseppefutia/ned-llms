import unittest
import json

from src.llm_model.model import LLM_Model
from src.nlp_task.path_manager import PathTranslation
from src.neo4j_graph.db_base import GraphDBBase

class TestPathTranslation(unittest.TestCase):

    def setUp(self):
        self.model = LLM_Model()
        self.store = GraphDBBase()

    def test_path_translation(self):
        paths = [
            {
                "id": 1,
                "path": "(Congenital Zika virus infection)-[:OCCURRENCE]->(Congenital)<-[:OCCURRENCE]-(Micrencephaly)"
            },
            {
                "id": 2,
                "path": "(Congenital Zika virus infection)-[:OCCURRENCE]->(Congenital)<-[:OCCURRENCE]-(Acrocephaly)"
            },
            {
                "id": 3,
                "path": "(Congenital Zika virus infection)-[:OCCURRENCE]->(Congenital)<-[:OCCURRENCE]-(Multiple congenital malformations)"
            },
            {
                "id": 4,
                "path": "(Congenital Zika virus infection)-[:OCCURRENCE]->(Congenital)<-[:OCCURRENCE]-(Congenital malformation)"
            },
            {
                "id": 5,
                "path": "(Congenital Zika virus infection)-[:OCCURRENCE]->(Congenital)<-[:OCCURRENCE]-([X]Other congenital malformations)"
            },
            {
                "id": 6,
                "path": "(Micrencephaly)-[:OCCURRENCE]->(Congenital)<-[:OCCURRENCE]-(Multiple congenital malformations)"
            },
            {
                "id": 7,
                "path": "(Micrencephaly)-[:OCCURRENCE]->(Congenital)<-[:OCCURRENCE]-(Congenital malformation)"
            },
            {
                "id": 8,
                "path": "(Micrencephaly)-[:OCCURRENCE]->(Congenital)<-[:OCCURRENCE]-([X]Other congenital malformations)"
            },
            {
                "id": 9,
                "path": "(Acrocephaly)-[:OCCURRENCE]->(Congenital)<-[:OCCURRENCE]-(Multiple congenital malformations)"
            },
            {
                "id": 10,
                "path": "(Acrocephaly)-[:IS_A]->(Craniosynostosis syndrome)-[:IS_A]->(Congenital malformation)"
            },
            {
                "id": 11,
                "path": "(Acrocephaly)-[:PATHOLOGICAL_PROCESS_(ATTRIBUTE)]->(Pathological developmental process)<-[:PATHOLOGICAL_PROCESS_(ATTRIBUTE)]-(Congenital malformation)"
            },
            {
                "id": 12,
                "path": "(Acrocephaly)-[:OCCURRENCE]->(Congenital)<-[:OCCURRENCE]-(Congenital malformation)"
            },
            {
                "id": 13,
                "path": "(Acrocephaly)-[:OCCURRENCE]->(Congenital)<-[:OCCURRENCE]-([X]Other congenital malformations)"
            }
        ]
        
        text_paths = []
        for path in paths:
            path_translator = PathTranslation(self.model, path)
            text_paths.append(path_translator.translate_paths_to_text())
        print(json.dumps(text_paths, indent=4))

if __name__ == '__main__':
    unittest.main()
