import re
import json
import vertexai
import importlib
from query_res import *
import query_res as q
import streamlit as st
from string import Template

from google.cloud import aiplatform
from langchain_community.graphs import Neo4jGraph
from google.oauth2 import service_account
from vertexai.preview.language_models import TextGenerationModel

import pickle




def extract_results(option,doc):
  project_id = st.secrets['project_id']
  location = st.secrets['location']
  key_path= st.secrets['key_path']
  credentials =  service_account.Credentials.from_service_account_file(key_path)
  vertexai.init(project=project_id , location = location , credentials = credentials)
  model = TextGenerationModel.from_pretrained("text-bison")
  results={"entities": [], "relationships": []}

  for p in option:
      if p == 'article_prompt_tpl':
         sample = str(doc.get(p)) + str(doc.get('reference_prompt_tpl'))
      else:
         sample = str(doc.get(p))
      prompt = Template(option[p]).substitute(ctext= re.sub(r'[^\x00-\x7F]+',' ', sample))
      response = model.predict(prompt,temperature =0 ,max_output_tokens=1024, top_k=40, top_p=0.8)
      response = response.text

      if 'Answer:\n' in response:
          response = response.split('Answer:\n ')[1]
      if response.strip() == '':

          continue
      try:
          print(response)
          response = json.loads(response.replace("\'", "'").replace('`', ''))
      except json.JSONDecodeError:
          response = response[:response.rfind("}")+1] + ']}'
          response = json.loads(response.replace("\'", "'"))
      results["entities"].extend(response["entities"])
      if "relationships" in response:
          results["relationships"].extend(response["relationships"])

  article_id = results["entities"][0]["id"]
  for e in results["entities"][1:]:
      if e['label'] == 'Authors':
          results["relationships"].append(f"{article_id}|HAS_AUTHOR|{e['id']}")
      if e['label'] == 'Keyword':
          results["relationships"].append(f"{article_id}|HAS_KEYWORD|{e['id']}")
      if e['label'] == 'Category':
          results["relationships"].append(f"{article_id}|HAS_CATEGORY|{e['id']}")
  return(results)



def generate_cypher(file_name, in_json):
    
    def get_cypher_compliant_var(_id):
      s = "_"+ re.sub(r'[\W_]', '', _id).lower() #avoid numbers appearing as firstchar; replace spaces
      return s[:20] #restrict variable size
    
    def get_prop_str(prop_dict, _id):
      s = []
      for key, val in prop_dict.items():
        if key != 'label' and key != 'id':
           s.append(_id+"."+key+' = "'+str(val).replace('\"', '"').replace('"', '\"')+'"') 
      return ' ON CREATE SET ' + ','.join(s)

    e_map = {}
    e_stmt = []
    r_stmt = []
    e_stmt_tpl = Template("($id:$label{id:'$key'})")
    r_stmt_tpl = Template("""
      MATCH $src
      MATCH $tgt
      MERGE ($src_id)-[:$rel]->($tgt_id)
    """)
    for obj in in_json:
      for j in obj['entities']:
          props = ''
          label = j['label']
          id = ''
          if label == 'Article':
            id = 'p'+str(file_name)
          elif label == 'Category':
            c = j['id'].replace('category', '_')
            id = f'j{str(file_name)}{c}'

          elif label == 'Keyword':
            c = j['id'].replace('keyword', '_')
            id = f'e{str(file_name)}{c}'

          else:
            id = get_cypher_compliant_var(j['name'])
          if label in ['Article', 'Reference', 'Authors', 'Category', 'Keyword']:
            varname = get_cypher_compliant_var(j['id'])
            stmt = e_stmt_tpl.substitute(id=varname, label=label, key=id)
            e_map[varname] = stmt
            e_stmt.append('MERGE '+ stmt + get_prop_str(j, varname))

      for st in obj['relationships']:
          rels = st.split("|")
          src_id = get_cypher_compliant_var(rels[0].strip())
          rel = rels[1].strip()
          if rel in ['HAS_AUTHOR', 'HAS_KEYWORD', 'REFERED', 'HAS_CATEGORY']: #we ignore other relationships
            tgt_id = get_cypher_compliant_var(rels[2].strip())
            stmt = r_stmt_tpl.substitute(
              src_id=src_id, tgt_id=tgt_id, src=e_map[src_id], tgt=e_map[tgt_id], rel=rel)
            r_stmt.append(stmt)

    return e_stmt, r_stmt


def neo4j_graph_creation(ent_cyp,rel_cyp):

  graph = Neo4jGraph(
  url=st.secrets['url'], username=st.secrets['username'], password=st.secrets['password']
  )
  for e in ent_cyp:
      graph.query(e)

  for r in rel_cyp:
      graph.query(r)


