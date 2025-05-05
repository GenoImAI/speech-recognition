import language_tool_python

# Assuming `result` is already obtained from transcription
result = model.transcribe(filename, temperature=0.0, word_timestamps=True, without_timestamps=True)
segments = result['segments']

# Initialize grammar checker
tool = language_tool_python.LanguageTool('en-US')

if len(segments) > 0:
    # len(segments) > 0 checks if the list contains at least one segment, meaning that the transcription produced some results.   
 
    start_time = segments[0]['start'] # The start time (in seconds) of the first word.
    end_time = segments[-1]['end'] # The end time (in seconds) of the last word.
       
    # Duration of the transcription excluding silence at the beginning and end
    transcription_duration = end_time - start_time

    # Option[1]: Combine all segment texts into one string
    transcribed_text = ' '.join([seg['text'] for seg in segments])

    # Option[2]: or if you have result['text'], it would be better to use that as it provides punctuations.
    transcribed_text = result['text']

    # Check grammar
    matches = tool.check(transcribed_text)

    if len(matches):
        '''
        Example of a match:
            {
                'message': 'Use “a” instead of ‘an’ if the following word doesn’t start with a vowel sound, e.g. ‘a sentence’, ‘a university’.',
                'replacements': ['a'],
                'offset': 18,
                'context': 'Hello, world! are an language tool.',
                'sentence': 'are an language tool.',
                'category': 'MISC',
                'ruleId': 'EN_A_VS_AN',
                'ruleIssueType': 'misspelling',
                'offsetInContext': 18,
                'errorLength': 2
            }
        where `category` and `ruleId` can be used to identify the type of error. So you can count the number of errors by them.
        '''
        grammar_issues = [m.__dict__ for m in matches] # this grammar issues can be stored somewhere, and you can use them to create the metrics/features later.
else:
    pass 