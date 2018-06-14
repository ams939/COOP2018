import qsGenerator

rq = {
      "scientificname":"Panthera Tigris",
      #"institutioncode":"amnh"
      }

limit = 5

qs = qsGenerator.qsGenerator(rq)

print(qs)
