from datasets import load_dataset, Dataset
import pandas as pd
from transformers import AutoTokenizer, AutoModel
import torch

device = torch.device("cpu")

class FAISS:
    def __init__(self, config, data_dir, **kwargs): 

        self.config = config
        model_id = self.config['model_id']
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModel.from_pretrained(model_id).to(device)
        self.data_dir = data_dir

    def query(self, input, k:int=5, return_pd:bool=True): 
        csv_dataset = self._preparing_csv_dataset(self.data_dir)
        embedding_dataset = self.get_embedding_dataset(csv_dataset)
        question_embedding = self.get_embeddings([input]).detach().numpy()
        embedding_dataset.add_faiss_index(column="embeddings")
        scores, samples = embedding_dataset.get_nearest_examples(
            "embeddings", question_embedding, k=k
        )
        if return_pd: 
            samples_df = pd.DataFrame.from_dict(samples)
            samples_df["scores"] = scores
            samples_df.sort_values("scores", ascending=False, inplace=True)
            return samples_df
        else: 
            return {"samples": samples, 
                    "scores": scores}

    def _preparing_csv_dataset(self, dir:str, 
                            keep_column:list[str]=['Platform', 'Distributor', 'Description', 'Min_CPU', 'Min_RAM_GB', 'Min_Storage_GB', 'Installed_Software', 'Image_Version']
                            )-> pd.DataFrame: 
        if not '.csv' in dir: 
            return None
        dataset = load_dataset('csv', data_files=dir)
        columns = dataset.column_names
        columns_to_remove = set(keep_column).symmetric_difference(columns['train'])
        issues_dataset = dataset.remove_columns(columns_to_remove)
        issues_dataset.set_format(type="pandas")
        df = issues_dataset['train'][:]
        return df

    def _concatenate_text(self, examples):
        return {
            "text": examples["Platform"] + " " + 
                examples["Distributor"] + " " + 
                examples["Description"] + " " + 
                "Min CPU: " + str(examples["Min_CPU"]) + " cores " + 
                "Min RAM: " + str(examples["Min_RAM_GB"]) + " GB " + 
                "Min Storage: " + str(examples["Min_Storage_GB"]) + " GB " +
                "Installed Software: " + examples["Installed_Software"] + " " + 
                "Image Version: " + examples["Image_Version"]
        }

    def cls_pooling(self, model_output):
        return model_output.last_hidden_state[:, 0]

    def get_embeddings(self, text_list):
        encoded_input = self.tokenizer(
            text_list, padding=True, truncation=True, return_tensors="pt"
        )
        encoded_input = {k: v.to(device) for k, v in encoded_input.items()}
        model_output = self.model(**encoded_input)
        return self.cls_pooling(model_output)

    def get_embedding_dataset(self, df: pd.DataFrame): 
        comments_dataset = Dataset.from_pandas(df)
        comments_dataset = comments_dataset.map(self._concatenate_text)

        embedding_dataset = comments_dataset.map(
        lambda x: {"embeddings": self.get_embeddings(x["text"])[0]}
        )
        return embedding_dataset