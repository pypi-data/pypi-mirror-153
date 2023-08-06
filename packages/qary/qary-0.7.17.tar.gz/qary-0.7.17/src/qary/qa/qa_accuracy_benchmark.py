import os
import json
import time
from tqdm import tqdm
import torch
from torch.utils.data import DataLoader, SequentialSampler
from transformers.data.processors.squad import (
    SquadResult, 
    SquadV1Processor,
    SquadV2Processor, 
)
from transformers import (
    AutoModelForQuestionAnswering,
    AutoTokenizer,
    squad_convert_examples_to_features,
)
from transformers.data.metrics.squad_metrics import (
    compute_predictions_logits,
    squad_evaluate,
)

from qary.constants import BASE_DIR, DATA_DIR

SQUAD_DIR = os.path.join(DATA_DIR, 'squad')
SQUAD_WITH_NEGATIVES = False

modelnames = [
    "bert-large-uncased-whole-word-masking-finetuned-squad",
    "ktrapeznikov/albert-xlarge-v2-squad-v2",
    "mrm8488/bert-tiny-5-finetuned-squadv2",
    "twmkn9/albert-base-v2-squad2",
    "distilbert-base-uncased",
    "distilbert-base-cased-distilled-squad",

    ]


def setup_model(modelname):

    prediction_settings = {
        "output_prediction_file": "predictions.json",
        "output_nbest_file": "nbest_predictions.json",
        "output_null_log_odds_file": "null_predictions.json",
        "n_best_size": 1,
        "max_answer_length": 254,
        "do_lower_case": True,
        "null_score_diff_threshold": 0.5,
    }

    tokenizer = AutoTokenizer.from_pretrained(modelname)
    model = AutoModelForQuestionAnswering.from_pretrained(modelname)

    return prediction_settings, tokenizer, model


def examples_to_features(tokenizer, squad_version=SQUAD_WITH_NEGATIVES, path=SQUAD_DIR):

    if squad_version is False:
        processor=SquadV1Processor()
        cached_features_file = os.path.join(path, f'dev-v1-features.json')
    elif squad_version == True:
        processor=SquadV2Processor()
        cached_features_file = os.path.join(path, f'dev-v2-features.json')

    try: 
        cached_data = torch.load(cached_features_file)
        examples = cached_data['examples']
        features = cached_data['features']
        dataset = cached_data['dataset']

    except FileNotFoundError:
        examples = processor.get_dev_examples(path)
        features, dataset = squad_convert_examples_to_features(
            examples=examples,
            tokenizer=tokenizer,
            max_seq_length=512,
            doc_stride = 128,
            max_query_length=256,
            is_training=False,
            return_dataset='pt',
            threads=16,
            )
        # torch.save({"features": features, "dataset": dataset, "examples": examples}, cached_features_file)

    return examples, features, dataset


def to_list(tensor):
    return tensor.detach().cpu().tolist()


def run_predictions(dataset, model, tokenizer, features):
    eval_sampler = SequentialSampler(dataset)
    eval_dataloader = DataLoader(dataset, sampler=eval_sampler, batch_size=20)
    
    all_results = []
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    for batch in tqdm(eval_dataloader):
        model.eval()
        batch = tuple(t.to(device) for t in batch)

        with torch.no_grad():

            inputs = {
                "input_ids": batch[0],
                "attention_mask": batch[1],
                "token_type_ids": batch[2],
            }

            example_indices = batch[3]

            outputs = model(**inputs)

            for i, example_index in enumerate(example_indices):
                eval_feature = features[example_index.item()]
                unique_id = int(eval_feature.unique_id)

                output = [to_list(output[i]) for output in outputs]

                start_logits, end_logits = output
                result = SquadResult(unique_id, start_logits, end_logits)
                all_results.append(result)
    return all_results


def distilbert_predictions(examples, dataset, features, model, tokenizer):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    eval_sampler = SequentialSampler(dataset)
    eval_dataloader = DataLoader(dataset, sampler=eval_sampler, batch_size=20)
    
    all_results = []
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    for batch in tqdm(eval_dataloader):
        model.eval()
        batch = tuple(t.to(device) for t in batch)

        with torch.no_grad():

            inputs = {
                "input_ids": batch[0],
                "attention_mask": batch[1],
            }

            example_indices = batch[3]

            outputs = model(**inputs)

            for i, example_index in enumerate(example_indices):
                eval_feature = features[example_index.item()]
                unique_id = int(eval_feature.unique_id)

                output = [to_list(output[i]) for output in outputs]

                start_logits, end_logits = output
                result = SquadResult(unique_id, start_logits, end_logits)
                all_results.append(result)

    return all_results


def evaluate_predictions(features,
                    examples,
                    results,
                    tokenizer,
                    modelname,
                    settings,
                    squad_with_negatives=SQUAD_WITH_NEGATIVES, 
                    output_path=DATA_DIR, 
                    verbose=False):
    modelname = modelname.replace("/", "-") 
    if squad_with_negatives is False:
        subfolder = "predictions-v1"
    elif squad_with_negatives is True:
        subfolder = "predictions-v2"
        
    results_path = os.path.join(output_path, subfolder, modelname)
    os.makedirs(results_path, exist_ok=True)

    output_prediction_file = os.path.join(results_path, settings["output_prediction_file"])
    output_nbest_file = os.path.join (results_path, settings["output_nbest_file"])
    output_null_log_odds_file = os.path.join(results_path, settings["output_null_log_odds_file"])
    n_best_size = settings["n_best_size"]
    max_answer_length = settings["max_answer_length"]
    do_lower_case = settings["do_lower_case"]
    null_score_diff_threshold = settings["null_score_diff_threshold"]

    predictions = compute_predictions_logits(
        examples,
        features,
        results,
        n_best_size,
        max_answer_length,
        do_lower_case,
        output_prediction_file,
        output_nbest_file,
        output_null_log_odds_file,
        False,  # verbose_logging
        squad_with_negatives,  # version_2_with_negative
        null_score_diff_threshold,
        tokenizer,
    )

    return predictions


def benchmark_model(modelname):
    prediction_settings, tokenizer, model = setup_model(modelname)
    examples, features, dataset = examples_to_features(tokenizer)

    if 'distilbert' in modelname:
        results = distilbert_predictions(examples,dataset, features, model, tokenizer)
    else:
        results = run_predictions(dataset, model, tokenizer, features)
    
    evaluate_predictions(features, examples, results, tokenizer, modelname, prediction_settings)


if __name__ == '__main__':
    for m in modelnames:
        benchmark_model(m)