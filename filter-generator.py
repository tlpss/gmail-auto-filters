
'''
These functions generate a simple filter for GMail which labels all mails containing addresses in the specified domains
'''

from pandas import read_csv
import numpy as np

def generate_xml(filtername, mail_list):
    """
    main function which creates the xml
    :param filtername: name for the gmail Label
    :param mail_list: list of email addresses (strings)
    :return: xml-formatted string which contains the filter
    """


    # header generation
    filter_string = \
"""<?xml version='1.0' encoding='UTF-8'?>
<feed xmlns='http://www.w3.org/2005/Atom' xmlns:apps='http://schemas.google.com/apps/2006'>
    <title>Mail Filters</title>
    <id></id>
    <updated></updated>
    <author>
        <name>Thomas Lips</name>
    </author>
    """

    # make filter entry
    mail_list = format_addresses(mail_list)
    filter_string += \
    f"""<entry>
    <category term='filter'></category>
    <title>Mail Filter</title>
    <id></id>
    <updated></updated>
    <content></content>
    <apps:property name='shouldNeverSpam' value='true'/>
    <apps:property name='label' value='{filtername}'/> 
    <apps:property name='from' value = '{mail_list}'/>
    <apps:property name='to' value = '{mail_list}'/>
    \n"""

    # close entry

    filter_string += """\t </entry> \n """
    # close header

    filter_string += "</feed>"
    return filter_string


def generate_addresses(csv_file):
    """
    :param csv_file: filename of a csv file which contains a column with header titled Email (or contains the word email)
    :return: a list of email addresses for all non-empty fields in that column
    """
    df = read_csv(csv_file)
    mails = df['E-mailadres contactpersoon'] #TODO: select mail column in more flexible way
    list = []
    for mail in mails:
        if mail is np.nan: # TODO: preprocess to filter nan's and replace with None or something else
            print('empty email')
        else:
            # print(mail)
            for item in mail.replace(';', ' ').split(','):
                try:
                    domain = item.split('@')[1]
                    list.append(domain)
                except:
                    print('invalid email')
    return list

def format_addresses(mail_list):
    """
    function to add 'OR' and format the emails according to the GMAIL API
    :param mail_list:
    :return:
    """
    string  =""
    for address in mail_list[:-1]:
        string += address
        string += " OR "
    string += mail_list[-1]
    return string

def write_xml(content, filename):
    f = open(filename, "w")
    f.write(content)
    f.close()


if __name__ == "__main__":

    # TODO: make user input for following fields
    csv = 'companies.csv'
    filtername = 'filtername'
    xmlname = 'test.xml'

    mail_list = generate_addresses(csv)
    string = generate_xml(filtername,mail_list)
    write_xml(string, xmlname)