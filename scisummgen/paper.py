from os import listdir
from os.path import join

from .annotation import Annotation
from .document import Document


class Paper:

    def __init__(self, path):
        citing_path = join(path, 'Citance_XML')
        reference_path = join(path, 'Reference_XML')
        annotations_path = join(path, 'annotation')

        self.citing = {}
        for file in listdir(citing_path):
            self.citing[file.split('.')[0]] = Document(join(citing_path, file))

        self.reference = Document(join(reference_path, listdir(reference_path)[0]))
        self.annotation = Annotation(join(annotations_path, listdir(annotations_path)[0]))

    def get_citance_text(self, citance):
        text = ''

        try:
            for sentence_id in citance['CO']:
                text += self.citing[citance['CP']].sentence[sentence_id]
        except KeyError as e:
            print(citance)
            raise e

        return text
