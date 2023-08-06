from geoparser import Geoparser

p = Geoparser()
doc = p.parse('Je visite la ville de Lyon, Annecy et le Mont-Blanc.')


print(' -- tei -- ')
print(doc.tei)


print(' -- tokens -- ')
for token in doc.tokens:
    print(token.text, token.lemma, token.pos)


print(' -- named entities -- ')
for entity in doc.ne:
    print(entity.text, '[' + entity.tag + ']')
    if entity.tag == 'place':
        entity.print_toponyms()
    

print(' -- nested named entities -- ')
for nestedEntity in doc.nne:
    print(nestedEntity.text, '[' + nestedEntity.tag + ']')
    if nestedEntity.tag == 'place':
        nestedEntity.print_toponyms()