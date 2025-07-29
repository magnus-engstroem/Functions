from pydantic import BaseModel, Field
from typing import Optional
import argostranslate.package
import argostranslate.translate

class Filter:
    # Valves: Configuration options for the filter
    class Valves(BaseModel):  
        YOUR_LANGUAGE: str = Field(
            default = 'nb',
            description = "Språket du skriver på. Bruk 'nb' for norsk bokmål"
        )


    class UserValves(BaseModel):  
        YOUR_LANGUAGE: str = Field(
            default = 'nb',
            description = "Språket du skriver på. Bruk 'nb' for norsk bokmål"
        )

    def __init__(self):
        # Initialize valves (optional configuration for the Filter)
        self.valves = self.Valves()
        self.toggle = True
        self.icon = """data:image/svg+xml,%3Csvg width='800px' height='800px' viewBox='0 0 24 24' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath fill='none' d='M0 0h24v24H0z'/%3E%3Cpath d='M14 10h2v.757a4.5 4.5 0 0 1 7 3.743V20h-2v-5.5c0-1.43-1.175-2.5-2.5-2.5S16 13.07 16 14.5V20h-2V10zm-2-6v2H4v5h8v2H4v5h8v2H2V4h10z'/%3E%3C/svg%3E"""
        self.name = "Langeled 1"
        self.intermediate_language = "en"
        self.remaining_languages_to_install = 0

        argostranslate.package.update_package_index()
        available_packages = argostranslate.package.get_available_packages()


        for from_code, to_code in self.language_pairs_to_install(self.intermediate_language, self.valves.YOUR_LANGUAGE):
            self.remaining_languages_to_install += 1
            print(from_code, to_code)
            package = next((p for p in available_packages if p.from_code == from_code and p.to_code == to_code), None)
            print(package)
            if package:
                print(f"Installing {from_code} → {to_code}")
                argostranslate.package.install_from_path(package.download())
                self.remaining_languages_to_install -= 1

        if self.remaining_languages_to_install:
            raise Exception(f'Your language "{self.valves.YOUR_LANGUAGE}" was not found. Try changing the language valve.')


    def is_pair_installed(self, from_code, to_code):
        try:
            translation =  argostranslate.translate.get_translation_from_codes(from_code, to_code)
        except AttributeError:
            return False
        else:
            if translation is not None:
                return True
            else: 
                return False

    def language_pairs_to_install(self, from_code, to_code):
        pairs = []
        if not self.is_pair_installed(from_code, to_code):
            pairs.append((from_code, to_code))
        if not self.is_pair_installed(to_code, from_code):
            pairs.append((to_code, from_code))
        return pairs

    def inlet(self, body: dict) -> dict:

        input = body['messages'][-1]['content']
        int_input = argostranslate.translate.translate(input, self.valves.YOUR_LANGUAGE, self.intermediate_language)
        body['messages'][-1]['content'] = int_input

        return body  


    def outlet(self, body: dict) -> None:
        int_output = body['messages'][-1]['content']
        output = argostranslate.translate.translate(int_output, self.intermediate_language, self.valves.YOUR_LANGUAGE)
        body['messages'][-1]['content'] = output

        return body
