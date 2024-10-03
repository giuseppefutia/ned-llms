from tqdm import tqdm
import itertools

class PathExtraction():
  def __init__(self, model, store, candidates, named_entities):
    self.model = model
    self.store = store
    self.candidates = candidates
    self.named_entities = named_entities

  def create_mention_pairs(self):
    mentions = [i['id'] for i in self.candidates['entities']]
    mention_pairs = list(itertools.combinations(mentions, 2))

    return mention_pairs

  def create_candidate_pairs(self, pair):
    src_ents = [i['candidates'] for i in self.candidates['entities'] if i['id'] == pair[0]][0]
    src_ids = [i['snomed_id'] for i in src_ents]

    dst_ents = [i['candidates'] for i in self.candidates['entities'] if i['id'] == pair[1]][0]
    dst_ids = [i['snomed_id'] for i in dst_ents]
    return list(itertools.product(src_ids, dst_ids))

  def get_co_occs_query(self, s1_id, s2_id):
    query = f"""
      CALL gds.degree.stream('snomedGraph')
      YIELD nodeId, score
      WITH gds.util.asNode(nodeId).name AS name, score AS degree
      ORDER BY degree DESC
      LIMIT 350
      WITH collect(name) as hub_nodes
      MATCH (s1), (s2)
      WHERE s1.id="{s1_id}" AND
            s2.id="{s2_id}" AND
            ANY(x IN s1.type WHERE x IN {self.named_entities}) AND
            ANY(x IN s2.type WHERE x IN {self.named_entities})
      WITH s1, s2, allShortestPaths((s1)-[:SNOMED_RELATION*1..2]-(s2)) AS paths, hub_nodes
      UNWIND paths AS path
      WITH relationships(path) AS path_edges, nodes(path) as path_nodes, hub_nodes
      WITH [n IN path_nodes | n.name] AS node_names,
          [r IN path_edges | r.type] AS rel_types,
          [n IN path_edges | startnode(n).name] AS rel_starts,
          hub_nodes
      WHERE not any(x IN node_names WHERE x IN hub_nodes)
      WITH [i in range(0, size(node_names)-1) | CASE
      WHEN i = size(node_names)-1
      THEN "(" + node_names[size(node_names)-1] + ")"
      WHEN node_names[i] = rel_starts[i]
      THEN "(" + node_names[i] + ")" + '-[:' + rel_types[i] + ']->'
      ELSE "(" + node_names[i] + ")" + '<-[:' + rel_types[i] + ']-' END] as string_paths
      RETURN DISTINCT apoc.text.join(string_paths, '') AS `Extracted paths`
    """.format(s1_id=s1_id, s2_id=s2_id, named_entities=self.named_entities)
    return query

  def get_paths(self):
    with self.store._driver.session() as session:
        paths = []
        mention_pairs = self.create_mention_pairs()

        outer_loop = tqdm(mention_pairs,
                        desc="Processing mention pairs...",
                        position=0,
                        leave=True)
        for i in outer_loop:
            candidate_pairs = self.create_candidate_pairs(i)
            inner_loop = tqdm(candidate_pairs,
                            desc="Processing candidates for each pair...",
                            position=1,
                            leave=False)
            for j in inner_loop:
                query = self.get_co_occs_query(j[0], j[1])
                paths.append(session.run(query))

        cleaned_paths = [sub_item['Extracted paths'] for item in paths for sub_item in item]

        out = {}
        out['paths'] = []
        for item in cleaned_paths:
            out['paths'].append({'id': len(out['paths']) + 1, 'path': item})

        return out