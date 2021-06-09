def parse(json_data):
    
    def new_token(Type, lexeme):
        return {"type" : Type, "lexeme" : lexeme}
    #####################################################################
    def lexer(data):
        # returns a list of tokens
        position = 0
        tokens = []
        errors = []
        while(position < len(data)):
            if(data[position] == ' '):
                position += 1
                continue
            elif(data[position] == '{'):
                tokens.append(new_token('OB', '{'))
            elif(data[position] == '}'):
                tokens.append(new_token('CB', '}'))
            elif(data[position] == '['):
                tokens.append(new_token('OSB', '['))
            elif(data[position] == ']'):
                tokens.append(new_token('CSB', ']'))
            elif(data[position] == '"'):
                # this is a string token.. parse it accordingly
                position += 1
                cur_lexeme = ""
                # while input str is not ", get whatever we have
                while(data[position] != '"'):
                    cur_lexeme += data[position]
                    position += 1
                tokens.append(new_token("String", cur_lexeme))
            elif(data[position] == ','):
                tokens.append(new_token("Comma", ','))
            elif(data[position] == ':'):
                tokens.append(new_token("Colon", ":"))
            elif(data[position].isdigit()):
                # this is a real value.. while value is 
                cur_lexeme = ""
                while(data[position].isdigit() or data[position] == '.'):
                    cur_lexeme += data[position]
                    position += 1
        
                tokens.append(new_token("Real", float(cur_lexeme)))
                position -= 1
            else:
                errors.append(f'Invalid token {data[position]}')
            position += 1
            
        return tokens, errors

    tokens, errors = lexer(json_data)
    if len(errors) > 0:
        print(errors)
        return None
    
    ####################################################################
    # no lexer errors, Go for parser
    
    position = 0
    
    def move(places):
        nonlocal position, tokens
        if(position + places < len(tokens)):
            position += places
        else:
            position = len(tokens) - 1
    
    next_ = lambda : move(1)
    
    def match(lexemeType):
        nonlocal position, tokens, errors

        if(tokens[position]["type"] != lexemeType):
            cur_token = tokens[position]["type"]
            errors.append(f'Unexpected token : {cur_token}, expected {lexemeType}')
            return None
        result_value = tokens[position]["lexeme"]
        next_()
        return result_value
    
    cur_token = lambda: tokens[position]
    result = {}
    errors = []
    
    def parse_list():
        nonlocal position, tokens
        result = []
        # this will parse list for sure
        match("OSB")
        # now It will parse the internal expressions
        while(cur_token()["type"] != "CSB"):
            new_value = cur_token()["lexeme"]
            result.append(new_value)
            next_()
            if(cur_token()["type"] != "CSB"):
                match("Comma")
                
        match("CSB")
        return result
    
    def parse_entry():
        nonlocal position, tokens
        key = match("String")

#         if(key_value == None):
#             errors.append(f'Unexpected Token: Expected String, Got: {cur_token_type}')

            # found a valid key,, 
        match("Colon") 
        value = None
        if(cur_token()["type"] == 'Real' or cur_token()["type"] == "String"):
            value = cur_token()["lexeme"]
        elif(cur_token()["type"] == 'OB'):
            value = parse_block()
        elif(cur_token()["type"] == "OSB"):
            # how to parse arrays
            value = parse_list()
            
            
        next_()
        
        return key, value
    
    def parse_block():
        nonlocal position, tokens
        match("OB")
        
        result = {}
        
        while position < len(tokens) and cur_token()["type"] != 'CB':
            key, value = parse_entry()    
            result[key] = value    
            if(cur_token()["type"] != 'CB'):
                match("Comma")
                
        
        match("CB")
        return result

    
    return parse_block()
    
    
def main():
	my_json_data = '{"name" : "Rishabh", "Age" : 21,"Company" : "Standard Chartered Bank", "Address" : {"Vill" : "Nanawan","P.O" : "Karsai","Teh" : "Barsar","Distt" : "Hamirpur","PIN" : 174312}, "x" : "y", "Z" : "t", "values" : [1, 2, "kareem", "Sam"], "t" : "s"}'
	parsed_json_data = parse(my_json_data)
	print(parsed_json_data)

main()
