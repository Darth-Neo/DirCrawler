__author__ = 'morrj140'

import textract

print ("PDF ...")
text = textract.process('./Examples/example.pdf')
print text[0:20]

print ("PPTX ...")
text = textract.process('./Examples/example.pptx')
print text[0:20]

print ("XLSX ...")
text = textract.process('./Examples/example.xlsx')
print text[0:20]

print ("DOCX ...")
text = textract.process('./Examples/example.docx')
print text[0:20]

print ("txt ...")
text = textract.process('./Examples/example.txt')
print text[0:20]

print ("jpg ...")
text = textract.process('./Examples/example.jpg')
print text[0:20]

print ("png ...")
text = textract.process('./Examples/example.png')
print text[0:20]