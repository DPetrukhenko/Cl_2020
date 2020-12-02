import re
# адреса

addresses = open('addresses.txt', 'r', encoding="utf-8")
addresses = addresses.read()
addresses_extracted = re.findall(r"^\d+.+\n.+\d+\n.+\d+", addresses, flags=re.MULTILINE)
print(addresses_extracted)

# прямая речь

direct_speech = open('d_speech.txt', 'r', encoding="utf-8")
direct_speech = direct_speech.read()
d_speech_extracted = re.findall(r'—.+?—|«.+?—|—.+', direct_speech)
print(d_speech_extracted)

# морж-корж

morzh = open('морж-корж.txt', 'r', encoding="utf-8")
morzh = morzh.read()
korzh1 = re.sub(r'морж', 'корж', morzh)
korzh = re.sub(r'Морж', 'Корж', korzh1)
print(korzh)
