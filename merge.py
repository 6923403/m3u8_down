import os

def me1():
    ts_path = "./v1/"
    os.system("rm %s.DS_Store" % ts_path)
    # 读取ts文件夹下所有的ts文件
    path_list = os.listdir(ts_path)
    # 对文件进行排序
    path_list.sort()
    path_list.sort(key=lambda x: int(x[:-3]))
    #path_list.sort(key = lambda x: int(x[:-3]))

    # 将排序后的ts的绝对路径放入列表中
    li = [os.path.join(ts_path, filename) for filename in path_list]
    # 类似于[001.ts|00.2ts|003.ts]
    input_file = '|'.join(li)
    # 指定输出文件名称
    output_file = "333.mp4"
    # 使用ffmpeg将ts合并为mp4
    command = 'ffmpeg -i "concat:%s" -acodec copy -vcodec copy -absf aac_adtstoasc %s' % (input_file, output_file)
    print(command)
    # 指行命令
    os.system(command)


def me2(): #多文件
    dirs = "./v1/"
    mp4 = "./v1/mp4/"
    filename = "s.mp4"
    os.system("rm %s.DS_Store" % dirs)
    a = 1
    content = ""
    os.system("rm -rf %s" %mp4)

    lists = os.listdir(dirs)
    lists.sort()
    lists.sort(key=lambda x: int(x[:-3]))
    b = [lists[i:i + 250] for i in range(0, len(lists), 250)]
    os.mkdir(mp4)
    for lis in b:
        cmd = "ffmpeg -i \"concat:"
        for file in lis:
            if file != '.DS_Store':
                file_path = os.path.join(dirs, file)
                cmd += file_path + '|'
                # print("文件：%s"%file_path)
        cmd = cmd[:-1]
        cmd += '\" -bsf:a aac_adtstoasc -c copy -vcodec copy %s%s.mp4' %(mp4, a)
        try:
            os.system(cmd)
            content += "file '%s.mp4'\n" % a
            a = a + 1
        except:
            print("Unexpected error")

    fp = open("%smp4list.txt" % mp4, 'a+')
    fp.write(content)
    fp.close()
    mp4cmd = "ffmpeg -y -f concat -i {0}mp4list.txt -c copy {0}{1}".format(mp4,filename)
    os.system(mp4cmd)

if __name__ == '__main__':
    me1()

