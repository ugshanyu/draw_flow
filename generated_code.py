We = 'TESTING'

node11 = llmGenerate('Hello', 'World', None)

node10 = extractOutput(node11)

match node10:

    case 'world':

        node18 =         llmGenerate('321', '123', node10)

    case 'hello':

        node20 =         llmGenerate('456', '876', node10)
