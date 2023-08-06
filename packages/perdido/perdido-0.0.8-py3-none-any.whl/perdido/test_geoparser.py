from geoparser import Geoparser


p = Geoparser()
doc = p.parse('Je visite la ville de Lyon, Annecy et le Mont-Blanc.')


print(' -- tei -- ')
print(doc.tei)


print(' -- geojson -- ')
print(doc.geojson)


print(' -- tokens -- ')
for token in doc.tokens:
    print("{0} {1} {2}".format(token.text, token.lemma, token.pos))


print(' -- named entities -- ')
for entity in doc.ne:
    print("{0} --> {1}".format(entity.text, entity.tag))
    if entity.tag == 'place':
        for t in entity.toponyms:
            print("{0} {1} - {2}".format(t.lat, t.lng, t.source))
    

print(' -- nested named entities -- ')
for nestedEntity in doc.nne:
    print("{0} --> {1}".format(nestedEntity.text, nestedEntity.tag))
    if nestedEntity.tag == 'place':
        for t in nestedEntity.toponyms:
            print("{0} {1} - {2}".format(t.lat, t.lng, t.source))


m = doc.get_folium_map()
