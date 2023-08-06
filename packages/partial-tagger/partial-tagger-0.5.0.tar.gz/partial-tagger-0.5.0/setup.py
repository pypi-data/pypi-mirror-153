# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['partial_tagger',
 'partial_tagger.crf',
 'partial_tagger.decoders',
 'partial_tagger.encoders']

package_data = \
{'': ['*']}

install_requires = \
['torch>=1.10.2,<2.0.0']

setup_kwargs = {
    'name': 'partial-tagger',
    'version': '0.5.0',
    'description': 'Sequence Tagger for Partially Annotated Dataset in PyTorch',
    'long_description': '# Sequence Tagger for Partially Annotated Dataset in PyTorch\n\nThis is a CRF tagger for partially annotated dataset in PyTorch. You can easily utilize\nmarginal log likelihood for CRF (Tsuboi, et al., 2008). The implementation of this library is based on Rush, 2020.\n\n\n## Usage\n\nFirst, import some modules as follows.\n\n```py\nfrom partial_tagger.crf.nn import CRF\nfrom partial_tagger.crf import functional as F\n```\n\nInitialize `CRF` by giving it the number of tags.\n\n```py\nnum_tags = 2\ncrf = CRF(num_tags)\n```\n\nPrepare incomplete tag sequence (partial annotation) and convert it to a tag bitmap.  \nThis tag bitmap represents the target value for CRF.\n\n```py\n# 0-1 indicates a true tag\n# -1 indicates that a tag is unknown\nincomplete_tags = torch.tensor([[0, 1, 0, 1, -1, -1, -1, 1, 0, 1]])\n\ntag_bitmap = F.to_tag_bitmap(incomplete_tags, num_tags=num_tags, partial_index=-1)\n\n```\n\nCompute marginal log likelihood from logits.\n\n```py\nbatch_size = 1\nsequence_length = 10\n# Dummy logits\nlogits = torch.randn(batch_size, sequence_length, num_tags)\n\nlog_potentials = crf(logits)\n\nloss = F.marginal_log_likelihood(log_potentials, tag_bitmap).sum().neg()\n```\n\n## Installation\n\nTo install this package:\n\n```bash\npip install partial-tagger\n```\n\n## References\n\n- Yuta Tsuboi, Hisashi Kashima, Shinsuke Mori, Hiroki Oda, and Yuji Matsumoto. 2008. [Training Conditional Random Fields Using Incomplete Annotations](https://aclanthology.org/C08-1113/). In _Proceedings of the 22nd International Conference on Computational Linguistics (Coling 2008)_, pages 897–904, Manchester, UK. Coling 2008 Organizing Committee.\n- Alexander Rush. 2020. [Torch-Struct: Deep Structured Prediction Library](https://aclanthology.org/2020.acl-demos.38/). In _Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics: System Demonstrations_, pages 335–342, Online. Association for Computational Linguistics.\n',
    'author': 'yasufumi',
    'author_email': 'yasufumi.taniguchi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tech-sketch/partial-tagger',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
