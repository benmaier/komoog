
with open('../README.rst','r') as f:
    text = f.read()

text = text.replace("komoog\n======\n","")

text = 'About\n=====\n' + text

with open('./about.rst','w') as f:
    f.write(text)
