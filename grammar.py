import language_tool_python
tool = language_tool_python.LanguageTool('en-US')
sentence = "ето полный трешб"
matches = tool.check(sentence)
print(matches)

