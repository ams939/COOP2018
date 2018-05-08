

rq = {
            "scientificname" : 'Puma" Concolor',
            "countrycode" : "KEN",
            "institution code" : "UTEP",
            "family" : "felidae"
     }


for key in rq:
    value = rq[key].replace('"', "'")
    rq[key] = value
    print(rq[key])
    
