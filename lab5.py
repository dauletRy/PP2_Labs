import re
#task1

txt = input()
x = re.search('a.*b', txt)
print(x)
#task2

txt = input()
x = re.search(r'ab{2,3}', txt)
print(x)

#task3
txt = 'wgasddas_sxcvrio'
txt1 = "ADADAVasdaADADfa"
x = re.findall(r'[a-z]+_[a-z]+', txt)
print(x if x else "No match")

#task4
txt = 'WASDDSANWFaasdaiernwif'
x = re.findall('[A-Z]{1}[a-z]+', txt)
print(x)

#task5

txt = 'sasdasrgiuageoiasdafaswfb'
x = re.search('a.*b$', txt)
print(x)

#task 6
txt = 'adfadf sdafafasd,qfddssd.wposdwsdcr'
x = re.sub('[ .,]', ':', txt, 4)
print(x)

#task 7
txt = 'hello_world'
txt2 = txt.upper()
camel = ''
i = 0
while(i != len(txt)):
    if txt[i] == '_':
        camel += txt[i] + txt2[i+1]
        i += 2
    else:
        camel += txt[i]
        i += 1
camel = re.sub('_', '', camel)
print(camel)

#task 8
txt = 'HelloWorld'
x = re.findall('[A-Z][^A-Z]*', txt)
print(x)

#task 9

str = "HelloWorld"
x = re.sub(r"([A-Z])", r" \1", str)
print(x)

#task 10
camel = 'HelloWorld'
snake = re.sub(r"([A-Z])", r" \1", camel)
snake = snake.lower()
snake = snake.strip()
snake = re.sub(r'\s', '_', snake)
print(snake)
