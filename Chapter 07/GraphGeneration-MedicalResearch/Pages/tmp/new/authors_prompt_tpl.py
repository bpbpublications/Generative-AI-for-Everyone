prompt = ''' From the artcile text for a reasearcher below, extract Entities strictly as instructed below
                1. Look for authors entity type and generate the information defined below:
                `id` property of each entity must be alphanumeric and must be unique among the entities. You will be referring this property to define the relationship between entities. NEVER create other entity types that aren't mentioned below. You will have to generate as many entities as needed as per the types below:
                Entity Definition:
                label:'Author',id:string,name:string,corresponding_author:string,author_affliation:string //Authors Node
                2. If you cannot find any information on the entities above, it is okay to return empty value. DO NOT create fictious data
                3. Do NOT create duplicate entities or properties
                4. Strictly extract only authors names and afflications. Each author is individual ENTITY
                5. corresponding_author is BINARY STRING of Yes or No if name is mentioned in corresponding author in the article
                6. DO NOT MISS out any Authors name related entity
                7. DO NOT CONSIDER AUTHORS IN REFERENCES
                8. NEVER Impute missing valuesA
                Output JSON (Strict):
                {"entities": [{"label":"Authors","id":A"author1","name":"Deipthan Prabakar","corresponding_author":"yes","author_affliation":"Internal Medicine, University of South Florida Morsani College of Medicine, Tampa, USA"}]}

                Question: Now, extract Authors information as mentioned above for the text below -
                $ctext

                Answer:
                 '''

