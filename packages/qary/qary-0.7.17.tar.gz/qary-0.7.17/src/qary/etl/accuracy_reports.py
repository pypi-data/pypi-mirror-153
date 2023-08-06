"""Accuracy reports"""

import json
import gzip
import pathlib
import datetime
import psutil
import multiprocessing

from collections import Counter

from qary import __version__
from qary import constants
from qary.etl.netutils import download_if_necessary, upload_to_digitalocean
from qary.qa.qa_datasets import get_bot_accuracies, load_qa_dataset


def accuracy_report(*skills, scored_qa_pairs=None, upload=True):
    """  get_bot_accuracies() on list of skills and appends to previous results, uploading copy to digitalocean

    FIXME: qa skill is broke because transformers and torch upgraded
    >> filepath = pathlib.Path(constants.DATA_DIR, 'testsets', 'dialog', 'qa-tiny-2020-05-24.json')
    >> scored_qa_pairs=load_qa_dataset(filepath)
    >> from qary.skills import qa
    >> accuracy_report(qa, scored_qa_pairs=scored_qa_pairs, upload=False)
    """

    if not scored_qa_pairs:
        scored_qa_pairs_path = pathlib.Path(constants.DATA_DIR, 'testsets', 'dialog', 'qa-2020-04-25.json')
        scored_qa_pairs = load_qa_dataset(scored_qa_pairs_path)
    for skill in skills:
        file_name = 'accuracy_report.gz'

        time = str(datetime.datetime.now())
        skill_name = pathlib.Path(str(skill)).stem
        skill = skill.Skill()
        cpu_count = multiprocessing.cpu_count()
        cpu_clock_rate = psutil.cpu_freq().current
        results = list(get_bot_accuracies(skill, scored_qa_pairs=scored_qa_pairs))

        report = [
            {
                "timestamp": time,
                "skill": skill_name,
                "qary_version": __version__,
                "cpu_count": cpu_count,
                "cpu_clock_rate": cpu_clock_rate,
                "results": results
            }
        ]

        results_summary = [
            {
                "total_tests": total_tests(results),
                "total_runtime": total_runtime(results),
                "total_w2v_similarity": total_w2v_similarity(results),
                "longest_run_time": question_of_longest_shortest_runtime(results)[0],
                "longest_run_question": question_of_longest_shortest_runtime(results)[1],
                "shortest_run_time": question_of_longest_shortest_runtime(results)[2],
                "shortest_run_question": question_of_longest_shortest_runtime(results)[3]
            }

        ]

        summary = [
            {
                "timestamp": time,
                "skill": skill_name,
                "qary_version": __version__,
                "cpu_count": cpu_count,
                "cpu_clock_rate": cpu_clock_rate,
                "summary": results_summary
            }
        ]

        gzip_report_filepath = pathlib.Path(constants.DATA_DIR, 'testsets', file_name)
        gzip_summary_report = pathlib.Path(constants.DATA_DIR, 'testsets', "summary_accuracy_report.gz")
        qa_filepath = download_if_necessary('accuracy_report')
        summary_filepath = download_if_necessary('summary_accuracy_report')

        if qa_filepath:  # if file already exists on digitalocean
            reports = gzip_decompress_decode_load_json(GZIP_FILEPATH=qa_filepath)
            accuracy_report = reports + report
            compressed_json = json_encode_compress(data=accuracy_report)

            with gzip.open(gzip_report_filepath, 'wb') as accu:
                accu.write(compressed_json)

            summary_reports = gzip_decompress_decode_load_json(GZIP_FILEPATH=summary_filepath)
            summary_accuracy_report = summary_reports + summary
            compressed_summary = json_encode_compress(data=summary_accuracy_report)

            with gzip.open(gzip_summary_report, 'wb') as accu:
                accu.write(compressed_summary)

        else:
            # if file does not already exists on digitalocean
            with gzip.open(gzip_report_filepath, 'wb') as accu:
                compressed_json = json_encode_compress(report)
                accu.write(compressed_json)

            with gzip.open(gzip_summary_report, 'wb') as accu:
                compressed_summary = json_encode_compress(summary)
                accu.write(compressed_summary)

        if upload:
            file_to_upload = str(gzip_report_filepath)
            name_of_space = "midata"
            digital_ocean_path_and_newfolders = 'public/nlp/qary/accuracy_reports'
            new_name_file_to_upload = file_name
            upload_to_digitalocean(file_to_upload, name_of_space, digital_ocean_path_and_newfolders, new_name_file_to_upload)
            gzip_report_filepath = pathlib.Path(constants.DATA_DIR, 'testsets', file_name).unlink()

            file_to_upload = str(gzip_summary_report)
            new_name_file_to_upload = "summary_accuracy_report.gz"
            upload_to_digitalocean(file_to_upload, name_of_space, digital_ocean_path_and_newfolders, new_name_file_to_upload)
            gzip_summary_report = pathlib.Path(constants.DATA_DIR, 'testsets', "summary_accuracy_report.gz").unlink()


