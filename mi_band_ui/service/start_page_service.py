from mi_band_ui.repository.rate_repository import RateRepository
from mi_band_ui.repository.util.data_util import clean_up_list


class StartPageService:
    def __init__(self, engine):
        self.engine = engine
        self.userRepository = RateRepository(self.engine)

    def get_existing_judges(self):
        result = self.userRepository.get_judges_unique()
        return clean_up_list(result)
