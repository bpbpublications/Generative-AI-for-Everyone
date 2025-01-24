import language_tool_python
def check_grammar(response):
    tool = language_tool_python.LanguageTool('en-US')

    # Check the sentence
    findings = tool.check(response)
    print(len(findings))
    # Display the results
    if findings:
        print("Potential issues found:")
        for finding in findings:
            print(f"{finding.ruleId}: {finding.message}")
    else:
        print("No grammatical errors detected.")

    return(len(findings))
