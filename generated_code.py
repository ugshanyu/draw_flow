def llmGenerate(a, b, c):
    print(a, b, c)
    return "CaseTwo"



IceTop = 'Hello'

node14 = llmGenerate('IceTop', 'Hello', None)

match node14:

    case 'CaseTwo':

        node16 =         llmGenerate('CaseTwoTest', 'me', node14)

    case 'CaseThree':

        node17 =         llmGenerate('CaseThreeTest', 'Why', node14)

    case 'caseOne':

        node15 =         llmGenerate('caseOneTest', 'on', node14)
