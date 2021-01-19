def ken_pom_tuple_to_json(tpl: tuple) -> dict:
    s = {
        "date": tpl[0],
        "favorite": tpl[1],
        "underdog": tpl[2],
        "actual": tpl[3],
        "predicted": tpl[4],
        "percentage": tpl[5],
        "correct": tpl[6],
        "covered": tpl[8],
    }

    return s
