# IDN Homograph Detector

The **IDN Homograph Detector** is a Python script used to detect homograph attacks of Internationalized Domain Names (IDNs). A write-up covering the concept of this script can be found at my blog at [intothethickof.it](https://intothethickof.it/2023/08/15/generating-and-detecting-phishing-domains-with-idn-homograph-attacks).

The script uses a mapping of Unicode characters that are *visually-similar* to Latin letters and a list of keywords to check to detect possible IDN homograph attacks.

Some use-cases include:
- Raising awareness of IDN homograph attacks
- Monitoring of newly registered domains to detect IDN homograph attacks of your company/brand


## Requirements

1. The script was developed in Python 3.10.5 and requires the ``` idna ``` library which can be installed using pip:

```
pip install idna
```
2. The script takes in as input a dictionary file (.txt file) which contains a mapping of Latin letters to visually-similar Unicode characters in their Hex values. The contents of the dictionary file should look like this:

```
a|0251|03B1|0430|203|...
b|13CF|1472|15AF|...
c|1D04|2CA5|0441|1043D|188|107...
.
.
.
x|0445|1541|157D|1E8D|3C7|...
y|0263|028F|03B3|0443|04AF|...
z|1D22|17A|17C|1E95|17E|...
```

3. The script takes in as input a text file of keywords to monitor. Each keyword should be separated by a new line. The contents of the file should look like this:

```
google
facebook
youtube
twitter
instagram
linkedin
apple
microsoft
...
```

4. The script takes in a text file of punycode domains to check. Each punycode domain should be separated by a new line. The contents of the file should look like this:

```
xn----ktbjphfiq9e1a.xn--p1acf
xn--65-1lc3f.xn--p1ai
xn--j1ai0c.com
xn--j1ai0c.store
xn--j1aij3c.xn--p1acf
xn--h1af0dg.xn--d1acj3b
xn--h1ahgigg2f.top
...
```

The contents of the dictionary can be adjusted depending on what is *visually-similar* to you. The input files will affect the output of the script and the amount of time/resources to complete the script as it will increase/decrease the number of possible IDN homographs. A free list of newly registered domains can be obtained from [WhoisDS](https://www.whoisds.com/newly-registered-domains).

## Usage

To run the script:

```
python idn_homograph_detector.py <dictionary_file> <keyword_file> <punycode_domains_file>
```

The script will output detected IDN homographs by printing the results to your console and saving them to a text file named **detected_homograph.txt**. 

For example, the console will look like this:

![detector_output](https://github.com/varrickkoh/IDN-Homograph-Detector/assets/142608053/9c75cdb4-0062-40ce-b005-4dac2cf84ac6)


The **detected_homograph.txt** file will look like this:

![detector_output_2](https://github.com/varrickkoh/IDN-Homograph-Detector/assets/142608053/1c6f1d39-bbce-4aee-8cc6-71ad6f258cf7)


## Disclaimer

**THIS SCRIPT IS FOR EDUCATIONAL AND INFORMATIONAL PURPOSES ONLY. THE AUTHOR DOES NOT TAKE RESPONSIBILITY FOR ANY MISUSE, LOSS, OR DAMAGE CAUSED BY THE USE OF THIS SCRIPT.**

