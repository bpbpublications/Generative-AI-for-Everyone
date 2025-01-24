prompt = '''  From the article text below, extract Entities strictly as instructed below
                1. Look for Category Entities in the text. The`id` property of each entity must be alphanumeric and must be unique among the entities. NEVER create new entity types that aren't mentioned below:
                Entity Definition:
                label:'Category',id:string,name:string //CATEGORY Node
                2. NEVER Impute missing values
                3. If you do not find any Category mentioned extract maximum of 2 Category for the article and Category MUST be related to Medical department or Medical Sub-specialities
                Example Output Format:
                {"entities": [{"label":"Category","id":"category1","name":"Internal Medicine"},{"label":"Category","id":"category2","name":"Neurology"}]}

                Question: Now, extract entities as mentioned above for the text below -
                $ctext

                Answer:
                  '''
