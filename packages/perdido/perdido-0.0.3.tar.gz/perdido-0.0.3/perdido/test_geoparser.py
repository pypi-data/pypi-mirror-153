from geoparser import Geoparser

p = Geoparser()
doc = p.parse('Je visite la ville de Pau.')

print(doc.tei)

for token in doc.tokens:
    print(token.text, token.lemma, token.pos)