
import requests
import argparse
import os
import datetime
import sys
from Crypto.Cipher import AES

download_path = ""

def downvideo(url):
    download_path = "./download"
    if not os.path.exists(download_path):
        os.mkdir(download_path)

    # 新建日期文件夹
    download_path = os.path.join(download_path, datetime.datetime.now().strftime('%Y_%m_%d_%H时%H分'))
    # print download_path
    if not os.path.exists(download_path):
        os.mkdir(download_path)
    soup = requests.get(url).text
    if "#EXTM3U" not in soup:
        print("非m3u8")

    if "EXT-X-STREAM-INF" in soup:  # 第一层
        file_line = soup.split("\n")
        for line in file_line:
            if '.m3u8' in line:
                url = url.rsplit("/", 1)[0] + "/" + line  # 拼出第二层m3u8的URL
                soup = requests.get(url).text

    file_line = soup.split("\n")
    unknow = True
    key = ""
    for index, line in enumerate(file_line):  # 第二层
        if "#EXT-X-KEY" in line:  # 找解密Key
            method_pos = line.find("METHOD")
            comma_pos = line.find(",")
            method = line[method_pos:comma_pos].split('=')[1]
            #print("Decode Method：", method)

            uri_pos = line.find("URI")
            quotation_mark_pos = line.rfind('"')
            key_path = line[uri_pos:quotation_mark_pos].split('"')[1]

            #key_url = url.rsplit("/", 1)[0] + "/" + key_path  # 拼出key解密密钥URL
            key_url = key_path  # 拼出key解密密钥URL
            res = requests.get(key_url)
            key = res.content
            print("key：", key)

        if "EXTINF" in line:  # 找ts地址并下载
            unknow = False
            pd_url = url.rsplit("/", 1)[0] + "/" + file_line[index + 1]  # 拼出ts片段的URL
            # print pd_url

            while True:
                try:
                    res = requests.get(pd_url)
                    break
                except:
                    continue

            c_fule_name = file_line[index + 1].rsplit("/", 1)[-1]
            if len(key):  # AES 解密
                cryptor = AES.new(key, AES.MODE_CBC, key)
                with open(os.path.join(download_path, c_fule_name), 'ab') as f:
                    f.write(cryptor.decrypt(res.content))
            else:
                with open(os.path.join(download_path, c_fule_name), 'ab') as f:
                    f.write(res.content)
                    f.flush()
    if unknow:
        print("未找到对应下载链接")
    else:
        print("下载完成")

if __name__ == '__main__':

    parse = argparse.ArgumentParser(prog='M3U8', prefix_chars='-')
    parse.add_argument('-l')
    #parse.add_argument('-k')
    args = parse.parse_args()
    url = args.l
    #key = args.k

    #downvideo(args.l, args.k)
    downvideo(args.l)
