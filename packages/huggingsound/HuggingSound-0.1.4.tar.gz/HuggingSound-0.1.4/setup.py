# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['huggingsound',
 'huggingsound.speech_classification',
 'huggingsound.speech_recognition']

package_data = \
{'': ['*']}

install_requires = \
['datasets>=1.18.3,<2.0.0',
 'jiwer>=2.3.0,<3.0.0',
 'librosa>=0.8.1,<0.9.0',
 'llvmlite>=0.36.0,<0.37.0',
 'numba>=0.53.1,<0.54.0',
 'torch>=1.9.0,<2.0.0',
 'transformers>=4.16.2,<5.0.0']

setup_kwargs = {
    'name': 'huggingsound',
    'version': '0.1.4',
    'description': "HuggingSound: A toolkit for speech-related tasks based on HuggingFace's tools.",
    'long_description': '# HuggingSound\n\nHuggingSound: A toolkit for speech-related tasks based on [HuggingFace\'s](https://huggingface.co/) tools.\n\nI have no intention of building a very complex tool here. \nI just wanna have an easy-to-use toolkit for my speech-related experiments.\nI hope this library could be helpful for someone else too :)\n\n# Requirements\n\n- Python 3.7+\n\n# Installation\n\n```console\n$ pip install huggingsound\n```\n\n# How to use it?\n\nI\'ll try to summarize the usage of this toolkit. \nBut many things will be missing from the documentation below. I promise to make it better soon.\nFor now, you can open an issue if you have some questions or look at the source code to see how it works.\nYou can check more usage examples in the repository `examples` folder.\n\n## Speech recognition\n\nFor speech recognition you can use any CTC model hosted on the Hugging Face Hub. You can find some available models [here](https://huggingface.co/models?pipeline_tag=automatic-speech-recognition).\n\n### Inference\n\n```python\nfrom huggingsound import SpeechRecognitionModel\n\nmodel = SpeechRecognitionModel("jonatasgrosman/wav2vec2-large-xlsr-53-english")\naudio_paths = ["/path/to/sagan.mp3", "/path/to/asimov.wav"]\n\ntranscriptions = model.transcribe(audio_paths)\n\nprint(transcriptions)\n\n# transcriptions format (a list of dicts, one for each audio file):\n# [\n#  {\n#   "transcription": "extraordinary claims require extraordinary evidence", \n#   "start_timestamps": [100, 120, 140, 180, ...],\n#   "end_timestamps": [120, 140, 180, 200, ...],\n#   "probabilities": [0.95, 0.88, 0.9, 0.97, ...]\n# },\n# ...]\n#\n# as you can see, not only the transcription is returned but also the timestamps (in milliseconds) \n# and probabilities of each character of the transcription.\n\n```\n\n### Inference (boosted by a language model)\n\n```python\nfrom huggingsound import SpeechRecognitionModel, KenshoLMDecoder\n\nmodel = SpeechRecognitionModel("jonatasgrosman/wav2vec2-large-xlsr-53-english")\naudio_paths = ["/path/to/sagan.mp3", "/path/to/asimov.wav"]\n\n# The LM format used by the LM decoders is the KenLM format (arpa or binary file).\n# You can download some LM files examples from here: https://huggingface.co/jonatasgrosman/wav2vec2-large-xlsr-53-english/tree/main/language_model\nlm_path = "path/to/your/lm_files/lm.binary"\nunigrams_path = "path/to/your/lm_files/unigrams.txt"\n\n# We implemented three different decoders for LM boosted decoding: KenshoLMDecoder, ParlanceLMDecoder, and FlashlightLMDecoder\n# On this example, we\'ll use the KenshoLMDecoder\n# To use this decoder you\'ll need to install the Kensho\'s ctcdecode first (https://github.com/kensho-technologies/pyctcdecode)\ndecoder = KenshoLMDecoder(model.token_set, lm_path=lm_path, unigrams_path=unigrams_path)\n\ntranscriptions = model.transcribe(audio_paths, decoder=decoder)\n\nprint(transcriptions)\n\n```\n\n### Evaluation\n```python\nfrom huggingsound import SpeechRecognitionModel\n\nmodel = SpeechRecognitionModel("jonatasgrosman/wav2vec2-large-xlsr-53-english")\n\nreferences = [\n    {"path": "/path/to/sagan.mp3", "transcription": "extraordinary claims require extraordinary evidence"},\n    {"path": "/path/to/asimov.wav", "transcription": "violence is the last refuge of the incompetent"},\n]\n\nevaluation = model.evaluate(references)\n\nprint(evaluation)\n\n# evaluation format: {"wer": 0.08, "cer": 0.02}\n```\n\n### Fine-tuning\n```python\nfrom huggingsound import TrainingArguments, ModelArguments, SpeechRecognitionModel, TokenSet\n\nmodel = SpeechRecognitionModel("facebook/wav2vec2-large-xlsr-53")\noutput_dir = "my/finetuned/model/output/dir"\n\n# first of all, you need to define your model\'s token set\n# however, the token set is only needed for non-finetuned models\n# if you pass a new token set for an already finetuned model, it\'ll be ignored during training\ntokens = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "\'"]\ntoken_set = TokenSet(tokens)\n\n# define your train/eval data\ntrain_data = [\n    {"path": "/path/to/sagan.mp3", "transcription": "extraordinary claims require extraordinary evidence"},\n    {"path": "/path/to/asimov.wav", "transcription": "violence is the last refuge of the incompetent"},\n]\neval_data = [\n    {"path": "/path/to/sagan2.mp3", "transcription": "absence of evidence is not evidence of absence"},\n    {"path": "/path/to/asimov2.wav", "transcription": "the true delight is in the finding out rather than in the knowing"},\n]\n\n# and finally, fine-tune your model\nmodel.finetune(\n    output_dir, \n    train_data=train_data, \n    eval_data=eval_data, # the eval_data is optional\n    token_set=token_set,\n)\n\n```\n\n# Troubleshooting\n\n- If you are having trouble when loading MP3 files: `$ sudo apt-get install ffmpeg`\n\n# Want to help?\n\nSee the [contribution guidelines](https://github.com/jonatasgrosman/huggingsound/blob/master/CONTRIBUTING.md)\nif you\'d like to contribute to HuggingSound project.\n\nYou don\'t even need to know how to code to contribute to the project. Even the improvement of our documentation is an outstanding contribution.\n\nIf this project has been useful for you, please share it with your friends. This project could be helpful for them too.\n\nIf you like this project and want to motivate the maintainers, give us a :star:. This kind of recognition will make us very happy with the work that we\'ve done with :heart:\n\nYou can also [!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/yellow_img.png)](https://www.buymeacoffee.com/jonatasgrosman)\n\n# Citation\nIf you want to cite the tool you can use this:\n\n```bibtex\n@misc{grosman2022huggingsound,\n  title={HuggingSound},\n  author={Grosman, Jonatas},\n  publisher={GitHub},\n  journal={GitHub repository},\n  howpublished={\\url{https://github.com/jonatasgrosman/huggingsound}},\n  year={2022}\n}\n```',
    'author': 'Jonatas Grosman',
    'author_email': 'jonatasgrosman@gmail.com',
    'maintainer': 'Jonatas Grosman',
    'maintainer_email': 'jonatasgrosman@gmail.com',
    'url': 'https://github.com/jonatasgrosman/huggingsound',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
