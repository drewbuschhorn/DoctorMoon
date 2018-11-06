# -*- coding: utf-8 -*-
import json
import sqlite3
conn = sqlite3.connect('D:\corpus\processed_data\id_positions.sqlite3')

node_dict = {}

def get_node(_key):
    if _key in node_dict:
        return node_dict[_key]
    
    c = conn.cursor()
    c.execute('SELECT * FROM positions WHERE uuid = ?', (_key,))
    result = c.fetchone()
    print(result)
    file = result[3]                
    if file == '0':
        file = 'D:\corpus\s2-corpus-00'
    with open(file, encoding='utf-8', errors='ignore') as f:
        f.seek(result[2])
        line = f.readline()
        node = json.loads(line)
        node_dict[_key] = node
    return node



with open("D:\\corpus\\nodes.txt", "r") as _input:
    with open("D:\\corpus\\analysis.html","w") as output:
        output.write('<html><head></head><body>')
        for line in _input:
            output.write('<div><ol>');
            line = line.strip()[1:-1].replace(' ','')
            nodes = line.split(',')
            for _id in nodes:
                output.write('<li>')
                node = get_node(_id)
                block = """
                <div>
                    <div>{title}</div>
                    <div>{keywords}</div>
                    <div>{authors}</div>
                    <div>{same_author}</div>
                </div>
                """.format(
                title = node['title'],
                keywords = node['entities'],
                authors = node['authors'],
                same_author = "false"
                )
                output.write(block)
                output.write('</li>')
            output.write('</ol></div>\n')
        output.write('</body></html>')            
print (len(node_dict))
conn.close()