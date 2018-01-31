# filter functions, named after selector id's

def telefoon(text: str) -> str:
    def checklen(substring):
        """are there 10 digits in the string"""
        if len([c for c in text if c.isdigit()]) == 10:
            return True

    for i in [text, *text.split()]:
        if checklen(i):
            return ''.join([c for c in text if c.isdigit()])

    res = ''.join([c for c in text if c.isdigit()])
    if res != '112':
        return res
    return ''

