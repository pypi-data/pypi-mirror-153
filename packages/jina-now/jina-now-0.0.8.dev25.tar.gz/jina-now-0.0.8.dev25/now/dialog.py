"""
This module implements a command-line dialog with the user.
Its goal is to configure a UserInput object with users specifications.
Optionally, values can be passed from the command-line when jina-now is launched. In that case,
the dialog won't ask for the value.
"""
from __future__ import annotations, print_function, unicode_literals

import os
import pathlib
from dataclasses import dataclass
from os.path import expanduser as user
from typing import Dict, List, Optional, Union

import cowsay
from kubernetes import client, config
from pyfiglet import Figlet

from now.constants import (
    AVAILABLE_DATASET,
    IMAGE_MODEL_QUALITY_MAP,
    DatasetTypes,
    DemoDatasets,
    Modalities,
    Qualities,
)
from now.deployment.deployment import cmd
from now.log.log import yaspin_extended
from now.thirdparty.PyInquirer import Separator
from now.thirdparty.PyInquirer.prompt import prompt
from now.utils import ffmpeg_is_installed, sigmap

cur_dir = pathlib.Path(__file__).parent.resolve()
NEW_CLUSTER = {'name': '🐣 create new', 'value': 'new'}
AVAILABLE_SOON = 'will be available in upcoming versions'


@dataclass
class UserInput:
    output_modality: Optional[Modalities] = None

    # data related
    data: Optional[str] = None
    is_custom_dataset: Optional[bool] = None

    custom_dataset_type: Optional[DatasetTypes] = None
    dataset_secret: Optional[str] = None
    dataset_url: Optional[str] = None
    dataset_path: Optional[str] = None

    # model related
    quality: Optional[Qualities] = None
    model_variant: Optional[str] = None

    # cluster related
    cluster: Optional[str] = None
    create_new_cluster: Optional[bool] = False
    deployment_type: Optional[str] = None


def configure_user_input(**kwargs) -> UserInput:
    print_headline()

    user_input = UserInput()
    _configure_output_modality(user_input, **kwargs)
    _configure_dataset(user_input, **kwargs)
    _configure_quality(user_input, **kwargs)
    _configure_cluster(user_input, **kwargs)

    return user_input


def print_headline():
    f = Figlet(font='slant')
    print('Welcome to:')
    print(f.renderText('Jina NOW'))
    print('Get your search case up and running - end to end.\n')
    print(
        'You can choose between image and text search. \nJina now trains a model, pushes it to the jina hub'
        ', deploys a flow and a playground app in the cloud or locally. \nCheckout one of the demo cases or bring '
        'your own data.\n'
    )
    print(
        'If you want learn more about our framework please visit: https://docs.jina.ai/'
    )
    print(
        '💡 Make sure you give enough memory to your Docker daemon. '
        '5GB - 8GB should be okay.'
    )
    print()


def _configure_output_modality(user_input: UserInput, **kwargs) -> None:
    """Asks user questions to set output_modality in user_input"""
    user_input.output_modality = _prompt_value(
        name='output_modality',
        choices=[
            {'name': '🏞 Image Search', 'value': Modalities.IMAGE},
            {'name': '📝 Text Search (experimental)', 'value': Modalities.TEXT},
            {
                'name': '🥁 Music Search',
                'value': Modalities.MUSIC,
                'disabled': AVAILABLE_SOON,
            },
        ],
        prompt_message='Which modalities you want to work with?',
        prompt_type='list',
        **kwargs,
    )


def _configure_dataset(user_input: UserInput, **kwargs) -> None:
    """Asks user to set dataset attribute of user_input"""
    if user_input.output_modality == Modalities.IMAGE:
        _configure_dataset_image(user_input, **kwargs)
    elif user_input.output_modality == Modalities.TEXT:
        _configure_dataset_text(user_input, **kwargs)
    elif user_input.output_modality == Modalities.MUSIC:
        if not ffmpeg_is_installed():
            _handle_ffmpeg_install_required()
        _configure_dataset_music(user_input, **kwargs)

    if user_input.data in AVAILABLE_DATASET[user_input.output_modality]:
        user_input.is_custom_dataset = False
    else:
        user_input.is_custom_dataset = True
        if user_input.data == 'custom':
            _configure_custom_dataset(user_input, **kwargs)
        else:
            _parse_custom_data_from_cli(user_input)


