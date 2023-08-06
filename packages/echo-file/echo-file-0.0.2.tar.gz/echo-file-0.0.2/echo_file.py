import os, argparse

def run():
    parser = argparse.ArgumentParser(description='Echo File, write text to file')
    text_arg = parser.add_argument('--text', type=str, default='hello world',help='text written to file')
    path_arg = parser.add_argument('--path', type=str, default='/tmp/test.txt', help='file path')
    args = parser.parse_args()
    text = args.text
    path = args.path
    dirname = os.path.dirname(path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    elif os.path.isfile(dirname):
        raise argparse.ArgumentError(path_arg, f'{dirname} is a file')
    elif os.path.isdir(path):
        raise argparse.ArgumentError(path_arg, f'{path} is a dir')
    else:
        with open(path, 'w') as f:
            f.write(text)

if __name__=='__main__':
    run()