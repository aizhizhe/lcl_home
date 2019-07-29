from functools import wraps,lru_cache
from collections import defaultdict
import time

original_price=[1, 5, 8, 9, 10, 17, 17, 20, 24, 30, 35]
price=defaultdict(int)
for i,p in enumerate(original_price):
    price[i+1]=p
    # print(price[11])
# print(max(1,2,3,4))
def example(f,arg):
    return f(arg)
def add_ten(num):
    return num+10
def mul_ten(num):
    return num*10

operations=[add_ten,mul_ten]

for f in operations:
    print(example(f,100))

called_time=defaultdict(int)
def get_call_times(f):
    result=f()
    print('function:{} called once!'.format(f.__name__))
    called_time[f.__name__]+=1
    return result
def f_name():
    print("hello")
    return "nihao"
def some_function_1():print("I am function 1")
def r(n):
    return max([price[n]]+[r(i)+r(n-i) for i in range(1,n)])
call_time_with_arg=defaultdict(int)

def get_call_time(f):
    """@param f is a function"""

    def wrap(n):
        """haha I am wrap"""
        print("IIII")
        result=f(n)
        call_time_with_arg[(f.__name__,n)]+=1
        return result
    return wrap

def add_ten(n):return n+10
add_ten=get_call_time(add_ten)

@get_call_time
def add_twenty(n):
    return n+20

def get_reply(f):
    def get_add(n):
        print("baozhuang")
        t=f(n)
        return t
    return get_add

@get_reply
def add(n):
    return n+2
call_time_with_arg=defaultdict(int)

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

@memo
def r(n):
    max_price,max_split=max([(price[n],0)]+[(r(i)+r(n-i),i) for i in range(1,n)],key=lambda x:x[0])
    solution[n]=(max_split,n-max_split)
    return max_price
def r1(n):
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

from collections import defaultdict

# original_price=[1,5,8,9,10,17,20,24,30]
# price=defaultdict(int)
for i,p in enumerate(original_price):
    price[i+1]=p
assert price[1]==1

def func_1(n):
    for i in range(n):
        print(n)

def call_time(func_1,arg):
    start=time.time()
    func_1(arg)
    print("used time:".format(time.time()-start))
function_called_time=defaultdict(int)
def get_call_time(func):
    @wraps(func)
    def _inner(arg):
        global function_called_time
        function_called_time[func.__name__]+=1
        result=func(arg)
        print('function called time is:{}'.format(function_called_time[func.__name__]))
        return result
    return _inner

@get_call_time
def func_1(n):
    for i in range(n):
        print(n)
    return 0

def func_slow(n):
    for i in range(n):
        time.sleep(0.2)
        print(n)
    # return "g"
@get_call_time
def func_slow1(n):
    for i in range(n):
        time.sleep(0.2)
        print(n)

solution={}

def edit_distance(string1,string2):
    if len(string1)==0:return len(string2)
    if len(string2)==0:return len(string1)
    tail_s1=string1[-1]
    tail_s2=string2[-1]
    candidates=[(edit_distance(string1[:-1],string2)+1,'DEL {}'.format(tail_s1)),(edit_distance(string1,string2[:-1])+1,'ADD {}'.format(tail_s2))]
    if tail_s1==tail_s2:
        both_forward=(edit_distance(string1[:-1],string2[:-1])+0,'')
    else:
        both_forward=(edit_distance(string1[:-1],string2[:-1])+1,'SUB {}=> {}'.format(tail_s1,tail_s2))
    candidates.append(both_forward)
    min_distance,operation=min(candidates,key=lambda x:x[0])
    solution[(string1,string2)]=operation
    return min_distance


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


if __name__=="__main__":
    print(edit_distance("A","ATCGGGA"))
    print(solution)
    # print(func_slow1(5))
    # print(call_time(func_1,10))
    # print(get_call_time(func_1)(10))
    # func_1(10)
    # for i in range(10):
    #     s=get_call_times(f_name)
    #     print(s)
    # get_call_times(some_function_1)
    # print(called_time)
    # print(r(231))
    # print(add_ten(10))
    # d=add_twenty(9)
    # print(d)
    # add_twenty=get_call_time(add_twenty)
    # dd=add_twenty(9)
    # print(dd)
    # print(add(10))
    # print(r(38))
    # print(solution)
    # s=memo1(r1,245)
    # print(s)
    # print(r)
    # print(call_time_with_arg)
    # print(parse_solution(38))
    # print(price[132])