from functools import wraps,lru_cache
from collections import defaultdict

original_price=[1, 5, 8, 9, 10, 17, 17, 20, 24, 30, 35]
price=defaultdict(int)
for i,p in enumerate(original_price):
    price[i+1]=p


def memo(f):
    memo.already_computed={}
    @wraps(f)
    def _wrap(arg):
        result=None
        if arg in memo.already_computed:
            result=memo.already_computed[arg]
        else:
            result=f(arg)
            memo.already_computed[arg]=result
        return result
    return _wrap
solution={}
# memo.already_computed={}
def r(n):
    max_price,max_split=max([(price[n],0)]+[(r(i)+r(n-i),i) for i in range(1,n)],key=lambda x:x[0])
    solution[n]=(n-max_split,max_split)
    return max_price
def memo1(f,arg):
    memo.already_computed={}
    result=None
    if arg in memo.already_computed:
        result=memo.already_computed[arg]
    else:
        result=f(arg)
        memo.already_computed[arg]=result
    return result

def parse_solution(n):
    left_split,right_split=solution[n]
    if right_split==0:return [left_split]
    return parse_solution(left_split)+parse_solution(right_split)

@lru_cache(maxsize=2 ** 10)
def edit_distance(string1, string2):
    if len(string1) == 0: return len(string2)
    if len(string2) == 0: return len(string1)
    tail_s1 = string1[-1]
    tail_s2 = string2[-1]
    candidates = [
        (edit_distance(string1[:-1], string2) + 1, 'DEL {}'.format(tail_s1)),  # string 1 delete tail
        (edit_distance(string1, string2[:-1]) + 1, 'ADD {} '.format(tail_s2)),  # string 1 add tail of string2
    ]
    if tail_s1 == tail_s2:
        both_forward = (edit_distance(string1[:-1], string2[:-1]) + 0, '')
    else:
        both_forward = (edit_distance(string1[:-1], string2[:-1]) + 1, 'SUB {} => {}'.format(tail_s1, tail_s2))
    candidates.append(both_forward)
    min_distance, operation = min(candidates, key=lambda x: x[0])
    solution[(string1, string2)] = operation
    return min_distance

def parse_solution_edit(string1,string2):
    '''
    solution parse
    :param string1:
    :param string2:
    :return:
    '''
    res=[]
    if string1==string2:return 0
    if string1=="" or string2=="":return [x for x in solution.values()]
    if len(string1)>len(string2):
        max=len(string1)
    else:
        max=len(string2)
    i=0
    j=0
    index=0
    while index<max:
        key=(string1[:len(string1)-i],string2[:len(string2)-j])
        i+=1
        j+=1
        if "ADD" in solution[key]:
            i-=1
        elif "DEL" in solution[key]:
            j-=1
        if solution[key]!='':
            res.append(solution[key])
        index+=1
    return [x for x in reversed(res)]

if __name__=="__main__":
    # print(r(16))
    # print(parse_solution(16))
    print(edit_distance("a","bcdf"))
    # print(solution)
    s=parse_solution_edit("a","bcdf")
    print(s)