# libreflow

LibreFlow is a complete film asset-manager flow example made on top of [Kabaret studio](https://gitlab.com/kabaretstudio/kabaret). Kabaret is a framework and a flow describes a specific organisation on top of it. In this case, we describe how to organize files and folders for an animation project.


## Install

To install the package, run :

> pip install libreflow --pre

This command will also install all needed dependencies, such as pySide, kabaret, and other important librairies.

Currently we need the `--pre` to allow pre releases, which is requiered to get the last version of Kabaret.

## Requierements 

This version is made for python 3.7 and above. And you must have a redis database running to use kabaret !


## Run

>  python -m libreflow.gui --host yourRedisHost --port 6379 --db 0 --cluster xxx --session xx

Where : 

> -m libreflow.gui : calling libre flow with its graphical interface
> --host host : the host url/ip of you redis instance
> --port port : the port of the redis instance
> --password password : if your redis instance is password protected, use this
> --db 0 : the redis index db. It's recommanded to set it to the default (0)
> --cluster clusterName : used to define a group of people within the same workgroup thant can access the same project. Don't change it otherwise you won't access existing projects.
> --session sessionName : to be defined
> --debug (optional) : kabaret debug mode on (it talks a lot)

Not yet implemented options :

> --root_dir path : force the root_dir value instead of the one in the project
> --site sitename : necessary when setting the multisite options ON