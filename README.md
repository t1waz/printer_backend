PRINTER BACKEND
===============

Simple app to run DYMO 400 LABEL printer.

You can send file via curl:

    curl -v -F file=@<filename> <backend_address>/print_file
    
filename - must be .ong

backend_address - obvious



DEPLOY
------

<Printer Host User> - user from printer host machine that can run print job.

* Add key to .rsa file. Key must be valid for <Printer Host User> 

* Fill .envs with data for:

    PRINTER_HOST=<Printer network address>
    PRINTER_USER=<Printer Host User Username> 
    HOST_APP_DIR=<where project is store on instance>

* Run:

    $ docker-compose build
    $ docker-compose up