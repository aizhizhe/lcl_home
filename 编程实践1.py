import random

choice = random.choice
def create_grammar(grammar_str, split='=', line_split='\n'):
    grammar = {}
    for line in grammar_str.split(line_split):
        if not line.strip(): continue
        exp, stmt = line.split(split)
        grammar[exp.strip()] = [s.split() for s in stmt.split('|')]
    return grammar

def generate(gram, target):
    if target not in gram: return target  # means target is a terminal expression
    expaned = [generate(gram, t) for t in choice(gram[target])]
    return ''.join([e if e != '/n' else '\n' for e in expaned if e != 'null'])
npc="""
doctor = 确认患者名字 询问情况 询问不适部位 探究原因
确认患者名字 = 称呼 确认 名字 结尾 标点
称呼 = 你 | 您 
确认 = 是 | 叫 | 名字是 | 名字叫 | 的名字是 | 就是
名字 = 王小二 | 张三 | 李四 | 王五
结尾 = 吗 | 吧 | 啊

询问情况 = 称呼 怎么回事 标点
称呼 = 你|您
怎么回事 =  怎么啦 | 是什么情况啊 | 说说你的情况吧 | 跟我说一下你的情况
标点 = ？| ！ | ，

询问不适部位 = 阐述 你 部位 伤痛 标点
阐述 = 说一说 | 讲一讲 | 说一下 | 告诉我 | 跟我说 
部位 = 哪里 | 哪个地方 | 哪个部位 | 什么位置
伤痛 = 不舒服 | 不适 | 疼 | 痛 | 不对劲 | 难受 | 疼痛 

探究原因 = 我会根据您的病情进行治疗 | 我给你开点药 | 我给你扎一针 | 我帮你治疗
"""

npc_1="""
intro = 人称 问候 推销商品
人称 = 先生 | 小姐 | 姑娘 | 夫人 | 太太 
问候 = 您好 | 你好 
推销商品 = 展示 商品 介绍优点 
展示 = 您看一下 | 给您看一下 | 请看一下 | 您看
商品 = 代指 是不是 修饰 物
代指 = 这个 | 这 | 这些 | 那些 | 那
是不是 = 是 | 就是 
修饰 = 厂商 产生
厂商 = 阿里巴巴 | 百度 | 微软 | 腾讯 | 苹果公司 | 华为 | 小米
产生 = 开发的 | 创造的 | 做出来的 | 做的
物 = app | 软件 | 操作系统 | 一套算法 | 智能机器人
介绍优点 = 史无前例 | 非常棒 | 效果很好 
"""
def generate_n():
    for i in range(20):
        print(generate(create_grammar(npc), target="doctor"))
        print(generate(create_grammar(npc_1), target="intro"))
if __name__=="__main__":
    generate_n()
