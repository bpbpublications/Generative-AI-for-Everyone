prompt = ''' From the Resume text for a job aspirant below, extract Entities & relationships strictly as instructed below
                1. First, look for atricle name , article types , publication data, DOI  and summarize the abstract to 20 words and summarize the conclusion in 15 words in the text and extract all reference in reference section in comma-separated format. 
                ARTICLE Entity denotes the text that is been analyzed. 
                REFERENCE node is the all references of articles mentioned in Reference section.
                `id` property of each entity must be alphanumeric and must be unique among the entities. You will be referring this property to define the relationship between entities. NEVER create new entity types that aren't mentioned below. You will have to generate as many entities as needed as per the types below:
                Entity Types:
                label:'Article',id:string,title:string,article_type:string,DOI:string,pub_date:string,abstract:string, conclusion:string //ARTICLE Node
                label:'Reference',id:string,name:string //REFERENCE Node
                2. Next generate each relationships as triples of head, relationship and tail.
                  To refer the head and tail entity, use their respective `id` property. 
                  NEVER create new Relationship types that aren't mentioned below:
                Relationship definition:
                Article|REFERED|Reference //Ensure this is a string in the generated output
                3. If you cannot find any information on the entities & relationships above, 
                it is okay to return empty value. DO NOT create fictious data
                4. Do NOT create duplicate entities. 
                5. No Names or Date information should be extracted from references.
                6. DO NOT MISS out any Article or References related information
                7. LOOK FOR reference in Reference section and there can be multiple references
                8. NEVER Impute missing values
                Example Output JSON:
                {"entities": [{"label":"Article","id":"article1","title":"Recurrent Multifocal Embolic Strokes in a 50-Year-Old Male: Unmasking Occult Squamous CellCarcinoma","article_type":"Open Acess report","DOI":"10.7759/cureus.45091","pub_date":"09/12/2023", "abstract":"Although the primary source of cancer could not be identified, the P16+ status suggests the right tonsil" , "conclusion":"In summary, this case report underscores the complex connection between cryptogenic stroke and hidden malignancy"},
                {"label":"Reference","id":"reference1","name":"Stroke: Etiology, classification, and epidemiology"},
                {"label":"Reference","id":"reference2","name":"Cryptogenic stroke and embolic stroke of undetermined source (ESUS) "}],
                "relationships": ["article1|REFERED|reference1","article1|REFERED|reference2"]}                
                
                Question: Now, extract entities & relationships as mentioned above for the text below -
                $ctext

                Answer:
                 '''

