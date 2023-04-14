import pandas as pd

data_df = pd.read_json('../data/proc_data/test_data-complete_task.jsonl', lines=True)

prompts = data_df['prompt'].tolist()

prompts = [prompt.replace('Analyse the following essay:\n\n', '') for prompt in prompts]

with open('../data/proc_data/validation_essays.txt', 'w') as f:
    for prompt in prompts:
        f.write(prompt)