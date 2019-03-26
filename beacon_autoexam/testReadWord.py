import docx

file = docx.Document("2018年2月份题库.docx")

print("段落数：" + str(len(file.paragraphs)))