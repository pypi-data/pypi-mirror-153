from carbon2_server.func import *
import argparse

if __name__=="__main__":

    parser = argparse.ArgumentParser(description='Carbon2-Server News Collector')
    parser.add_argument('config_path', metavar='N', type=str, nargs='+',default="carbon2.txt",
                        help='config path for carbon2-server')
    args=parser.parse_args()
    fetch_news(config_path=args.config_path)