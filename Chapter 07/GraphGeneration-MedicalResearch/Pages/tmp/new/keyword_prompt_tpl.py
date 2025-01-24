prompt = '''  From the article text below, extract Entities strictly as instructed below
                1. Look for keywords Entities in the text. The`id` property of each entity must be alphanumeric and must be unique among the entities. NEVER create new entity types that aren't mentioned below:
                Entity Definition:
                label:'Keyword',id:string,name:string //KEYWORDS Node
                2. NEVER Impute missing values
                3. If you do not find any keywords mentioned extract maximum of 6 keywords for the article and keywords msut be related to Medicine or Medical terms
                Example Output Format:
                {"entities": [{"label":"Keyword","id":"keyword1","name":"embolic stroke"},{"label":"Keyword","id":"keyword2","name":"occult malignancy"}]}

                Question: Now, extract entities as mentioned above for the text below -
                $ctext

                Answer:
                  '''