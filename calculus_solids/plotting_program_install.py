import pip
import subprocess
import sys

# just use input() wherever
try:
    input = raw_input
except NameError:
    pass

def setup():
    # watchdog
    # livereload plotly
    install_prompt('Do you want to install plotly w/ automatic reloading?',"plotly livereload")
    pass

def question_prompt(text,default_install=False):
    default_char = 'y' if default_install else 'n'
    answer = ''
    while(answer != 'y' and answer != 'n'):
        answer = input(text+' [y]es/[n]o? (default: %s): '%(default_char)) or default_char
    # if answer=='y':
    #     install(package)
    return answer=='y'

def install_prompt(text,package,default_install=False):
    answer = question_prompt(text,default_install)
    if answer:
        return install(package)


def install(package):
    return subprocess.call([sys.executable, "-m", "pip", "install"]+package.split()) == 0


if __name__=='__main__':
    setup()