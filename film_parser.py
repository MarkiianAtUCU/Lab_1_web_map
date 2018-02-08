
import re


def get_name(year, line):
    return line[:line.find("(" + year)].strip().strip('"')


def get_filming_place(line, year_pos):
    bracket_pos = line.find("{")
    if bracket_pos != -1:
        place = line[bracket_pos + 1:].strip()
    else:
        place = line[line.find(")") + 1:].strip()

    if place[-1] == ")":
        r_line = place[::-1]
        place = r_line[r_line.find("(") + 1:][::-1].strip()
    return place





def read_file(path, year):
    """
    (str) -> (list)
    Return list of lines from file (path to file)
    [name, loc]
    """
    res = []
    with open(path, "r",encoding="iso8859") as file:
        for i in range(14):
            file.readline()
        for i in file:
            position = [m.start() for m in re.finditer("\(", i)]
            for pos in position:
                if i[pos + 1:pos + 5].isdigit():
                    if i[pos + 1:pos + 5] == year:
                        name = get_name(year, i)
                        place = get_filming_place(i, pos)
                        res.append((name, place))
                    break

    return res
