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
        for f in listdir(citing_path):
            self.citing[f] = Document(join(citing_path, f))

        self.reference = Document(join(reference_path, listdir(reference_path)[0]))
        self.annotation = Annotation(join(annotations_path, listdir(annotations_path)[0]))
