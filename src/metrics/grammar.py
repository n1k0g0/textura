import language_tool_python
tool = language_tool_python.LanguageTool('ru-Ru')
sentence = "ето полный трешб"
matches = tool.check(sentence)
print(matches)
