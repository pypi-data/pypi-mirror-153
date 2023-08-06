import functools
import os
import re
from pprint import pformat
import yaml


CONTRACT_IMPORT_FUNCTION = "Contract"
CONTRACT_PATH = "ASSEMBLY_CONTRACT_PATH"
YAML_NAME = "contract.yaml"
PATH_SEPARATOR = ":"


class ContractRef:
    """class used to reference contracts in tests"""

    @staticmethod
    def parse_version(v):
        match = re.fullmatch(r"(\d+-)?(\d+\.\d+\.\d+)", v)
        if not match:
            raise RuntimeError(
                "Cannot parse the contract version expected something like 1.0.1 or 2-1.0.1"
            )
        r = match.groups()
        if r[0] is None:
            return 1, r[1]
        else:
            return int(r[0].strip("-")), r[1]

    def version_to_use_on_api(self):
        return "{}-{}".format(self.language, self.version)

    def __init__(self, name, version, language):
        assert isinstance(language, int)
        self.name = name
        self.version = version
        self.language = language

    def __eq__(self, other):
        if isinstance(other, ContractRef):
            return (
                self.name == other.name
                and self.version == other.version
                and self.language == other.language
            )
        else:
            return False

    def __repr__(self):
        if self.language == 1:
            return "{}<{}>".format(self.name, self.version)
        else:
            return "{}<{}>-<{}>".format(self.name, self.language, self.version)

    def to_json(self):
        return {"name": self.name, "version": self.version, "language": self.language}

    @staticmethod
    def from_repr(repr):
        match = re.fullmatch(r"([\w_]+)<(\d+)>-<(\d+\.\d+\.\d+)>", repr)
        if not match:
            match = re.fullmatch(r"([\w_]+)<(\d+\.\d+\.\d+)>", repr)
            if not match:
                raise RuntimeError("could not build ContractRef from {}".format(repr))
            name, version = match.groups()
            return ContractRef(name, version, 1)
        name, language, version = match.groups()
        return ContractRef(name, version, int(language))

    @staticmethod
    def from_json(obj):
        if "name" not in obj or "version" not in obj:
            raise RuntimeError("could not build ContractRef from {}".format(obj))
        # this is a horrid hack which we will once pay dearly for but we do not have to change the interface of anything
        # client facing
        # if there is `language` explicitly provided in `obj` we will use it:
        if "language" in obj:
            language = int(obj["language"])
            _, version = ContractRef.parse_version(obj["version"])
        else:
            # otherwise we will try to infer it from the version field
            language, version = ContractRef.parse_version(obj["version"])
        return ContractRef(obj["name"], version, language)


def find_files_named(name, path):
    return [
        os.path.join(os.path.abspath(relpath), name)
        for relpath, _, files in os.walk(path)
        if name in files
    ]


def load_yaml(file_path):
    with open(file_path) as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def parse_metadata(metadata, yaml_path):
    contract_name = metadata["name"]
    language_version = metadata.get("language", 1)

    if language_version >= 6:
        # Lang 6 and upward, we support both .py AND .sympl file extension
        contract_files = search_sympl_or_py_file(contract_name, yaml_path)
        if not contract_files:
            raise Exception(f"No source code found for contract {contract_name}.")
        if len(contract_files) > 1:
            raise Exception(
                f"Found multiple source code files for contract {contract_name}. You must keep only one."
            )
        contract_path = contract_files[0]
    else:
        contract_path = os.path.join(
            os.path.dirname(yaml_path), "{}.py".format(contract_name)
        )

    return {
        str(
            ContractRef(contract_name, metadata["version"], language_version)
        ): contract_path
    }


def search_sympl_or_py_file(contract_name, yaml_path):
    found_contract_files = []
    for extension in ["sympl", "py"]:
        contract_path = os.path.join(
            os.path.dirname(yaml_path), "{}.{}".format(contract_name, extension)
        )
        if os.path.isfile(contract_path):
            found_contract_files.append(contract_path)
    return found_contract_files


@functools.lru_cache(maxsize=32)
def _find_contracts(path):
    path = os.path.expandvars(path)
    yaml_paths = []
    yaml_paths += find_files_named(YAML_NAME, path)

    paths_by_ref = {}
    for path in yaml_paths:
        contract_metadata = load_yaml(path)
        if contract_metadata is None:
            continue

        errors = metadata_validation_errors(contract_metadata)
        if len(errors) == 0:
            path_by_ref = parse_metadata(contract_metadata, path)
            paths_by_ref.update(path_by_ref)
        else:
            # temporary print statement until something better is figured out
            raise ValueError("{} is invalid: \n{}".format(path, pformat(errors)))

    return paths_by_ref


def find_contracts(paths):
    """
    Returns a dictionary mapping <name><lang>-<version> to the path of the contract.
    """
    if not paths:
        raise Exception(f"No contracts found. Please use --contract-path.")

    results = {}
    for path in paths:
        results.update(_find_contracts(path))

    return results


def metadata_validation_errors(metadata):
    errors = []

    if "name" not in metadata:
        errors.append("'name' field not found")

    if "version" in metadata:
        version_number_pattern = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}")
        if not version_number_pattern.match(metadata["version"]):
            errors.append("version must be 3 numbers separated by dots (ex: 1.0.0)")
    else:
        errors.append("'version' field not found")

    if "language" in metadata:
        if not isinstance(metadata["language"], int):
            errors.append("'language' must be an integer value")

    return errors


def contract_ref_from_path(contract_file_path):
    contract_dir = os.path.abspath(os.path.dirname(contract_file_path))
    yaml_file_path = contract_dir + "/contract.yaml"

    if not os.path.isfile(yaml_file_path):
        raise Exception(
            "{} does not have a coresponding contract.yaml file".format(
                contract_file_path
            )
        )

    metadata = load_yaml(yaml_file_path)
    errors = metadata_validation_errors(metadata)
    if len(errors) > 0:
        raise Exception(
            "{} contains malformed metadata {}\n errors: {}".format(
                yaml_file_path, metadata, pformat(errors)
            )
        )

    return ContractRef(
        metadata["name"], metadata["version"], int(metadata.get("language", 1))
    )


def local_path_from_ref(contract_path, contract_ref):
    identifier = str(contract_ref)
    paths_by_ref = find_contracts(contract_path)

    if not paths_by_ref or identifier not in paths_by_ref:
        raise Exception(
            "Contract {} could not be located. "
            "Please use --contract-path.".format(identifier)
        )

    return paths_by_ref[identifier]


def local_code_from_ref(contract_path, contract_ref):
    path = local_path_from_ref(contract_path, contract_ref)

    with open(path, "r") as contract_file:
        code = contract_file.read()

    return code
