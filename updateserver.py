try:
    try:
        import pip
        main = pip.main
    except:
        import pip._internal
        main = pip._internal.main
except:
    exit(1)
import sys

version = '.'.join(map(str,sys.version_info[0:2]))
if (version == '2.7' or version == '2.6') and True or main("show Calculus-Solids-of-Known-Volume".split()) == 1:
    main('install --upgrade https://github.com/auryan898/calculus-solids/archive/master.zip --user'.split())
else:
    print('Use python 2.7 or 2.6 for best results. Will not install.')
# from calculus_solids import web
# web.start()