def gzip_decompress_decode_load_json(GZIP_FILEPATH):
    """opens gzip file decompresses decodes and returns object

    >>> GZIP_FILEPATH = pathlib.Path(constants.DATA_DIR, 'testsets', 'unit_test_data.gz')
    >>> gzip_decompress_decode_load_json(GZIP_FILEPATH)
    {'Hello World': 42}
    """

    with gzip.open(GZIP_FILEPATH) as data:
        obj = data.read()
        obj = gzip.decompress(obj)
        obj = obj.decode('utf-8')
        obj = json.loads(obj)
        return obj


def json_encode_compress(data):
    """compresses and encodes data

    >>> data = {"Hello World": 42}
    >>> compressed_json = json_encode_compress(data)
    >>> type(compressed_json)
    <class 'bytes'>
    """

    obj = json.dumps(data)
    encoded_json = obj.encode('utf-8')
    compressed_json = gzip.compress(encoded_json)
    return compressed_json


def print_accuracy_report(verbose=True, qa_filepath=None):
    """ prints reports to terminal

    >>> print_accuracy_report(verbose=False)
    """

    qa_filepath = qa_filepath or download_if_necessary('accuracy_report')
    with gzip.open(qa_filepath) as accu_test:
        accu_test = accu_test.read()
        accu_test = gzip.decompress(accu_test)
        accu_test = accu_test.decode('utf-8')
        results = json.loads(accu_test)
    if verbose:
        print(json.dumps(results, indent=4, separators=(", ", ": ")))


def report_obj(qa_filepath=None):
    """ loads accuracy_report json object for data manipulation

    >>> obj = report_obj()
    >>> obj[0]['qary_version']
    '0.5.19.post0.dev18+g540a53c.dirty'
    """

    qa_filepath = qa_filepath or download_if_necessary('accuracy_report')
    with gzip.open(qa_filepath) as obj:
        obj = obj.read()
        obj = gzip.decompress(obj)
        obj = obj.decode('utf-8')
        return json.loads(obj)


def total_w2v_similarity(results):
    """ gets sum of 'bot_w2v_similarity'

    >>> results = report_obj()[0]['results']
    >>> total_w2v_similarity(results)
    62.506820987096695
    """

    summary = Counter()
    for result in results:
        summary.update(result)
    return summary['bot_w2v_similarity']


def total_tests(results):  # or len(results)
    """Gets total tests

    >>> results = report_obj()[0]['results']
    >>> total_tests(results)
    154
    """

    total = sum([1 for result in results])
    return total


def total_runtime(results):
    """gets longest run_time

    >>> results = report_obj()[0]['results']
    >>> total_runtime(results)
    1986.6971192359924
    """

    results = [result['run_time'] for result in results]
    return sum(results)


def question_of_longest_shortest_runtime(results):
    """gets longest_run_time, shortest_run_time and their associated questions

    >>> results = report_obj()[0]['results']
    >>> question_of_longest_shortest_runtime(results)
    (3..., 'When was Barack Obama President?', 8..., 'Who is the Famous motivational speaker from Atlanta?')
    """

    longest_run_time = int()
    longest_run_question = str()
    shortest_run_time = 10
    shortest_run_question = str()
    for test in results:
        if test['run_time'] > longest_run_time:
            longest_run_time = test['run_time']
            longest_run_question = test['question']
        elif test['run_time'] > 1 and test['run_time'] < shortest_run_time:
            shortest_run_time = test['run_time']
            shortest_run_question = test['question']
    return longest_run_time, longest_run_question, shortest_run_time, shortest_run_question


def print_report_summary(verbose=True, summary_filepath=None):
    """ prints reports to terminal

    >>> print_report_summary(verbose=False)
    """

    summary_filepath = summary_filepath or download_if_necessary('summary_accuracy_report')
    with gzip.open(summary_filepath) as accu_test:
        accu_test = accu_test.read()
        accu_test = gzip.decompress(accu_test)
        accu_test = accu_test.decode('utf-8')
        results = json.loads(accu_test)
    if verbose:
        print(json.dumps(results, indent=4, separators=(", ", ": ")))
