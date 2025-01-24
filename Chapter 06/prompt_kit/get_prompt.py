import os
def list_prompt():
    prompt_names=[]
    path = 'new'
    for filename in os.listdir(path):
        if filename.endswith('.py'):
            (name, ext) = os.path.splitext(filename)
            prompt_names.append(name)
    return(prompt_names)

