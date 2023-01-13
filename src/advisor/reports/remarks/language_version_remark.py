from ..report_item import ReportItem
from .version_remark import VersionRemark


class LanguageVersionRemark(VersionRemark):
    def __init__(self,
                language_name,
                min_version,
                description=None,
                details=None,
                recommended_version=None,
                installed_version=None,
                details_url=None,
                override_text=None,
                item_type=ReportItem.NEUTRAL):
        
        description = f'detected {language_name} code.'

        super().__init__(None,
                        None,
                        name=language_name,
                        description=description,
                        details=details,
                        min_version=min_version,
                        recommended_version=recommended_version,
                        installed_version=installed_version,
                        details_url=details_url,
                        override_text=override_text,
                        item_type=item_type)