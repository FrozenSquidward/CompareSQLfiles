import re  
#import sqlparse


modify_sql = []

# 编译正则表达式模式  （某些sql导出之后建表语句);不在一行）
pattern = re.compile(r'CREATE TABLE "([^"]+)" \((.*?)\)\n;', re.DOTALL | re.MULTILINE) 
# 结尾不换行的正则 
pattern2 = re.compile(r'CREATE TABLE "([^"]+)" \((.*?)\);', re.DOTALL | re.MULTILINE)  

# 初始化一个字典来存储格式化后的CREATE TABLE语句  
formatted_statements = {}  
formatted_statements_second = {}  

def find_first_space_or_length(s):  
    # 查找第一个空格的位置  
    index = s.find(' ')  
    # 如果没有找到空格，返回字符串的长度  
    return index if index != -1 else len(s)
    
# 读取SQL文件内容  
with open('path_to_first_sql_file.sql', 'r', encoding='utf-8') as file:  
    sql_first = file.read()  
with open('path_to_second_sql_file.sql', 'r', encoding='utf-8') as file:  
    sql_second = file.read()  
    
# 查找所有的CREATE TABLE语句  
create_first_table_statements = pattern.findall(sql_first)  
create_second_table_statements = pattern2.findall(sql_second)  

for table_name, table_definition in create_second_table_statements:  
    # 提取完整的CREATE TABLE语句  
    full_statement = f'CREATE TABLE "{table_name}" ({table_definition});\n'  
    formatted_statements_second[table_name] = full_statement
    
        
# 格式化并打印每个CREATE TABLE语句  
for table_name, table_definition in create_first_table_statements:  
    # 提取完整的CREATE TABLE语句  
    full_statement = f'CREATE TABLE "{table_name}" ({table_definition});\n'  
    #print(f"{full_statement}")  
    #formatted_statements[table_name] = full_statement

    # 使用sqlparse来格式化语句  （这个有错误）
    #formatted_statement = sqlparse.format(full_statement, style=sqlparse.styles.SQLStyle.ANSI)  
    
    # 打印格式化后的语句  
    #print(formatted_statement)  
    #print("-" * 80)  # 打印分隔线以便于区分不同的语句
    
    
    # 处理逻辑！！！！！！！！！！！！！！！！！！！！！！！！
    match = pattern2.search(full_statement)
    if match:  
        # 提取表名  
        table_name = match.group(1)  
        #print(f"主Table Name: {table_name}")  
        
        if table_name in formatted_statements_second:
            # 子库存在对应表，判断字段是否一致
            # 提取字段信息  
            table_first = re.findall(r'"([^"]+)" ([^,\n]+)', match.group(2))
            
            match_second = pattern2.search(formatted_statements_second[table_name])
            table_second = re.findall(r'"([^"]+)" ([^,\n]+)', match_second.group(2))
            fields_second = {}
            for field_name, field_type in table_second:  
                index = find_first_space_or_length(field_type)
                field_type = re.sub(r'\s+', '', field_type)
                #print(f"子  {field_name}: {field_type[0:index]}")
                fields_second[field_name]=field_type[0:index]
            #print(f"子")  
            #print(fields_second)  
            #print("主Fields:")  
            for field_name, field_type in table_first:  
                index = find_first_space_or_length(field_type)
                field_type = re.sub(r'\s+', '', field_type)
                #print(f"主  {field_name}: {field_type[0:index]}")
                if field_name in fields_second:
                    #存在字段，判断类型
                    if field_type[0:index] != fields_second[field_name]:
                        print(f"表存在不同类型字段 {table_name} {field_name} {field_type[0:index]},{fields_second[field_name]}")
                else:
                    #缺失字段，生成插入语句
                    print(f"缺失字段 {table_name} {field_name}")
                    modify_sql.append(f"ALTER TABLE {table_name} ADD {field_name} {field_type[0:index]};")  
        else:
            #多的表数据
            print(f"主多的表 : {table_name}")
    else:  
        print("主 No match found.")

    
#print(formatted_statements["COS_FRS_ACCOUNTS"])
#判断字典中是否有KEY
#print("1" in formatted_statements)
#print('COS_FRS_ACCOUNTS' in formatted_statements)
