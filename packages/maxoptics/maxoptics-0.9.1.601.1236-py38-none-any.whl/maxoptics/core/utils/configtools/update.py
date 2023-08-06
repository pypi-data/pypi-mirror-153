# coding=UTF-8
import glob
import json
import os
from copy import deepcopy
from pathlib import Path

from maxoptics.config import BASEDIR
# FIXME: dep on var
from maxoptics.var.models.generators.YAMLGenerator import ClassCollection


# def byteify(input, encoding='utf-8'):
#     if isinstance(input, dict):
#         return {byteify(key): byteify(value) for key, value in input.iteritems()}
#     elif isinstance(input, list):
#         return [byteify(element) for element in input]
#     elif isinstance(input, unicode):
#         return input.encode(encoding)
#     else:
#         return input


def analyse(file_path: Path, ClassColle):
    # Import file
    file_type = str(file_path).split(".")[-1]
    with open(file_path, "r", encoding="utf-8") as f:
        print(f"{file_path = }")
        print(f"{file_type = }")
        sample: dict = json.load(f, encoding="utf-8")
    # import file identical key set
    importable_file_key_set = {"data", "materials", "waveforms", "code"}
    # "concrete" object identical key set
    concrete_object_key_set = {"name", "attrs", "children", "type"}
    # "abstract" object key set
    abstract_object_key_set = {"name", "attrs"}
    if importable_file_key_set.issubset(sample.keys()):  # Is importable files
        # Traversal the "data" dict
        # (Dict, key, None); or (Dict, key, index) where Dict[key] is an Iterable
        next_layer = [(sample, "data", None)]

        while True:  # BFS
            this_layer = next_layer
            next_layer = []

            for tup in this_layer:
                # Mother object, key value, index
                dikt, dikt_key, index = tup

                # Child object
                sub_dict: dict = (
                    deepcopy(dikt[dikt_key])
                    if index is None
                    else deepcopy(dikt[dikt_key][index])
                )

                # Prepare the next layer
                for sub_dict_key, sub_val in sub_dict.items():
                    if isinstance(sub_val, dict):
                        next_layer.insert(0, (sub_dict, sub_dict_key, None))

                    elif isinstance(sub_val, list):
                        for _ind in range(len(sub_val)):
                            if isinstance(sub_val[_ind], dict):
                                next_layer.insert(
                                    0, (sub_dict, sub_dict_key, _ind)
                                )

                # Classify self; pop self
                #  A CONCRETE
                if "type" in dikt and not isinstance(dikt["type"], int):
                    belong2 = "__CONCRETE__" + dikt["type"]["name"]

                #  A BASE CLASS
                elif "name" in dikt:
                    belong2 = dikt["name"]

                #  AT ROOT OF DOCUMENT
                elif "tree" in dikt:
                    belong2 = "$<----" + dikt_key + (index is not None) * "*"

                #  Same Level with DOCUMENT?
                else:
                    pass

                if concrete_object_key_set.issubset(
                    sub_dict.keys()
                ):  # Concrete Object
                    sub_dict["type"]["__delete__"] = True
                    ClassColle.inject(
                        "__CONCRETE__" + sub_dict["type"]["name"],
                        (sub_dict["type"]["name"],),
                        sub_dict,
                        (file_type, belong2),
                    )

                    # Remove self from superior dict
                    if index is None:
                        dikt[dikt_key]["__delete__"] = True
                    else:
                        dikt[dikt_key].append("__delete__")

                elif abstract_object_key_set.issubset(
                    sub_dict.keys()
                ):  # Abstract Object

                    if "base" in sub_dict:
                        # A redundancy delete
                        sub_dict["base"]["__delete__"] = True

                        ClassColle.inject(
                            sub_dict["name"],
                            (sub_dict["base"]["name"],),
                            sub_dict,
                            (file_type, belong2),
                        )

                    # Is 2nd level class
                    else:
                        ClassColle.inject(
                            sub_dict["name"],
                            ("__object__",),
                            sub_dict,
                            (file_type, belong2),
                        )

                    # Remove self from superior dict
                    if index is None:
                        dikt[dikt_key]["__delete__"] = True
                    else:
                        dikt[dikt_key].append("__delete__")

            if not next_layer:
                break
    else:
        return sample


# Component Analyser

# detect files changes
# if changed resampling
def update():
    sample_path = BASEDIR / "samples"
    sample_path = Path(sample_path)

    samples = os.listdir(sample_path)
    for sample in samples:
        if not sample.endswith(".rec") and not sample.endswith("."):
            filepath = sample_path / sample
            analyse(filepath)

    ClassCollection.rmredundancy()
    ClassCollection.store()


def update_one(fp):
    filepath = Path(fp)
    for files in glob.glob(filepath):
        analyse(files, ClassCollection)
        ClassCollection.rmredundancy()
        ClassCollection.store()