def _configure_dataset_image(user_input: UserInput, **kwargs) -> None:
    user_input.data = _prompt_value(
        name='data',
        prompt_message='What dataset do you want to use?',
        choices=[
            {'name': '🖼  artworks (≈8K docs)', 'value': DemoDatasets.BEST_ARTWORKS},
            {
                'name': '💰 nft - bored apes (10K docs)',
                'value': DemoDatasets.NFT_MONKEY,
            },
            {'name': '👬 totally looks like (≈12K docs)', 'value': DemoDatasets.TLL},
            {'name': '🦆 birds (≈12K docs)', 'value': DemoDatasets.BIRD_SPECIES},
            {'name': '🚗 cars (≈16K docs)', 'value': DemoDatasets.STANFORD_CARS},
            {
                'name': '🏞 geolocation (≈50K docs)',
                'value': DemoDatasets.GEOLOCATION_GEOGUESSR,
            },
            {'name': '👕 fashion (≈53K docs)', 'value': DemoDatasets.DEEP_FASHION},
            {
                'name': '☢️ chest x-ray (≈100K docs)',
                'value': DemoDatasets.NIH_CHEST_XRAYS,
            },
            Separator(),
            {
                'name': '✨ custom',
                'value': 'custom',
            },
        ],
        **kwargs,
    )


def _configure_dataset_text(user_input: UserInput, **kwargs):
    user_input.data = _prompt_value(
        name='data',
        prompt_message='What dataset do you want to use?',
        choices=[
            {'name': '🎤 rock lyrics (200K docs)', 'value': 'rock-lyrics'},
            {'name': '🎤 pop lyrics (200K docs)', 'value': 'pop-lyrics'},
            {'name': '🎤 rap lyrics (200K docs)', 'value': 'rap-lyrics'},
            {'name': '🎤 indie lyrics (200K docs)', 'value': 'indie-lyrics'},
            {'name': '🎤 metal lyrics (200K docs)', 'value': 'metal-lyrics'},
            Separator(),
            {
                'name': '✨ custom .txt files',
                'value': 'custom',
            },
        ],
        **kwargs,
    )


def _configure_dataset_music(user_input: UserInput, **kwargs):
    user_input.data = _prompt_value(
        name='data',
        prompt_message='What dataset do you want to use?',
        choices=[
            {
                'name': '🎸 music mid (≈2K docs)',
                'value': DemoDatasets.MUSIC_GENRES_MID,
            },
            {
                'name': '🎸 music large (≈10K docs)',
                'value': DemoDatasets.MUSIC_GENRES_LARGE,
            },
            Separator(),
            {
                'name': '✨ custom',
                'value': 'custom',
            },
        ],
        **kwargs,
    )


def _configure_custom_dataset(user_input: UserInput, **kwargs) -> None:
    """Asks user questions to setup custom dataset in user_input."""
    user_input.custom_dataset_type = _prompt_value(
        name='custom_dataset_type',
        prompt_message='How do you want to provide input? (format: https://docarray.jina.ai/)',
        choices=[
            {
                'name': 'docarray.pull id (recommended)',
                'value': DatasetTypes.DOCARRAY,
            },
            {
                'name': 'docarray URL',
                'value': DatasetTypes.URL,
            },
            {
                'name': 'local path',
                'value': DatasetTypes.PATH,
            },
        ],
        **kwargs,
    )
    if user_input.custom_dataset_type == DatasetTypes.DOCARRAY:
        user_input.dataset_secret = _prompt_value(
            name='dataset_secret',
            prompt_message='Please enter your docarray secret.',
            prompt_type='password',
        )

    elif user_input.custom_dataset_type == DatasetTypes.URL:
        user_input.dataset_url = _prompt_value(
            name='dataset_url',
            prompt_message='Please paste in your url for the docarray.',
            prompt_type='input',
        )

    elif user_input.custom_dataset_type == DatasetTypes.PATH:
        user_input.dataset_path = _prompt_value(
            name='dataset_path',
            prompt_message='Please enter the path to the local folder.',
            prompt_type='input',
        )


def _configure_cluster(user_input: UserInput, skip=False, **kwargs):
    """Asks user question to determine cluster for user_input object"""

    def ask_deployment():
        user_input.deployment_type = _prompt_value(
            name='deployment_type',
            choices=[
                {
                    'name': '⛅️ Jina Cloud',
                    'value': 'remote',
                },
                {
                    'name': '📍 Local',
                    'value': 'local',
                },
            ],
            prompt_message='Where do you want to deploy your search engine?',
            prompt_type='list',
            **kwargs,
        )

    if not skip:
        ask_deployment()

    if user_input.deployment_type == 'remote':
        _maybe_login_wolf()
        os.environ['JCLOUD_NO_SURVEY'] = '1'
    else:
        # get all local cluster contexts
        choices = _construct_local_cluster_choices(
            active_context=kwargs.get('active_context'), contexts=kwargs.get('contexts')
        )
        # prompt the local cluster context choices to the user
        user_input.cluster = _prompt_value(
            name='cluster',
            choices=choices,
            prompt_message='Which cluster you want to use to deploy your search engine?',
            prompt_type='list',
            **kwargs,
        )
        if user_input.cluster != NEW_CLUSTER['value']:
            if not _cluster_running(user_input.cluster):
                print(
                    f'Cluster {user_input.cluster} is not running. Please select a different one.'
                )
                _configure_cluster(user_input, skip=True, **kwargs)
        else:
            user_input.create_new_cluster = True


