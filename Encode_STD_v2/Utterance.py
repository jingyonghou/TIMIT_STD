from BaseEntity import BaseEntity
class Utterance(BaseEntity):
    def __init__(self, utterance_dir, utterance_id, feature_type, phone_type="PHN39", wav_sampling_rate=16000):
        BaseEntity.__init__(self, utterance_dir, utterance_id, feature_type, phone_type="PHN39", wav_sampling_rate=16000)
