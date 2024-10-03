class CandidateSelection:
    # TODO: Add embedding search
    def __init__(self, store):
        self.store = store

    def full_text_query(self):
        query = """
                CALL db.index.fulltext.queryNodes("names", $fulltextQuery, {limit: $limit})
                YIELD node
                WHERE node:SnomedEntity
                RETURN distinct node.name AS candidate_name, node.id AS candidate_id
                """

        return query

    def generate_full_text_query(self, input):
        full_text_query = ""
        words = [el for el in input.split() if el]

        if len(words) > 1:
            for word in words[:-1]:
                full_text_query += f" {word}~2 AND"
                full_text_query += f" {words[-1]}~2"
        else:
            full_text_query = words[0] + "~2"

        return full_text_query.strip()

    def get_candidates(self, input, limit = 10):
        ft_query = self.generate_full_text_query(input)
        with self.store._driver.session() as session:
            candidates = session.run(self.full_text_query(), {"fulltextQuery": ft_query, "limit":limit})

            return [{"snomed_id" :c["candidate_id"], "name": c['candidate_name']} for c in candidates]
