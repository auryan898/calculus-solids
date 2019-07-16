# 3D Modeling: Solids of Known Volume for Calculus

### Purpose

Do a quick search on "solids of known volume" to find visualizations for them, and you'll find fancy animations and colorful designs that offer a lot in terms of learning, but what about function?

This tool gives a concise, simple representation for solids of known volume for use in 3D modeling software and simple visualization tools.  It's great for teachers and students in calculus to better understand these solids, in and out.

The two main formats include either an STL 3D model, or a 3D coordinate plot of the calculated points.  Formats also export to OpenJsCAD and OpenSCAD for further 3D modeling applications.

### Quick Start

See our live demo at [repl.it](https://calculus-solids2--ryanau.repl.co/). It works, but it's not meant to be hosted online, so it's buggy.

### Installation

Best results in Python 2.7/2.6

Python 3 was giving weird bugs I didn't bother to address.

This tool is meant to be installed and run on your computer. It opens up a simple server and uses your browser as an interface to its functionality.

**To Install:**  
It isn't super easy, but perform 
`pip install https://github.com/auryan898/calculus-solids/archive/master.zip`

Then run in a script:

    from calculus_solids import web
    web.start()

And a browser window should open up for your local version of the application. (Note: files are generated in directory where this code is executed.)

Will eventually simplify the process.
