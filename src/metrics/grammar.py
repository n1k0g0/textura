import language_tool_python
tool = language_tool_python.LanguageTool('ru-Ru')
sentence = ""
matches = tool.check(sentence)
print(matches)
