import argparse

from naverkin.kin import test_naverkin
from navertoon.toon import test_navertoon
from kofia.crawler import test_kofia
from druginfo.crawler import test_druginfo
from costores.crawler import coscores_search
from naverplace.test import test_naverplace_results_collecting
from fromcurl.from_curl import test_fromcurl
from freeproxylists.freeproxy import test_freeproxylists_crawler
from logparser.nginx import test_ngin_log_parser
from maxmind.geoip import test_maxmind_geoip
from eurosatory.crawler import test_eurosatory
from dcinside.crawler import test_dcinside_crawler
from exposeguridadmexico.crawler import test_expo_guarid

def main():
    argparser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter, description='Test For crawlite'
    )
    argparser.add_argument('appname', type=str,  help='Input app name for test')
    argparser.add_argument('-keywords', '--keywords', default='')
    argparser.add_argument('-titleId', '--titleId', default='783053')
    argparser.add_argument('-ip', '--ip', default='52.79.116.98')
    argparser.add_argument('-start_date', '--start_date', default='')
    argparser.add_argument('-end_date', '--end_date', default='')
    argparser.add_argument('-search', '--search', nargs='?', default='')
    argparser.add_argument('-page_range', '--page_range', nargs='?')

    args = argparser.parse_args()
    if args.appname in ['naverkin', 'kin']:
        test_naverkin(args.keywords, args.page_range)
    
    if args.appname == 'navertoon':
        test_navertoon(titleId=args.titleId)
    
    if args.appname == 'kofia':
        test_kofia(
            start_date=args.start_date,
            end_date= args.end_date
        )
    
    if args.appname == 'druginfo':
        test_druginfo(
            q=args.search
        )
    
    if args.appname == 'coscores':
        coscores_search(search=args.search)

    if args.appname == 'naverplace':
        test_naverplace_results_collecting()
    
    if args.appname ==  'curl':
        test_fromcurl()
    
    if args.appname == 'freeproxy':
        test_freeproxylists_crawler()
    
    if args.appname == 'logparser':
        test_ngin_log_parser()
    
    if args.appname == 'maxmind':
        test_maxmind_geoip(ip=args.ip)

    if args.appname == 'eurosatory':
        test_eurosatory()

    if args.appname == 'dcinside':
        test_dcinside_crawler()

    
    if args.appname == 'expo':
        test_expo_guarid()

if __name__ == '__main__':
    main()