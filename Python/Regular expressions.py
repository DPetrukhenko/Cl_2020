import re
# адреса

with open('addresses.txt', 'r', encoding="utf-8") as file:
    addresses = file.read()
addresses_extracted = re.findall(r"^\d+.+\n.+\d+\n.+\d+", addresses, flags=re.MULTILINE)
print(addresses_extracted)

# прямая речь

with open('d_speech.txt', 'r', encoding="utf-8") as file:
    direct_speech = file.read()
d_speech_extracted = re.findall(r'—.+?—|«.+?—|—.+', direct_speech)
print(d_speech_extracted)

# морж-корж

with open('морж-корж.txt', 'r', encoding="utf-8") as file:
    morzh = file.read()
korzh1 = re.sub(r'морж', 'корж', morzh)
korzh = re.sub(r'Морж', 'Корж', korzh1)
print(korzh)
