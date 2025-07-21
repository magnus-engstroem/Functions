import argostranslate.package
import argostranslate.translate

spoken_lang_code = "nb" 
int_lang_code = "en"

text =  """
Som kjent er, forstår man med Wuppertal, et navn som holdes slik i vanry blant Lysets venner (Freunden des Lichtes), de to byene Elberfeld og Barmen, som strekker seg langs etter dalen over en reiseavstand på nesten tre timer. De purpurfargede bølgene på den smale elven skyller av og til raskt, av og til roligere, mellom rykende fabrikkbygninger og blekeplasser fulle av garn. Dens sterke rødfarge skyldes imidlertid ikke et blodig slag, for den eneste kampen som her foregår, utkjempes kun av teologiske skrivere og ordrike gamle kjerringer, stort sett over keiserens skjegg, og heller ikke skam over menneskenes virksomhet, selv om det riktig nok kan være grunn nok til det, men ene og alene at de mange fargeriene benytter tyrkiskrødt. Når man reiser fra Düsseldorf, ankommer man det hellige området ved Sonnborn; den gjørmete Wupper flyter sakte forbi, og sammenlignet med Rhinen som man just har forlatt, fremstår den som en skuffelse med sin begredelige fremtoning. Omgivelsene er ellers nokså tiltalende: de ganske lave fjellene som av og til hever seg varsomt, andre ganger stupbratt, den tette skogen som kjekt går over i grønne enger, og i godvær den blå himmelen som speiler seg i Wupper og fører til at den røde fargen fullstendig forsvinner. Etter en sving rundt et klippefremspring ser man de underlige tårnene i Elberfeld rett foran seg (de ringere husene er skjult bak hagene), og noen få minutter senere kommer man til obskurantenes Zion. Så å si utenfor byen er den katolske kirken; den står der som var den bannlyst fra de hellige murene. Den er i bysantinsk stil, dårlig bygd av en særdeles uerfaren arkitekt etter meget gode tegninger; den gamle katolske kirken er blitt revet for å gi rom for den venstre fløyen, fremdeles ikke bygd, av Rådhuset; bare tårnet står igjen og tjener på sitt vis det allmenne vel, nemlig som fengsel. Straks etter kommer man til en stor bygning hvis tak bæres av søyler, men disse søylene er av et helt ekstraordinært slag; de er egyptiske i basis, doriske i midten og joniske i toppen; dessuten klarer de seg, av gode grunner, uten alt overflødig tilbehør, slik som pidestaller og kapitéler. Denne bygningen ble tidligere kalt for museet, men musene holdt seg borte og bare en stor gjeldstyngde stod igjen, slik at bygningen for ikke veldig lenge siden ble solgt på auksjon og ble gjort om til et kasino, et navn som nå pryder den nakne fasaden og jager vekk alle minner og det tidligere poetiske navnet. For øvrig er bygningen så plumpt proporsjonert at den på kveldstid ser ut som en kamel. Her begynner de triste gatene, uten enhver karakter; det fine, nye Rådhuset, som bare er halvferdig, er på grunn av plassmangel plassert slik at dets fasade ligger ut mot en trangt, heslig smug. Til slutt treffer man på Wupper igjen, og en vakker bro forteller en at man nærmer deg Barmen, der man i det minste legger større vekt på vakker arkitektur. Så snart man krysser elven, gir det hele et mer innbydende inntrykk; store, massive hus bygd smakfullt i moderne stil erstatter de middelmådige Elberfeld-bygningene, som verken er gammeldagse eller moderne, verken vakre eller karikaturer. Nye murte hus spretter opp overalt; gatedekket tar slutt og gaten fortsetter som en rett aveny, med bebyggelse på begge sider. Mellom husene skimter man grønne blekeplasser; Wupper er fremdeles klar her, og fjellene som nærmer seg med sine lett svungne omriss, og den stadige skiftningen mellom skog, eng og hager der røde tak stikker frem, gjør området mer og mer attraktivt jo lenger man går. Halvveis ned alléen møter man den noe tilbaketrukne fasaden på kirken i Unterbarmen; den er dalens vakreste bygning, fint konstruert i den mest edle bysantinske stil. Men snart begynner gatedekket igjen, og de grå skiferhusene trenger seg på. Det er imidlertid langt større avveksling her enn i Elberfeld, for monotonien brytes snart av en frisk blekeplass, snart av et hus i moderne stil, snart av et stykke av elven og snart av en rekke med hager langs veien. Alt dette gjør at man blir i tvil om Barmen skal regnes som en by eller bare som et konglomerat av allehånde bygninger; den er da også kun en forening av mange mindre distrikter som holdes sammen av byens institusjonelle bånd. De viktigste av disse distriktene er: Gemarke, det gamle senter for den reformerte tro; Unterbarmen i retning Elberfeld, ikke langt fra Wupperfeld og over Gemarke; lenger borte Rittershausen, som har Wichlinghausen til venstre og Hekinghausen med den usedvanlig pittoreske Rauhental til høyre. Innbyggerne er overalt lutheranere tilhørende begge kirkesamfunn; katolikkene - i høyden to eller tre tusen - er spredt over hele dalen. Etter Rittershausen forlater den reisende ved verdens ende fjellene og går over grensen til det gammel-prøyssiske vestfaliske området.
"""

argostranslate.package.update_package_index()
available_packages = argostranslate.package.get_available_packages()

def is_pair_installed(from_code, to_code):
    try:
        translation =  argostranslate.translate.get_translation_from_codes(from_code, to_code)
    except AttributeError:
        return False
    else:
        if translation is not None:
            return True
        else: 
            return False

def language_pairs_to_install(from_code, to_code):
    pairs = []
    if not is_pair_installed(from_code, to_code):
        pairs.append((from_code, to_code))
    if not is_pair_installed(to_code, from_code):
        pairs.append((to_code, from_code))
    return pairs


print(language_pairs_to_install(spoken_lang_code, int_lang_code))
print(available_packages)


for from_code, to_code in language_pairs_to_install(spoken_lang_code, int_lang_code):
    print(from_code, to_code)
    package = next((p for p in available_packages if p.from_code == from_code and p.to_code == to_code), None)
    print(package)
    if package:
        print(f"Installing {from_code} → {to_code}")
        argostranslate.package.install_from_path(package.download())


int_text = argostranslate.translate.translate(text, spoken_lang_code, int_lang_code)
print(int_text)

print('\n \n')

out_text = argostranslate.translate.translate(int_text, int_lang_code, spoken_lang_code)
print(out_text)
