from BaseEntity import BaseEntity
class Keyword(BaseEntity):
    def __init__(self, keyword_dir, keyword_id, feature_type, phone_type="PHN39", wav_sampling_rate=16000):
        BaseEntity.__init__(self, keyword_dir, keyword_id, feature_type, phone_type="PHN39", wav_sampling_rate=16000)


