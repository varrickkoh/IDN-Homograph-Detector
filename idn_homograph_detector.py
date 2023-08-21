import idna
import unicodedata
import sys
import math

# build the list of keywords to monitor based on the user's wordlist
def build_monitored_keywords(filename):
    try:
        with open(filename,'r') as keywords_flie:
            return keywords_flie.read().strip().split('\n')
    except FileNotFoundError:
        print(f'[!] Error - {filename} not found')
        sys.exit(1)
    except Exception as e:
        print(f'[!] Error - {e}')
        sys.exit(1)


# checks if a IDN contains Unicode characters that 
# are visually similar to Latin letters
def check_similar_characters(punycode_domain, similar_chars):

    unicode_domain = idna.decode(punycode_domain.encode('ascii'))
    similar_string = ""

    # take only the main domain, removing the TLD
    unicode_domain = unicode_domain.split('.')[0]

    for char in unicode_domain:
        found_similar = False
        for latin_char, similar_unicode_chars in similar_chars.items():
            if char in similar_unicode_chars:
                similar_string += latin_char
                found_similar = True
                break
        
        if not found_similar:
            similar_string += char

    return [unicode_domain, similar_string]


# convert a string to Unicode based on its Hex values
def hex_to_unicode(hex_string):
    try:
        unicode_code_point = int(hex_string, 16)
        unicode_character = chr(unicode_code_point)
        return unicode_character
    except:
        return ""

# encodes a domain from Unicode to punycode
def convert_to_punycode(domain):

    try:
        normalized = unicodedata.normalize('NFC', domain)
        punycoded = idna.encode(normalized).decode('utf-8')
        
        return punycoded
    except Exception:
        return None


# build the similar_chars dictionary based on the user's wordlist
def build_dictionary(filename):

    similar_chars_dict = {}
    lines = []
    try:
        with open(filename,'r') as dictionary_file:
            lines = dictionary_file.read().strip().split('\n')
    except FileNotFoundError:
        print(f'[!] Error - {filename} not found')
        sys.exit(1)
    except Exception as e:
        print(f'[!] Error - {e}')
        sys.exit(1)

    for line in lines:
        # len(line) is 1 when there are no confusables for a specific letter
        if len(line) == 1:
            similar_chars_dict[line] = [line]
        else:
            # split each line by the separator |
            temp = line.split('|')
            # key is the first value, which should be a latin letter
            key = temp.pop(0)
            # convert each hex string into the unicode character
            unicode_chars = [hex_to_unicode(char) for char in temp] 
            # add the latin letter back into the unicode_chars list
            unicode_chars.insert(0,key)
            # remove duplicates from the list of unicode characters
            unicode_chars = list(set(unicode_chars))
            
            similar_chars_dict[key] = unicode_chars

    return similar_chars_dict
        

def main():

    if len(sys.argv) < 4:
        print("[!] Usage: python idn_homograph_detector.py <dictionary_file> <keyword_file> <punycode_domains_file>")
        sys.exit(1)
    
    dictionary_file = sys.argv[1]
    keyword_file = sys.argv[2]
    domains_file = sys.argv[3]

    # 1. Build dictionary of Unicode characters to use
    similar_chars_dict = build_dictionary(dictionary_file)
    print(f'\n[-] Loaded dictionary from {dictionary_file}')

    for key in similar_chars_dict:
        print(f'[{key}] -> {", ".join(similar_chars_dict[key])}')

    # 2. Build list of keywords to monitor
    keywords_to_monitor = build_monitored_keywords(keyword_file)
    print(f'[-] Number of keywords to monitor: {len(keywords_to_monitor)}')
  
    # 3. Check through list of domains from domains_file
    punycode_domains = []
    with open(domains_file,'r') as domains_file:
        punycode_domains = domains_file.read().strip().split('\n')
 
    number_of_domains = len(punycode_domains)
    print(f'[-] Number of punycode domains to check: {number_of_domains}')

    count = 0
    checkpoint = math.ceil(number_of_domains/10)

    RED_COLOR_CODE = '\033[91m'
    RESET_COLOR_CODE = '\033[0m'    

    for domain in punycode_domains:
        count += 1
        if count % checkpoint == 0:
            print(f'[-] Checking domain number {count}')

        result = check_similar_characters(domain,similar_chars_dict)
        keyword = result[1]

        if keyword in keywords_to_monitor:
            unicode_domain = result[0]
            
            alert = f"""
{RED_COLOR_CODE}[!] Possible IDN Homograph Attack!{RESET_COLOR_CODE}
[{count}] Punycode Domain = {domain}
[{count}] IDN = {unicode_domain}
[{count}] Keyword = {keyword}
"""

            print(alert)

            with open('detected_homograph.txt','a+', encoding='utf-8') as results_file:
                results_file.write(f'{domain}|{unicode_domain}|{keyword}\n')

    print(f'[-] Program completed running . . . results saved to "detected_homograph.txt"')

if __name__ == '__main__':
    main()
