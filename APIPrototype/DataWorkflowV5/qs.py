import qsGenerator

rq = {
      "institutioncode":"amnh",
      "country":"colombia"
      }

qs = qsGenerator.qsGenerator(rq)

print(qs)
