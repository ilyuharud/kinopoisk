from kinopoisk.movie import Movie
import re

inputFile = open("input/part-1.csv", "r")
outputFile = open('output/part-1.csv', "w")
pattern = re.compile(r'(/film/)(.*?)/')

FIELD_SEPARATOR = '\u0001'
COLLECT_SEPARATOR = '\t'


def complete_ids(file):
    input = open(file, "r")
    ids = []
    for line in input:
        res = line.split('\u0001')[0]
        ids.append(int(res))
    return ids


ready_ids = complete_ids('output/part-1_tmp.csv')
ready_cnt = len(ready_ids)
full_cnt = 4840
iterator = 0

for line in inputFile:
    m = re.match(pattern, line)
    if m:
        iterator += 1
        id_extract = m.group(2).split('-')[-1]
        if int(id_extract) in ready_ids:
            print("%s is ready..." % id_extract)
        else:
            print(id_extract, end=' ')
            movie = Movie(id=id_extract)
            movie.get_content('main_page')
            title = movie.title
            year = str(movie.year)
            directors = '\t'.join(str(x) for x in movie.directors)
            actors = '\t'.join(str(x) for x in movie.actors)
            genres = '\t'.join(str(x) for x in movie.genres)
            description = movie.plot.replace('\n', ' ')
            row = "{}\u0001{}\u0001{}\u0001{}\u0001{}\u0001{}\u0001{}\n".format(id_extract, title, year, directors,
                                                                                actors, genres, description)
            outputFile.write(row)
            print('complete... %s/%s' % (iterator, full_cnt))

outputFile.close()
