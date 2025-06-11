from collections import deque

stack_deque = deque([])
for j in range(10):
    stack_deque.append(j)

# キーボード入力を受け付ける
input_text = input("pushまたはpopと入力してください: ")
if input_text == "push":
    input_number = int(input("追加する値を入力してください: "))
    stack_deque.append(input_number) # スタックにpush
elif input_text == "pop":
    if stack_deque:
      stack_deque.pop() # スタックからpop
    else:
        print("スタックは空です")
else:
    print("無効な入力です")

# スタックの表示
print("スタックの中身:"+str(stack_deque))
