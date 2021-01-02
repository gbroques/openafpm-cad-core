def enforce_recompute_last_spreadsheet(document):
    sheets = document.findObjects('Spreadsheet::Sheet')
    last_sheet = sheets[len(sheets) - 1]
    last_sheet.enforceRecompute()


def make_compound(document, name, objects):
    compound = document.addObject('Part::Compound', name)
    compound.Links = objects
    return compound
