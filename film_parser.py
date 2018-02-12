import re


def nyl_split(st):
    """
    (str) -> str, str, str

    Function returns splitted line: name, year of filming and location
    """
    splitted = st.split("\t")
    year = "(????" if ("(????") in splitted[0] else re.findall(
        "\([1-3][0-9]{3}", splitted[0])[-1]
    name = splitted[0][:splitted[0].rfind(year)].strip().strip('"')
    location = splitted[-1] if "(" not in splitted[-1] else splitted[-2]
    return name, year, location


def read_file(path, year):
    """
    (str, str) -> (list of tuples (str, str))

    Return list of tuples with name of film and adress of filming
    """
    res = []
    with open(path, "r", encoding="iso8859") as file:
        for i in range(14):
            file.readline()
        for i in file:
            if "-------------" not in i:
                if "("+year in i:
                    name, f_year, place = nyl_split(i)
                    if f_year == "(" + year:
                        res.append((name, place))
    return res
