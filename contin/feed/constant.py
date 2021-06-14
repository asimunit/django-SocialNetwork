from pathlib import Path

# Base directory
BASE_DIR = Path().absolute()

# similar post threshold
THRESHOLD_SIMILARITY = 0.5

# post classifier model path
jar_file_path = str(BASE_DIR) + '/feed/ml_models/stanford-ner.jar'

# stanford model path
ner_model_file_path = str(
    BASE_DIR) + '/feed/ml_models/english.all.3class''.distsim.crf.ser.gz'

# post classifier model path
classifier_file_path = str(BASE_DIR) + '/feed/ml_models/model.joblib'

# post classifier labels
comment_classes = ['toxic', 'severe_toxic', 'obscene',
                   'threat', 'insult',
                   'identity_hate']
