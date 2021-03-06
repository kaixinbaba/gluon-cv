from gluoncv.auto.tasks import ImageClassification
from gluoncv.auto.tasks import ObjectDetection

IMAGE_CLASS_DATASET, _, _ = ImageClassification.Dataset.from_folders('https://autogluon.s3.amazonaws.com/datasets/shopee-iet.zip')
OBJECT_DETCTION_DATASET = ObjectDetection.Dataset.from_voc('https://autogluon.s3.amazonaws.com/datasets/tiny_motorbike.zip')

def test_image_classification():
    from gluoncv.auto.tasks import ImageClassification
    task = ImageClassification({'num_trials': 1})
    classifier = task.fit(IMAGE_CLASS_DATASET)
    assert task.fit_summary.get('valid_acc', 0) > 0

def test_center_net_estimator():
    from gluoncv.auto.tasks import ObjectDetection
    task = ObjectDetection({'num_trials': 1})
    detector = task.fit(OBJECT_DETCTION_DATASET)
    assert task.fit_summary.get('valid_map', 0) > 0
