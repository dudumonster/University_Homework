# 通过传入的列表寻找结果
def find_data(process_data_list):
    # 依次进行循环查找并对过程排序
    for epoch, data_process in enumerate(data_process_list):
        # 用于判断此过程是否成立
        num = 0
        for i in process_data_list:
            if i in data_process:
                num += 1
        # 过程成立则数值相同，可以进入下一步
        if num == len(data_process):
            # 此过程中结果是否为最终结果，不是将此过程结果加入到过程中
            if data_result_list[epoch] not in result_list:
                # 弹出过程和此过程结果，因为此过程已经进行过，此结果存入需要查找的过程中
                result = data_result_list.pop(epoch)
                process = data_process_list.pop(epoch)
                # 判断结果是否已经存在过程中，存在则重新寻找，不存在则加入过程，并将其存入最终结果
                if result not in process_data_list:
                    dict_input['，'.join(process)] = result
                    end_result = find_data(process_data_list + [result])
                    if end_result == 1:
                        return 1
                    else:
                        return 0
                # 存在则直接寻找
                else:
                    end_result = find_data(process_data_list)
                    if end_result == 1:
                        return 1
                    else:
                        return 0
            # 找到最终结果，取出结果后返回
            else:
                process = data_process_list.pop(epoch)
                dict_input['，'.join(process)] = data_result_list[epoch]
                return 1



def reverse_inference(result, database, data_process_list, data_result_list):
    # 初始化一个列表，用于存储逆向推理得到的前提条件
    inferred_conditions = []

    # 遍历数据库中的每一条记录
    for key, value in database.items():
        # 如果结果与目标结果匹配，则开始逆向推理
        if value == result:
            inferred_conditions.append(key)  # 将当前记录的键（前提条件）加入到结果列表中

            # 寻找此前提条件是否出现在其他过程的结果中，如果是则继续逆向推理
            while True:
                found = False  # 用于标记是否找到匹配的前提条件
                for i, process in enumerate(data_process_list):
                    if data_result_list[i] == key:  # 如果此过程的结果与当前前提条件匹配
                        inferred_conditions.extend(process)  # 将此过程的前提条件加入到结果列表中
                        key = ''.join(process)  # 更新当前前提条件为新的前提条件
                        found = True
                        break
                if not found:
                    break

    return inferred_conditions


if __name__ == '__main__':
    # 用于储存中间过程
    data_process_list = []
    # 用于存储过程对应的结果
    data_result_list = []
    # 存储用于查询的数据
    list_data = []
    # 用于存储输出结果
    dict_input = {}

    # 规则库
    txt = '''有毛发，是哺乳动物
有奶，是哺乳动物
有羽毛，是鸟
会飞，会下蛋，是鸟
有鳃，是鱼
吃肉，是食肉动物
有犬齿，有爪，眼盯前方，是食肉动物
是哺乳动物，有蹄，是蹄类动物
是哺乳动物，是咀嚼反刍动物，是蹄类动物
是哺乳动物，是食肉动物，是黄褐色，身上有暗斑点，花豹
是哺乳动物，是食肉动物，是黄褐色，身上有黑色条纹，虎
是蹄类动物，有长脖子，有长腿，身上有暗斑点，长颈鹿
是蹄类动物，身上有黑色条纹，斑马
是鸟，有长脖子，有长腿，不会飞，有黑白二色，鸵鸟
是鸟，会游泳，不会飞，有黑白二色，企鹅
是鸟，善飞，雪燕
是鱼，善游，旗鱼'''
    # 将数据预处理
    datas = txt.split('\n')
    for data in datas:
        data = data.split('，')
        data_process_list.append(data[:-1])
        data_result_list.append(data[-1].replace('\n', ''))
    # 最终结果列表
    result_list = ['雪燕', '鸵鸟', '斑马', '长颈鹿', '虎', '花豹', '企鹅', '鱼', '旗鱼']
    # 数据库对应的过程
    database = {'1': '有毛发', '2': '有奶', '3': '有羽毛', '4': '有鳃', '5': '会飞', '6': '会下蛋', '7': '吃肉', '8': '有犬齿',
                '9': '有爪', '10': '眼盯前方', '11': '有蹄', '12': '是咀嚼反刍动物', '13': '是黄褐色', '14': '身上有暗斑点', '15': '身上有黑色条纹',
                '16': '有长脖子', '17': '有长腿', '18': '不会飞', '19': '会游泳', '20': '有黑白二色', '21': '善飞', '22': '善游', '23': '是哺乳动物',
                '24': '是鸟', '25': '是鱼', '26': '是食肉动物', '27': '是蹄类动物', '28': '花豹', '29': '虎', '30': '长颈鹿', '31': '斑马',
                '32': '鸵鸟', '33': '企鹅', '34': '雪燕', '35': '旗鱼'}
    # 循环进行输入，直到碰见0后退出
    while 1:
        term = input("")
        if term == '0':
            break
        if database[term] not in list_data:
            list_data.append(database[term])
    # 打印前提条件
    print('前提条件为：')
    print(' '.join(list_data) + '\n')
    # 进行递归查找，直到找到最终结果,返回1则找到最终结果
    end_result=find_data(list_data)
    if end_result == 1:
        print('推理过程如下：')
        # 将结果进行打印
        for i in dict_input.keys():
            print(f"{i}->{dict_input[i]}")
            # 得到最终结果即输出所识别动物
            if dict_input[i] in result_list:
                print(f'所识别的动物为{dict_input[i]}')
    else:
        # 将结果进行打印
        for i in dict_input.keys():
            print(f"{i}->{dict_input[i]}")
