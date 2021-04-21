from Manage import Manage

def main():
    white_list = ['about:blank']  # 白名单
    # 配置信息

    print("在这里配置初始信息")
    conf = {
        'kw': '山东大学数据结构实验',
        'engine': 'baidu',
        'target_page': 3,
        'white_list': white_list,
    }

    dict = Manage(conf).get_local_analyse()
    with open('result\web_check_result.txt', 'w') as f:
        for key in dict:
            f.writelines('"' + str(key) + '": ' + str(dict[key]))
            f.write('\n')

    print('done')

main()