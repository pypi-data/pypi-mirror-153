import os
import pickle
from re import match
import xgboost as xgb

from molgenis.capice import __version__
from molgenis.capice.main_predict import CapicePredict
from molgenis.capice.core.capice_manager import CapiceManager
from molgenis.capice.cli.args_handler_parent import ArgsHandlerParent
from molgenis.capice.utilities.enums import Versioning


class ArgsHandlerPredict(ArgsHandlerParent):
    """
    Child class ArgsHandlerPredict, specific to the predict part of CAPICE
    """

    def __init__(self, parser):
        super(ArgsHandlerPredict, self).__init__(parser=parser)

    @property
    def _extension(self):
        return '.tsv', '.tsv.gz'

    @property
    def _required_output_extensions(self):
        return '.tsv', '.tsv.gz'

    @property
    def _empty_output_extension(self):
        return self._required_output_extensions[1]

    def create(self):
        self.parser.add_argument(
            '-i',
            '--input',
            action='append',
            type=str,
            required=True,
            help='path to annotated variants file (.tsv or .tsv.gz)'
        )
        self.parser.add_argument(
            '-m',
            '--model',
            action='append',
            type=str,
            required=True,
            help='path to trained model (.dat)'
        )
        self.parser.add_argument(
            '-o',
            '--output',
            action='append',
            type=str,
            help='path to variant predictions file (.tsv or .tsv.gz)'
        )
        self.parser.add_argument(
            '-f',
            '--force',
            action='store_true',
            help='overwrites output if it already exists'
        )

    def _handle_module_specific_args(self, input_path, output_path, output_filename, args):
        model_path = self.validate_length_one(args.model, '-m/--model')
        model = self.validate_model(model_path)
        CapiceManager().output_filename = output_filename
        CapicePredict(input_path, model, output_path).run()

    def validate_model(self, model_path):
        """
        Function to validate if the given model location is indeed a pickled
        model and matches the current CAPICE version.
        :param model_path: str, path-like, path to the model
        :return: model, xgb.XGBClassifier class
        """
        self._validate_model_path(model_path)
        with open(model_path, 'rb') as model_file:
            model = pickle.load(model_file)
        self._validate_model_class(model)
        self._validate_model_attributes(model)
        self._validate_model_version(model)
        return model

    def _validate_model_path(self, model_path):
        if not os.path.exists(model_path):
            self.parser.error("Input model does not exist!")
        if not model_path.endswith('.pickle.dat'):
            self.parser.error("Model does not have the right extension!")

    def _validate_model_class(self, model):
        if not model.__class__ == xgb.XGBClassifier:
            self.parser.error("Given pickle is not a XGBClassifier class!")

    def _validate_model_attributes(self, model):
        required_attributes = ['CAPICE_version', 'impute_values', 'predict_proba']
        for attribute in required_attributes:
            if attribute not in dir(model):
                self.parser.error(f'Unable to locate attribute {attribute} in model file!')

    def _validate_model_version(self, model):
        model_version = match(Versioning.VALIDATION_REGEX.value, model.CAPICE_version)
        if model_version is None:
            self.parser.error(f'Model version does not adhere to correct format: '
                              f'{model.CAPICE_version}!')

        capice_version = match(Versioning.VALIDATION_REGEX.value, __version__)
        if model_version.group('major') != capice_version.group('major'):
            self.parser.error(f'Model major version {model.CAPICE_version} does not match '
                              f'with CAPICE: {__version__}!')

        if model_version.group('prerelease') or capice_version.group('prerelease'):
            if model_version.group('minor') != capice_version.group('minor'):
                self.parser.error(f'Model minor version {model.CAPICE_version} does not match with '
                                  f'CAPICE: {__version__} (should match for pre-releases)!')
            elif model_version.group('patch') != capice_version.group('patch'):
                self.parser.error(f'Model patch version {model.CAPICE_version} does not match with '
                                  f'CAPICE: {__version__} (should match for pre-releases)!')
            elif model_version.group('prerelease') != capice_version.group('prerelease'):
                self.parser.error(f'Model pre-release version {model.CAPICE_version} does not '
                                  f'match with CAPICE: {__version__}!')
