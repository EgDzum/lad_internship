from parser import WebParser

link = 'https://career.habr.com/vacancies?page=1&s[]=44&s[]=76&s[]=43&type=all'

parser = WebParser(link)

parser.parse()

df = parser.get_data()

print(df)
print()
print(df['grade'].value_counts())
