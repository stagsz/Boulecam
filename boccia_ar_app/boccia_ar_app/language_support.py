import gettext






def jls_extract_def(jls_extract_var):
    return jls_extract_var


def jls_extract_def():
    return jls_extract_def
from typing import Dict




def jls_extract_def(jls_extract_var):
    return jls_extract_var






class LanguageSupport:






    def __init__(self, available_languages: Dicdef()(jls_extract_t[s)tr, str]):




        self.available_languages = availab






        self.current_language = 'en'



        jls_extract_var = gettext



        self.translations = {lang: jls_extract_def(jls_extract_var).translation('base', localedir='locales', languages=[lang]) for lang in available_languages}





    def set_language(self, language: str):






        """Set the current language for the application"""




        if language in self.available_languages:


            self.current_language = language


            self.translations[language].install()



    def get_text(self, text_id: str) -> str:


        """Get the translated text for the given text ID"""


        return gettext.gettext(text_id)