def _configure_quality(user_input: UserInput, **kwargs) -> None:
    """Asks users questions to set quality attribute of user_input"""
    if user_input.output_modality == Modalities.MUSIC:
        return
    user_input.quality = _prompt_value(
        name='quality',
        choices=[
            {'name': '🦊 medium (≈3GB mem, 15q/s)', 'value': Qualities.MEDIUM},
            {'name': '🐻 good (≈3GB mem, 2.5q/s)', 'value': Qualities.GOOD},
            {
                'name': '🦄 excellent (≈4GB mem, 0.5q/s)',
                'value': Qualities.EXCELLENT,
            },
        ],
        prompt_message='What quality do you expect?',
        prompt_type='list',
        **kwargs,
    )
    if user_input.quality == Qualities.MEDIUM:
        print('  🚀 you trade-off a bit of quality for having the best speed')
    elif user_input.quality == Qualities.GOOD:
        print('  ⚖️ you have the best out of speed and quality')
    elif user_input.quality == Qualities.EXCELLENT:
        print('  ✨ you trade-off speed to having the best quality')

    _, user_input.model_variant = IMAGE_MODEL_QUALITY_MAP[user_input.quality]


def _construct_local_cluster_choices(active_context, contexts):
    context_names = _get_context_names(contexts, active_context)
    choices = [NEW_CLUSTER]
    # filter contexts with `gke`
    if len(context_names) > 0 and len(context_names[0]) > 0:
        context_names = [context for context in context_names if 'gke' not in context]
        choices = context_names + choices
    return choices


def maybe_prompt_user(questions, attribute, **kwargs):
    """
    Checks the `kwargs` for the `attribute` name. If present, the value is returned directly.
    If not, the user is prompted via the cmd-line using the `questions` argument.

    :param questions: A dictionary that is passed to `PyInquirer.prompt`
        See docs: https://github.com/CITGuru/PyInquirer#documentation
    :param attribute: Name of the value to get. Make sure this matches the name in `kwargs`

    :return: A single value of either from `kwargs` or the user cli input.
    """
    if kwargs and kwargs.get(attribute) is not None:
        return kwargs[attribute]
    else:
        answer = prompt(questions)
        if attribute in answer:
            return answer[attribute]
        else:
            print("\n" * 10)
            cowsay.cow('see you soon 👋')
            exit(0)


def _prompt_value(
    name: str,
    prompt_message: str,
    prompt_type: str = 'input',
    choices: Optional[List[Union[Dict, str]]] = None,
    **kwargs: Dict,
):
    qs = {'name': name, 'type': prompt_type, 'message': prompt_message}

    if choices is not None:
        qs['choices'] = choices
        qs['type'] = 'list'
    return maybe_prompt_user(qs, name, **kwargs)


def _get_context_names(contexts, active_context=None):
    names = [c for c in contexts] if contexts is not None else []
    if active_context is not None:
        names.remove(active_context)
        names = [active_context] + names
    return names


def _cluster_running(cluster):
    config.load_kube_config(context=cluster)
    v1 = client.CoreV1Api()
    try:
        v1.list_namespace()
    except Exception as e:
        return False
    return True


def _maybe_login_wolf():
    if not os.path.exists(user('~/.jina/config.json')):
        with yaspin_extended(
            sigmap=sigmap, text='Log in to JCloud', color='green'
        ) as spinner:
            cmd('jcloud login')
        spinner.ok('🛠️')


def _parse_custom_data_from_cli(user_input: UserInput):
    data = user_input.data
    try:
        data = os.path.expanduser(data)
    except Exception:
        pass
    if os.path.exists(data):
        user_input.custom_dataset_type = DatasetTypes.PATH
        user_input.dataset_path = data
    elif 'http' in data:
        user_input.custom_dataset_type = DatasetTypes.URL
        user_input.dataset_url = data
    else:
        user_input.custom_dataset_type = DatasetTypes.DOCARRAY
        user_input.dataset_secret = data


def _handle_ffmpeg_install_required():
    bc_red = '\033[91m'
    bc_end = '\033[0m'
    print()
    print(
        f"{bc_red}To use the audio modality you need the ffmpeg audio processing"
        f" library installed on your system.{bc_end}"
    )
    print(
        f"{bc_red}For MacOS please run 'brew install ffmpeg' and on"
        f" Linux 'apt-get install ffmpeg libavcodec-extra'.{bc_end}"
    )
    print(
        f"{bc_red}After the installation, restart Jina Now and have fun with music search 🎸!{bc_end}"
    )
    cowsay.cow('see you soon 👋')
    exit(1)
