from .preidict import predict

if __name__ == '__main__':
    text = [
        '对你不满意',
        '大美女',
        '帅哥',
        '我妈说明儿不让出去玩',
        '心情不爽出来散散心'
    ]
    for i in text:
        print(predict(text))
