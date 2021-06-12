from grammar import Grammar
from Cky import cky_parse

if __name__ == "__main__":
    # english
    #sentence = "Book the flight through Houston"
    #sentence = "Does she prefer a morning flight"
    #data = cky_parse(sentence, Grammar('L1_grammar_CF.txt'))

    # dothraki
    #sentence = 'Anha zhilak yera'
    #sentence = 'Anha gavork'
    sentence = 'Hash yer astoe ki Dothraki'
    gr = Grammar('L1_grammar_CF.txt')
    gr.print()
    print(gr.get_rules_for_tag('Verb NP'))
