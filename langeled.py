#Name: Oversett
#Description Oversetter prompt fra norsk til engelse før det sendes til modellen. Er tregere, men kan noen ganger forbedre kvalitet på svaret sammenliknet med å snakke direkte modellen på norsk.

from pydantic import BaseModel, Field
from typing import Optional
import logging
import time
import importlib
import subprocess
import sys

#In order to use a package that is not already installed
def ensure_package(package):
    try:
        importlib.import_module(package)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
ensure_package("argostranslate")


import argostranslate.package
import argostranslate.translate



class Filter:
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
        self.toggle = True #Creates a toggle button

        #The visible icon SVG image encoded as Data URI (string)
        self.icon = "data:image/svg+xml,%3Csvg width='800px' height='800px' viewBox='0 0 48 48' xmlns='http://www.w3.org/2000/svg'%3E%3Cdefs%3E%3Cstyle%3E.a%7Bfill:none;stroke:%23000000;stroke-linecap:round;stroke-linejoin:round;%7D%3C/style%3E%3C/defs%3E%3Ccircle class='a' cx='24' cy='24' r='21.5'/%3E%3Cline class='a' x1='30.6916' y1='44.4321' x2='17.3084' y2='3.5679'/%3E%3Cpolyline class='a' points='22.429 36.637 16.773 19.235 10.9 36.637'/%3E%3Cline class='a' x1='12.8577' y1='30.7637' x2='20.471' y2='30.7637'/%3E%3Cpath class='a' d='M27.2363,11.1588c-.0324,4.5431-.26,11.6173,5.16,17.3286'/%3E%3Cpath class='a' d='M22.9238,13.9955a38.5878,38.5878,0,0,0,15.4107-1.7334'/%3E%3Cpath class='a' d='M23.7854,23.3448c2.5858-4.3938,13.61-7.906,14.5491-.7309a5.5319,5.5319,0,0,1-2.1877,5.17'/%3E%3Cpath class='a' d='M35.4464,16.0588c.1685,5.1934-6.1155,13.58-10.1157,12.0113'/%3E%3C/svg%3E"
        
        self.name = "Langeled 1"
        self.intermediate_language = "en"  #Default: talk to model via English
        self.remaining_languages_to_install = 0

        self.logger = logging.getLogger(self.name) #Can be viewed with "docker logs open-webui"


        self.logger.info('initializing argostranslate')
        
        argostranslate.package.update_package_index()
        self.available_packages = argostranslate.package.get_available_packages()

    def init_language(self):

        argostranslate.package.update_package_index()
        self.available_packages = argostranslate.package.get_available_packages()

        self.logger.info('Finding requierede language packages to install')

        for from_code, to_code in self.language_pairs_to_install(self.intermediate_language, self.valves.YOUR_LANGUAGE):
            self.remaining_languages_to_install += 1
            self.logger.info(f"Attempting to install ")
            print(from_code, to_code)
            package = next((p for p in self.available_packages if p.from_code == from_code and p.to_code == to_code), None)
            print(package)
            if package:
                print(f"Installing {from_code} → {to_code}")
                argostranslate.package.install_from_path(package.download())
                self.remaining_languages_to_install -= 1


        
        if self.remaining_languages_to_install:
            self.logger.error("A language package was not installed")
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

        self.init_language()

        input = body['messages'][-1]['content']
        
        
        self.logger.info('Translating input into intermediate language "' + self.intermediate_language + '".')
        start_translate = time.time()

        int_input = argostranslate.translate.translate(input, self.valves.YOUR_LANGUAGE, self.intermediate_language)
        body['messages'][-1]['content'] = int_input


        self.logger.info(f'Finished translating input into intermediate language in {time.time() - start_translate} s')
        self.logger.debug('The translated message is: ')
        self.logger.debug(int_input)

        return body  


    def outlet(self, body: dict) -> dict:

        self.logger.info('Translating from intermediate language "' + self.intermediate_language + '" to "' + self.valves.YOUR_LANGUAGE + '".')
        start_translate = time.time()

        int_output = body['messages'][-1]['content']
        output = argostranslate.translate.translate(int_output, self.intermediate_language, self.valves.YOUR_LANGUAGE)
        body['messages'][-1]['content'] = output

        self.logger.info(f'Finished translating output to spoken language in {time.time() - start_translate} s')

        return body
