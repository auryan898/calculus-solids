
try:
    try:
        import pip
        main = pip.main
    except:
        import pip._internal
        main = pip._internal.main
except:
    exit(1)
if main("show Calculus-Solids-of-Known-Volume".split()) == 1:
    main('install https://github.com/auryan898/calculus-solids/archive/master.zip --user'.split())

from calculus_solids import web
web.start()
