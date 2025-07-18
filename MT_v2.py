import argostranslate.package
import argostranslate.translate

spoken_language = "en"
intermediate_language = "de"

input_text_no = "Hej"
input_text_en = "A spectre is haunting Europe"

installed_languages = argostranslate.translate.get_installed_languages()
print(type(installed_languages))


# Download and install Argos Translate package
# argostranslate.package.update_package_index()
# available_packages = argostranslate.package.get_available_packages()
# package_to_install = next(
#     p for p in available_packages if (p.from_code == spoken_language and p.to_code == intermediate_language) or (p.from_code == intermediate_language and p.to_code == spoken_language)
# )
# argostranslate.package.install_from_path(package_to_install.download())

# Translate
intermediate_text = argostranslate.translate.translate(input_text_no, spoken_language, intermediate_language)
print(intermediate_text)


#output_text = argostranslate.translate.translate(intermediate_text, intermediate_language, spoken_language)
#print("  ")
#print(output_text)
