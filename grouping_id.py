import re
import tkinter as tk

import pyperclip
from prettytable import PrettyTable


def replace_commas(match):
    content = match.group(1)
    new_content = content.replace(',', '，')
    return f'({new_content})'


def replace_(text):
    pattern1 = r'\(([^(]*)\)'
    pattern2 = r'\(([^)]*)\)'

    arg1 = re.sub(pattern1, replace_commas, text)
    return re.sub(pattern2, replace_commas, arg1)


def cal(arg):
    arg2 = replace_(arg)
    groupby = {i: '1' for i in
               re.split(',', re.search(r'(?<=GROUPBY|groupby)[，\w.,()\'\"=\u4e00-\u9fff]*(?=GROUPINGSETS|groupingsets)',
                                       re.sub(r'\s', '', arg2)).group(0))}

    grouping = [re.split(',', replace_(j)) for j in re.split('\),\(', '),('.join(
        re.findall(r'(?<=GROUPINGSETS\(\(|groupingsets\(\()[，\w\(\).,\'\"=\u4e00-\u9fff]*(?=\)\))',
                   re.sub(r'\s', '', arg))))]

    ans = ''
    i = 0
    table = PrettyTable(['序号', '维度', 'grouping_id'])
    table.align["维度"] = "l"
    for x in grouping:
        for y in x:
            if y in list(groupby.keys()):
                groupby[y] = '0'
        for z in groupby:
            ans = ans + groupby[z]
        i += 1
        table.add_row([i, ', '.join(x).replace('，', ','), str(int(ans, 2))])
        ans = ''
        for t in groupby:
            groupby[t] = '1'
    return table


def show_result():
    input_text = text_input.get("1.0", "end-1c")
    ans = cal(input_text)
    result_box.config(state="normal")
    result_box.delete("1.0", "end")  # 清空结果框
    result_box.insert("1.0", f"{ans}")
    result_box.config(state="disabled")
    pyperclip.copy(ans.get_string())


import base64, os
from icon import img

tmp = open("tmp.ico", "wb+")
tmp.write(base64.b64decode(img))
tmp.close()

# 创建主窗口
root = tk.Tk()
root.title("grouping_id计算器")
root.geometry("600x400")

root.iconbitmap("tmp.ico")
os.remove("tmp.ico")

# 添加说明标签
input_label = tk.Label(root, text="输入框：")
input_label.grid(row=0, column=0, padx=20, pady=0, sticky="w")

# 创建多行文本输入区域
text_input = tk.Text(root, height=8, width=40)
text_input.grid(row=1, column=0, padx=20, pady=0, sticky="nsew")

# 创建按钮
show_button = tk.Button(root, text="计算", command=show_result)
show_button.grid(row=2, column=0, pady=10)

result_label = tk.Label(root, text="结果框：")
result_label.grid(row=3, column=0, padx=20, pady=0, sticky="w")

# 创建结果框区域
result_box = tk.Text(root, height=8, width=40, state="disabled")
result_box.grid(row=4, column=0, padx=20, pady=10, sticky="nsew")

# 创建垂直滚动条并关联到文本输入区域
text_scrollbar = tk.Scrollbar(root, command=text_input.yview)
text_scrollbar.grid(row=1, column=1, sticky="ns")
text_input.config(yscrollcommand=text_scrollbar.set)

# 设置行和列的权重，使其能够随窗口大小变化而适应
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(4, weight=1)
root.grid_columnconfigure(0, weight=1)

# 运行主循环
root.mainloop()
