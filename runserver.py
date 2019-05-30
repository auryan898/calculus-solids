import pip
try:
    import pip._internal
    install = None
    try:
        main = pip.main
    except:
        main = pip._internal.main
except:
    exit(1)
if main("show Calculus-Solids-of-Known-Volume".split()) == 1:
    main('install https://github.com/auryan898/calculus-solids/archive/master.zip --user'.split())

from calculus_solids import web
web.start()