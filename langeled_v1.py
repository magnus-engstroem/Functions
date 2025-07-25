from pydantic import BaseModel, Field
#import argostranslate
from fastapi import Request
from open_webui.models.users import Users
from open_webui.utils.chat import generate_chat_completion




class Pipe:
    # def _is_pair_installed(self, from_code, to_code):
    #     try:
    #         translation =  argostranslate.translate.get_translation_from_codes(from_code, to_code)
    #     except AttributeError:
    #         return False
    #     else:
    #         if translation is not None:
    #             return True
    #         else: 
    #             return False
    
    # def _language_pairs_to_install(self, from_code, to_code):
    #     pairs = []
    #     if not self._is_pair_installed(from_code, to_code):
    #         pairs.append((from_code, to_code))
    #     if not self._is_pair_installed(to_code, from_code):
    #         pairs.append((to_code, from_code))
    #     return pairs




    class Valves(BaseModel):
        MODEL: str = Field(
            default="nhn-small:latest",
            description="Model to chat with",
        )

        INTERMEDIATE_LANGUAGE: str = Field(
            default="en",
            description="The language the model understands",
        )

    def __init__(self):
        self.valves = self.Valves
        self.name = "Langeled_1"

        # for from_code, to_code in self._language_pairs_to_install("no", self.valves.INTERMEDIATE_LANGUAGE):
        #     print(from_code, to_code)
        #     package = next((p for p in argostranslate.package.available_packages if p.from_code == from_code and p.to_code == to_code), None)
        #     print(package)
        #     if package:
        #         print(f"Installing {from_code} → {to_code}")
        #         argostranslate.package.install_from_path(package.download())



    def pipe(self, body: dict, __user__: dict, __request__: Request,) -> str:

        user = Users.get_user_by_id(__user__["id"])
        body["model"] = self.valves.MODEL
        return generate_chat_completion(__request__, body, user)
