import unittest
from unittest.mock import MagicMock, patch
from src.nlp_task.ned_cs import CandidateSelection

class TestCandidateSelection(unittest.TestCase):

    def setUp(self):
        # Set up mock store object
        self.store = MagicMock()
        self.session_mock = MagicMock()
        self.store._driver.session.return_value.__enter__.return_value = self.session_mock
        
        # Instantiate the CandidateSelection class with mocked store
        self.candidate_selection = CandidateSelection(self.store)

    def test_full_text_query(self):
        expected_query = """
                CALL db.index.fulltext.queryNodes("names", $fulltextQuery, {limit: $limit})
                YIELD node
                WHERE node:SnomedEntity
                RETURN distinct node.name AS candidate_name, node.id AS candidate_id
                """
        result = self.candidate_selection.full_text_query()
        self.assertEqual(result.strip(), expected_query.strip())

    def test_generate_full_text_query_single_word(self):
        input_text = "heart"
        expected_query = "heart~2"
        result = self.candidate_selection.generate_full_text_query(input_text)
        self.assertEqual(result, expected_query)

    def test_generate_full_text_query_multiple_words(self):
        input_text = "heart attack"
        expected_query = "heart~2 AND attack~2"
        result = self.candidate_selection.generate_full_text_query(input_text)
        self.assertEqual(result, expected_query)

    @patch('src.nlp_task.ned_cs.CandidateSelection.generate_full_text_query')  # Mock internal method
    def test_get_candidates(self, mock_generate_ft_query):
        input_text = "heart attack"
        limit = 10
        mock_generate_ft_query.return_value = """ 
                CALL db.index.fulltext.queryNodes("names", $fulltextQuery, {limit: $limit})
                YIELD node
                WHERE node:SnomedEntity
                RETURN distinct node.name AS candidate_name, node.id AS candidate_id
                """
        
        mock_candidates = [
            {"candidate_name": "Heart Disease", "candidate_id": "S12345"},
            {"candidate_name": "Myocardial Infarction", "candidate_id": "S67890"}
        ]
        self.session_mock.run.return_value = mock_candidates

        result = self.candidate_selection.get_candidates(input_text, limit=2)
        
        expected_result = [
            {"snomed_id": "S12345", "name": "Heart Disease"},
            {"snomed_id": "S67890", "name": "Myocardial Infarction"}
        ]
        
        self.assertEqual(result, expected_result)

        # Ensure the session.run method was called with correct arguments
        self.session_mock.run.assert_called_once_with("mocked_full_text_query", index="entity", limit=2)
        mock_generate_ft_query.assert_called_once_with(input_text)

if __name__ == '__main__':
    unittest.main()
